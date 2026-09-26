#!/usr/bin/env python3
"""
Deconstruct a REFERENCE VIDEO so a model can "watch" it: shots, rhythm, camera motion,
palette, brightness, audio energy and tempo — plus contact sheets to look at.

    python3 analyze_video.py ref.mp4 [--out ref_analysis] [--scene 0.28] [--max-shots 60]

Writes to <out>/ :
  analysis.json    machine-readable: meta, shots[], audio{}, rhythm{}
  analysis.md      human/model-readable shot log + rhythm summary (read this first)
  shots_NN.jpg     contact sheets: one row per shot = 4 frames across the shot (start, 1/3, 2/3, end)
                   with timecodes — read these to see framing, type, motion and transitions
  overview.jpg     one mid-frame per shot, small grid (the whole film at a glance)

How to use the output (see DIRECTOR.md §1.5): read analysis.md, then every shots_NN.jpg, then
fill the Shot Log and the Style DNA. Borrow the grammar (rhythm, camera, transitions, type
system, palette logic), never the content (their brand, copy, logos, people).

Needs: ffmpeg/ffprobe, numpy, opencv-python-headless, pillow, scipy.
"""
import json, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def opt(a, k, d=None):
    return a[a.index(k) + 1] if k in a else d


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration:stream=codec_type,width,height,r_frame_rate,sample_rate,channels",
                        "-of", "json", path], capture_output=True, text=True, check=True)
    j = json.loads(r.stdout)
    v = next((s for s in j["streams"] if s["codec_type"] == "video"), {})
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    num, den = (v.get("r_frame_rate", "30/1").split("/") + ["1"])[:2]
    return {"duration": float(j["format"]["duration"]), "width": v.get("width"), "height": v.get("height"),
            "fps": round(float(num) / float(den or 1), 3), "has_audio": a is not None}


def gray_frames(path, fps, w=160, h=90):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={fps},scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(-1, h, w).astype(np.float32)


def rgb_frame(path, t, w=480):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1", "-vf", f"scale={w}:-2", "-f", "image2pipe", "-vcodec", "png", "-"],
                       capture_output=True)
    if not r.stdout:
        return None
    from io import BytesIO
    return Image.open(BytesIO(r.stdout)).convert("RGB")


def scene_cuts(path, thr):
    r = subprocess.run(["ffmpeg", "-v", "info", "-i", path, "-vf", f"select='gt(scene,{thr})',showinfo", "-f", "null", "-"],
                       capture_output=True, text=True)
    return [float(m) for m in re.findall(r"pts_time:([\d.]+)", r.stderr)]


def palette(img, n=5):
    q = img.resize((96, 54)).quantize(colors=n, method=Image.MEDIANCUT)
    pal = q.getpalette()[: n * 3]
    cnt = sorted(q.getcolors(), reverse=True)
    tot = sum(c for c, _ in cnt)
    return [{"hex": "#%02X%02X%02X" % tuple(pal[i * 3:i * 3 + 3]), "share": round(c / tot, 2)} for c, i in cnt]


def camera_motion(frames):
    """Global translation between consecutive frames via phase correlation + scale via edge spread."""
    import cv2
    if len(frames) < 2:
        return {"type": "static", "pan_px_s": 0.0}
    dx = dy = 0.0; mags = []
    for a, b in zip(frames[:-1], frames[1:]):
        (sx, sy), resp = cv2.phaseCorrelate(a, b)
        if resp > 0.05:
            dx += sx; dy += sy; mags.append(np.hypot(sx, sy))
    # zoom hint: compare central vs full-frame change
    first, last = frames[0], frames[-1]
    def spread(f):
        g = np.abs(np.diff(f, axis=1)).mean(0)
        c = np.arange(len(g)) - len(g) / 2
        return float((np.abs(c) * g).sum() / (g.sum() + 1e-6))
    zoom = spread(last) - spread(first)
    diff = float(np.mean([np.abs(b - a).mean() for a, b in zip(frames[:-1], frames[1:])]))
    kind = "static"
    if diff > 2.0: kind = "moving (in-frame motion)"
    if abs(dx) + abs(dy) > 6:
        horiz = "pan right→left content (camera pans right)" if dx < 0 else "pan left→right content (camera pans left)"
        vert = "tilt" if abs(dy) > abs(dx) else None
        kind = ("vertical move " + ("up" if dy < 0 else "down")) if vert else horiz
    if abs(zoom) > 1.2 and abs(dx) + abs(dy) <= 6:
        kind = "push-in / scale up" if zoom < 0 else "pull-out / scale down"
    return {"type": kind, "pan_dx": round(dx, 1), "pan_dy": round(dy, 1), "frame_diff": round(diff, 2), "zoom_hint": round(zoom, 2)}


def audio_analysis(path, dur):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "22050", "-f", "f32le", "-"], capture_output=True)
    x = np.frombuffer(r.stdout, np.float32)
    if len(x) < 22050:
        return None
    sr = 22050; hop = 512
    nfr = len(x) // hop
    frames = x[: nfr * hop].reshape(nfr, hop)
    rms = np.sqrt((frames ** 2).mean(1) + 1e-12)
    db = 20 * np.log10(rms + 1e-9)
    # onset strength: positive spectral flux
    win = np.hanning(1024)
    spec = []
    for i in range(0, len(x) - 1024, hop):
        spec.append(np.abs(np.fft.rfft(x[i:i + 1024] * win))[:200])
    spec = np.log1p(np.array(spec))
    flux = np.maximum(0, np.diff(spec, axis=0)).sum(1)
    flux = (flux - flux.mean()) / (flux.std() + 1e-9)
    fps_o = sr / hop
    # tempo by autocorrelation (60–180 bpm)
    ac = np.correlate(flux, flux, "full")[len(flux) - 1:]
    lo, hi = int(fps_o * 60 / 180), int(fps_o * 60 / 60)
    lag = lo + int(np.argmax(ac[lo:hi])) if hi > lo else lo
    bpm = 60 * fps_o / lag if lag else 0
    while bpm < 80 and bpm > 0: bpm *= 2
    while bpm > 150: bpm /= 2
    # beat phase: best offset of a comb at the period
    period = 60 / bpm if bpm else 0.5
    best, phase = -1e9, 0.0
    for ph in np.linspace(0, period, 24, endpoint=False):
        idx = (np.arange(ph, dur, period) * fps_o).astype(int)
        idx = idx[idx < len(flux)]
        s = flux[idx].sum()
        if s > best: best, phase = s, ph
    beats = [round(b, 3) for b in np.arange(phase, dur, period)]
    # energy curve per second and silence spans
    sec = int(np.ceil(dur))
    per_s = []
    for i in range(sec):
        seg = db[int(i * fps_o):int((i + 1) * fps_o)]
        per_s.append(round(float(seg.max()), 1) if len(seg) else -90.0)
    thr = np.percentile(db, 95) - 35
    silent = db < thr
    spans, start = [], None
    for i, s in enumerate(silent):
        t = i / fps_o
        if s and start is None: start = t
        if not s and start is not None:
            if t - start > 0.35: spans.append([round(start, 2), round(t, 2)])
            start = None
    peaks = np.argsort(flux)[::-1][:12]
    hits = sorted(round(p / fps_o, 2) for p in peaks)
    return {"bpm": round(bpm, 1), "beat_period": round(period, 3), "beats": beats, "loudness_db_per_s": per_s,
            "silences": spans, "strongest_hits": hits}


def color_frames(path, fps=2, w=64, h=36):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={fps},scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(-1, h, w, 3).astype(np.float32)


def beats_in(shot, cf, fps=2, thr=38.0, min_len=1.5):
    """Split a continuous shot where the picture has drifted far from the beat's first frame."""
    s, e = shot["start"], shot["end"]
    i0, i1 = int(s * fps), min(len(cf), int(e * fps))
    out, start, ref = [], s, None
    for i in range(i0, i1):
        t = i / fps
        if ref is None: ref = cf[i]; continue
        d = float(np.abs(cf[i] - ref).mean())
        if d > thr and t - start >= min_len:
            out.append([round(start, 2), round(t, 2)]); start = t; ref = cf[i]
    out.append([round(start, 2), round(e, 2)])
    return out


def label(img, text):
    d = ImageDraw.Draw(img)
    try: f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 14)
    except Exception: f = ImageFont.load_default()
    d.rectangle([0, 0, 8 + 8.5 * len(text), 20], fill=(0, 0, 0))
    d.text((4, 2), text, fill=(255, 255, 255), font=f)
    return img


def main():
    a = sys.argv[1:]
    if not a or a[0].startswith("-"):
        print(__doc__); sys.exit(1)
    src = a[0]
    out = opt(a, "--out", os.path.splitext(os.path.basename(src))[0] + "_analysis")
    thr = float(opt(a, "--scene", 0.28)); max_shots = int(opt(a, "--max-shots", 60))
    os.makedirs(out, exist_ok=True)
    meta = probe(src); D = meta["duration"]
    cuts = [c for c in scene_cuts(src, thr) if 0.25 < c < D - 0.25]
    merged = []
    for c in cuts:
        if not merged or c - merged[-1] > 0.35: merged.append(c)
    bounds = [0.0] + merged + [D]
    if len(bounds) - 1 > max_shots:  # keep the strongest spread if extremely cut-heavy
        idx = np.linspace(0, len(bounds) - 1, max_shots + 1).astype(int)
        bounds = [bounds[i] for i in idx]
    g = gray_frames(src, 8)
    shots = []
    for k in range(len(bounds) - 1):
        s, e = bounds[k], bounds[k + 1]
        fr = g[int(s * 8): max(int(s * 8) + 1, int(e * 8))]
        mid = rgb_frame(src, (s + e) / 2, 320)
        lum = float(np.mean(fr)) if len(fr) else 0
        shots.append({"n": k + 1, "start": round(s, 2), "end": round(e, 2), "dur": round(e - s, 2),
                      "camera": camera_motion([f for f in fr[:: max(1, len(fr) // 12)]]),
                      "brightness": "dark" if lum < 70 else ("light" if lum > 170 else "mid"),
                      "palette": palette(mid) if mid else []})
    # beats: continuous films change scene without cuts -> segment long shots by appearance drift
    cf = color_frames(src)
    beats = []
    for sh in shots:
        segs = beats_in(sh, cf) if sh["dur"] > 5 else [[sh["start"], sh["end"]]]
        for j, (a0, b0) in enumerate(segs):
            beats.append({"n": len(beats) + 1, "shot": sh["n"], "start": a0, "end": b0, "dur": round(b0 - a0, 2),
                          "enters_by": "cut" if j == 0 and sh["n"] > 1 else ("start" if j == 0 else "continuous transition")})
    # motion energy curve (per 0.5 s)
    diffs = np.abs(np.diff(g, axis=0)).mean((1, 2)) if len(g) > 1 else np.zeros(1)
    energy = [round(float(diffs[i:i + 4].mean()), 2) for i in range(0, len(diffs), 4)]
    audio = audio_analysis(src, D) if meta["has_audio"] else None
    rhythm = {"shots": len(shots), "avg_shot_s": round(D / max(1, len(shots)), 2),
              "shortest_s": min(s["dur"] for s in shots), "longest_s": max(s["dur"] for s in shots),
              "motion_energy_per_0.5s": energy}
    if audio and merged:
        near = [c for c in merged if min(abs(c - b) for b in audio["beats"]) < 0.08]
        rhythm["cuts_on_beat_pct"] = round(100 * len(near) / len(merged))
    # contact sheets: 4 frames per shot, 6 shots per sheet
    W = 360; H = int(W * (meta["height"] or 1080) / (meta["width"] or 1920))
    sheets = []
    for si in range(0, len(shots), 6):
        grp = shots[si:si + 6]
        sheet = Image.new("RGB", (W * 4 + 5 * 6, (H + 6) * len(grp) + 6), (24, 24, 24))
        for r, sh in enumerate(grp):
            s, e = sh["start"], sh["end"]
            for c, f in enumerate([0.04, 1 / 3, 2 / 3, 0.96]):
                t = s + (e - s) * f
                im = rgb_frame(src, t, W)
                if im is None: continue
                im = im.resize((W, H))
                label(im, f"#{sh['n']} {t:5.2f}s")
                sheet.paste(im, (6 + c * (W + 6), 6 + r * (H + 6)))
        p = os.path.join(out, f"shots_{si // 6 + 1:02d}.jpg"); sheet.save(p, quality=85); sheets.append(p)
    # timeline sheets: a frame every `step` seconds regardless of cuts (the film as a flipbook)
    step = max(0.5, round(D / 48, 1)) if D > 24 else 0.5
    times = list(np.arange(0.25, D, step))
    tw = 300; th = int(tw * H / W); per = 24; tcols = 6
    for si in range(0, len(times), per):
        grp = times[si:si + per]; rows = int(np.ceil(len(grp) / tcols))
        sh_img = Image.new("RGB", (tcols * (tw + 4) + 4, rows * (th + 4) + 4), (24, 24, 24))
        for i, t in enumerate(grp):
            im = rgb_frame(src, t, tw)
            if im is None: continue
            sh_img.paste(label(im.resize((tw, th)), f"{t:5.2f}s"), (4 + (i % tcols) * (tw + 4), 4 + (i // tcols) * (th + 4)))
        p = os.path.join(out, f"timeline_{si // per + 1:02d}.jpg"); sh_img.save(p, quality=85); sheets.append(p)
    # overview grid
    cols = 6; ow = 240; oh = int(ow * H / W); rows = int(np.ceil(len(shots) / cols))
    ov = Image.new("RGB", (cols * (ow + 4) + 4, rows * (oh + 4) + 4), (24, 24, 24))
    for i, sh in enumerate(shots):
        im = rgb_frame(src, (sh["start"] + sh["end"]) / 2, ow)
        if im is None: continue
        ov.paste(label(im.resize((ow, oh)), f"#{sh['n']}"), (4 + (i % cols) * (ow + 4), 4 + (i // cols) * (oh + 4)))
    ov.save(os.path.join(out, "overview.jpg"), quality=85)

    rhythm["beats"] = len(beats)
    rhythm["avg_beat_s"] = round(D / max(1, len(beats)), 2)
    res = {"source": os.path.abspath(src), "meta": meta, "rhythm": rhythm, "shots": shots, "beats": beats, "audio": audio, "sheets": sheets}
    json.dump(res, open(os.path.join(out, "analysis.json"), "w"), indent=1)
    L = [f"# Reference analysis — {os.path.basename(src)}", "",
         f"{meta['width']}×{meta['height']} · {meta['fps']} fps · {D:.2f} s · audio: {'yes' if meta['has_audio'] else 'no'}", "",
         f"**Rhythm:** {rhythm['shots']} shots · avg {rhythm['avg_shot_s']} s · shortest {rhythm['shortest_s']} s · longest {rhythm['longest_s']} s"
         + (f" · cuts on beat {rhythm.get('cuts_on_beat_pct', 0)}%" if 'cuts_on_beat_pct' in rhythm else ""), ""]
    if audio:
        L += [f"**Audio:** ~{audio['bpm']} bpm (rough estimate — may be 2/3× or 1.5× the felt tempo) (beat {audio['beat_period']} s) · strongest hits at {', '.join(map(str, audio['strongest_hits']))} s"
              + (f" · quiet spans {audio['silences']}" if audio['silences'] else ""), ""]
    L += ["| # | time | dur | camera / motion | light | palette |", "|---|---|---|---|---|---|"]
    for s in shots:
        pal = " ".join(p["hex"] for p in s["palette"][:4])
        L.append(f"| {s['n']} | {s['start']:.2f}–{s['end']:.2f} | {s['dur']:.2f} | {s['camera']['type']} (Δ{s['camera']['frame_diff']}) | {s['brightness']} | {pal} |")
    L += ["", f"**Beats** (scene changes incl. continuous transitions): {len(beats)} · avg {rhythm['avg_beat_s']} s", "",
          "| beat | time | dur | enters by |", "|---|---|---|---|"]
    for b in beats:
        L.append(f"| {b['n']} | {b['start']:.2f}–{b['end']:.2f} | {b['dur']:.2f} | {b['enters_by']} |")
    L += ["", "Motion energy per 0.5 s (higher = more movement):", "`" + " ".join(f"{e:.0f}" for e in energy) + "`", "",
          "Contact sheets (read all of them): " + ", ".join(os.path.basename(p) for p in sheets) + ", overview.jpg", "",
          "Next: fill the Shot Log + Style DNA (DIRECTOR.md §1.5). Camera labels are heuristics — confirm on the sheets."]
    open(os.path.join(out, "analysis.md"), "w").write("\n".join(L) + "\n")
    print(os.path.join(out, "analysis.md"))
    for p in sheets: print(p)
    print(os.path.join(out, "overview.jpg"))


if __name__ == "__main__":
    main()
