"""線画の部品：人物・時計・公衆電話・家・駅・矢印・吹き出し・伝言板など。

すべてオリジナルの簡略図。実在の製品や駅の再現ではない。
線は「boil」（数フレームごとにわずかに揺れる手描き風）にしている。
"""
import math
import os
import random

import cairo
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "..", "fonts")
FONTS = {"bold": os.path.join(FONT_DIR, "NotoSansJP-Bold.otf"),
         "medium": os.path.join(FONT_DIR, "NotoSansJP-Medium.otf")}

# --- 色 ---
def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

PAPER = rgb("#F7F3EA")
INK = rgb("#2A2A2A")
GRAY = rgb("#9A968E")
LIGHT = rgb("#E6E0D3")
RED = rgb("#E04A3A")
YELLOW = rgb("#F6C744")
GREEN = rgb("#3FA66B")
BLUE = rgb("#3D7CC9")
A_COL = rgb("#3FA66B")   # 待つ側
B_COL = rgb("#E07B39")   # 遅れる側
WHITE = (1, 1, 1)
BOARD = rgb("#2F4A3A")
CHALK = rgb("#F2F0E6")
WOOD = rgb("#9B6B43")


# --- イージング ---
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))

def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3

def ease_io(x):
    x = clamp(x)
    return 3 * x * x - 2 * x * x * x

def ease_back(x):
    x = clamp(x)
    c = 1.9
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

def lerp(a, b, t):
    return a + (b - a) * t


# --- 文字（PILで描いてcairoに貼る。キャッシュあり） ---
_tcache = {}
_fcache = {}

def _font(weight, size):
    k = (weight, size)
    if k not in _fcache:
        _fcache[k] = ImageFont.truetype(FONTS[weight], size)
    return _fcache[k]

def text_surface(s, size, weight="bold", color=INK, stroke=0, stroke_color=WHITE, spacing=0.28):
    key = (s, size, weight, color, stroke, stroke_color)
    if key in _tcache:
        return _tcache[key]
    f = _font(weight, size)
    lines = s.split("\n")
    lh = int(size * (1 + spacing))
    widths = [f.getbbox(l or " ", stroke_width=stroke)[2] for l in lines]
    w = max(widths) + 2 * stroke + 8
    h = lh * len(lines) + 2 * stroke + int(size * 0.25)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c255 = tuple(int(v * 255) for v in color)
    s255 = tuple(int(v * 255) for v in stroke_color)
    for i, l in enumerate(lines):
        x = (w - widths[i]) / 2
        d.text((x, stroke + i * lh), l, font=f, fill=c255, stroke_width=stroke, stroke_fill=s255)
    a = np.asarray(img).astype(np.float32)
    al = a[..., 3:4] / 255
    bgra = np.concatenate([a[..., 2:3] * al, a[..., 1:2] * al, a[..., 0:1] * al, a[..., 3:4]], axis=2)
    stride = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_ARGB32, w)
    buf = np.zeros((h, stride // 4, 4), np.uint8)
    buf[:, :w] = bgra.round().astype(np.uint8)
    surf = cairo.ImageSurface.create_for_data(memoryview(buf).cast("B"), cairo.FORMAT_ARGB32, w, h, stride)
    _tcache[key] = (surf, w, h, buf)
    return _tcache[key]


class Pen:
    """cairo コンテキストと手描き風の揺れをまとめたもの。"""

    def __init__(self, ctx, frame, fps):
        self.c = ctx
        self.boil = frame // max(1, fps // 6)  # 1秒に6回だけ線が揺れる
        self.lw = 6

    # 揺れ
    def j(self, x, y, seed, amp=1.6):
        r = random.Random(hash((round(x), round(y), seed, self.boil)) & 0xFFFFFFFF)
        return x + r.uniform(-amp, amp), y + r.uniform(-amp, amp)

    def stroke(self, color=INK, width=None, alpha=1.0, dash=None):
        c = self.c
        c.set_source_rgba(*color, alpha)
        c.set_line_width(width or self.lw)
        c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.set_line_join(cairo.LINE_JOIN_ROUND)
        c.set_dash(dash or [])
        c.stroke()
        c.set_dash([])

    def fill(self, color, alpha=1.0, preserve=False):
        self.c.set_source_rgba(*color, alpha)
        (self.c.fill_preserve if preserve else self.c.fill)()

    def poly(self, pts, closed=False, seed=0, amp=1.4):
        c = self.c
        pts = [self.j(x, y, seed + i, amp) for i, (x, y) in enumerate(pts)]
        c.move_to(*pts[0])
        for p in pts[1:]:
            c.line_to(*p)
        if closed:
            c.close_path()

    def line(self, x0, y0, x1, y1, color=INK, width=None, alpha=1.0, dash=None, seed=0):
        self.poly([(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2), (x1, y1)], seed=seed)
        self.stroke(color, width, alpha, dash)

    def circle(self, x, y, r, seed=0, amp=1.2, n=28):
        pts = [(x + r * math.cos(2 * math.pi * i / n), y + r * math.sin(2 * math.pi * i / n)) for i in range(n)]
        r_ = random.Random(hash((seed, self.boil)) & 0xFFFFFFFF)
        pts = [(px + r_.uniform(-amp, amp), py + r_.uniform(-amp, amp)) for px, py in pts]
        c = self.c
        c.move_to(*pts[0])
        for p in pts[1:]:
            c.line_to(*p)
        c.close_path()

    def rrect(self, x, y, w, h, r=14, seed=0):
        c = self.c
        jx, jy = self.j(0, 0, seed, 1.0)
        x += jx; y += jy
        c.new_sub_path()
        c.arc(x + w - r, y + r, r, -math.pi / 2, 0)
        c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
        c.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
        c.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
        c.close_path()

    def text(self, s, x, y, size=48, weight="bold", color=INK, ax=0.5, ay=0.5, alpha=1.0, scale=1.0,
             stroke=0, stroke_color=WHITE, rot=0.0):
        if alpha <= 0.01 or scale <= 0.01:
            return 0, 0
        surf, w, h, _ = text_surface(s, size, weight, color, stroke, stroke_color)
        c = self.c
        c.save()
        c.translate(x, y)
        if rot:
            c.rotate(rot)
        c.scale(scale, scale)
        c.set_source_surface(surf, -w * ax, -h * ay)
        c.paint_with_alpha(clamp(alpha))
        c.restore()
        return w, h

    def text_size(self, s, size=48, weight="bold"):
        _, w, h, _ = text_surface(s, size, weight)
        return w, h


# ---------------------------------------------------------------------------
# 部品
# ---------------------------------------------------------------------------

def push(pen, x, y, s=1.0, alpha=1.0, rot=0.0):
    c = pen.c
    c.save()
    c.translate(x, y)
    if rot:
        c.rotate(rot)
    s = s if abs(s) > 1e-3 else 1e-3  # 拡大率0は描けないので最小値に
    c.scale(s, s)
    if alpha < 1:
        c.push_group()
    return alpha

def pop(pen, alpha=1.0):
    c = pen.c
    if alpha < 1:
        c.pop_group_to_source()
        c.paint_with_alpha(clamp(alpha))
    c.restore()


def person(pen, x, y, s=1.0, col=A_COL, face="normal", pose="stand", t=0.0, flip=False, alpha=1.0,
           hair="bob", seed=0, look=0.0):
    """足元 (x, y) 基準。高さ約 280*s。"""
    if alpha <= 0.01 or s <= 0.01:
        return
    a = push(pen, x, y, s, alpha)
    c = pen.c
    if flip:
        c.scale(-1, 1)
    lw = 7
    sw = math.sin(t * 14) if pose == "run" else 0.0
    # 脚
    if pose == "run":
        pen.poly([(-8, -110), (-22 + 28 * sw, -55), (-34 + 50 * sw, 0)], seed=seed + 1); pen.stroke(width=lw)
        pen.poly([(8, -110), (22 - 28 * sw, -55), (30 - 50 * sw, -4)], seed=seed + 2); pen.stroke(width=lw)
    else:
        pen.poly([(-14, -110), (-18, -55), (-22, 0)], seed=seed + 1); pen.stroke(width=lw)
        pen.poly([(14, -110), (18, -55), (22, 0)], seed=seed + 2); pen.stroke(width=lw)
    # 胴（シャツ）
    pen.poly([(-38, -190), (38, -190), (34, -105), (-34, -105)], closed=True, seed=seed + 3)
    pen.fill(col, 0.85, preserve=True); pen.stroke(width=lw)
    # 腕
    if pose == "run":
        pen.poly([(-36, -182), (-60 - 20 * sw, -150), (-48 - 30 * sw, -120)], seed=seed + 4); pen.stroke(width=lw)
        pen.poly([(36, -182), (60 + 20 * sw, -150), (70 + 25 * sw, -168)], seed=seed + 5); pen.stroke(width=lw)
    elif pose == "phone":   # 右手を耳へ
        pen.poly([(-36, -182), (-52, -140), (-48, -105)], seed=seed + 4); pen.stroke(width=lw)
        pen.poly([(36, -182), (62, -205), (34, -232)], seed=seed + 5); pen.stroke(width=lw)
    elif pose == "wave":
        wv = math.sin(t * 9) * 12
        pen.poly([(-36, -182), (-52, -140), (-48, -105)], seed=seed + 4); pen.stroke(width=lw)
        pen.poly([(36, -182), (66, -222), (72 + wv, -268)], seed=seed + 5); pen.stroke(width=lw)
    elif pose == "read":    # 片手をあご
        pen.poly([(-36, -182), (-52, -140), (-48, -105)], seed=seed + 4); pen.stroke(width=lw)
        pen.poly([(36, -182), (44, -150), (14, -200)], seed=seed + 5); pen.stroke(width=lw)
    else:
        pen.poly([(-36, -182), (-54, -140), (-50, -100)], seed=seed + 4); pen.stroke(width=lw)
        pen.poly([(36, -182), (54, -140), (50, -100)], seed=seed + 5); pen.stroke(width=lw)
    # 頭
    hx, hy, r = look * 6, -240, 44
    pen.circle(hx, hy, r, seed=seed + 6)
    pen.fill(WHITE, preserve=True); pen.stroke(width=lw)
    # 髪
    if hair == "bob":
        c.new_path()
        c.arc(hx, hy - 2, r + 4, math.pi * 1.0, math.pi * 2.0)
        c.line_to(hx + r + 4, hy + 18)
        c.line_to(hx + r - 8, hy - 6)
        c.curve_to(hx + 10, hy - 30, hx - 20, hy - 22, hx - r + 8, hy - 6)
        c.line_to(hx - r - 4, hy + 18)
        c.close_path()
        pen.fill(INK)
    else:  # short
        c.new_path()
        c.arc(hx, hy - 4, r + 2, math.pi * 1.08, math.pi * 1.92)
        c.curve_to(hx + 20, hy - 22, hx - 10, hy - 36, hx - r + 2, hy - 16)
        c.close_path()
        pen.fill(INK)
    # 顔
    ex = 15
    if face == "surprise":
        for sx in (-ex, ex):
            pen.circle(hx + sx + look * 4, hy + 2, 6, seed=seed + 7, amp=0.5); pen.fill(INK)
        pen.circle(hx + look * 4, hy + 24, 8, seed=seed + 8, amp=0.6); pen.stroke(width=5)
    else:
        for sx in (-ex, ex):
            pen.circle(hx + sx + look * 4, hy + 2, 4.5, seed=seed + 7, amp=0.4); pen.fill(INK)
        if face == "happy":
            c.new_path(); c.arc(hx + look * 4, hy + 14, 14, 0.15 * math.pi, 0.85 * math.pi); pen.stroke(width=5)
        elif face == "worry":
            pen.poly([(hx - 12, hy + 26), (hx - 4, hy + 21), (hx + 4, hy + 26), (hx + 12, hy + 21)], seed=seed + 9, amp=0.4)
            pen.stroke(width=5)
            # 眉
            pen.line(hx - ex - 9, hy - 14, hx - ex + 7, hy - 9, width=4, seed=seed + 10)
            pen.line(hx + ex + 9, hy - 14, hx + ex - 7, hy - 9, width=4, seed=seed + 11)
        else:
            pen.line(hx - 9 + look * 4, hy + 22, hx + 9 + look * 4, hy + 22, width=5, seed=seed + 12)
    pop(pen, a)


def sweat(pen, x, y, s=1.0, alpha=1.0):
    a = push(pen, x, y, s, alpha)
    c = pen.c
    c.new_path(); c.move_to(0, -18); c.curve_to(10, 0, 10, 12, 0, 12); c.curve_to(-10, 12, -10, 0, 0, -18)
    pen.fill(rgb("#7EC8F0"), preserve=True); pen.stroke(width=3)
    pop(pen, a)


def clock(pen, x, y, r, hour=2, minute=0, alpha=1.0, s=1.0, sector=None, frame_col=INK, face=WHITE, seed=0):
    """sector=(m0, m1) で分針の範囲を赤く塗る。"""
    a = push(pen, x, y, s, alpha)
    c = pen.c
    pen.circle(0, 0, r, seed=seed, amp=1.0); pen.fill(face, preserve=True); pen.stroke(frame_col, width=max(6, r * 0.07))
    if sector and sector[1] > sector[0]:
        c.new_path(); c.move_to(0, 0)
        c.arc(0, 0, r * 0.86, -math.pi / 2 + sector[0] / 60 * 2 * math.pi, -math.pi / 2 + sector[1] / 60 * 2 * math.pi)
        c.close_path(); pen.fill(RED, 0.28)
    for i in range(12):
        ang = i / 12 * 2 * math.pi
        r0 = r * (0.78 if i % 3 == 0 else 0.84)
        c.new_path()
        c.move_to(math.sin(ang) * r0, -math.cos(ang) * r0)
        c.line_to(math.sin(ang) * r * 0.92, -math.cos(ang) * r * 0.92)
        pen.stroke(width=max(3, r * (0.05 if i % 3 == 0 else 0.03)))
    ha = (hour % 12 + minute / 60) / 12 * 2 * math.pi
    ma = minute / 60 * 2 * math.pi
    c.new_path(); c.move_to(0, 0); c.line_to(math.sin(ha) * r * 0.5, -math.cos(ha) * r * 0.5)
    pen.stroke(width=max(5, r * 0.08))
    c.new_path(); c.move_to(0, 0); c.line_to(math.sin(ma) * r * 0.74, -math.cos(ma) * r * 0.74)
    pen.stroke(width=max(4, r * 0.055))
    pen.circle(0, 0, max(4, r * 0.05), amp=0.2); pen.fill(INK)
    pop(pen, a)


def station_clock(pen, x, y, hour=2, minute=0, alpha=1.0, s=1.0):
    """柱の上の時計。(x, y) は柱の根元。"""
    a = push(pen, x, y, s, alpha)
    pen.poly([(-6, 0), (-6, -300)], seed=31); pen.stroke(width=10)
    pen.poly([(-40, 0), (40, 0)], seed=32); pen.stroke(width=8)
    clock(pen, -6, -350, 58, hour, minute, seed=33)
    pop(pen, a)


def payphone(pen, x, y, s=1.0, alpha=1.0, body=rgb("#6FB27E"), ringing=0.0, label=True):
    """簡略化した公衆電話（特定機種の再現ではない）。(x, y) は台の下中央。"""
    a = push(pen, x, y, s, alpha)
    c = pen.c
    # 台
    pen.poly([(-70, 0), (-70, -150), (70, -150), (70, 0)], seed=41); pen.fill(LIGHT, preserve=True); pen.stroke(width=6)
    # 本体
    pen.rrect(-62, -330, 124, 180, 16, seed=42); pen.fill(body, preserve=True); pen.stroke(width=6)
    # 受話器
    pen.rrect(-86, -320, 26, 120, 12, seed=43); pen.fill(body, preserve=True); pen.stroke(width=6)
    # 表示窓・ボタン（抽象）
    pen.rrect(-30, -310, 76, 26, 6, seed=44); pen.fill(WHITE, preserve=True); pen.stroke(width=4)
    for i in range(3):
        for k in range(3):
            pen.rrect(-26 + k * 24, -270 + i * 26, 16, 16, 4, seed=45 + i * 3 + k); pen.fill(WHITE, preserve=True); pen.stroke(width=3)
    if label:
        pen.text("公衆電話", 0, -365, 30, color=INK)
    if ringing > 0:
        for i in range(3):
            rr = 30 + i * 22 + (ringing * 30) % 22
            c.new_path(); c.arc(-110, -280, rr, math.pi * 0.75, math.pi * 1.25); pen.stroke(RED, 5, alpha=0.8)
    pop(pen, a)


def house(pen, x, y, s=1.0, alpha=1.0, roof=RED, door_open=False, phone_ring=0.0, label=None, empty=False):
    """家と、中の電話。(x, y) は地面中央。"""
    a = push(pen, x, y, s, alpha)
    c = pen.c
    pen.poly([(-130, 0), (-130, -170), (130, -170), (130, 0)], closed=True, seed=51)
    pen.fill(WHITE, preserve=True); pen.stroke(width=6)
    pen.poly([(-155, -165), (0, -280), (155, -165)], closed=True, seed=52)
    pen.fill(roof, 0.9, preserve=True); pen.stroke(width=6)
    # 戸
    if door_open:
        pen.poly([(60, 0), (60, -110), (100, -100), (100, 6)], closed=True, seed=53); pen.fill(LIGHT, preserve=True); pen.stroke(width=5)
    else:
        pen.poly([(60, 0), (60, -110), (110, -110), (110, 0)], closed=True, seed=53); pen.fill(LIGHT, preserve=True); pen.stroke(width=5)
    # 窓の中の電話
    pen.rrect(-105, -140, 120, 95, 8, seed=54); pen.fill(rgb("#FFF8E6"), preserve=True); pen.stroke(width=5)
    home_phone(pen, -45, -70, 0.55, ring=phone_ring)
    if label:
        pen.text(label, 0, 40, 32, color=INK)
    pop(pen, a)


def home_phone(pen, x, y, s=1.0, ring=0.0, alpha=1.0):
    """家庭用電話の簡略図。"""
    a = push(pen, x, y, s, alpha)
    c = pen.c
    sh = math.sin(ring * 40) * 4 if ring > 0 else 0
    c.translate(sh, 0)
    pen.poly([(-60, 0), (-48, -50), (48, -50), (60, 0)], closed=True, seed=61); pen.fill(rgb("#F2EDE0"), preserve=True); pen.stroke(width=6)
    pen.rrect(-70, -84, 140, 30, 14, seed=62); pen.fill(rgb("#F2EDE0"), preserve=True); pen.stroke(width=6)
    pen.circle(0, -24, 14, seed=63); pen.stroke(width=4)
    if ring > 0:
        for side in (-1, 1):
            for i in range(2):
                c.new_path(); c.arc(0, -50, 90 + i * 26, -math.pi / 2 + side * 0.5 - 0.3, -math.pi / 2 + side * 0.5 + 0.3)
                pen.stroke(RED, 6)
    pop(pen, a)


def station(pen, x, y, s=1.0, alpha=1.0, name="駅", clock_t=None):
    """駅舎の正面。(x, y) は地面中央。"""
    a = push(pen, x, y, s, alpha)
    pen.poly([(-260, 0), (-260, -220), (260, -220), (260, 0)], closed=True, seed=71)
    pen.fill(WHITE, preserve=True); pen.stroke(width=6)
    pen.poly([(-290, -215), (-240, -300), (240, -300), (290, -215)], closed=True, seed=72)
    pen.fill(rgb("#5B7FA6"), 0.9, preserve=True); pen.stroke(width=6)
    pen.rrect(-90, -282, 180, 56, 8, seed=73); pen.fill(WHITE, preserve=True); pen.stroke(width=5)
    pen.text(name, 0, -254, 38)
    # 入口
    for i, ex in enumerate((-150, 0, 150)):
        pen.poly([(ex - 55, 0), (ex - 55, -140), (ex + 55, -140), (ex + 55, 0)], closed=True, seed=74 + i)
        pen.fill(rgb("#E9E3D4"), preserve=True); pen.stroke(width=5)
    if clock_t is not None:
        clock(pen, 0, -370, 46, *clock_t, seed=79)
    pop(pen, a)


def gate(pen, x, y, s=1.0, alpha=1.0, n=3):
    """改札機の簡略図。"""
    a = push(pen, x, y, s, alpha)
    for i in range(n):
        gx = (i - (n - 1) / 2) * 90
        pen.rrect(gx - 22, -90, 44, 90, 6, seed=81 + i); pen.fill(rgb("#D9DEE6"), preserve=True); pen.stroke(width=5)
        pen.rrect(gx - 14, -82, 28, 12, 3, seed=85 + i); pen.fill(YELLOW, preserve=True); pen.stroke(width=3)
    pen.text("改札", 0, -125, 30)
    pop(pen, a)


def blackboard(pen, x, y, s=1.0, alpha=1.0, lines=(), write=1.0, label=True, w=520, h=300):
    """伝言板（黒板）。(x, y) は中央。lines は [(文字列, 進み0-1)]."""
    a = push(pen, x, y, s, alpha)
    c = pen.c
    pen.rrect(-w / 2 - 18, -h / 2 - 18, w + 36, h + 36, 10, seed=91); pen.fill(WOOD, preserve=True); pen.stroke(width=6)
    pen.rrect(-w / 2, -h / 2, w, h, 4, seed=92); pen.fill(BOARD)
    if label:
        pen.rrect(-110, -h / 2 - 78, 220, 54, 8, seed=93); pen.fill(WHITE, preserve=True); pen.stroke(width=5)
        pen.text("伝 言 板", 0, -h / 2 - 51, 34)
    # チョーク受け
    pen.poly([(-w / 2, h / 2 + 18), (w / 2, h / 2 + 18)], seed=94); pen.stroke(WOOD, width=10)
    for i, (ln, p) in enumerate(lines):
        if p <= 0:
            continue
        n = max(1, round(len(ln) * clamp(p)))
        pen.text(ln[:n], -w / 2 + 30, -h / 2 + 50 + i * 78, 42, weight="medium", color=CHALK, ax=0, ay=0.5,
                 rot=-0.015 * (1 if i % 2 else -1))
    pop(pen, a)


def phone_modern(pen, x, y, s=1.0, alpha=1.0, msgs=(), notif=0.0):
    """スマートフォンの簡略図。msgs: [(文字列, 側'l'/'r', 進み, 既読)]"""
    a = push(pen, x, y, s, alpha)
    c = pen.c
    pen.rrect(-120, -220, 240, 440, 30, seed=101); pen.fill(rgb("#33363C"), preserve=True); pen.stroke(width=6)
    pen.rrect(-104, -196, 208, 392, 16, seed=102); pen.fill(WHITE)
    yy = -160
    for txt, side, p, read in msgs:
        if p <= 0:
            continue
        sc = ease_back(p)
        tw, th = pen.text_size(txt, 30, "medium")
        bw = tw + 22
        bx = (96 - bw) if side == "r" else -96
        col = rgb("#BDE7A5") if side == "r" else rgb("#EDEDED")
        c.save(); c.translate(bx + bw / 2, yy + 26); c.scale(max(sc, 1e-3), max(sc, 1e-3))
        pen.rrect(-bw / 2, -26, bw, 52, 14, seed=103); pen.fill(col)
        pen.text(txt, 0, 0, 30, "medium")
        c.restore()
        if read and side == "r":
            pen.text("既読", bx - 8, yy + 40, 20, "medium", color=GRAY, ax=1, alpha=clamp(read))
        yy += 74
    if notif > 0:
        sc = ease_back(notif)
        c.save(); c.translate(0, -230); c.scale(max(sc, 1e-3), max(sc, 1e-3))
        pen.rrect(-150, -36, 300, 72, 18, seed=104); pen.fill(WHITE, preserve=True); pen.stroke(width=5)
        bell(pen, -110, 0, 0.7)
        pen.text("新着メッセージ", 20, 0, 30, "medium")
        c.restore()
    pop(pen, a)


def bell(pen, x, y, s=1.0, alpha=1.0, crossed=False):
    a = push(pen, x, y, s, alpha)
    c = pen.c
    c.new_path(); c.move_to(-30, 20); c.curve_to(-26, -30, 26, -30, 30, 20); c.close_path()
    pen.fill(YELLOW, preserve=True); pen.stroke(width=5)
    pen.circle(0, 28, 7, amp=0.3); pen.fill(INK)
    if crossed:
        pen.line(-40, -36, 40, 40, RED, 8)
    pop(pen, a)


def bubble(pen, x, y, txt, size=40, tail=(-1, 1), alpha=1.0, s=1.0, color=WHITE, pad=26, think=False,
           text_col=INK, weight="bold"):
    """吹き出し。(x, y) は中心。tail は尾の向き。"""
    if alpha <= 0.01 or s <= 0.01:
        return
    a = push(pen, x, y, s, alpha)
    c = pen.c
    tw, th = pen.text_size(txt, size, weight)
    w, h = tw + pad * 2, th + pad
    if think:
        pen.rrect(-w / 2, -h / 2, w, h, h / 2, seed=111); pen.fill(color, preserve=True); pen.stroke(width=5)
        for i, rr in enumerate((12, 8)):
            pen.circle(tail[0] * (w / 2 - 20 + i * 26), tail[1] * (h / 2 + 18 + i * 22), rr, seed=112 + i)
            pen.fill(color, preserve=True); pen.stroke(width=4)
    else:
        bx, by = tail[0] * w * 0.22, tail[1] * h / 2
        pen.rrect(-w / 2, -h / 2, w, h, 22, seed=111); pen.fill(color, preserve=True); pen.stroke(width=5)
        c.new_path(); c.move_to(bx - 18, by - tail[1] * 3); c.line_to(bx + tail[0] * 34, by + tail[1] * 40); c.line_to(bx + 18, by - tail[1] * 3)
        pen.fill(color, preserve=True); pen.stroke(width=5)
        c.new_path(); c.move_to(bx - 15, by - tail[1] * 5); c.line_to(bx + 15, by - tail[1] * 5); pen.stroke(color, width=8)
    pen.text(txt, 0, 0, size, weight, color=text_col)
    pop(pen, a)


def arrow(pen, x0, y0, x1, y1, p=1.0, color=RED, width=9, dash=None, bend=0.0, head=True, seed=0, stop=None):
    """p: 伸びる割合。bend: 曲がり（垂直方向のずれ px）。stop: 0-1 で途中停止して×。"""
    if p <= 0.0:
        return
    c = pen.c
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1
    cx, cy = mx - dy / L * bend, my + dx / L * bend
    pend = clamp(p) if stop is None else min(clamp(p), stop)
    pts = []
    n = 30
    for i in range(int(n * pend) + 1):
        tt = i / n
        pts.append(((1 - tt) ** 2 * x0 + 2 * (1 - tt) * tt * cx + tt * tt * x1,
                    (1 - tt) ** 2 * y0 + 2 * (1 - tt) * tt * cy + tt * tt * y1))
    if len(pts) < 2:
        return
    pen.poly(pts, seed=seed, amp=0.8)
    pen.stroke(color, width, dash=dash)
    ex, ey = pts[-1]
    px, py = pts[-2]
    ang = math.atan2(ey - py, ex - px)
    if stop is not None and p >= stop:
        k = 22
        pen.line(ex - k, ey - k, ex + k, ey + k, RED, 9)
        pen.line(ex - k, ey + k, ex + k, ey - k, RED, 9)
    elif head:
        hl = width * 3.2
        c.new_path()
        c.move_to(ex + math.cos(ang) * 4, ey + math.sin(ang) * 4)
        c.line_to(ex - hl * math.cos(ang - 0.5), ey - hl * math.sin(ang - 0.5))
        c.line_to(ex - hl * math.cos(ang + 0.5), ey - hl * math.sin(ang + 0.5))
        c.close_path()
        pen.fill(color)


def cross(pen, x, y, r=40, p=1.0, color=RED, width=12):
    if p <= 0:
        return
    p1, p2 = clamp(p * 2), clamp(p * 2 - 1)
    pen.line(x - r, y - r, x - r + 2 * r * p1, y - r + 2 * r * p1, color, width)
    if p2 > 0:
        pen.line(x + r, y - r, x + r - 2 * r * p2, y - r + 2 * r * p2, color, width)


def check(pen, x, y, r=36, p=1.0, color=GREEN, width=12):
    if p <= 0:
        return
    pts = [(x - r, y), (x - r * 0.3, y + r * 0.7), (x + r, y - r * 0.8)]
    p1, p2 = clamp(p * 2), clamp(p * 2 - 1)
    pen.line(pts[0][0], pts[0][1], lerp(pts[0][0], pts[1][0], p1), lerp(pts[0][1], pts[1][1], p1), color, width)
    if p2 > 0:
        pen.line(pts[1][0], pts[1][1], lerp(pts[1][0], pts[2][0], p2), lerp(pts[1][1], pts[2][1], p2), color, width)


def ring(pen, x, y, rx, ry, p=1.0, color=RED, width=9, seed=0):
    """手描きの丸囲み。"""
    if p <= 0:
        return
    c = pen.c
    n = 50
    pts = []
    for i in range(int(n * clamp(p) * 1.08) + 1):
        a = -math.pi * 0.6 + i / n * 2 * math.pi
        k = 1 + 0.04 * math.sin(i * 0.7 + seed)
        pts.append((x + rx * k * math.cos(a), y + ry * k * math.sin(a)))
    if len(pts) > 1:
        pen.poly(pts, seed=seed, amp=0.6)
        pen.stroke(color, width)


def tag(pen, x, y, txt, size=38, bg=YELLOW, fg=INK, alpha=1.0, s=1.0, weight="bold"):
    if alpha <= 0.01 or s <= 0.01:
        return
    a = push(pen, x, y, s, alpha)
    tw, th = pen.text_size(txt, size, weight)
    pen.rrect(-tw / 2 - 18, -th / 2 - 4, tw + 36, th + 8, 12, seed=121); pen.fill(bg, preserve=True); pen.stroke(width=5)
    pen.text(txt, 0, 0, size, weight, color=fg)
    pop(pen, a)


def train(pen, x, y, s=1.0, alpha=1.0, cars=3):
    a = push(pen, x, y, s, alpha)
    for k in range(cars):
        ox = k * 330
        pen.rrect(ox, -170, 310, 150, 22, seed=131 + k); pen.fill(rgb("#F0EBDD"), preserve=True); pen.stroke(width=6)
        pen.poly([(ox, -70), (ox + 310, -70)], seed=135 + k); pen.stroke(rgb("#E07B39"), 12)
        for i in range(4):
            pen.rrect(ox + 22 + i * 72, -150, 52, 50, 6, seed=140 + i); pen.fill(rgb("#BFD6EA"), preserve=True); pen.stroke(width=4)
        for wx in (50, 260):
            pen.circle(ox + wx, -14, 18, seed=150 + wx); pen.fill(INK)
    pop(pen, a)


def pager(pen, x, y, s=1.0, alpha=1.0):
    """ポケベルの簡略図。"""
    a = push(pen, x, y, s, alpha)
    pen.rrect(-80, -50, 160, 100, 18, seed=161); pen.fill(rgb("#5B6C8F"), preserve=True); pen.stroke(width=6)
    pen.rrect(-60, -32, 120, 40, 6, seed=162); pen.fill(rgb("#CFE3C8"), preserve=True); pen.stroke(width=4)
    pen.text("・・・", 0, -12, 28, color=INK)
    pop(pen, a)


def cellphone(pen, x, y, s=1.0, alpha=1.0):
    """折りたたみ前の、アンテナ付き携帯の簡略図。"""
    a = push(pen, x, y, s, alpha)
    pen.poly([(30, -110), (30, -160)], seed=171); pen.stroke(width=8)
    pen.rrect(-45, -110, 90, 220, 18, seed=172); pen.fill(rgb("#8A8F98"), preserve=True); pen.stroke(width=6)
    pen.rrect(-32, -92, 64, 54, 6, seed=173); pen.fill(rgb("#CFE3C8"), preserve=True); pen.stroke(width=4)
    for i in range(3):
        for k in range(3):
            pen.circle(-22 + k * 22, -10 + i * 26, 7, seed=174 + i * 3 + k, amp=0.4); pen.fill(WHITE, preserve=True); pen.stroke(width=3)
    pop(pen, a)


def eye(pen, x, y, s=1.0, alpha=1.0):
    a = push(pen, x, y, s, alpha)
    c = pen.c
    c.new_path(); c.move_to(-36, 0); c.curve_to(-14, -26, 14, -26, 36, 0); c.curve_to(14, 26, -14, 26, -36, 0)
    pen.fill(WHITE, preserve=True); pen.stroke(width=5)
    pen.circle(0, 0, 11, amp=0.4); pen.fill(INK)
    pop(pen, a)


def doc_icon(pen, x, y, s=1.0, alpha=1.0):
    a = push(pen, x, y, s, alpha)
    pen.poly([(-70, -95), (40, -95), (70, -65), (70, 95), (-70, 95)], closed=True, seed=181)
    pen.fill(WHITE, preserve=True); pen.stroke(width=6)
    for i in range(5):
        pen.line(-48, -50 + i * 30, 48 - (30 if i == 4 else 0), -50 + i * 30, GRAY, 6, seed=182 + i)
    pop(pen, a)


def pin(pen, x, y, s=1.0, alpha=1.0, color=RED):
    a = push(pen, x, y, s, alpha)
    c = pen.c
    c.new_path(); c.move_to(0, 0); c.curve_to(-40, -40, -34, -86, 0, -86); c.curve_to(34, -86, 40, -40, 0, 0)
    pen.fill(color, preserve=True); pen.stroke(width=5)
    pen.circle(0, -56, 12, amp=0.3); pen.fill(WHITE)
    pop(pen, a)


def paper_background():
    """生成りの紙（わずかなざらつき）。一度だけ作る。"""
    rng = np.random.default_rng(7)
    noise = rng.normal(0, 1, (H // 4, W // 4)).astype(np.float32)
    img = Image.fromarray(((noise * 3.5) + 128).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    n = (np.asarray(img).astype(np.float32) - 128) / 255
    base = np.array(PAPER, np.float32)[None, None, ::-1] * 255  # BGR
    bgr = (base + n[..., None] * 255).clip(0, 255)
    yy, xx = np.mgrid[0:H, 0:W]
    vign = 1 - 0.06 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    bgr *= vign[..., None]
    stride = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_ARGB32, W)
    buf = np.zeros((H, stride // 4, 4), np.uint8)
    buf[:, :W, :3] = bgr.clip(0, 255).astype(np.uint8)
    buf[:, :W, 3] = 255
    surf = cairo.ImageSurface.create_for_data(memoryview(buf).cast("B"), cairo.FORMAT_ARGB32, W, H, stride)
    return surf, buf
