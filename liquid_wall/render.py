import sys, os
import numpy as np
from multiprocessing import Pool

W, H = int(os.environ.get("W", 1280)), int(os.environ.get("H", 720))
FPS = 30
DUR = float(os.environ.get("DUR", 15))
OUT = sys.argv[1]

rng = np.random.default_rng(7)
PERM = np.concatenate([rng.permutation(256)] * 2).astype(np.int32)
GRAD = rng.random(256).astype(np.float32)


def vnoise(x, y):
    xi = np.floor(x); yi = np.floor(y)
    xf = x - xi; yf = y - yi
    xi = xi.astype(np.int32) & 255; yi = yi.astype(np.int32) & 255
    u = xf * xf * (3 - 2 * xf); v = yf * yf * (3 - 2 * yf)
    a = GRAD[PERM[PERM[xi] + yi]]
    b = GRAD[PERM[PERM[xi + 1] + yi]]
    c = GRAD[PERM[PERM[xi] + yi + 1]]
    d = GRAD[PERM[PERM[xi + 1] + yi + 1]]
    return (a + (b - a) * u) + ((c + (d - c) * u) - (a + (b - a) * u)) * v


def fbm(x, y, oct=5):
    s = np.zeros_like(x); amp = 0.5
    for _ in range(oct):
        s += amp * vnoise(x, y)
        x, y = 1.6 * x + 1.2 * y + 3.1, -1.2 * x + 1.6 * y + 1.7
        amp *= 0.5
    return s


def pal(t, d):
    return 0.58 + 0.42 * np.cos(6.28318 * (t[..., None] + d))


RAMP = np.array([
    [0.10, 0.12, 0.45], [0.20, 0.70, 0.95], [0.92, 0.97, 1.00], [0.70, 0.55, 0.95],
    [0.95, 0.35, 0.75], [1.00, 0.80, 0.85], [0.35, 0.90, 0.80], [0.05, 0.35, 0.40],
    [0.55, 0.30, 0.85], [0.95, 0.85, 0.45]], np.float32)


def ramp(t):
    n = len(RAMP)
    x = np.mod(t, 1.0) * n
    i = np.floor(x).astype(np.int32) % n
    f = (x - np.floor(x))[..., None]
    f = f * f * (3 - 2 * f)
    return RAMP[i] * (1 - f) + RAMP[(i + 1) % n] * f


ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
U = (xs - W / 2) / H
V = (ys - H / 2) / H

# drifting "touch" vortices
VORT = [(-0.45, 0.05, 0.22, 1), (0.35, -0.12, 0.18, -1), (0.05, 0.25, 0.15, 1), (0.6, 0.2, 0.2, -1)]


def frame(i):
    t = i / FPS
    x, y = U.copy(), V.copy()
    for k, (cx, cy, rad, sg) in enumerate(VORT):
        cx2 = cx + 0.15 * np.sin(0.21 * t + k * 1.7)
        cy2 = cy + 0.10 * np.cos(0.17 * t + k * 2.3)
        dx, dy = x - cx2, y - cy2
        r2 = dx * dx + dy * dy
        pulse = 0.5 + 0.5 * np.sin(0.35 * t + k * 2.1)
        ang = sg * (1.6 + 2.0 * pulse) * np.exp(-r2 / (rad * rad))
        ca, sa = np.cos(ang), np.sin(ang)
        x, y = cx2 + ca * dx - sa * dy, cy2 + sa * dx + ca * dy

    px, py = x * 1.3, y * 1.3
    qx = fbm(px + 0.06 * t, py)
    qy = fbm(px + 5.2, py + 1.3 - 0.05 * t)
    rx = fbm(px + 4 * qx + 1.7 + 0.09 * t, py + 4 * qy + 9.2)
    ry = fbm(px + 4 * qx + 8.3, py + 4 * qy + 2.8 + 0.07 * t)
    f = fbm(px + 4 * rx, py + 4 * ry)

    # marbled bands
    band = f * 3.6 + np.sqrt(qx * qx + qy * qy) * 1.2 + 0.04 * t
    col = ramp(band * 0.55 + 0.03 * np.sin(0.1 * t))

    # chrome-like shading from the height field
    gy, gx = np.gradient(f * 900.0 / H * (H / 720))
    nx, ny = -gx * 6, -gy * 6
    nl = 1 / np.sqrt(nx * nx + ny * ny + 1)
    nx, ny, nz = nx * nl, ny * nl, nl
    env = pal(nx * 0.8 + ny * 0.5 + band * 0.25,
              np.array([0.1, 0.25, 0.55], np.float32))
    lx, ly, lz = 0.35, -0.5, 0.79
    diff = np.clip(nx * lx + ny * ly + nz * lz, 0, 1)
    spec = np.clip(diff, 0, 1) ** 25
    metal = np.clip(1.0 - nz, 0, 1) ** 0.6
    c = col * (0.35 + 0.75 * diff[..., None])
    c = c * (1 - 0.55 * metal[..., None]) + env * 0.55 * metal[..., None]
    c += spec[..., None] * 0.9
    # thin dark/bright contour lines -> marbled ink look
    fr = np.abs(np.mod(band * 1.0, 1.0) - 0.5)
    line = np.clip(1 - fr / 0.06, 0, 1)
    hi = np.clip(1 - np.abs(fr - 0.12) / 0.03, 0, 1)
    c = c * (1 - 0.45 * line[..., None]) + 0.45 * hi[..., None]
    # boost saturation/contrast
    g = c.mean(-1, keepdims=True)
    c = np.clip(g + (c - g) * 1.1, 0, None)
    c = (c - 0.08) * 1.15

    # deep teal background in calm regions, like the room's base glow
    calm = np.clip((rx - 0.47 - 0.05 * np.sin(0.2 * t)) * 4.0, 0, 1)
    calm = calm * calm * (3 - 2 * calm)
    bg = np.array([0.0, 0.05, 0.05], np.float32) + 0.22 * pal(qy * 1.5 + 0.02 * t, np.array([0.45, 0.35, 0.6], np.float32)) * np.array([0.2, 1.0, 0.6], np.float32)
    c = c * (1 - calm[..., None]) + bg * calm[..., None]

    # vignette + tonemap
    vig = 1 - 0.35 * (U * U + V * V)
    c = c * vig[..., None]
    c = np.clip(c, 0, 1) ** 0.9
    return (c * 255).astype(np.uint8).tobytes()


if __name__ == "__main__":
    n = int(FPS * DUR)
    if OUT.endswith(".png"):
        import subprocess
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-i", "-", OUT],
                       input=frame(int(os.environ.get("F", 60))), check=True)
        sys.exit()
    import subprocess
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                          "-preset", "slow", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    with Pool(4) as pool:
        for k, b in enumerate(pool.imap(frame, range(n), chunksize=2)):
            p.stdin.write(b)
            if k % 30 == 0:
                print(k, "/", n, flush=True)
    p.stdin.close(); p.wait()
