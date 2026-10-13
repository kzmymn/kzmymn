"""仕上げ：夕方らしい暖色の色調、ほのかな光のにじみ、周辺減光。"""
import sys
import numpy as np
from PIL import Image, ImageFilter

src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
a = np.asarray(im).astype(np.float32) / 255
# 暖色寄りに（影はわずかに青、明部は橙）
lum = a.mean(axis=2, keepdims=True)
warm = np.array([1.06, 1.0, 0.9])
cool = np.array([0.96, 1.0, 1.06])
a = a * (lum * warm + (1 - lum) * cool)
# 光のにじみ（明るい部分だけぼかして足す）
bright = np.clip((a - 0.72) * 3, 0, 1)
glow = np.asarray(Image.fromarray((bright * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(28))).astype(np.float32) / 255
a = a + glow * np.array([0.22, 0.15, 0.08])
# 周辺減光
h, w = a.shape[:2]
yy, xx = np.mgrid[0:h, 0:w]
v = 1 - 0.18 * (((xx - w / 2) / (w / 2)) ** 2 * 0.8 + ((yy - h / 2) / (h / 2)) ** 2) ** 1.3
a = a * v[..., None] * 1.1
Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).save(dst, quality=93)
print("->", dst)
