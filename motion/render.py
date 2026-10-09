"""Vertical (1080x1920) kinetic-typography motion piece: "Time flows by."
Renders frames with cairo + numpy and pipes them to ffmpeg."""
import math, os, sys, subprocess
from functools import lru_cache
from multiprocessing import Pool
import numpy as np
import cairo, cv2
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
DUR = 8.4
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "fonts")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "time_flows_by_vertical.mp4")

BLUE = (0.10, 0.13, 0.96)
YELLOW = (1.0, 0.80, 0.05)
MINT = (0.22, 0.90, 0.62)
MAGENTA = (1.0, 0.06, 0.58)
PURPLE = (0.55, 0.12, 0.95)
WHITE = (1, 1, 1)
BLACK = (0, 0, 0)


# ---------------------------------------------------------------- easing
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))

def prog(t, a, b):
    return clamp((t - a) / (b - a))

def ease_out(x):
    return 1 - (1 - x) ** 3

def ease_in_out(x):
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2

def back_out(x, s=1.9):
    x -= 1
    return x * x * ((s + 1) * x + s) + 1

def lerp(a, b, x):
    return a + (b - a) * x

def mix(c1, c2, x):
    return tuple(lerp(a, b, x) for a, b in zip(c1, c2))


# ---------------------------------------------------------------- canvas helpers
def new_canvas(bg=BLACK):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    ctx.set_source_rgb(*bg)
    ctx.paint()
    return surf, ctx

def arr_of(surf):
    surf.flush()
    return np.ndarray((H, W, 4), np.uint8, surf.get_data())

def paste_mask(surf, mask, cx, cy, color, alpha=1.0):
    """Blend a float mask (0..1) centred at (cx,cy) onto the surface in `color`."""
    mh, mw = mask.shape
    x0, y0 = int(round(cx - mw / 2)), int(round(cy - mh / 2))
    sx0, sy0 = max(0, -x0), max(0, -y0)
    dx0, dy0 = max(0, x0), max(0, y0)
    dx1, dy1 = min(W, x0 + mw), min(H, y0 + mh)
    if dx1 <= dx0 or dy1 <= dy0:
        return
    m = mask[sy0:sy0 + dy1 - dy0, sx0:sx0 + dx1 - dx0][..., None] * alpha
    a = arr_of(surf)
    region = a[dy0:dy1, dx0:dx1, :3].astype(np.float32)
    col = np.array([color[2], color[1], color[0]], np.float32) * 255
    a[dy0:dy1, dx0:dx1, :3] = (region * (1 - m) + col * m).astype(np.uint8)
    surf.mark_dirty()


@lru_cache(maxsize=64)
def text_mask(text, font, size, variation=None, pad=40):
    f = ImageFont.truetype(os.path.join(FONT, font), size)
    if variation:
        f.set_variation_by_name(variation)
    l, t, r, b = f.getbbox(text)
    img = Image.new("L", (r - l + pad * 2, b - t + pad * 2), 0)
    ImageDraw.Draw(img).text((pad - l, pad - t), text, font=f, fill=255)
    return np.asarray(img, np.float32) / 255.0

def stretch(mask, sx, sy):
    h, w = mask.shape
    return cv2.resize(mask, (max(1, int(w * sx)), max(1, int(h * sy))), interpolation=cv2.INTER_LINEAR)

def wave_warp(mask, amp_y, freq_x, phase, amp_x=0.0, freq_y=0.0, pad=None):
    h, w = mask.shape
    pad = int(abs(amp_y) + 4) if pad is None else pad
    src = cv2.copyMakeBorder(mask, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
    hh, ww = src.shape
    yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
    mx = xx + amp_x * np.sin(yy * freq_y + phase)
    my = yy + amp_y * np.sin(xx * freq_x + phase)
    return cv2.remap(src, mx, my, cv2.INTER_LINEAR, borderValue=0)

def rotate_mask(mask, deg):
    h, w = mask.shape
    d = int(math.hypot(w, h)) + 2
    src = cv2.copyMakeBorder(mask, (d - h) // 2, (d - h + 1) // 2, (d - w) // 2, (d - w + 1) // 2,
                             cv2.BORDER_CONSTANT, value=0)
    M = cv2.getRotationMatrix2D((d / 2, d / 2), deg, 1.0)
    return cv2.warpAffine(src, M, (d, d), flags=cv2.INTER_LINEAR, borderValue=0)


# ---------------------------------------------------------------- primitives
def square_with_hole(ctx, cx, cy, size, angle, hole=0.78, fill=WHITE, hole_col=BLACK):
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(angle)
    ctx.rectangle(-size / 2, -size / 2, size, size)
    ctx.set_source_rgb(*fill)
    ctx.fill()
    ctx.arc(0, 0, size / 2 * hole, 0, 2 * math.pi)
    ctx.set_source_rgb(*hole_col)
    ctx.fill()
    ctx.restore()

def disc(ctx, cx, cy, r, col):
    ctx.arc(cx, cy, max(r, 0.1), 0, 2 * math.pi)
    ctx.set_source_rgb(*col)
    ctx.fill()

def ring(ctx, cx, cy, r, width, col):
    ctx.set_line_width(width)
    ctx.arc(cx, cy, max(r, 0.1), 0, 2 * math.pi)
    ctx.set_source_rgb(*col)
    ctx.stroke()

def dashed_arcs(ctx, cx, cy, r, width, col, rot, n=7, gap=0.35):
    ctx.set_line_width(width)
    ctx.set_source_rgb(*col)
    seg = 2 * math.pi / n
    for i in range(n):
        a0 = rot + i * seg
        ctx.arc(cx, cy, r, a0, a0 + seg * (1 - gap))
        ctx.stroke()

def network(ctx, seed, t, origin, spread, n=14, col=WHITE, alpha=0.9):
    rng = np.random.default_rng(seed)
    ox, oy = origin
    ctx.set_line_width(2.2)
    for i in range(n):
        ang = rng.uniform(0, 2 * math.pi)
        L = rng.uniform(0.3, 1.0) * spread
        bend = rng.uniform(-0.6, 0.6)
        grow = ease_out(clamp(t * 1.6 - rng.uniform(0, 0.4)))
        ex = ox + math.cos(ang) * L * grow
        ey = oy + math.sin(ang) * L * grow
        mx = (ox + ex) / 2 + math.cos(ang + 1.57) * L * bend * 0.5
        my = (oy + ey) / 2 + math.sin(ang + 1.57) * L * bend * 0.5
        ctx.set_source_rgba(*col, alpha)
        ctx.move_to(ox, oy)
        ctx.curve_to(mx, my, mx, my, ex, ey)
        ctx.stroke()
        ctx.arc(ex, ey, 7, 0, 2 * math.pi)
        ctx.fill()
        ctx.set_source_rgb(0, 0, 0)
        ctx.arc(ex, ey, 3, 0, 2 * math.pi)
        ctx.fill()


# ---------------------------------------------------------------- shaded sphere sprites
def _norm(v):
    v = np.array(v, np.float32)
    return v / np.linalg.norm(v)

KEY = _norm((-0.55, -0.70, 0.55))      # warm key light, upper left front
FILL = _norm((0.85, 0.15, 0.45))       # cool fill, right
RIM = _norm((0.35, 0.55, -0.75))       # back light, lower right behind
HALF_KEY = _norm(KEY + np.array((0, 0, 1), np.float32))
SS = 3                                 # supersampling for clean edges

def _lin(c):
    c = np.asarray(c, np.float32)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)

def _srgb(x):
    x = np.clip(x, 0, 1)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055)

def _tonemap(x):  # ACES fitted curve
    return np.clip((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14), 0, 1)

@lru_cache(maxsize=4096)
def sphere_sprite(color, r, ao=0, blur=0, gloss=1.0):
    """Per-pixel lit sphere: lambert key+fill, rim, blinn spec + clearcoat, softbox reflection, AO."""
    size = (r + 2) * 2
    n = size * SS
    yy, xx = (np.mgrid[0:n, 0:n].astype(np.float32) + 0.5) / SS - size / 2
    d2 = (xx ** 2 + yy ** 2) / (r * r)
    inside = d2 < 1
    nz = np.sqrt(np.clip(1 - d2, 0, 1))
    N = np.stack([xx / r, yy / r, nz], -1)
    alb = _lin(color)
    ndk = np.clip(N @ KEY, 0, 1)
    wrap = np.clip((N @ KEY + 0.25) / 1.25, 0, 1)            # soft terminator
    ndf = np.clip(N @ FILL, 0, 1)
    fres = (1 - nz) ** 3
    rim = np.clip(N @ RIM + 0.4, 0, 1) * fres
    nh = np.clip(N @ HALF_KEY, 0, 1)
    spec = nh ** 90 * 2.2 * gloss + nh ** 14 * 0.18 * gloss
    # reflection of an overhead softbox (stretched highlight band near top)
    refl_y = 2 * N[..., 1] * nz                                 # reflect view vector, y comp
    box = np.clip(1 - np.abs(refl_y + 0.75) / 0.18, 0, 1) * np.clip(1 - np.abs(N[..., 0] + 0.15) / 0.45, 0, 1)
    occl = 1 - 0.55 * (ao / 3)
    bottom_ao = 1 - 0.45 * np.clip(N[..., 1], 0, 1) ** 1.5 * (0.5 + ao / 6)
    diffuse = alb * (wrap[..., None] * 1.25 * np.array((1.0, 0.96, 0.9)) + ndf[..., None] * 0.30 * np.array((0.7, 0.8, 1.0))
                     + 0.06) * (occl * bottom_ao)[..., None]
    col = diffuse + (spec * occl)[..., None] + rim[..., None] * (0.55 * alb + 0.25) + \
        (box * (0.12 + 0.6 * fres) * gloss)[..., None]
    col = _srgb(_tonemap(col * 1.15))
    a = inside.astype(np.float32)
    img = np.concatenate([col * a[..., None], a[..., None]], -1)          # premultiplied
    img = cv2.resize(img, (size, size), interpolation=cv2.INTER_AREA)
    if blur:
        img = cv2.GaussianBlur(img, (0, 0), blur)
    bgra = np.ascontiguousarray((img[..., [2, 1, 0, 3]] * 255).astype(np.uint8))
    surf = cairo.ImageSurface.create_for_data(memoryview(bgra), cairo.FORMAT_ARGB32, size, size)
    return surf, bgra  # keep buffer alive

def contact_shadow(ctx, x, y, r, strength=0.55):
    g = cairo.RadialGradient(x + r * 0.12, y + r * 0.18, r * 0.85, x + r * 0.12, y + r * 0.18, r * 1.5)
    g.add_color_stop_rgba(0, 0, 0, 0, strength)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(g)
    ctx.arc(x + r * 0.12, y + r * 0.18, r * 1.5, 0, 2 * math.pi)
    ctx.fill()

def sphere(ctx, x, y, r, c, ao=0, blur=0, shadow=True, gloss=1.0):
    ri = max(1, int(round(r)))
    if shadow and ri > 3:
        contact_shadow(ctx, x, y, ri)
    surf, _ = sphere_sprite(tuple(round(v, 3) for v in c), ri, ao, blur, gloss)
    s = surf.get_width()
    ctx.set_source_surface(surf, x - s / 2, y - s / 2)
    ctx.paint()


# ---------------------------------------------------------------- sphere clusters
CLUSTER_PALETTES = {
    "green": [MINT, (0.10, 0.75, 0.70), (0.55, 0.85, 0.15), (0.05, 0.35, 0.55), (0.95, 0.95, 0.4)],
    "purple": [PURPLE, MAGENTA, (0.25, 0.15, 0.95), (0.85, 0.55, 1.0), (0.95, 0.9, 1.0)],
    "mono": [(0.95, 0.95, 0.95), (0.7, 0.7, 0.72), (0.45, 0.45, 0.48), (0.85, 0.85, 0.88)],
}

@lru_cache(maxsize=16)
def make_cluster(seed, n=420, lumps=6):
    rng = np.random.default_rng(seed)
    centers = rng.normal(0, 0.32, (lumps, 3))
    idx = rng.integers(0, lumps, n)
    pts = centers[idx] + rng.normal(0, 0.17, (n, 3))
    rad = rng.uniform(0.04, 0.12, n) * (1.3 - 0.9 * np.linalg.norm(pts - centers[idx], axis=1))
    rad = np.clip(rad, 0.02, 0.14)
    col = rng.integers(0, 64, n)
    # ambient occlusion level 0..3 from local crowding
    dist = np.linalg.norm(pts[:, None] - pts[None], axis=-1)
    crowd = (dist < 0.22).sum(1) - 1
    ao = np.clip((crowd - crowd.min()) / max(1, np.ptp(crowd)) * 3.99, 0, 3).astype(int)
    return pts, rad, col, ao

def cluster(ctx, cx, cy, scale, rot, palette, seed, grow=1.0, n=420):
    pts, rad, col, ao = make_cluster(seed, n)
    pal = CLUSTER_PALETTES[palette]
    ca, sa = math.cos(rot), math.sin(rot)
    x = pts[:, 0] * ca + pts[:, 2] * sa
    z = -pts[:, 0] * sa + pts[:, 2] * ca
    y = pts[:, 1]
    persp = 1.0 / (1.0 + z * 0.25)
    for i in np.argsort(-z):
        r = rad[i] * scale * persp[i] * grow
        if r < 0.8:
            continue
        sphere(ctx, cx + x[i] * scale * persp[i] * grow, cy + y[i] * scale * persp[i] * grow, r,
               pal[col[i] % len(pal)], ao=int(ao[i]))


# ---------------------------------------------------------------- particle field
@lru_cache(maxsize=1)
def field_points(n=9500):
    rng = np.random.default_rng(7)
    r = np.sqrt(rng.uniform(0, 1, n)) * 1250
    a = rng.uniform(0, 2 * math.pi, n)
    s = rng.uniform(8, 15, n)
    return r, a, s, rng.uniform(0, 1, n)

FIELD_COLS = [BLUE, (0.05, 0.2, 0.6), WHITE, YELLOW, (0.4, 0.85, 0.25), (0.15, 0.55, 0.85), (0.92, 0.92, 0.8)]

def particle_field(ctx, t, cx=W / 2, cy=H * 0.47):
    r, a, s, k = field_points()
    swirl = a + 0.55 * t * (1.6 - r / 1250) + 0.0016 * r
    x = cx + np.cos(swirl) * r * 0.82
    y = cy + np.sin(swirl) * r * 1.15
    band = (np.sin(r * 0.011 - swirl * 1.0 + t * 1.5) * 0.5 + 0.5) * (len(FIELD_COLS) - 1)
    band = (band + k * 1.4).astype(int) % len(FIELD_COLS)
    depth = 0.75 + 0.5 * np.sin(swirl * 2 + r * 0.004)
    for i in np.argsort(depth):
        rr = s[i] * depth[i]
        if -20 < x[i] < W + 20 and -20 < y[i] < H + 20:
            # shallow depth of field: far dots are blurred and darker, near dots crisp
            blur = 2 if depth[i] < 0.5 else (1 if depth[i] < 0.7 else 0)
            c = mix(FIELD_COLS[band[i]], BLACK, clamp((0.9 - depth[i]) * 0.9))
            sphere(ctx, x[i], y[i], rr, c, ao=int(clamp((1.1 - depth[i]) * 4, 0, 3)), blur=blur,
                   shadow=depth[i] > 0.6)


# ---------------------------------------------------------------- scenes
def scene_intro(surf, ctx, t, lt):
    # white square + black hole spins in, blue disc rises, cluster peeks in
    p = ease_out(prog(lt, 0, 0.7))
    size = lerp(60, 720, back_out(prog(lt, 0, 0.6)))
    square_with_hole(ctx, W / 2 - 40, H * 0.40, size, lerp(-1.4, 0.32, p) + lt * 0.25)
    by = lerp(H + 300, H * 0.70, back_out(prog(lt, 0.25, 0.85)))
    disc(ctx, W * 0.62, by, 210, BLUE)
    cluster(ctx, W + 40 - 120 * ease_out(prog(lt, 0.3, 1.2)), H * 0.30, 330, t * 0.8, "green", 3,
            grow=ease_out(prog(lt, 0.2, 0.9)))
    ctx.set_source_rgb(*MINT)
    ctx.set_line_width(28)
    ctx.move_to(W * 0.18, H)
    ctx.line_to(W * 0.18 + 160 * p, H - 300 * p)
    ctx.stroke()


def scene_flowing(surf, ctx, t, lt):
    cx, cy = W / 2, H * 0.47
    zoom = lerp(0.85, 1.05, ease_out(prog(lt, 0, 1.4)))
    ring(ctx, cx, cy, 420 * zoom, 300 * zoom, BLUE)
    dashed_arcs(ctx, cx, cy, 175 * zoom, 22, BLUE, lt * 2.4)
    disc(ctx, cx, cy, 60 * zoom, BLUE)
    square_with_hole(ctx, 190, 330, 360, 0.25 + lt * 0.5)
    ring(ctx, W - 210, 300, 115, 34, MINT)
    ctx.set_source_rgb(*MINT)
    ctx.move_to(0, H * 0.70)
    ctx.line_to(300, H * 0.62)
    ctx.line_to(260, H * 0.80)
    ctx.close_path()
    ctx.fill()
    network(ctx, 11, lt, (W - 120, H * 0.30), 700)
    cluster(ctx, W - 130, H * 0.82, 380, t * 0.7, "green", 5, n=520)
    cluster(ctx, 120, H * 0.20, 220, -t * 0.9, "green", 9)
    # FLOWING: tall condensed letters, staggered vertical stretch
    letters = "FLOWING"
    span = W * 0.86
    step = span / len(letters)
    for i, ch in enumerate(letters):
        pi_ = back_out(prog(lt, 0.08 + i * 0.07, 0.45 + i * 0.07), 1.4)
        if pi_ <= 0:
            continue
        m = text_mask(ch, "Anton.ttf", 190)
        m = stretch(m, 0.62, 3.3 * max(pi_, 0.02))
        x = (W - span) / 2 + step * (i + 0.5)
        y = cy + math.sin(lt * 5 + i * 0.9) * 22
        paste_mask(surf, m, x + 7, y + 9, BLUE)
        paste_mask(surf, m, x, y, YELLOW)


def scene_wavetext(surf, ctx, t, lt):
    rows = [
        ("FLOWS TIME FLOWS TIME FLOWS", 120, -5, 1.0, 0.13),
        ("TIME FLOWS TIME FLOWS TIME", 260, 8, -1.3, 0.25),
        ("FLOW FLOW FLOW FLOW", 380, -10, 1.7, 0.42),
        ("FLOWS TIME FLOWS TIME", 170, 14, -1.0, 0.60),
        ("TIME FLOWS TIME", 300, -6, 1.4, 0.76),
        ("FLOWS TIME FLOWS TIME FLOWS", 140, 4, -1.6, 0.91),
    ]
    network(ctx, 23, lt, (W * 0.3, H * 0.5), 900, n=10, alpha=0.7)
    for j, (txt, size, rot, speed, ypos) in enumerate(rows):
        appear = ease_out(prog(lt, j * 0.05, 0.3 + j * 0.05))
        if appear <= 0:
            continue
        m = text_mask(txt, "PlayfairDisplay.ttf", size, b"Black")
        m = wave_warp(m, size * 0.28, 2 * math.pi / (size * 4.5), lt * 6 + j, amp_x=size * 0.08,
                      freq_y=0.02)
        m = rotate_mask(m, rot)
        x = W / 2 + speed * lt * 260 + (1 - appear) * speed * 600
        y = H * ypos
        paste_mask(surf, m, x + 10, y + 10, BLUE)
        paste_mask(surf, m, x, y, YELLOW)
    # white square + mono cluster slides in at the end, wiping into next scene
    q = ease_in_out(prog(lt, 0.75, 1.2))
    if q > 0:
        sx = lerp(W + 500, W * 0.62, q)
        ctx.set_source_rgb(*WHITE)
        ctx.rectangle(sx - 330, H * 0.55 - 330, 660, 660)
        ctx.fill()
        disc(ctx, sx, H * 0.55, 230, BLACK)
        ctx.set_source_rgb(*MINT)
        ctx.rectangle(sx - 420, H * 0.55 - 140, 150, 600)
        ctx.fill()
        cluster(ctx, sx + 80, H * 0.48, 520, t, "mono", 13, n=560)


def scene_collage(surf, ctx, t, lt):
    jit = math.floor(lt * 12) % 2
    # blue wavy stripe panel
    ctx.set_source_rgb(*BLUE)
    ctx.rectangle(W * 0.30, H * 0.36, W * 0.46, H * 0.30)
    ctx.fill()
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(14)
    for i in range(9):
        x0 = W * 0.33 + i * 50
        ctx.move_to(x0, H * 0.36)
        for k in range(30):
            yy = H * 0.36 + k * (H * 0.30 / 29)
            ctx.line_to(x0 + 16 * math.sin(k * 0.8 + lt * 9 + i * 0.5), yy)
        ctx.stroke()
    ctx.set_source_rgb(*YELLOW)
    ctx.rectangle(W * 0.58, H * 0.52 + jit * 12, 260, 300)
    ctx.fill()
    ctx.rectangle(W * 0.70, H * 0.12, 90, 90)
    ctx.fill()
    square_with_hole(ctx, W * 0.24, H * 0.47, 280, lt * 1.5, hole=0.7)
    square_with_hole(ctx, W * 0.80, H * 0.84, 170, -lt * 2, hole=0.6, fill=WHITE)
    ring(ctx, W * 0.66, H * 0.86, 60, 18, MINT)
    ctx.set_source_rgb(*MINT)
    ctx.rectangle(40, H * 0.70, 70, 330)
    ctx.fill()
    cluster(ctx, W * 0.22, H * 0.24, 330, t * 1.1, "purple", 17, n=520,
            grow=ease_out(prog(lt, 0, 0.35)))
    cluster(ctx, W * 0.82, H * 0.32, 290, -t * 0.9, "purple", 19, n=480,
            grow=ease_out(prog(lt, 0.08, 0.45)))
    cluster(ctx, W * 0.30, H * 0.72, 240, t * 1.3, "purple", 21, n=380,
            grow=ease_out(prog(lt, 0.15, 0.5)))
    network(ctx, 31, lt, (W * 0.5, H * 0.55), 650, n=12)
    for txt, fs, x, y, col, d in [("PULSE", 150, W * 0.60, H * 0.21, PURPLE, 0.0),
                                  ("OF", 330, W * 0.40, H * 0.86, WHITE, 0.1),
                                  ("FLOW", 170, W * 0.17, H * 0.92, YELLOW, 0.18),
                                  ("THE", 90, W * 0.86, H * 0.95, PURPLE, 0.25)]:
        p = back_out(prog(lt, d, d + 0.3), 1.5)
        if p > 0:
            m = stretch(text_mask(txt, "Anton.ttf", fs), 0.75, max(p, 0.02) * 1.5)
            paste_mask(surf, m, x, y, col)


def scene_field(surf, ctx, t, lt):
    particle_field(ctx, t)
    # mint wave stack -> magenta "Time flows by."
    morph = ease_in_out(prog(lt, 0.9, 1.25))
    lines = ["Time", "flows", "by."]
    for j, ln in enumerate(lines):
        base = text_mask(ln, "Oswald.ttf", 230, b"Bold")
        base = stretch(base, 0.82, 2.05)
        y = H * 0.47 + (j - 1) * 420
        if morph < 1:
            # stacked green copies, waving like an extruded ribbon
            n = 8
            for k in range(n):
                ph = lt * 7 + k * 0.45 + j
                m = wave_warp(base, 60 * (1 - morph), 2 * math.pi / 380, ph, pad=70)
                a = (0.35 + 0.65 * k / (n - 1)) * (1 - morph)
                off = (k - n + 1) * 7
                paste_mask(surf, m, W / 2 + off, y + off, mix(MINT, (0.05, 0.4, 0.3), 1 - k / (n - 1)), a)
        if morph > 0:
            settle = 1 - ease_out(prog(lt, 1.0, 1.8))
            m = wave_warp(base, 45 * settle, 2 * math.pi / 380, lt * 7 + j, pad=50)
            paste_mask(surf, m, W / 2 + 8, y + 8, (0.35, 0.0, 0.25), morph * 0.8)
            paste_mask(surf, m, W / 2, y, MAGENTA, morph)


def scene_outro(surf, ctx, t, lt):
    cx, cy = W / 2, H * 0.48
    z = lerp(1.35, 0.92, ease_out(prog(lt, 0, 0.8)))
    ring(ctx, cx, cy, 430 * z, 320 * z, BLUE)
    dashed_arcs(ctx, cx, cy, 190 * z, 20, BLUE, -lt * 2)
    disc(ctx, cx, cy, 70 * z, BLUE)
    square_with_hole(ctx, cx - 300 * z, cy - 520 * z, 420 * z, 0.35 - lt * 0.6)
    cluster(ctx, cx + 420 * z, cy - 300 * z, 360 * z, t * 0.8, "green", 3)
    cluster(ctx, cx - 380 * z, cy + 560 * z, 300 * z, -t * 0.7, "green", 9)
    disc(ctx, cx - 200, cy + 400, 14, WHITE)
    m = text_mask("Time flows by.", "Oswald.ttf", 92, b"Bold")
    m = stretch(m, 1.0, 1.6)
    p = ease_out(prog(lt, 0.3, 0.7))
    paste_mask(surf, m, W / 2, H * 0.89, WHITE, p)


SCENES = [  # (start, end, fn)
    (0.0, 1.25, scene_intro),
    (1.25, 2.65, scene_flowing),
    (2.65, 4.00, scene_wavetext),
    (4.00, 5.05, scene_collage),
    (5.05, 7.30, scene_field),
    (7.30, DUR, scene_outro),
]


def render(fi):
    t = fi / FPS
    surf, ctx = new_canvas()
    for a, b, fn in SCENES:
        if a <= t < b:
            fn(surf, ctx, t, t - a)
            # quick white flash on every cut
            if t - a < 1.5 / FPS and a > 0:
                ctx.set_source_rgba(1, 1, 1, 0.55)
                ctx.paint()
            break
    fade = prog(t, DUR - 0.45, DUR)
    if fade > 0:
        ctx.set_source_rgba(0, 0, 0, fade)
        ctx.paint()
    return bytes(arr_of(surf))


def main():
    frames = int(DUR * FPS)
    only = os.environ.get("FRAMES")
    if only:  # preview stills
        for f in map(int, only.split(",")):
            a = np.frombuffer(render(f), np.uint8).reshape(H, W, 4)
            cv2.imwrite(os.path.join(HERE, f"prev_{f:03d}.png"), a[..., :3])
        return
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                           "-pix_fmt", "yuv420p", "-crf", "17", "-preset", "medium",
                           "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    with Pool(os.cpu_count()) as pool:
        for i, buf in enumerate(pool.imap(render, range(frames), chunksize=2)):
            ff.stdin.write(buf)
            if i % 30 == 0:
                print(f"frame {i}/{frames}", flush=True)
    ff.stdin.close()
    ff.wait()
    print("done", OUT)


if __name__ == "__main__":
    main()
