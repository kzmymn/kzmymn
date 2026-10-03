# Short 02 v3 "pro" edit: kinetic captions, animated scale diagrams, counters, caustics, SFX
import os, sys, subprocess, wave, math, random
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'out'); os.makedirs(OUT, exist_ok=True)
W, H, FPS, DUR = 1080, 1920, 30, 45.0
FD = '/tmp/claude-0/-home-user-kzmymn/3e7f1713-6c7b-55bd-b789-3923738060fb/scratchpad/short/noto/Sans/OTF/Japanese/'
FB, FM = FD + 'NotoSansCJKjp-Bold.otf', FD + 'NotoSansCJKjp-Medium.otf'
F = lambda s, b=True: ImageFont.truetype(FB if b else FM, s)
f_sub, f_big, f_huge, f_tag, f_lab, f_cnt = F(64), F(100), F(150), F(30, False), F(30, False), F(84)
AMBER = (242, 179, 61); WHITE = (255, 255, 255)
SAFE_CX, SUB_CY = 490, 1215

# ---------------- images ----------------
def load(p, scale=1.5):
    im = cv2.imread(os.path.join(D, p)); h, w = im.shape[:2]; k = W * scale / w
    return cv2.resize(im, (int(w*k), int(h*k)), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
IMG = {k: load('images/' + v) for k, v in dict(I1='I1_megalodon_tank.png', I2='I2_greatwhite_tank.png',
       I5='I5_museum_ceiling.png', I6='I6_whaleshark_tank.png', I7='I7_bay_aquarium.png').items()}

def view(key, cx, cy, s, dark=0.0, t=0.0):
    im = IMG[key]; ih, iw = im.shape[:2]
    cx += 0.0015*math.sin(t*0.9); cy += 0.0012*math.sin(t*0.7+1)      # very subtle "operator" drift
    sc = W / (iw / s)
    M = np.array([[sc, 0, W/2 - sc*cx*iw], [0, sc, H/2 - sc*cy*ih]], np.float32)
    out = cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    return out * (1 - dark) if dark else out

L = lambda a, b, x: a + (b - a) * x
def E(x): x = min(max(x, 0), 1); return x*x*(3-2*x)
def EO(x): x = min(max(x, 0), 1); return 1 - (1-x)**3

# ---------------- overlays ----------------
yy, xx = np.mgrid[0:120, 0:68].astype(np.float32)
def caustics(t):
    v = 0
    for kx, ky, w, ph in [(0.21, 0.13, 1.1, 0), (-0.17, 0.19, 0.8, 2), (0.11, -0.23, 1.3, 4), (0.27, 0.05, 0.6, 1)]:
        v = v + np.sin(xx*kx + yy*ky + t*w + ph)
    c = np.clip(1 - np.abs(v)/1.2, 0, 1)**6
    c = cv2.resize(c, (W, H), interpolation=cv2.INTER_CUBIC)
    mask = np.clip(1 - np.linspace(0, 1, H)/0.6, 0, 1)[:, None]
    return (c * mask)[..., None] * np.array([255, 235, 190], np.float32) * 0.10   # BGR-ish cool light
rng = random.Random(3)
SPECKS = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(4, 14), rng.uniform(1.2, 3.2), rng.uniform(.15, .45)) for _ in range(70)]
def specks(img, t):
    for x, y, v, r, a in SPECKS:
        py = (y - v*t*3) % H; px = x + 6*math.sin(t*0.5 + y)
        cv2.circle(img, (int(px), int(py)), int(r), (230, 240, 245), -1, cv2.LINE_AA)
VIG = (lambda g: (0.55 + 0.45*g)[..., None])(np.clip(1 - (((np.mgrid[0:H, 0:W][1]-W/2)/(W*0.75))**2 + ((np.mgrid[0:H, 0:W][0]-H*0.45)/(H*0.7))**2), 0, 1)).astype(np.float32)
SHADE = np.array([0 if y < 950 else min(.42, (y-950)/650*.42) for y in range(H)], np.float32)[:, None, None]

def underwater(fr, t, k=1.0):
    fr = fr + caustics(t) * k
    s = np.zeros_like(fr); specks(s, t); return fr + s * 0.22 * k

# ---------------- diagrams (accurate scale: 35 m tank = 900 px) ----------------
PX = 900/35.0; TX, TY = 90, 600; TD = 10*PX
NAVY = np.zeros((H, W, 3), np.float32)
for y in range(H): NAVY[y] = np.array(L(np.array([52, 26, 10]), np.array([18, 8, 3]), y/H), np.float32)
def shark_poly(x, y, Lm):
    l = Lm*PX; h = l*0.16
    top = [(0, -.95), (.06, -.55), (.12, -.12), (.2, -.3), (.3, -.48), (.4, -.62), (.44, -1.02), (.5, -1.05), (.53, -.66),
           (.62, -.7), (.72, -.66), (.82, -.55), (.9, -.38), (.96, -.18), (1, 0)]
    bot = [(.97, .2), (.9, .36), (.8, .46), (.7, .5), (.66, .75), (.6, .52), (.48, .5), (.36, .42), (.28, .55), (.25, .38),
           (.16, .2), (.1, .1), (.03, .6), (.07, .05)]
    return [(x+u*l, y+v*h) for u, v in top+bot]
def tank(d, p):
    p = E(p)
    d.rectangle([TX, TY, TX+900, TY+TD], fill=(20, 70, 120, int(170*p)))
    pts = [(TX, TY), (TX+900, TY), (TX+900, TY+TD), (TX, TY+TD), (TX, TY)]
    seg = p*4; cur = []
    for i in range(4):
        a, b = pts[i], pts[i+1]; k = min(max(seg - i, 0), 1)
        if k > 0: d.line([a, (a[0]+(b[0]-a[0])*k, a[1]+(b[1]-a[1])*k)], fill=(205, 228, 246), width=4)
    if p > .6:
        al = int(255*min(1, (p-.6)/.4))
        d.text((TX, TY-50), '国内最大級の水槽　長さ35m・深さ10m', font=f_lab, fill=(215, 228, 242, al))
        hx, hy = TX+870, TY+TD
        d.ellipse([hx-6, hy-44, hx+6, hy-32], fill=(235, 240, 245, al)); d.rectangle([hx-5, hy-32, hx+5, hy], fill=(235, 240, 245, al))
        d.text((hx-95, hy+10), '人（1.7m）', font=F(24, False), fill=(200, 212, 228, al))
def diagram_A(t):
    im = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(im)
    tank(d, t/0.8)
    for i, (Lm, y, col, lab, lc) in enumerate([(3.5, TY+TD*.32, (205, 215, 225), 'ホホジロザメ 約3.5m', WHITE),
                                              (3.8, TY+TD*.66, AMBER, '生まれたてのメガロドン 約3.6〜3.9m（推定）', AMBER)]):
        p = EO((t - 0.7 - i*0.9) / 0.8)
        if p <= 0: continue
        x = L(TX - 160, TX + 380, p)
        d.polygon(shark_poly(x, y, Lm), fill=col + (int(235*p),))
        tw = f_lab.getlength(lab); ty = y - 70 if i == 0 else TY + TD + 14
        d.text(((TX + 450 - tw/2) if i == 0 else TX, ty), lab, font=f_lab, fill=lc + (int(255*p),))
    return im
def diagram_B(t):
    im = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(im)
    tank(d, 1.0)
    pin = EO(t/0.7); grow = E((t - 2.8) / 1.6)
    Lm = L(16.0, 24.3, grow)
    col = tuple(int(L(a, b, grow)) for a, b in zip(AMBER, (235, 120, 50)))
    d.polygon(shark_poly(L(TX-420, TX+40, pin), TY+TD*.5, Lm), fill=col + (int(225*pin),))
    lab = f'{Lm:.1f}m'
    d.text((TX, TY+TD+40), lab, font=f_cnt, fill=col + (int(255*pin),))
    d.text((TX + f_cnt.getlength(lab) + 20, TY+TD+80), '推定全長' if grow < .99 else '最大推定', font=f_lab, fill=(225, 230, 240, int(255*pin)))
    if grow >= 1:
        a = int(255*E((t - 4.5)/0.5))
        d.text((TX, TY+TD+150), '→ 水槽の長さの約7割', font=F(40), fill=(240, 205, 170, a))
    return im
def navy_with(layer):
    base = Image.fromarray(cv2.cvtColor(NAVY.astype(np.uint8), cv2.COLOR_BGR2RGB)).convert('RGBA')
    base.alpha_composite(layer)
    return cv2.cvtColor(np.array(base.convert('RGB')), cv2.COLOR_RGB2BGR).astype(np.float32)

# ---------------- timeline ----------------
UW = 'uw'
SHOTS = [  # start, end, fn(local, dur, abs t), underwater?
    (0.0, 4.0,   lambda t, d, T: view('I1', L(.50, .49, E(t/d)), L(.47, .45, E(t/d)), L(1.06, 1.16, EO(t/d)), t=T), UW),
    (4.0, 8.5,   lambda t, d, T: view('I2', L(.46, .52, E(t/d)), .49, L(1.02, 1.08, t/d), t=T), UW),
    (8.5, 11.5,  lambda t, d, T: view('I2', L(.53, .58, E(t/d)), L(.47, .41, E(t/d)), L(1.12, 1.30, E(t/d)), t=T), UW),
    (11.5, 13.0, lambda t, d, T: view('I2', .58, .41, L(1.30, 1.36, t/d), dark=L(.35, .7, t/d), t=T), UW),
    (13.0, 14.8, lambda t, d, T: view('I2', .58, .41, L(1.36, 1.40, t/d), dark=.82, t=T), None),
    (14.8, 19.8, lambda t, d, T: navy_with(diagram_A(t)), None),
    (19.8, 26.3, lambda t, d, T: navy_with(diagram_B(t)), None),
    (26.3, 29.5, lambda t, d, T: view('I1', .49, .46, L(1.16, 1.02, E(t/d)), dark=.55, t=T), UW),
    (29.5, 34.0, lambda t, d, T: view('I6', L(.50, .53, E(t/d)), L(.47, .43, E(t/d)), L(1.00, 1.10, t/d), t=T), UW),
    (34.0, 38.2, lambda t, d, T: view('I7', L(.50, .47, E(t/d)), L(.60, .45, E(t/d)), L(1.00, 1.22, E(t/d)), t=T), None),
    (38.2, 45.0, lambda t, d, T: view('I5', .50, L(.60, .40, E(t/d)), L(1.08, 1.16, t/d), t=T), None),
]
CUTS = {4.0: 'whoosh', 8.5: None, 11.5: None, 13.0: 'boom', 14.8: 'whoosh', 19.8: 'whoosh', 26.3: 'boom_soft',
        29.5: 'whoosh', 34.0: 'whoosh', 38.2: 'whoosh'}
XF = 0.3
TAGS = [(0, 14.8, '仮想シーン／AI生成'), (14.8, 26.3, '模式図（縮尺はおおむね正確）'), (26.3, 29.5, '仮想シーン／AI生成'),
        (29.5, 34.0, 'イメージ（AI生成）'), (34.0, 38.2, 'もしも（想像）／AI生成'), (38.2, 45.0, 'イメージ（実際の展示とは異なります）')]
# captions: (start, end, text, style); {..} = emphasis colour
SUBS = [
    (0.0, 3.9, 'メガロドンは、\n{水族館}で飼えるのか？', 'sub'),
    (4.2, 8.3, '実は、{ホホジロザメ}でさえ\n難しい。', 'sub'),
    (8.7, 11.4, '2016年、沖縄で展示された\n{約3.5m}のホホジロザメは、', 'sub'),
    (11.5, 12.0, '1日目', 'cnt'), (12.0, 12.5, '2日目', 'cnt'), (12.5, 13.0, '3日目', 'cnt'),
    (13.1, 14.7, '{3日}で死んだ。', 'big'),
    (15.0, 17.2, 'メガロドンは、生まれた時点で\n{約3.6〜3.9m}。', 'sub'),
    (17.3, 19.6, 'そのホホジロザメと、\n{ほぼ同じ大きさ}。', 'sub'),
    (20.0, 22.5, '大人は、推定{16m}。', 'sub'),
    (22.7, 26.1, '最大で、{約24m}。', 'sub'),
    (26.5, 29.3, '結論：\n{かなり厳しい}。', 'sub'),
    (29.8, 33.8, '8.8mのジンベエザメでも、\n長さ35mの{巨大水槽}。', 'sub'),
    (34.2, 35.7, 'メガロドンを飼うなら――', 'sub'),
    (35.8, 38.0, '{湾をまるごと}、\n水槽にするしかない。', 'sub'),
    (38.5, 41.3, '現実に“飼える”メガロドンは、\n{1頭だけ}。', 'sub'),
    (41.5, 44.8, '埼玉の博物館の、\n{天井}に。', 'sub'),
]
BADGES = [(30.3, 33.8, '1995年から飼育30年・世界最長')]

def shot_at(T):
    for i, (a, b, fn, uw) in enumerate(SHOTS):
        if a <= T < b or (i == len(SHOTS)-1 and T >= b):
            def render(j, tt):
                aa, bb, ff, u = SHOTS[j]; fr = ff(min(max(tt-aa, 0), bb-aa), bb-aa, tt)
                return underwater(fr, tt) if u else fr
            fr = render(i, T)
            if i+1 < len(SHOTS) and T > b - XF/2 and SHOTS[i+1][0] not in (13.0,):
                k = (T - (b - XF/2)) / XF; fr = fr*(1-k) + render(i+1, T)*k
            if i > 0 and T < a + XF/2 and a not in (13.0,):
                k = .5 + (T-a)/XF; fr = render(i-1, T)*(1-k) + fr*k
            return fr

def rich_line(d, x, y, line, font, alpha, shadow=False):
    parts = []; buf = ''; emph = False
    for ch in line:
        if ch in '{}':
            if buf: parts.append((buf, emph)); buf = ''
            emph = ch == '{'
        else: buf += ch
    if buf: parts.append((buf, emph))
    for s, e in parts:
        if shadow:
            d.text((x, y+4), s, font=font, fill=(0, 0, 0, int(235*alpha)), stroke_width=7, stroke_fill=(0, 0, 0, int(235*alpha)))
        else:
            d.text((x, y), s, font=font, fill=(AMBER if e else WHITE) + (int(255*alpha),))
        x += font.getlength(s)
plain = lambda l: l.replace('{', '').replace('}', '')

def caption(base, T, a, b, text, font, cy, kinetic=True):
    lines = text.split('\n'); sz = font.size; lh = 1.42
    tot = sz*lh*(len(lines)-1) + sz
    lay = Image.new('RGBA', (W, H)); sh = Image.new('RGBA', (W, H))
    d, ds = ImageDraw.Draw(lay), ImageDraw.Draw(sh)
    out_a = min(1, (b - T)/0.18)
    for i, l in enumerate(lines):
        p = 1.0 if (a == 0.0 and T < 0.5) else EO((T - a - i*0.12)/0.28)
        al = max(0, min(p, out_a))
        if al <= 0: continue
        x = SAFE_CX - font.getlength(plain(l))/2; y = cy - tot/2 + i*sz*lh + (1-p)*30*kinetic
        rich_line(ds, x, y, l, font, al, shadow=True); rich_line(d, x, y, l, font, al)
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8))); base.alpha_composite(lay)

def frame(T):
    fr = shot_at(T)
    fr = fr * (1 - SHADE)
    # grade: gentle S-curve + vignette + grain
    fr = np.clip(fr, 0, 255) / 255.0
    fr = fr + 0.08*(fr - 0.5) - 0.08*(fr - 0.5)**3*4
    fr = fr * VIG * 255 + np.random.normal(0, 3.2, (H, W, 1))
    im = Image.fromarray(cv2.cvtColor(np.clip(fr, 0, 255).astype(np.uint8), cv2.COLOR_BGR2RGB)).convert('RGBA')
    d = ImageDraw.Draw(im)
    for a, b, tag in TAGS:
        if a <= T < b:
            d.text((56, 150), tag, font=f_tag, fill=(255, 255, 255, 215), stroke_width=2, stroke_fill=(0, 0, 0, 150))
    for a, b, tag in BADGES:
        if a <= T < b:
            al = min(EO((T-a)/0.3), (b-T)/0.2)
            tw = f_tag.getlength(tag)
            lay = Image.new('RGBA', (W, H)); dl = ImageDraw.Draw(lay)
            dl.rounded_rectangle([56, 205, 56+tw+36, 257], 26, fill=(10, 20, 40, int(170*al)), outline=AMBER + (int(220*al),), width=2)
            dl.text((74, 211), tag, font=f_tag, fill=(255, 235, 200, int(255*al)))
            im.alpha_composite(lay)
    for a, b, txt, st in SUBS:
        if a <= T < b:
            if st == 'sub': caption(im, T, a, b, txt, f_sub, SUB_CY)
            elif st == 'big': caption(im, T, a, b, txt, f_big, 930)
            elif st == 'cnt':
                p = EO((T-a)/0.15); s = 1 + 0.25*(1-p)
                f = F(int(150*s)); tw = f.getlength(txt)
                lay = Image.new('RGBA', (W, H)); dl = ImageDraw.Draw(lay)
                dl.text((SAFE_CX - tw/2, 860 - 75*s), txt, font=f, fill=WHITE + (int(255*p),), stroke_width=4, stroke_fill=(0, 0, 0, 200))
                im.alpha_composite(lay)
    rgb = np.array(im.convert('RGB'), np.float32)
    if T > DUR - 0.35: rgb *= max(0, (DUR - T)/0.35)
    return rgb.astype(np.uint8)

# ---------------- sound (all synthesised here, no third-party audio) ----------------
SR = 48000
def mix_audio(path):
    n = int(SR*DUR); tt = np.arange(n)/SR; rng = np.random.default_rng(11); out = np.zeros(n)
    b = np.cumsum(rng.standard_normal(n)); b -= np.convolve(b, np.ones(4801)/4801, 'same'); b /= np.abs(b).max()
    bed = .5*b*(.6+.4*np.sin(2*np.pi*tt/9)) + .22*np.sin(2*np.pi*55*tt) + .12*np.sin(2*np.pi*82.4*tt+1)
    out += bed * 0.10
    # tension pulse 4.0-13.0 (soft sub heartbeat, 84 bpm)
    for s in np.arange(4.0, 13.0, 60/84):
        i = int(s*SR); m = int(.35*SR); e = np.exp(-np.arange(m)/SR*14)
        out[i:i+m] += .22*np.sin(2*np.pi*48*np.arange(m)/SR)*e * min(1, (s-4)/2)
    def add(t0, sig, g=1.0):
        i = int(t0*SR); out[i:i+len(sig)] += g*sig[:max(0, n-i)]
    def boom(dur=1.6, f0=60):
        m = int(dur*SR); x = np.arange(m)/SR
        return np.sin(2*np.pi*(f0*x - 18*x**2)) * np.exp(-x*3) + .25*rng.standard_normal(m)*np.exp(-x*30)
    def whoosh(dur=.45):
        m = int(dur*SR); x = np.linspace(0, 1, m); nz = rng.standard_normal(m)
        nz = np.convolve(nz, np.ones(9)/9, 'same'); return nz*np.sin(np.pi*x)**2*.35
    def tick():
        m = int(.06*SR); x = np.arange(m)/SR; return np.sin(2*np.pi*1800*x)*np.exp(-x*90)*.35
    def riser(dur=1.6):
        m = int(dur*SR); x = np.arange(m)/SR; return np.sin(2*np.pi*(80*x + 60*x**2))*(x/dur)**2*.3
    def chime(dur=3.5):
        m = int(dur*SR); x = np.arange(m)/SR
        return sum(np.sin(2*np.pi*f*x) for f in (392, 587.3, 784)) * np.exp(-x*1.2) * .08
    add(0.0, boom(1.8, 55), .9)
    for t0, kind in CUTS.items():
        if kind == 'whoosh': add(t0 - .2, whoosh())
        elif kind == 'boom': add(t0, boom(), .9)
        elif kind == 'boom_soft': add(t0, boom(1.2, 70), .45)
    for t0 in (11.5, 12.0, 12.5): add(t0, tick())
    add(22.6, riser(), .8); add(24.3, boom(1.0, 70), .35)
    add(35.8, boom(1.4, 50), .5)
    add(41.5, chime())
    out *= np.minimum(1, (DUR - tt)/0.4)
    st = np.stack([out, np.roll(out, 180)], 1); st /= np.abs(st).max()
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*0.9*32767).astype(np.int16).tobytes())

def srt(path):
    ts = lambda x: (lambda ms: f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}')(int(round(x*1000)))
    rows = [s for s in SUBS if s[3] != 'cnt']
    with open(path, 'w', encoding='utf-8') as f:
        for i, (a, b, txt, _) in enumerate(rows, 1): f.write(f'{i}\n{ts(a)} --> {ts(b)}\n{plain(txt)}\n\n')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'still':
        for t in map(float, sys.argv[2:]): Image.fromarray(frame(t)).save(os.path.join(OUT, f'v3_still_{t:04.1f}.png'))
        sys.exit()
    srt(os.path.join(OUT, 'aquarium_megalodon_v3.srt')); wav = os.path.join(OUT, 'v3_mix.wav'); mix_audio(wav)
    silent = os.path.join(OUT, 'aquarium_megalodon_v3_silent.mp4')
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p',
                          '-movflags', '+faststart', silent], stdin=subprocess.PIPE)
    for i in range(int(DUR*FPS)): p.stdin.write(frame(i/FPS).tobytes())
    p.stdin.close(); p.wait()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', silent, '-i', wav, '-c:v', 'copy',
                    '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-shortest',
                    os.path.join(OUT, 'aquarium_megalodon_v3.mp4')], check=True)
    print('done')
