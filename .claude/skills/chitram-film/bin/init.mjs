#!/usr/bin/env node
// Scaffold a new film project:   node bin/init.mjs <dir> [--duration 30] [--size 1920x1080] [--fps 30]
// Copies the engine (runtime, kit, fonts, gsap) into <dir>/engine so the project is self-contained.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "./lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const skill = path.resolve(here, "..");
const args = parseArgs(process.argv.slice(2));
const dest = path.resolve(args._[0] || "film");
const [w, h] = String(args.size || "1920x1080").split("x").map(Number);
const duration = args.duration || 30, fps = args.fps || 30;

if (fs.existsSync(path.join(dest, "index.html")) && !args.force) { console.error(`${dest}/index.html exists (use --force)`); process.exit(1); }
fs.mkdirSync(path.join(dest, "assets"), { recursive: true });
fs.cpSync(path.join(skill, "engine"), path.join(dest, "engine"), { recursive: true });
let tpl = fs.readFileSync(path.join(skill, "template", "index.html"), "utf8");
tpl = tpl.replaceAll("{{W}}", w).replaceAll("{{H}}", h).replaceAll("{{DURATION}}", duration).replaceAll("{{FPS}}", fps);
fs.writeFileSync(path.join(dest, "index.html"), tpl);
fs.copyFileSync(path.join(skill, "template", "cues.json"), path.join(dest, "cues.json"));
console.log(`Film project ready: ${dest}
  edit      ${path.join(dest, "index.html")}
  preview   node ${path.join(skill, "bin/preview.mjs")} ${dest}
  check     node ${path.join(skill, "bin/check.mjs")} ${dest}
  snapshot  node ${path.join(skill, "bin/render.mjs")} ${dest} --at 1,5,10
  audio     python3 ${path.join(skill, "audio/synth.py")} ${path.join(dest, "cues.json")} ${path.join(dest, "assets/score.wav")}
  render    node ${path.join(skill, "bin/render.mjs")} ${dest} --out ${path.join(dest, "out/film.mp4")}`);
