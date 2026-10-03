import os, subprocess, math, random, wave
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, 'out'); os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1080, 1920, 30
DUR = 38.0
FB = os.path.join(D, 'noto/Sans/OTF/Japanese/NotoSansCJKjp-Bold.otf')
FM = os.path.join(D, 'noto/Sans/OTF/Japanese/NotoSansCJKjp-Medium.otf')
f_sub = ImageFont.truetype(FB, 62)
f_big = ImageFont.truetype(FB, 92)
f_tag = ImageFont.truetype(FM, 30)
f_logo = ImageFont.truetype(FM, 34)
f_diag = ImageFont.truetype(FM, 30)

plate = cv2.imread(os.path.join(D, 'source_shark_boat.png')).astype(np.float32)  # full-res original
PH, PW = plate.shape[:2]

def view(cx, cy, s, dark=0.0):
    """crop of the plate centred at (cx,cy) in plate px, zoom s (1 = full frame)"""
    k = PW / 1080.0; cx, cy = cx * k, cy * k   # layout coords are in 1080-wide units
    sx = W / (PW / s); sy = H / (PH / s)
    M = np.array([[sx, 0, W/2 - sx*cx], [0, sy, H/2 - sy*cy]], np.float32)
    im = cv2.warpAffine(plate, M, (W, H), flags=cv2.INTER_AREA if s < PW/1080 else cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    if dark: im = im * (1 - dark)
    return im

def lerp(a, b, t): return a + (b - a) * t
def ease(t): t = min(max(t, 0), 1); return t*t*(3-2*t)

# ---- schematic background (deep sea food supply) ----
rng = random.Random(7)
parts = []
for i in range(420):
    parts.append(dict(x=rng.uniform(40, W-40), y0=rng.uniform(-200, 1900), v=rng.uniform(28, 55),
                      r=rng.uniform(1.6, 3.6), life=rng.uniform(0.15, 1.0)))
grad = np.zeros((H, W, 3), np.float32)
for y in range(H):
    t = y / H
    top = np.array([0x3a, 0x6f, 0x8f]); mid = np.array([0x0c, 0x1d, 0x3a]); bot = np.array([0x02, 0x05, 0x10])
    c = lerp(top, mid, min(t/0.18, 1)) if t < 0.18 else lerp(mid, bot, (t-0.18)/0.82)
    grad[y, :] = c[::-1]  # BGR

def diagram(tt):
    im = Image.fromarray(cv2.cvtColor(grad.astype(np.uint8), cv2.COLOR_BGR2RGB))
    d = ImageDraw.Draw(im, 'RGBA')
    for p in parts:
        y = (p['y0'] + p['v'] * tt) % 1900
        depth = y / 1900
        # fewer particles survive deeper: hide if depth beyond its life
        if depth > p['life']: continue
        a = int(200 * (1 - depth*0.75))
        d.ellipse([p['x']-p['r'], y-p['r'], p['x']+p['r'], y+p['r']], fill=(220, 235, 240, a))
    d.text((70, 330), '表層', font=f_diag, fill=(220, 235, 245, 210))
    d.line([(70, 380), (70, 1580)], fill=(200, 220, 235, 90), width=2)
    d.polygon([(62, 1570), (78, 1570), (70, 1595)], fill=(200, 220, 235, 120))
    d.text((70, 1610), '深海', font=f_diag, fill=(200, 215, 230, 200))
    d.text((110, 460), '有機物（マリンスノー）が沈む', font=f_diag, fill=(220, 235, 245, 170))
    return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR).astype(np.float32)

# ---- timeline ----
# shots: (start, end, fn(t_local, dur) -> BGR float)
P1 = (640, 860)
def s1(t, d): return view(lerp(540, P1[0], ease(t/d)), lerp(960, P1[1], ease(t/d)), lerp(1.0, 1.10, t/d))
def s2(t, d): return view(lerp(P1[0], 600, ease(t/d)), lerp(P1[1], 760, ease(t/d)), lerp(1.10, 1.24, t/d))
def s3(t, d): return view(lerp(360, 375, t/d), lerp(1420, 1385, t/d), lerp(1.50, 1.56, t/d))
def s4(t, d): return view(lerp(375, 385, t/d), lerp(1385, 1365, t/d), lerp(1.56, 1.60, t/d), dark=0.62)
def s5(t, d): return diagram(t)
def s6(t, d): return view(lerp(600, 560, t/d), lerp(820, 940, t/d), lerp(1.12, 1.0, ease(t/d)), dark=0.58)
SHOTS = [(0, 5, s1), (5, 10, s2), (10, 15, s3), (15, 22, s4), (22, 28, s5), (28, 38, s6)]
XF = 0.5  # crossfade seconds (centred on cut)

TAGS = [(0, 10, '仮想シーン／AI再現'), (10, 22, '復元イメージ／AI生成'), (22, 28, '模式図'), (28, 38, '仮想シーン／AI再現')]
# subtitles: (start, end, text, style)
SUBS = [
    (0.4, 4.8, 'メガロドンは、\n今も深海に隠れている？', 'sub'),
    (5.3, 9.8, '想像すると、\n海を見る目が変わります。', 'sub'),
    (10.3, 14.8, 'でも、生き延びるには、\n大きな壁があります。', 'sub'),
    (15.4, 17.9, 'それは、餌。', 'big'),
    (18.1, 21.8, '巨大な体を支えるには、\n多くの食料が必要です。', 'sub'),
    (22.5, 27.8, '深海の多くは、\nその食料が乏しい世界。', 'sub'),
    (28.4, 32.6, '約360万年前に絶滅したと\n考えられています。', 'sub'),
    (32.9, 37.4, '今も生きているという、\n確かな証拠はありません。', 'sub'),
]
LOGO = (35.0, 38.0, 'ロストジャイアント')

SAFE_CX = 490      # keep clear of the right-side action buttons
SUB_CY = 1190      # above the bottom caption / channel area

def shot_frame(t):
    for i, (a, b, fn) in enumerate(SHOTS):
        if a <= t < b:
            fr = fn(t - a, b - a)
            if i + 1 < len(SHOTS) and t > b - XF/2:
                na, nb, nfn = SHOTS[i+1]
                k = (t - (b - XF/2)) / XF
                fr = fr * (1-k) + nfn(0, nb-na) * k
            if i > 0 and t < a + XF/2:
                pa, pb, pfn = SHOTS[i-1]
                k = 0.5 + (t - a) / XF
                fr = pfn(pb-pa, pb-pa) * (1-k) + fr * k
            return fr
    return SHOTS[-1][2](SHOTS[-1][1]-SHOTS[-1][0], 1)

def alpha_of(t, a, b, f=0.35):
    if t < a or t > b: return 0
    return min(1, (t-a)/f, (b-t)/f)

def draw_text_block(base, text, font, cy, alpha, lh=1.42):
    lines = text.split('\n')
    asc = font.size
    widths = [font.getlength(l) for l in lines]
    tot_h = int(asc * lh * (len(lines)-1) + asc)
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer); ds = ImageDraw.Draw(sh)
    y0 = cy - tot_h // 2
    for i, l in enumerate(lines):
        x = SAFE_CX - widths[i] / 2
        y = y0 + i * asc * lh
        ds.text((x, y + 3), l, font=font, fill=(0, 0, 0, 230), stroke_width=6, stroke_fill=(0, 0, 0, 230))
        d.text((x, y), l, font=font, fill=(255, 255, 255, 255))
    sh = sh.filter(ImageFilter.GaussianBlur(9))
    out = Image.alpha_composite(sh, layer)
    if alpha < 1:
        a = out.getchannel('A').point(lambda v: int(v * alpha)); out.putalpha(a)
    base.alpha_composite(out)

# subtle bottom-to-mid gradient for readability
shade = np.zeros((H, W), np.float32)
for y in range(H):
    shade[y] = 0.0 if y < 900 else min(0.38, (y-900)/700*0.38)

def render_frame(t):
    fr = shot_frame(t)
    fr = fr * (1 - shade[..., None])
    im = Image.fromarray(cv2.cvtColor(np.clip(fr, 0, 255).astype(np.uint8), cv2.COLOR_BGR2RGB)).convert('RGBA')
    for a, b, tag in TAGS:
        al = alpha_of(t, a + 0.1, b - 0.1, 0.3)
        if al:
            l = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(l)
            d.text((56, 150), tag, font=f_tag, fill=(255, 255, 255, int(215*al)), stroke_width=2, stroke_fill=(0, 0, 0, int(140*al)))
            im.alpha_composite(l)
    for a, b, txt, st in SUBS:
        al = alpha_of(t, a, b)
        if al:
            if st == 'big': draw_text_block(im, txt, f_big, 930, al)
            else: draw_text_block(im, txt, f_sub, SUB_CY, al)
    a, b, txt = LOGO
    al = alpha_of(t, a, b + 1, 0.6)
    if al:
        l = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(l)
        tw = f_logo.getlength(txt)
        d.text((SAFE_CX - tw/2, 1395), txt, font=f_logo, fill=(225, 232, 240, int(230*al)))
        d.line([(SAFE_CX - 60, 1383), (SAFE_CX + 60, 1383)], fill=(225, 232, 240, int(150*al)), width=2)
        im.alpha_composite(l)
    # fade out the last 0.6 s
    rgb = np.array(im.convert('RGB'), np.float32)
    if t > DUR - 0.6: rgb *= max(0, (DUR - t) / 0.6)
    if t < 0.4: rgb *= t / 0.4
    return rgb.astype(np.uint8)

def make_audio(path):
    sr = 48000; n = int(sr * DUR); rng = np.random.default_rng(3)
    white = rng.standard_normal(n)
    brown = np.cumsum(white); brown -= np.convolve(brown, np.ones(4801)/4801, 'same'); brown /= np.abs(brown).max()
    tt = np.arange(n) / sr
    swell = 0.6 + 0.4 * np.sin(2*np.pi*tt/9.0)
    drone = 0.35*np.sin(2*np.pi*55*tt) + 0.2*np.sin(2*np.pi*82.4*tt + 1.0)
    sig = 0.55*brown*swell + 0.25*drone
    env = np.minimum(1, tt/2.5) * np.minimum(1, (DUR - tt)/2.0)
    sig = sig * env
    sig = sig / np.abs(sig).max() * 10**(-24/20)   # peak about -24 dBFS: quiet bed
    st = np.stack([sig, np.roll(sig, 240)], 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((st * 32767).astype(np.int16).tobytes())

def srt(path):
    def ts(x):
        ms = int(round(x*1000)); return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
    with open(path, 'w', encoding='utf-8') as f:
        for i, (a, b, txt, _) in enumerate(SUBS, 1):
            f.write(f'{i}\n{ts(a)} --> {ts(b)}\n{txt}\n\n')

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'still':
        for t in [float(x) for x in sys.argv[2:]]:
            Image.fromarray(render_frame(t)).save(os.path.join(OUT, f'still_{t:05.1f}.png'))
        raise SystemExit
    srt(os.path.join(OUT, 'megalodon_short.srt'))
    wav = os.path.join(OUT, 'ambience.wav'); make_audio(wav)
    silent = os.path.join(OUT, 'megalodon_short_silent.mp4')
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', silent], stdin=subprocess.PIPE)
    for i in range(int(DUR*FPS)):
        p.stdin.write(render_frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', silent, '-i', wav, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest',
                    os.path.join(OUT, 'megalodon_short.mp4')], check=True)
    print('done')
