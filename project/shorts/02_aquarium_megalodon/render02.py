# Short 02「メガロドンは、水族館で飼育できるのか？」 still-image edit -> 1080x1920 MP4
import os, sys, subprocess, wave
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, 'out'); os.makedirs(OUT, exist_ok=True)
W, H, FPS, DUR = 1080, 1920, 30, 38.0
FONTDIR = '/tmp/claude-0/-home-user-kzmymn/3e7f1713-6c7b-55bd-b789-3923738060fb/scratchpad/short/noto/Sans/OTF/Japanese/'
FB, FM = FONTDIR + 'NotoSansCJKjp-Bold.otf', FONTDIR + 'NotoSansCJKjp-Medium.otf'
f_sub, f_big, f_tag, f_logo = (ImageFont.truetype(FB, 62), ImageFont.truetype(FB, 96),
                               ImageFont.truetype(FM, 30), ImageFont.truetype(FM, 34))

def load(p, scale=1.5):
    im = cv2.imread(os.path.join(D, p))
    h, w = im.shape[:2]; k = W * scale / w
    return cv2.resize(im, (int(w * k), int(h * k)), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)

IMG = {k: load(v) for k, v in {'I1': 'images/I1_megalodon_tank.png', 'I2': 'images/I2_greatwhite_tank.png',
                               'I5': 'images/I5_museum_ceiling.png'}.items()}
IMG.update({k: load(v, 1.0) for k, v in {'A': 'diagram_A_newborn.png', 'B1': 'diagram_B1_adult16m.png',
                                         'B2': 'diagram_B2_max24m.png'}.items()})

def view(key, cx, cy, s, dark=0.0):
    """cx, cy: centre in 0-1 image coords; s: zoom (1 = whole frame)"""
    im = IMG[key]; ih, iw = im.shape[:2]
    sc = W / (iw / s)
    M = np.array([[sc, 0, W/2 - sc*cx*iw], [0, sc, H/2 - sc*cy*ih]], np.float32)
    out = cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_AREA if sc < 1 else cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    return out * (1 - dark) if dark else out

L = lambda a, b, t: a + (b - a) * t
E = lambda t: (lambda x: x*x*(3-2*x))(min(max(t, 0), 1))

SHOTS = [  # start, end, fn(local t, duration)
    (0.0, 4.0,  lambda t, d: view('I1', L(.50, .49, E(t/d)), L(.50, .47, E(t/d)), L(1.00, 1.08, t/d))),
    (4.0, 8.5,  lambda t, d: view('I2', L(.48, .52, t/d), .50, L(1.00, 1.06, t/d))),
    (8.5, 14.0, lambda t, d: view('I2', L(.52, .56, t/d), L(.50, .43, E(t/d)), L(1.06, 1.20, t/d))),
    (14.0, 18.5, lambda t, d: view('I2', .56, .43, L(1.20, 1.25, t/d), dark=.55)),
    (18.5, 23.5, lambda t, d: view('A', .5, .476, L(1.15, 1.17, t/d))),
    (23.5, 26.5, lambda t, d: view('B1', .5, .476, 1.15)),
    (26.5, 30.0, lambda t, d: view('B2', .5, .476, L(1.15, 1.17, t/d))),
    (30.0, 33.0, lambda t, d: view('I1', .49, .47, L(1.10, 1.00, E(t/d)), dark=.58)),
    (33.0, 38.0, lambda t, d: view('I5', .50, L(.56, .42, E(t/d)), L(1.10, 1.16, t/d))),
]
XF = 0.5
TAGS = [(0, 18.5, '仮想シーン／AI生成'), (18.5, 30, '模式図（縮尺はおおむね正確）'), (30, 33, '仮想シーン／AI生成'), (33, 38, 'イメージ（実際の展示とは異なります）')]
SUBS = [
    (0.3, 3.9, 'メガロドンは、\n水族館で飼えるのか？', 'sub'),
    (4.3, 8.3, '実は、ホホジロザメでさえ\n難しい。', 'sub'),
    (8.7, 11.6, '2016年、沖縄で展示された\n約3.5mのホホジロザメは、', 'sub'),
    (11.8, 13.9, '3日で死んだ。', 'big'),
    (14.3, 16.3, '泳ぎ続けて\n呼吸するサメ。', 'sub'),
    (16.4, 18.3, '飼育は、極めて難しい。', 'sub'),
    (18.8, 21.0, 'メガロドンは、生まれた時点で\n約3.6〜3.9m。', 'sub'),
    (21.1, 23.3, 'そのホホジロザメと、\nほぼ同じ大きさ。', 'sub'),
    (23.7, 26.4, '大人は、推定16m。', 'sub'),
    (26.7, 29.8, '最大で、約24m。', 'sub'),
    (30.2, 32.9, '答え：今の技術では、\nまず不可能。', 'sub'),
    (33.3, 35.6, 'ただし1頭だけ、\n“飼える”メガロドンがいる。', 'sub'),
    (35.7, 37.6, '埼玉の博物館の、\n天井に。', 'sub'),
]
LOGO = (36.0, 38.0, 'ロストジャイアント')
SAFE_CX, SUB_CY = 490, 1210

shade = np.array([0 if y < 900 else min(.4, (y-900)/700*.4) for y in range(H)], np.float32)[:, None, None]

def shot_frame(t):
    for i, (a, b, fn) in enumerate(SHOTS):
        if a <= t < b or (i == len(SHOTS)-1 and t >= b):
            fr = fn(min(t, b) - a, b - a)
            if i + 1 < len(SHOTS) and t > b - XF/2:
                na, nb, nfn = SHOTS[i+1]; k = (t - (b - XF/2)) / XF
                fr = fr*(1-k) + nfn(0, nb-na)*k
            if i > 0 and t < a + XF/2:
                pa, pb, pfn = SHOTS[i-1]; k = .5 + (t-a)/XF
                fr = pfn(pb-pa, pb-pa)*(1-k) + fr*k
            return fr

def alpha(t, a, b, f=.3):
    return 0 if t < a or t > b else min(1, (t-a)/f, (b-t)/f)

def text_block(base, text, font, cy, al, lh=1.42):
    lines = text.split('\n'); sz = font.size
    tot = int(sz*lh*(len(lines)-1) + sz)
    lay = Image.new('RGBA', (W, H)); sh = Image.new('RGBA', (W, H))
    d, ds = ImageDraw.Draw(lay), ImageDraw.Draw(sh)
    for i, l in enumerate(lines):
        x = SAFE_CX - font.getlength(l)/2; y = cy - tot//2 + i*sz*lh
        ds.text((x, y+3), l, font=font, fill=(0, 0, 0, 230), stroke_width=6, stroke_fill=(0, 0, 0, 230))
        d.text((x, y), l, font=font, fill=(255, 255, 255, 255))
    out = Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)), lay)
    if al < 1: out.putalpha(out.getchannel('A').point(lambda v: int(v*al)))
    base.alpha_composite(out)

def frame(t):
    fr = shot_frame(t) * (1 - shade)
    im = Image.fromarray(cv2.cvtColor(np.clip(fr, 0, 255).astype(np.uint8), cv2.COLOR_BGR2RGB)).convert('RGBA')
    for a, b, tag in TAGS:
        al = alpha(t, a+.1, b-.1)
        if al:
            l = Image.new('RGBA', (W, H))
            ImageDraw.Draw(l).text((56, 150), tag, font=f_tag, fill=(255, 255, 255, int(215*al)),
                                   stroke_width=2, stroke_fill=(0, 0, 0, int(140*al)))
            im.alpha_composite(l)
    for a, b, txt, st in SUBS:
        al = alpha(t, a, b)
        if al: text_block(im, txt, f_big if st == 'big' else f_sub, SUB_CY, al)
    a, b, txt = LOGO; al = alpha(t, a, b+1, .6)
    if al:
        l = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(l); tw = f_logo.getlength(txt)
        d.text((SAFE_CX-tw/2, 1420), txt, font=f_logo, fill=(230, 235, 240, int(230*al)))
        im.alpha_composite(l)
    rgb = np.array(im.convert('RGB'), np.float32)
    if t > DUR-.6: rgb *= max(0, (DUR-t)/.6)
    if t < .3: rgb *= t/.3
    return rgb.astype(np.uint8)

def audio(path):
    sr = 48000; n = int(sr*DUR); rng = np.random.default_rng(5); tt = np.arange(n)/sr
    b = np.cumsum(rng.standard_normal(n)); b -= np.convolve(b, np.ones(4801)/4801, 'same'); b /= np.abs(b).max()
    sig = .55*b*(.6+.4*np.sin(2*np.pi*tt/9)) + .25*(.35*np.sin(2*np.pi*55*tt) + .2*np.sin(2*np.pi*82.4*tt+1))
    sig *= np.minimum(1, tt/2.5)*np.minimum(1, (DUR-tt)/2); sig = sig/np.abs(sig).max()*10**(-24/20)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.stack([sig, np.roll(sig, 240)], 1)*32767).astype(np.int16).tobytes())

def srt(path):
    ts = lambda x: (lambda ms: f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}')(int(round(x*1000)))
    with open(path, 'w', encoding='utf-8') as f:
        for i, (a, b, txt, _) in enumerate(SUBS, 1): f.write(f'{i}\n{ts(a)} --> {ts(b)}\n{txt}\n\n')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'still':
        for t in map(float, sys.argv[2:]): Image.fromarray(frame(t)).save(os.path.join(OUT, f'still_{t:04.1f}.png'))
        sys.exit()
    srt(os.path.join(OUT, 'aquarium_megalodon.srt')); wav = os.path.join(OUT, 'ambience.wav'); audio(wav)
    silent = os.path.join(OUT, 'aquarium_megalodon_silent.mp4')
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p',
                          '-movflags', '+faststart', silent], stdin=subprocess.PIPE)
    for i in range(int(DUR*FPS)): p.stdin.write(frame(i/FPS).tobytes())
    p.stdin.close(); p.wait()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', silent, '-i', wav, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                    '-shortest', os.path.join(OUT, 'aquarium_megalodon.mp4')], check=True)
    print('done')
