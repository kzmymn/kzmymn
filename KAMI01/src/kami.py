"""紙芝居版 試作の音声と映像を作る。

  python3 kami.py --voice jm_kumo            # 音声合成 → out/narration-<voice>.wav と timing
  python3 kami.py --voice jm_kumo --render   # 上に続けて MP4 も書き出す
  python3 kami.py --voice jm_kumo --stills   # 各ビートの静止画（確認用）

画面は絵が主役。語りの文字は画面に出さず、字幕はSRTで別に出す。
音声合成は EP01/src/narration.py の仕組み（Kokoro-82M）を使う。
"""
import argparse, json, math, os, subprocess, sys, tempfile
from functools import lru_cache
from multiprocessing import Pool

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
sys.path.insert(1, os.path.join(ROOT, "..", "EP01", "src"))
from script import BEATS, CARDS, FACES  # noqa: E402

W, H, FPS = 1920, 1080, 30
T = 30                      # 木枠の太さ
SW, SH = W - 2 * T, H - 2 * T
SR = 48000
LEAD = 0.15                 # 絵の切り替えを声より少し先に
PULL = 0.75                 # 絵を抜く時間
ASSETS = os.path.join(ROOT, "assets")
OUT = os.path.join(ROOT, "out")
SERIF = os.path.join(ROOT, "fonts", "NotoSerifJP-Bold.otf")
SERIF_M = os.path.join(ROOT, "fonts", "NotoSerifJP-SemiBold.otf")

INK = (34, 28, 22)
GOLD = (214, 178, 102)
RED = (178, 48, 38)
PAPER = (236, 224, 198)


# ---------------------------------------------------------------------------
# 音
# ---------------------------------------------------------------------------
def clap(strength=1.0):
    """拍子木の音（合成。録音素材は使わない）。"""
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(3)
    y = np.zeros(n)
    for f, d, a in ((2150, 0.030, 1.0), (3400, 0.018, 0.55), (1180, 0.045, 0.45), (5200, 0.010, 0.3)):
        y += a * np.sin(2 * np.pi * f * t) * np.exp(-t / d)
    y += 0.5 * rng.normal(0, 1, n) * np.exp(-t / 0.004)
    return (y / np.abs(y).max() * 0.7 * strength).astype(np.float32)


def build_audio(voice, model_dir):
    from narration import KokoroTTS, trim, resample  # EP01 の仕組み
    tts = KokoroTTS(model_dir, voice)
    claps = [(0.20, 1.0), (0.62, 1.0)]
    t = 1.35
    parts = []   # (開始秒, 波形)
    timing = []
    for i, b in enumerate(BEATS):
        if b["text"] is None:
            timing.append(dict(i=i, card=b["card"], start=round(t, 3), end=round(t + b["hold"], 3), text=None))
            t += b["hold"]
            continue
        a, sr = tts(b.get("say", b["text"]))
        a = trim(resample(a, sr))
        d = len(a) / SR
        parts.append((t, a))
        timing.append(dict(i=i, card=b["card"], start=round(t, 3), end=round(t + d, 3), text=b["text"],
                           name=b.get("name")))
        t += d + b["pause"]
        if b.get("claps") == "roll":   # 「はじまり、はじまり」のあとの連打
            for k, dt in enumerate((0.05, 0.33, 0.55, 0.71, 0.83, 0.92, 0.99, 1.05)):
                claps.append((t + dt, 0.75 + 0.03 * k))
            t += 1.0
        print(f"{i:02d} {timing[-1]['start']:6.2f}-{timing[-1]['end']:6.2f} {b['text']}")
    dur = t
    mix = np.zeros(int((dur + 0.2) * SR), np.float32)
    for st, a in parts:
        k = int(st * SR); mix[k:k + len(a)] += a
    voice_peak = np.abs(mix).max()
    mix *= 0.85 / voice_peak
    for st, s in claps:
        c = clap(s) * 0.55
        k = int(st * SR); mix[k:k + len(c)] += c
    raw = os.path.join(OUT, f"narration-{voice}-raw.wav")
    sf.write(raw, np.clip(mix, -1, 1), SR, subtype="PCM_16")
    wav = os.path.join(OUT, f"narration-{voice}.wav")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                    "-ar", str(SR), "-ac", "1", wav], check=True)
    os.remove(raw)
    with open(os.path.join(OUT, f"timing-{voice}.json"), "w", encoding="utf-8") as f:
        json.dump(dict(duration=round(dur, 3), voice=voice, beats=timing), f, ensure_ascii=False, indent=1)
    print("total", round(dur, 2))


# ---------------------------------------------------------------------------
# 絵の部品
# ---------------------------------------------------------------------------
def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


@lru_cache(maxsize=None)
def font(size, path=SERIF):
    return ImageFont.truetype(path, size)


@lru_cache(maxsize=None)
def src(name):
    return Image.open(os.path.join(ASSETS, name)).convert("RGB")


def cam_crop(img, cx, cy, z, aspect):
    """中心(cx,cy)・見える幅の割合 z で切り抜く（はみ出さないよう補正）。"""
    w0, h0 = img.size
    w = w0 * z
    h = w / aspect
    if h > h0:
        h = h0; w = h * aspect
    x = min(max(cx * w0 - w / 2, 0), w0 - w)
    y = min(max(cy * h0 - h / 2, 0), h0 - h)
    return img.crop((x, y, x + w, y + h))


def ken(card, p):
    (a, b) = card["cam"]
    e = ease(p)
    return tuple(a[k] + (b[k] - a[k]) * e for k in range(3))


@lru_cache(maxsize=None)
def paper(w, h, seed=1):
    rng = np.random.default_rng(seed)
    base = np.array(PAPER, np.float32)
    n = rng.normal(0, 1, (h // 3, w // 3)).astype(np.float32)
    n = np.asarray(Image.fromarray(((n * 10) + 128).clip(0, 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)).astype(np.float32) - 128
    fib = rng.normal(0, 1, (h, w // 8)).astype(np.float32)
    fib = np.asarray(Image.fromarray(((fib * 8) + 128).clip(0, 255).astype(np.uint8)).resize((w, h), Image.BILINEAR)).astype(np.float32) - 128
    yy, xx = np.mgrid[0:h, 0:w]
    vig = 1 - 0.18 * (((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    a = (base[None, None] + (n * 0.5 + fib * 0.35)[..., None]) * vig[..., None]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def vtext(d, x, y, s, size, fill, path=SERIF, gap=1.08):
    f = font(size, path)
    for i, ch in enumerate(s):
        d.text((x, y + i * size * gap), ch, font=f, fill=fill, anchor="mt")


def name_plate(img, name, alpha):
    if alpha <= 0:
        return img
    size = 52
    h = int(len(name) * size * 1.08 + 46)
    plate = Image.new("RGBA", (size + 44, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(plate)
    d.rectangle((0, 0, size + 43, h - 1), fill=(241, 232, 210, 235), outline=(90, 64, 40, 255), width=3)
    d.rectangle((6, 6, size + 37, h - 7), outline=(150, 112, 70, 255), width=1)
    vtext(d, (size + 44) // 2, 22, name, size, INK)
    plate.putalpha(Image.eval(plate.getchannel("A"), lambda v: int(v * alpha)))
    img.paste(plate, (64, 60), plate)
    return img


def note(img, txt="肖像・情景は創作イメージ"):
    d = ImageDraw.Draw(img)
    f = font(22, SERIF_M)
    x, y = SW - 22, SH - 18
    d.text((x + 1, y + 1), txt, font=f, fill=(0, 0, 0), anchor="rd")
    d.text((x, y), txt, font=f, fill=(235, 228, 210), anchor="rd")
    return img


def panel(name, pw, ph, zoom):
    im = src(name)
    w0, h0 = im.size
    fx, fy = FACES[name]
    h = h0 * zoom
    w = h * pw / ph
    x = min(max(fx * w0 - w / 2, 0), w0 - w)
    y = min(max(fy * h0 - h / 2, 0), h0 - h)
    return im.crop((x, y, x + w, y + h)).resize((pw, ph), Image.BICUBIC)


def castle(d, x, y, s, col=INK, fill=(222, 206, 172)):
    d.rectangle((x - 34 * s, y - 30 * s, x + 34 * s, y + 18 * s), fill=fill, outline=col, width=max(2, int(4 * s)))
    d.polygon([(x - 50 * s, y - 28 * s), (x, y - 62 * s), (x + 50 * s, y - 28 * s)], fill=(70, 60, 52), outline=col)
    d.rectangle((x - 10 * s, y - 6 * s, x + 10 * s, y + 18 * s), fill=(70, 60, 52))
    d.rectangle((x - 48 * s, y + 18 * s, x + 48 * s, y + 30 * s), fill=(150, 140, 125), outline=col, width=2)


def brush_line(d, pts, col, width):
    d.line(pts, fill=col, width=width, joint="curve")
    for p in (pts[0], pts[-1]):
        d.ellipse((p[0] - width / 2, p[1] - width / 2, p[0] + width / 2, p[1] + width / 2), fill=col)


# ---------------------------------------------------------------------------
# カードの描画（ステージ内の画像を返す）
# ---------------------------------------------------------------------------
def draw_card(cid, p, lt, seg):
    c = CARDS[cid]
    k = c["kind"]
    if k in ("img", "title"):
        im = src(c["src"])
        if "crop" in c:
            x0, y0, x1, y1 = c["crop"]
            w0, h0 = im.size
            im = im.crop((x0 * w0, y0 * h0, x1 * w0, y1 * h0))
        cx, cy, z = ken(c, p)
        out = cam_crop(im, cx, cy, z, SW / SH).resize((SW, SH), Image.BICUBIC)
        if c.get("bright"):
            out = Image.eval(out, lambda v: min(255, int(v * c["bright"])))
        if k == "title":
            a = ease((lt - 0.2) / 0.9)
            out = Image.blend(out, Image.new("RGB", out.size, (8, 8, 6)), 0.5 * a)
            d = ImageDraw.Draw(out)
            f1, f2 = font(118), font(46, SERIF_M)
            col1 = tuple(int(v * a + 8 * (1 - a)) for v in GOLD)
            col2 = tuple(int(v * a + 8 * (1 - a)) for v in (236, 228, 208))
            tx = int(SW * 0.33)   # 鳥（右側）に重ねない
            d.text((tx, SH // 2 - 70), "信長・秀吉・家康", font=f1, fill=col1, anchor="mm")
            d.line((tx - 330, SH // 2 + 20, tx + 330, SH // 2 + 20), fill=col1, width=2)
            d.text((tx, SH // 2 + 82), "ホトトギスの句ではわからない、三人の関係", font=f2, fill=col2, anchor="mm")
        else:
            nm = seg.get("name")
            if nm:
                out = name_plate(out, nm, ease((lt - 0.3) / 0.4))
            out = note(out)
        return out
    if k in ("trio", "rivals"):
        names = ["nobunaga.png", "hideyoshi.png", "ieyasu.png"] if k == "trio" else ["hideyoshi.png", "ieyasu.png"]
        labels = ["織田信長", "豊臣秀吉", "徳川家康"] if k == "trio" else ["豊臣秀吉", "徳川家康"]
        n = len(names)
        pw = SW // n
        zoom = 0.92 - 0.12 * ease(p)
        out = Image.new("RGB", (SW, SH), (12, 10, 8))
        for i, nmf in enumerate(names):
            out.paste(panel(nmf, pw, SH, zoom), (i * pw, 0))
        d = ImageDraw.Draw(out)
        for i in range(1, n):
            col = GOLD if k == "trio" else RED
            d.rectangle((i * pw - 3, 0, i * pw + 3, SH), fill=col)
        for i, lab in enumerate(labels):
            sub = out.crop((i * pw, 0, (i + 1) * pw, SH))
            sub = name_plate(sub, lab, ease((lt - 0.2) / 0.4) * 0.95)
            out.paste(sub, (i * pw, 0))
        return note(out)
    if k == "map":
        out = paper(SW, SH).copy()
        d = ImageDraw.Draw(out)
        d.text((SW // 2, 110), "尾張（おわり）の位置", font=font(64), fill=INK, anchor="mm")
        d.text((SW // 2, 180), "位置関係の模式図（境界や距離は正確ではありません）", font=font(28, SERIF_M), fill=(110, 92, 70), anchor="mm")
        y = SH // 2 + 40
        brush_line(d, [(260, y), (SW - 260, y)], (120, 100, 78), 6)
        d.text((230, y + 120), "西", font=font(40), fill=(110, 92, 70), anchor="mm")
        d.text((SW - 230, y + 120), "東", font=font(40), fill=(110, 92, 70), anchor="mm")
        nodes = [(0.24, "京都", None, False), (0.58, "尾張", "いまの愛知県西部", True), (0.80, "三河", "いまの愛知県東部", False)]
        for j, (fx, lab, sub, hi) in enumerate(nodes):
            a = ease((lt - 0.15 - 0.25 * j) / 0.35)
            if a <= 0:
                continue
            x = int(fx * SW)
            r = 26
            fillc = RED if hi else (90, 76, 60)
            d.ellipse((x - r, y - r, x + r, y + r), fill=fillc)
            d.text((x, y - (105 if hi else 70)), lab, font=font(76 if hi else 54), fill=RED if hi else INK, anchor="mm")
            if sub:
                d.text((x, y + 100), sub, font=font(38 if hi else 30, SERIF_M), fill=INK if hi else (110, 92, 70), anchor="mm")
            if hi:
                g = ease((lt - 0.8) / 0.6)
                if g > 0:
                    rr = 44 + 8 * g
                    d.arc((x - rr, y - rr, x + rr, y + rr), start=270, end=270 + 360 * g, fill=RED, width=6)
        return out
    if k == "kyoto":
        out = paper(SW, SH, 2).copy()
        d = ImageDraw.Draw(out)
        bt = seg["beat_starts"]   # このカード内の各ビート開始（絶対秒）
        t = seg["t"]
        cx, cy = SW // 2, SH // 2 + 20
        pos = [(cx + 660 * math.cos(a), cy + 300 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 7)[:-1] + 0.5]
        # 各地の大名と争い
        for j, (x, y) in enumerate(pos):
            a = ease((t - bt[0] - 0.12 * j) / 0.3)
            if a > 0:
                castle(d, x, y, 1.45 * a)
                d.text((x, y + 82), "大名", font=font(42), fill=INK, anchor="mm")
        for j in range(6):
            a = ease((t - bt[0] - 1.0 - 0.15 * j) / 0.3)
            if a > 0:
                x0, y0 = pos[j]; x1, y1 = pos[(j + 1) % 6]
                mx, my = (x0 + x1) / 2, (y0 + y1) / 2
                s = 26 * a
                d.line((mx - s, my - s, mx + s, my + s), fill=RED, width=7)
                d.line((mx - s, my + s, mx + s, my - s), fill=RED, width=7)
        # 京都（天皇・朝廷／将軍）
        if len(bt) > 1:
            a = ease((t - bt[1]) / 0.4)
            if a > 0:
                r = 150 * (0.85 + 0.15 * a)
                d.ellipse((cx - r * 1.35, cy - r, cx + r * 1.35, cy + r), fill=(246, 238, 220), outline=INK, width=5)
                d.text((cx, cy - 52), "京都", font=font(72), fill=INK, anchor="mm")
                d.text((cx, cy + 34), "天皇・朝廷", font=font(40, SERIF_M), fill=INK, anchor="mm")
                d.text((cx, cy + 88), "将軍", font=font(40, SERIF_M), fill=INK, anchor="mm")
        # 命令が届ききらない
        if len(bt) > 2:
            for j, (x, y) in enumerate(pos):
                a = ease((t - bt[2] - 0.6 - 0.08 * j) / 0.6)
                if a <= 0:
                    continue
                L = 0.42 * a
                sx, sy = cx + (x - cx) * 0.33, cy + (y - cy) * 0.36
                ex, ey = sx + (x - sx) * L, sy + (y - sy) * L
                d.line((sx, sy, ex, ey), fill=(120, 100, 78), width=5)
                if a >= 1:
                    s = 16
                    d.line((ex - s, ey - s, ex + s, ey + s), fill=RED, width=6)
                    d.line((ex - s, ey + s, ex + s, ey - s), fill=RED, width=6)
        return out
    raise ValueError(k)


# ---------------------------------------------------------------------------
# 時間割と合成
# ---------------------------------------------------------------------------
def segments(Tm):
    segs = []
    for b in Tm["beats"]:
        if segs and segs[-1]["card"] == b["card"]:
            segs[-1]["beat_starts"].append(b["start"])
            continue
        st = 0.0 if not segs else (b["start"] if b["text"] is None else b["start"] - LEAD)
        segs.append(dict(card=b["card"], start=st, beat_starts=[b["start"]], name=b.get("name"),
                         trans="fade" if CARDS[b["card"]]["kind"] == "title" else "pull"))
    for i, s in enumerate(segs):
        s["end"] = segs[i + 1]["start"] if i + 1 < len(segs) else Tm["duration"]
    return segs


def stage_at(segs, i, t):
    s = dict(segs[i]); s["t"] = t
    p = (t - s["start"]) / max(0.1, s["end"] - s["start"])
    return draw_card(s["card"], p, t - s["start"], s)


@lru_cache(maxsize=1)
def frame_overlay():
    """紙芝居の木枠（ステージの外側）。"""
    rng = np.random.default_rng(5)
    g = rng.normal(0, 1, (H, 12)).astype(np.float32)
    grain = np.asarray(Image.fromarray(((g * 18) + 128).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)).astype(np.float32) - 128
    base = np.array((104, 70, 42), np.float32)
    wood = (base[None, None] + grain[..., None] * np.array((0.5, 0.36, 0.22))).clip(0, 255).astype(np.uint8)
    img = Image.fromarray(wood).convert("RGBA")
    mask = Image.new("L", (W, H), 255)
    ImageDraw.Draw(mask).rectangle((T, T, W - T - 1, H - T - 1), fill=0)
    img.putalpha(mask)
    d = ImageDraw.Draw(img)
    d.rectangle((T - 4, T - 4, W - T + 3, H - T + 3), outline=(40, 26, 14, 255), width=4)
    d.rectangle((1, 1, W - 2, H - 2), outline=(150, 110, 70, 255), width=2)
    return img


def render_frame(segs, f):
    t = f / FPS
    i = max(k for k, s in enumerate(segs) if s["start"] <= t) if t >= 0 else 0
    s = segs[i]
    cur = stage_at(segs, i, t)
    lt = t - s["start"]
    if i > 0 and lt < PULL:
        prev = stage_at(segs, i - 1, s["start"])
        e = ease(lt / PULL)
        if s["trans"] == "fade":
            cur = Image.blend(prev, cur, e)
        else:   # 紙を右へ抜く
            dx = int(e * SW)
            canvas = cur.copy()
            sh = Image.new("L", (40, SH), 0)
            ImageDraw.Draw(sh).rectangle((0, 0, 40, SH), fill=90)
            shadow = Image.new("RGB", (40, SH), (0, 0, 0))
            canvas.paste(shadow, (max(0, dx - 30), 0), sh.filter(ImageFilter.GaussianBlur(10)))
            canvas.paste(prev.crop((0, 0, SW - dx, SH)), (dx, 0))
            cur = canvas
    out = Image.new("RGB", (W, H))
    out.paste(cur, (T, T))
    fr = frame_overlay()
    out.paste(fr, (0, 0), fr)
    return out


def _worker(args):
    tm, f0, f1, path = args
    segs = segments(json.load(open(tm, encoding="utf-8")))
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                           "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for f in range(f0, f1):
        ff.stdin.write(render_frame(segs, f).tobytes())
    ff.stdin.close(); ff.wait()
    return path


def write_srt(Tm, path):
    def ts(x):
        ms = int(round(x * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    bs = [b for b in Tm["beats"] if b["text"]]
    with open(path, "w", encoding="utf-8") as f:
        for i, b in enumerate(bs):
            nxt = bs[i + 1]["start"] if i + 1 < len(bs) else Tm["duration"]
            f.write(f"{i + 1}\n{ts(b['start'] - 0.05)} --> {ts(min(nxt - 0.1, b['end'] + 0.6))}\n{b['text']}\n\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default="jm_kumo")
    ap.add_argument("--model", default="/tmp/claude-0/kokoro")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--stills", action="store_true")
    ap.add_argument("--skip-audio", action="store_true")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    tm = os.path.join(OUT, f"timing-{a.voice}.json")
    if not a.skip_audio:
        build_audio(a.voice, a.model)
    Tm = json.load(open(tm, encoding="utf-8"))
    write_srt(Tm, os.path.join(OUT, f"KAMI01-trial-{a.voice}.ja.srt"))
    segs = segments(Tm)
    if a.stills:
        d = os.path.join(OUT, "stills"); os.makedirs(d, exist_ok=True)
        for b in Tm["beats"]:
            render_frame(segs, int((b["end"] - 0.1) * FPS)).save(os.path.join(d, f"beat{b['i']:02d}.jpg"), quality=85)
        print("stills ->", d)
    if a.render:
        n = int(math.ceil(Tm["duration"] * FPS))
        tmp = tempfile.mkdtemp(dir=OUT)
        k = os.cpu_count()
        jobs = [(tm, n * j // k, n * (j + 1) // k, os.path.join(tmp, f"p{j}.mp4")) for j in range(k)]
        with Pool(k) as pool:
            parts = pool.map(_worker, jobs)
        lst = os.path.join(tmp, "l.txt")
        open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
        out = os.path.join(OUT, f"KAMI01-trial-{a.voice}.mp4")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                        "-i", os.path.join(OUT, f"narration-{a.voice}.wav"), "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
        for p in parts:
            os.remove(p)
        os.remove(lst); os.rmdir(tmp)
        print("->", out)


if __name__ == "__main__":
    main()
