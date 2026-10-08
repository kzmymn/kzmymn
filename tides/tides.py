"""潮騒の記憶 / THE MEMORY OF TIDES — kinetic typography teaser.

Monochrome ink-on-paper posters, one per beat-bar, hard cuts with glitch.
Usage: python3 tides.py out.mp4   |   F=<frame> python3 tides.py test.png
"""
import os, sys, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from multiprocessing import Pool

W, H = 1920, 1080
FPS = 30
BPM = 90
BAR = 4 * 60 / BPM            # 2.667s per scene
SCENES = 7                     # 6 poems + finale
DUR = BAR * SCENES
NF = int(round(DUR * FPS))

FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
def _f(pkg, name):
    return os.path.join(FD, pkg, "package", name.split("_")[1].split(".")[0], name)
SERIF = _f("expo-google-fonts-noto-serif-jp-0.4.4", "NotoSerifJP_900Black.ttf")
SERIF_M = _f("expo-google-fonts-noto-serif-jp-0.4.4", "NotoSerifJP_500Medium.ttf")
SANS = _f("expo-google-fonts-noto-sans-jp-0.4.4", "NotoSansJP_900Black.ttf")
SANS_M = _f("expo-google-fonts-noto-sans-jp-0.4.4", "NotoSansJP_500Medium.ttf")
MONO = _f("expo-google-fonts-space-mono-0.4.2", "SpaceMono_700Bold.ttf")
MONO_R = _f("expo-google-fonts-space-mono-0.4.2", "SpaceMono_400Regular.ttf")
_fc = {}
def font(path, size):
    k = (path, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]

ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


def hash01(*a):
    v = math.sin(sum((i + 1) * 12.9898 * x for i, x in enumerate(a)) + 78.233) * 43758.5453
    return v - math.floor(v)


# ---------------------------------------------------------------- type helpers
def text_h(ink, s, fpath, size, x, y, t, delay=0.0, stagger=0.05, rise=40, track=0):
    """Horizontal text revealed char-by-char (slide up + flicker)."""
    d = ImageDraw.Draw(ink)
    f = font(fpath, size)
    cx = x
    for i, ch in enumerate(s):
        p = (t - delay - i * stagger) / 0.35
        if p > 0:
            on = p > 1 or hash01(i, int(t * FPS)) < p + 0.2
            if on:
                dy = (1 - ease(p)) * rise
                d.text((cx, y + dy), ch, font=f, fill=255)
        cx += f.getlength(ch) + track
    return cx


def text_v(ink, s, fpath, size, x, y, t, delay=0.0, stagger=0.06, lead=1.0):
    """Vertical (tategaki) text, top to bottom."""
    d = ImageDraw.Draw(ink)
    f = font(fpath, size)
    cy = y
    for i, ch in enumerate(s):
        p = (t - delay - i * stagger) / 0.35
        if p > 0 and (p > 1 or hash01(i, 7, int(t * FPS)) < p + 0.2):
            dx = (1 - ease(p)) * -30
            w = f.getlength(ch)
            if ch in "、。":
                d.text((x + size * 0.55 + dx, cy - size * 0.55), ch, font=f, fill=255)
            else:
                d.text((x + (size - w) / 2 + dx, cy), ch, font=f, fill=255)
        cy += size * lead
    return cy


def text_rot(ink, s, fpath, size, x, y, angle=90):
    """Small rotated caption (e.g. running up the edge)."""
    f = font(fpath, size)
    w = int(f.getlength(s)) + 4
    tmp = Image.new("L", (w, size + 10), 0)
    ImageDraw.Draw(tmp).text((0, 0), s, font=f, fill=255)
    tmp = tmp.rotate(angle, expand=True)
    ink.paste(255, (int(x), int(y)), tmp)


def circled(ink, s, x, y, size=26):
    d = ImageDraw.Draw(ink)
    f = font(MONO, size)
    w = f.getlength(s)
    d.rounded_rectangle((x, y, x + w + size * 1.2, y + size * 1.45), radius=size, outline=255, width=3)
    d.text((x + size * 0.6, y + size * 0.05), s, font=f, fill=255)


def meta(ink, n, t, en):
    """Shared poster furniture: corners, scene number, date block, footer row."""
    d = ImageDraw.Draw(ink)
    sm, xs_ = font(MONO, 22), font(MONO_R, 17)
    d.text((70, 52), "TIDE / MEMORY  —  AMBIENT ELECTRONIC SESSIONS", font=xs_, fill=255)
    d.text((W - 70 - xs_.getlength("ZUSHI BEACH — KANAGAWA"), 52), "ZUSHI BEACH — KANAGAWA", font=xs_, fill=255)
    d.line((70, 84, W - 70, 84), fill=255, width=2)
    foot = [f"NO.{n:02d}", "FIELD REC.", en, "2026.11.21 SAT", "OPEN 23:00 — 05:00"]
    xs2 = np.linspace(70, W - 70, len(foot) + 1)[:-1]
    for i, s in enumerate(foot):
        d.text((xs2[i], H - 64), s, font=xs_, fill=255)
    d.line((70, H - 78, W - 70, H - 78), fill=255, width=2)
    # blinking record dot
    if int(t * 2) % 2 == 0:
        d.ellipse((W - 96, H - 64, W - 80, H - 48), fill=255)


def date_block(ink, x, y, n):
    circled(ink, f"{n:02d}", x, y)
    d = ImageDraw.Draw(ink)
    f = font(MONO, 34)
    for i, s in enumerate(["2026", "NOV", "NIGHT"]):
        d.text((x, y + 52 + i * 36), s, font=f, fill=255)


# ------------------------------------------------------------- image helpers
def halftone(I, cell=9, angle=0.5, ox=0.0, oy=0.0):
    """Intensity field (0..1, ink amount) -> amplitude-modulated dot screen."""
    ca, sa = math.cos(angle), math.sin(angle)
    u = (xs * ca + ys * sa) / cell + ox
    v = (-xs * sa + ys * ca) / cell + oy
    fu, fv = u - np.floor(u) - 0.5, v - np.floor(v) - 0.5
    r = np.sqrt(fu * fu + fv * fv)
    rad = np.sqrt(np.clip(I, 0, 1)) * 0.62
    return np.clip((rad - r) * cell * 0.9 + 0.5, 0, 1)


def vnoise(x, y, seed=0):
    xi, yi = np.floor(x), np.floor(y)
    xf, yf = x - xi, y - yi
    def h(a, b):
        v = np.sin(a * 127.1 + b * 311.7 + seed * 74.7) * 43758.5453
        return v - np.floor(v)
    u, v = xf * xf * (3 - 2 * xf), yf * yf * (3 - 2 * yf)
    a, b, c, d = h(xi, yi), h(xi + 1, yi), h(xi, yi + 1), h(xi + 1, yi + 1)
    return (a + (b - a) * u) * (1 - v) + (c + (d - c) * u) * v


def fbm(x, y, seed=0, o=4):
    s, a = 0, 0.5
    for k in range(o):
        s = s + a * vnoise(x, y, seed + k)
        x, y, a = x * 2.03, y * 2.03, a * 0.5
    return s


def smooth(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


# ------------------------------------------------------------------- scenes
def s1(t, ink):
    """01 波を数える夜 — stacked wave lines scrolling."""
    d = ImageDraw.Draw(ink)
    x = np.arange(0, W + 8, 8, dtype=np.float32)
    for k in range(26):
        base = 690 + k * 13
        amp = 6 + k * 1.6
        ph = t * (1.2 + k * 0.05) + k * 0.6
        yv = base + amp * np.sin(x * (0.004 + 0.0002 * k) + ph) + 0.5 * amp * np.sin(x * 0.011 - ph * 1.3)
        reveal = ease((t - k * 0.02) / 0.8)
        n = max(2, int(len(x) * reveal))
        d.line(list(zip(x[:n].tolist(), yv[:n].tolist())), fill=255, width=2 + k // 8)
    f = SERIF
    text_h(ink, "潮騒の記憶", SANS, 54, 70, 118, t, 0.0, 0.04)
    text_h(ink, "THE MEMORY", MONO, 92, 70, 190, t, 0.1, 0.025)
    text_h(ink, "OF TIDES", MONO, 92, 70, 290, t, 0.2, 0.025)
    text_h(ink, "波を", f, 300, 1010, 70, t, 0.25, 0.12)
    text_h(ink, "数える夜", f, 200, 1080, 400, t, 0.45, 0.1)
    date_block(ink, 760, 120, 1)
    text_rot(ink, "COUNTING THE WAVES UNTIL DAWN", MONO_R, 18, W - 110, 120)
    meta(ink, 1, t, "COUNTING WAVES")


def s2(t, ink):
    """02 月が満ちる — halftone moon swelling."""
    cx, cy = 900 + 20 * t, 560
    R = 300 + 40 * ease(t / BAR)
    dx, dy = (xs - cx) / R, (ys - cy) / R
    r2 = dx * dx + dy * dy
    disk = smooth(1.0, 0.97, np.sqrt(r2))
    phase = -1.1 + 1.4 * ease(t / (BAR * 0.8))           # terminator sweeps -> fuller moon
    lit = smooth(-0.15, 0.15, dx - phase * np.sqrt(np.clip(1 - dy * dy, 0, 1)))
    craters = fbm(dx * 3 + 5, dy * 3, 3)
    I = disk * (0.18 + 0.7 * lit * (0.55 + 0.6 * craters))
    I += smooth(1.35, 1.0, np.sqrt(r2)) * 0.12 * (1 - disk)   # halo
    m = halftone(I, cell=10, angle=0.4 + 0.05 * t)
    a = np.asarray(ink, np.float32) / 255
    ink.paste(Image.fromarray((np.maximum(a, m) * 255).astype(np.uint8)))
    text_v(ink, "月が満ちる", SERIF, 160, 1590, 120, t, 0.2, 0.12, 0.98)
    text_h(ink, "満", SERIF, 520, 110, 330, t, 0.05, 0.1)
    date_block(ink, 1350, 120, 2)
    text_rot(ink, "THE MOON IS FULL — AND SO IS THE SEA", MONO_R, 18, 70, 140)
    text_h(ink, "THE MOON", MONO, 40, 1350, 820, t, 0.6, 0.03)
    text_h(ink, "IS FULL", MONO, 40, 1350, 868, t, 0.7, 0.03)
    meta(ink, 2, t, "FULL MOON")


def s3(t, ink):
    """03 言葉が沈む — a sentence sinks and dissolves."""
    sink = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(sink)
    s = "言えなかった言葉が、静かに沈んでいく。"
    f = font(SERIF_M, 64)
    x = 220
    for i, ch in enumerate(s):
        st = 0.5 + hash01(i, 3) * 0.9
        p = max(0.0, t - st)
        y = 300 + p * p * (90 + 160 * hash01(i, 9)) + math.sin(p * 2 + i) * 6 * p
        d.text((x, y), ch, font=f, fill=int(255 * max(0.0, 1 - p * 0.35)))
        x += f.getlength(ch)
    sink = sink.filter(ImageFilter.GaussianBlur(min(6, max(0, t - 1.0) * 3)))
    ink.paste(255, (0, 0), sink)
    text_h(ink, "言葉が", SERIF, 290, 120, 500, t, 0.0, 0.1)
    text_h(ink, "沈む", SERIF, 290, 1100, 600, t, 0.35, 0.14)
    date_block(ink, 1600, 130, 3)
    text_h(ink, "WORDS SINK", MONO, 30, 220, 230, t, 0.1, 0.03)
    text_h(ink, "TO THE BOTTOM", MONO, 30, 220, 264, t, 0.2, 0.03)
    # depth gauge
    d2 = ImageDraw.Draw(ink)
    for k in range(18):
        y = 160 + k * 46
        d2.line((W - 110, y, W - 110 + (28 if k % 5 == 0 else 14), y), fill=255, width=2)
    gy = 160 + min(1, t / BAR) * 17 * 46
    d2.polygon([(W - 120, gy), (W - 140, gy - 10), (W - 140, gy + 10)], fill=255)
    meta(ink, 3, t, "SINKING WORDS")


def s4(t, ink):
    """04 遠い灯台 — lighthouse beam sweeping."""
    lx, ly = 520, 470
    ang = -2.6 + 2.2 * (t / BAR)                         # sweep
    wid = 0.10 + 0.08 * abs(math.cos(t * 1.3))
    a = np.arctan2(ys - ly, xs - lx)
    da = np.angle(np.exp(1j * (a - ang)))
    dist = np.sqrt((xs - lx) ** 2 + (ys - ly) ** 2)
    beam = smooth(wid, wid * 0.3, np.abs(da)) * smooth(30, 120, dist) * np.exp(-dist / 1400)
    # mirrored dim beam (back side of the lamp)
    da2 = np.angle(np.exp(1j * (a - ang - math.pi)))
    beam += 0.35 * smooth(wid, wid * 0.3, np.abs(da2)) * smooth(30, 120, dist) * np.exp(-dist / 600)
    sea = (ys > 760) * (0.25 + 0.2 * np.sin(xs * 0.02 + ys * 0.3 + t * 3) * smooth(760, 1000, ys))
    I = np.clip(beam * 0.95 + sea * 0.4, 0, 1)
    m = halftone(I, cell=7, angle=1.1)
    arr = np.asarray(ink, np.float32) / 255
    ink.paste(Image.fromarray((np.maximum(arr, m) * 255).astype(np.uint8)))
    d = ImageDraw.Draw(ink)
    # tower silhouette
    d.polygon([(lx - 38, ly + 20), (lx + 38, ly + 20), (lx + 62, 770), (lx - 62, 770)], fill=255)
    d.rectangle((lx - 46, ly - 34, lx + 46, ly + 20), fill=255)
    d.polygon([(lx - 52, ly - 34), (lx + 52, ly - 34), (lx, ly - 90)], fill=255)
    d.ellipse((lx - 20, ly - 26, lx + 20, ly + 14), fill=0)
    d.rectangle((0, 768, W, 774), fill=255)
    text_h(ink, "遠い", SERIF, 240, 1040, 110, t, 0.1, 0.12)
    text_h(ink, "灯台", SERIF, 240, 1300, 360, t, 0.3, 0.12)
    date_block(ink, 80, 130, 4)
    text_h(ink, "A DISTANT LIGHTHOUSE", MONO, 34, 1040, 640, t, 0.6, 0.02)
    text_h(ink, "光は、ここにいると告げる。", SANS_M, 36, 1040, 690, t, 0.8, 0.04)
    meta(ink, 4, t, "LIGHTHOUSE")


def s5(t, ink):
    """05 泡になる — bubbles rising through big type."""
    text_v(ink, "泡に", SERIF, 300, 1560, 100, t, 0.0, 0.12, 1.0)
    text_v(ink, "なる", SERIF, 300, 1240, 240, t, 0.2, 0.12, 1.0)
    d = ImageDraw.Draw(ink)
    for i in range(70):
        r = 6 + 60 * hash01(i, 1) ** 3
        sp = 120 + 260 * hash01(i, 2)
        x0 = 80 + hash01(i, 3) * 1700
        y = H + 80 - ((t + hash01(i, 4) * 6) * sp) % (H + 200)
        x = x0 + math.sin(t * 2 + i) * 18
        if hash01(i, 5) < 0.35:
            d.ellipse((x - r, y - r, x + r, y + r), fill=255)
            d.ellipse((x - r * 0.55, y - r * 0.65, x - r * 0.15, y - r * 0.25), fill=0)
        else:
            d.ellipse((x - r, y - r, x + r, y + r), outline=255, width=max(2, int(r / 8)))
    date_block(ink, 80, 130, 5)
    text_h(ink, "BECOMING", MONO, 96, 80, 700, t, 0.4, 0.03)
    text_h(ink, "FOAM", MONO, 96, 80, 810, t, 0.5, 0.03)
    text_rot(ink, "EVERYTHING RETURNS TO THE SEA", MONO_R, 18, W - 110, 140)
    meta(ink, 5, t, "FOAM")


def s6(t, ink):
    """06 また、朝が来る — sunrise over the horizon."""
    hy = 690
    rise = ease(t / BAR)
    sx, sy, R = 960, hy + 140 - 260 * rise, 230
    dist = np.sqrt((xs - sx) ** 2 + (ys - sy) ** 2)
    sun = smooth(R, R - 3, dist) * (ys < hy)
    glow = np.exp(-np.maximum(dist - R, 0) / 260) * 0.35 * (ys < hy)
    refl = (ys > hy) * np.exp(-np.abs(xs - sx) / np.maximum(90 + (ys - hy) * 0.6, 30)) * (0.5 + 0.5 * np.sin(ys * 0.45 + t * 4)) * smooth(1000, hy, ys)
    I = np.clip(np.maximum(sun * 0.95, glow) + refl * 0.9 * rise, 0, 1)
    m = halftone(I, cell=8, angle=0.25)
    arr = np.asarray(ink, np.float32) / 255
    ink.paste(Image.fromarray((np.maximum(arr, m) * 255).astype(np.uint8)))
    ImageDraw.Draw(ink).rectangle((70, hy - 2, W - 70, hy + 2), fill=255)
    text_h(ink, "また、", SERIF, 210, 90, 130, t, 0.0, 0.12)
    text_h(ink, "朝が来る", SERIF, 210, 960, 130, t, 0.3, 0.12)
    date_block(ink, 90, 800, 6)
    text_h(ink, "MORNING COMES AGAIN", MONO, 34, 1260, 820, t, 0.6, 0.02)
    meta(ink, 6, t, "SUNRISE")


def s7(t, ink):
    """Finale — title card with event details."""
    x = np.arange(0, W + 8, 8, dtype=np.float32)
    d = ImageDraw.Draw(ink)
    for k in range(6):
        yv = 880 + k * 14 + 5 * np.sin(x * 0.006 + t * 1.5 + k)
        d.line(list(zip(x.tolist(), yv.tolist())), fill=255, width=2)
    text_h(ink, "潮騒の記憶", SERIF, 250, 230, 230, t, 0.0, 0.1)
    text_h(ink, "THE MEMORY OF TIDES", MONO, 64, 240, 560, t, 0.4, 0.02)
    text_h(ink, "2026.11.21 SAT  23:00 — 05:00  /  ZUSHI BEACH", MONO_R, 30, 240, 670, t, 0.7, 0.012)
    text_h(ink, "実験的なアンビエント・エレクトロニック・ミュージック", SANS_M, 30, 240, 730, t, 0.9, 0.015)
    circled(ink, "FIN", 240, 140)
    meta(ink, 7, t, "SEE YOU AT THE SHORE")


SCENE_FNS = [s1, s2, s3, s4, s5, s6, s7]

# ---------------------------------------------------------------- compositing
PAPER = None


def paper():
    global PAPER
    if PAPER is None:
        rng = np.random.default_rng(1)
        base = 0.905 + 0.035 * (fbm(xs / 300, ys / 300, 11) - 0.5)
        fib = fbm(xs / 3, ys / 40, 21, 3) - 0.5          # paper fibres
        blot = smooth(0.62, 0.8, fbm(xs / 120, ys / 120, 31))
        PAPER = np.clip(base + 0.03 * fib - 0.05 * blot, 0, 1).astype(np.float32)
    return PAPER


def frame(i):
    t_all = i / FPS
    si = min(int(t_all // BAR), SCENES - 1)
    t = t_all - si * BAR
    ink = Image.new("L", (W, H), 0)
    SCENE_FNS[si](t, ink)

    # slow push-in
    z = 1.0 + 0.025 * (t / BAR)
    if z > 1.0005:
        cw, ch = W / z, H / z
        ink = ink.resize((W, H), Image.BILINEAR, box=((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2))
    a = np.asarray(ink, np.float32) / 255

    rng = np.random.default_rng(i)
    # stop-motion jitter (changes every 2 frames)
    jr = np.random.default_rng(i // 2)
    a = np.roll(a, (int(jr.integers(-2, 3)), int(jr.integers(-2, 3))), axis=(0, 1))

    # rough ink: speckle + slight bleed
    grain = rng.random((H, W), dtype=np.float32)
    a = a * (0.82 + 0.18 * grain)
    a = np.where(grain < 0.012, a * 0.2, a)

    p = paper() * (0.985 + 0.015 * rng.random())
    img = p * (1 - 0.9 * a)
    img += (rng.random((H, W), dtype=np.float32) - 0.5) * 0.09

    # glitch on cuts: slice offsets + one inverted flash
    fi = int(round(t * FPS))
    if si > 0 and fi < 4:
        if fi == 0:
            img = 1 - img * 0.9
        for k in range(10):
            y0 = int(rng.integers(0, H - 40)); hh = int(rng.integers(6, 60))
            img[y0:y0 + hh] = np.roll(img[y0:y0 + hh], int(rng.integers(-160, 160)), axis=1)

    vig = 1 - 0.18 * (((xs - W / 2) / W) ** 2 + ((ys - H / 2) / H) ** 2) * 2
    img = np.clip(img * vig, 0, 1)
    return (img * 255).astype(np.uint8).tobytes()


# --------------------------------------------------------------------- audio
def make_audio(path, sr=48000):
    n = int(DUR * sr) + sr
    tt = np.arange(n) / sr
    out = np.zeros((n, 2), np.float32)
    beat = 60 / BPM
    rng = np.random.default_rng(3)

    # pad: slow detuned chords (Dm9 -> Bbmaj7 -> Fadd9 -> C6sus)
    chords = [[146.8, 220.0, 261.6, 329.6], [116.5, 174.6, 220.0, 293.7],
              [174.6, 261.6, 349.2, 392.0], [130.8, 196.0, 293.7, 440.0]]
    pad = np.zeros(n)
    for ci in range(int(DUR / BAR) + 1):
        c = chords[ci % 4]
        s0 = int(ci * BAR * sr); s1_ = min(n, int((ci + 1.15) * BAR * sr))
        seg = tt[s0:s1_] - ci * BAR
        env = np.minimum(1, seg / 0.6) * np.minimum(1, (BAR * 1.15 - seg) / 0.6)
        for f in c:
            for det in (-0.6, 0.6):
                pad[s0:s1_] += np.sin(2 * np.pi * (f + det) * seg + det) * env * 0.035
    out += pad[:, None]

    # wave wash: filtered noise breathing every 2 bars
    noise = rng.standard_normal(n)
    k = np.ones(400) / 400
    wash = np.convolve(noise, k, mode="same") * 6
    wash *= 0.5 + 0.5 * np.sin(2 * np.pi * tt / (BAR * 2) - 1.5)
    out[:, 0] += wash * 0.10; out[:, 1] += np.roll(wash, 900) * 0.10

    # kick on beats (skip first bar), hats on off-beats, click on cuts
    nb = int(DUR / beat)
    for b in range(nb):
        s0 = int(b * beat * sr)
        if b >= 4:
            L = int(0.35 * sr); seg = np.arange(min(L, n - s0)) / sr
            f = 45 + 90 * np.exp(-seg * 30)
            kick = np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-seg * 7) * 0.55
            out[s0:s0 + len(seg)] += kick[:, None]
            h0 = int((b + 0.5) * beat * sr); L = int(0.05 * sr)
            if h0 + L < n:
                hat = np.diff(rng.standard_normal(L + 1)) * np.exp(-np.arange(L) / sr * 80) * 0.06
                out[h0:h0 + L, 0] += hat * 0.8; out[h0:h0 + L, 1] += hat
        if b % 4 == 0 and b > 0:
            L = int(0.08 * sr)
            gl = np.sign(np.sin(2 * np.pi * 1800 * np.arange(L) / sr)) * np.exp(-np.arange(L) / sr * 40) * 0.12
            out[s0:s0 + L] += gl[:, None]
    # bell melody (pentatonic) from bar 3
    notes = [587.3, 440.0, 523.3, 392.0, 659.3, 587.3, 440.0, 349.2]
    for j in range(int(DUR / (beat * 1.5))):
        s0 = int((BAR * 2 + j * beat * 1.5) * sr)
        if s0 >= n - sr or s0 > int((DUR - BAR) * sr):
            break
        L = int(1.2 * sr); seg = np.arange(L) / sr
        f = notes[j % len(notes)]
        bell = (np.sin(2 * np.pi * f * seg) + 0.3 * np.sin(2 * np.pi * f * 2.76 * seg)) * np.exp(-seg * 3.5) * 0.07
        pan = 0.5 + 0.4 * math.sin(j)
        out[s0:s0 + L, 0] += bell * (1 - pan); out[s0:s0 + L, 1] += bell * pan
    # simple echo
    d = int(beat * 0.75 * sr)
    out[d:] += out[:-d] * 0.25
    out = out[: int(DUR * sr)]
    fade = np.minimum(1, np.minimum(np.arange(len(out)) / (0.3 * sr), (len(out) - np.arange(len(out))) / (1.5 * sr)))
    out *= fade[:, None]
    out = np.tanh(out * 1.2) * 0.8
    import wave
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((out * 32767).astype(np.int16).tobytes())


if __name__ == "__main__":
    OUT = sys.argv[1]
    if OUT.endswith(".png"):
        fi = int(os.environ.get("F", 40))
        Image.frombytes("L", (W, H), frame(fi)).save(OUT)
        sys.exit()
    wav = OUT + ".wav"
    make_audio(wav)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p",
                          "-crf", "20", "-preset", "medium", "-tune", "grain", "-c:a", "aac", "-b:a", "192k",
                          "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    with Pool(4) as pool:
        for k, b in enumerate(pool.imap(frame, range(NF), chunksize=2)):
            p.stdin.write(b)
            if k % 60 == 0:
                print(k, "/", NF, flush=True)
    p.stdin.close(); p.wait()
    os.remove(wav)
