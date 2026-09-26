#!/usr/bin/env node
// QA gate. Run before every full render:   node bin/check.mjs <project>
// Static:  determinism bans, external URLs, CSS animations, unknown fonts.
// Runtime: script errors, missing assets, timeline length, and a text audit sampled over
//          the whole film (off-frame / outside safe area, overlapping captions, text that
//          is not on screen long enough to read).
// Exit code 1 if any ERROR is found.
import fs from "node:fs";
import path from "node:path";
import { serve, launch, openFilm, parseArgs, resolveProject } from "./lib.mjs";

const args = parseArgs(process.argv.slice(2));
const { dir, entry } = resolveProject(args._[0]);
const errors = [], warns = [];
const E = (m) => errors.push(m), W = (m) => warns.push(m);

// ---------------- static ----------------
const html = fs.readFileSync(path.join(dir, entry), "utf8");
const localScripts = [...html.matchAll(/<script[^>]*src="([^"]+)"/g)].map((m) => m[1]).filter((s) => !/^https?:/.test(s) && !/engine\//.test(s));
const sources = [["" + entry, html], ...localScripts.map((s) => [s, fs.existsSync(path.join(dir, s)) ? fs.readFileSync(path.join(dir, s), "utf8") : ""])];
for (const [name, src] of sources) {
  const code = name.endsWith(".html") ? [...src.matchAll(/<script(?![^>]*src=)[^>]*>([\s\S]*?)<\/script>/g)].map((m) => m[1]).join("\n") : src;
  if (/Math\.random\s*\(/.test(code)) E(`${name}: Math.random() — use MK.rng(seed)`);
  if (/Date\.now\s*\(|new Date\s*\(|performance\.now\s*\(/.test(code)) E(`${name}: clock reads (Date/performance.now) — frames must depend only on t`);
  if (/repeat\s*:\s*-1/.test(code)) E(`${name}: repeat:-1 — use MK.repeats(span, period)`);
  if (/\.play\s*\(\s*\)/.test(code)) E(`${name}: tl.play()/video.play() — the renderer seeks; never play`);
  if (/setTimeout|setInterval|requestAnimationFrame/.test(code)) W(`${name}: timers/rAF in film code — animation must live on the timeline`);
  if (/fetch\s*\(|XMLHttpRequest/.test(code)) E(`${name}: network fetch in film code — inline or bundle data`);
}
if (!/data-film/.test(html)) E("no [data-film] root");
if (!/data-duration="[\d.]+"/.test(html)) E("root is missing data-duration");
if (!/Film\.build\s*\(/.test(html)) E("no Film.build(tl => {...}) call");
for (const m of html.matchAll(/(?:src|href)="(https?:\/\/[^"]+)"/g)) E(`external URL ${m[1]} — download it into assets/ (renders must be offline)`);
if (/@keyframes|animation\s*:|animation-name/.test(html)) W("CSS @keyframes/animation found — not seekable; move it onto the GSAP timeline");
if (/transition\s*:\s*(?!none)/.test(html)) W("CSS transition found — frames may capture mid-transition; remove it");
for (const m of html.matchAll(/<video[^>]*src="([^"]+)"/g)) if (!/\.webm$/i.test(m[1])) W(`video ${m[1]}: Chromium may not decode H.264 — convert with tools/prep_video.sh (webm or image sequence)`);
// fonts
const faces = new Set();
const fontCss = [html];
for (const m of html.matchAll(/<link[^>]*href="([^"]+\.css)"/g)) { const p = path.join(dir, m[1]); if (fs.existsSync(p)) fontCss.push(fs.readFileSync(p, "utf8")); }
for (const css of fontCss) for (const m of css.matchAll(/@font-face\s*{[^}]*font-family\s*:\s*["']?([^"';]+)["']?/g)) faces.add(m[1].trim().toLowerCase());
const generic = new Set(["serif", "sans-serif", "monospace", "system-ui", "ui-sans-serif", "cursive", "inherit", "initial"]);
const vars = {};
for (const css of fontCss) for (const m of css.matchAll(/(--[\w-]+)\s*:\s*([^;}]+)/g)) vars[m[1]] = m[2].trim();
const resolveVar = (v) => { let k = 0; while (/var\((--[\w-]+)\)/.test(v) && k++ < 5) v = v.replace(/var\((--[\w-]+)\)/, (_, n) => vars[n] || ""); return v; };
const used = new Set();
for (const m of html.matchAll(/font-family\s*:\s*([^;}"]+)/g)) used.add(resolveVar(m[1]).split(",")[0].replace(/['"]/g, "").trim().toLowerCase());
for (const m of html.matchAll(/font\s*:\s*[^;}"]*?\d+px(?:\/[\d.]+)?\s+['"]?([A-Za-z][^,;'"}]*)/g)) used.add(resolveVar(m[1].trim()).split(",")[0].replace(/['"]/g, "").trim().toLowerCase());
for (const f of used) if (f && !generic.has(f) && !faces.has(f)) W(`font "${f}" has no @font-face — it will fall back to a system font`);

// ---------------- runtime ----------------
const { server, port } = await serve(dir);
const browser = await launch();
let cfg;
try {
  const film = await openFilm(browser, port, entry, 0.5);
  cfg = film.cfg;
  const page = film.page;
  film.logs.forEach((l) => (/requestfailed|http 4|pageerror/.test(l) ? E(l) : W(l)));
  const tlDur = await page.evaluate(() => window.__film.timelineDuration());
  if (tlDur > cfg.duration + 0.05) W(`timeline runs to ${tlDur.toFixed(2)}s but film is ${cfg.duration}s — tweens after the end are cut`);
  const step = parseFloat(args.step || 0.2);
  const samples = [];
  for (let t = 0; t <= cfg.duration + 1e-6; t += step) {
    await page.evaluate((x) => window.__film.seek(x), t);
    const vis = await page.evaluate(({ W, H }) => {
      const out = [];
      const els = document.querySelectorAll(".t, [data-qa=text]");
      els.forEach((el, idx) => {
        if (!el.id) el.id = "__t" + idx;
        let op = 1, n = el, hidden = false;
        while (n && n.nodeType === 1) {
          const cs = getComputedStyle(n);
          op *= parseFloat(cs.opacity);
          if (cs.visibility === "hidden" || cs.display === "none") hidden = true;
          n = n.parentElement;
        }
        // real text only: skip kit overlays (sweep / glitch clones) and measure glyph boxes
        let text = "", x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
        const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, { acceptNode: (nd) => nd.parentElement.closest(".mk-sweep,.mk-glitch,.sw,[aria-hidden=true]") ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT });
        while (tw.nextNode()) {
          const nd = tw.currentNode;
          if (!nd.textContent.trim()) continue;
          const pe = nd.parentElement, pcs = getComputedStyle(pe);
          if (pcs.display === "none" || pcs.visibility === "hidden") continue;
          text += nd.textContent;
          const rg = document.createRange(); rg.selectNodeContents(nd);
          for (const r of rg.getClientRects()) { if (r.width < 1) continue; x0 = Math.min(x0, r.left); y0 = Math.min(y0, r.top); x1 = Math.max(x1, r.right); y1 = Math.max(y1, r.bottom); }
        }
        text = text.replace(/\s+/g, " ").trim();
        if (hidden || op < 0.6 || !text || x1 < x0) return;
        out.push({ id: el.id, text: text.slice(0, 40), words: text.split(" ").length, op, x: x0, y: y0, w: x1 - x0, h: y1 - y0 });
      });
      return out;
    }, { W: cfg.width, H: cfg.height });
    samples.push({ t, vis });
  }
  const safeX = cfg.width * 0.04, safeY = cfg.height * 0.04;
  const reported = new Set();
  const onTime = {};
  for (const { t, vis } of samples) {
    for (const v of vis) {
      if (v.op > 0.85) onTime[v.id] = onTime[v.id] || { text: v.text, words: v.words, runs: [], cur: null };
      const o = onTime[v.id];
      if (o && v.op > 0.85) { if (o.cur && Math.abs(o.cur.end - (t - step)) < 1e-6) o.cur.end = t; else { o.cur = { start: t, end: t }; o.runs.push(o.cur); } }
      const off = v.x < safeX || v.y < safeY || v.x + v.w > cfg.width - safeX || v.y + v.h > cfg.height - safeY;
      const key = "off" + v.id;
      if (off && !reported.has(key)) { reported.add(key); W(`t=${t.toFixed(1)}s "${v.text}" is outside the 4% safe area (box ${Math.round(v.x)},${Math.round(v.y)} ${Math.round(v.w)}x${Math.round(v.h)})`); }
    }
    for (let i = 0; i < vis.length; i++) for (let j = i + 1; j < vis.length; j++) {
      const a = vis[i], b = vis[j];
      if (a.id === b.id) continue;
      const ix = Math.max(0, Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x));
      const iy = Math.max(0, Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y));
      const small = Math.min(a.w * a.h, b.w * b.h);
      const key = "ov" + [a.id, b.id].sort().join("|");
      if (ix * iy > 0.12 * small && iy > 0.38 * Math.min(a.h, b.h) && !reported.has(key)) { reported.add(key); W(`t=${t.toFixed(1)}s overlapping text: "${a.text}" / "${b.text}"`); }
    }
  }
  for (const id in onTime) {
    const o = onTime[id];
    const longest = Math.max(0, ...o.runs.map((r) => r.end - r.start + step));
    const need = Math.min(2.5, 0.6 + o.words * 0.22);
    if (longest + step * 0.5 < need) W(`"${o.text}" is fully readable for only ${longest.toFixed(1)}s (needs ~${need.toFixed(1)}s for ${o.words} words)`);
  }
} catch (e) {
  E("runtime: " + (e.message || e));
} finally {
  await browser.close();
  server.close();
}

console.log(`\nchitram check — ${entry}${cfg ? ` (${cfg.width}x${cfg.height}, ${cfg.duration}s @ ${cfg.fps}fps)` : ""}`);
errors.forEach((m) => console.log("  ERROR  " + m));
warns.forEach((m) => console.log("  warn   " + m));
console.log(`\n${errors.length} error(s), ${warns.length} warning(s)`);
process.exit(errors.length ? 1 : 0);
