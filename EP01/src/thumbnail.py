"""サムネイル（1280×720）：「遅れた。連絡できない。」＋時計と待つ人物。"""
import os, sys

import cairo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import *  # noqa

surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
ctx = cairo.Context(surf)
bg, _k = paper_background()
ctx.set_source_surface(bg, 0, 0); ctx.paint()
pen = Pen(ctx, 0, 30)
pen.lw = 8
# 右：時計の下で待つ人
station_clock(pen, 1330, 1010, 2, 30, s=1.25)
clock(pen, 1322, 572, 74, 2, 30, sector=(0, 30), seed=33)
person(pen, 1580, 1010, 1.45, A_COL, "worry", "stand", 0, look=-0.6)
sweat(pen, 1660, 560, 1.4)
bubble(pen, 1640, 330, "まだ…？", 64, tail=(-1, 1), think=True)
# 左：大きな文字
pen.text("遅れた。", 100, 330, 180, color=INK, stroke=10, stroke_color=WHITE, ax=0)
ctx.set_source_rgba(*YELLOW, 0.9); ctx.rectangle(90, 600, 960, 80); ctx.fill()
pen.text("連絡できない。", 100, 580, 140, color=RED, stroke=10, stroke_color=WHITE, ax=0)
tag(pen, 330, 840, "携帯がない時代", 64, bg=WHITE)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out")
surf.write_to_png(os.path.join(out, "thumb-1920.png"))
from PIL import Image
Image.open(os.path.join(out, "thumb-1920.png")).convert("RGB").resize((1280, 720), Image.LANCZOS).save(
    os.path.join(out, "EP01-thumbnail.jpg"), quality=92)
os.remove(os.path.join(out, "thumb-1920.png"))
print("-> out/EP01-thumbnail.jpg")
