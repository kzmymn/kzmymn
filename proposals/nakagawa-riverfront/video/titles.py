# Builds an ffmpeg filter script for the motion-typography layer.
# Usage: python3 titles.py <fonts_dir> <textdir> <out_filter_file>
import os, sys
FONTS, TXT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(TXT, exist_ok=True)
MIN = f"{FONTS}/ShipporiMincho-800.ttf"; GOT = f"{FONTS}/ZenKakuGothicNew-500.ttf"
LATB = f"{FONTS}/Lato-900.ttf"; LATL = f"{FONTS}/Lato-400.ttf"
items = []
def text(key, s, font, size, t0, t1, x="(w-text_w)/2", y="(h-text_h)/2", color="white", rise=24, fin=0.45, fout=0.3, spacing=0, shadow=True):
    p = f"{TXT}/{key}.txt"; open(p, "w", encoding="utf-8").write(s)
    a = f"clip(min((t-{t0})/{fin}\\,({t1}-t)/{fout})\\,0\\,1)"
    yy = f"{y}+{rise}*pow(1-clip((t-{t0})/0.6\\,0\\,1)\\,3)"
    sh = ":shadowcolor=black@0.75:shadowx=0:shadowy=4:borderw=2:bordercolor=black@0.25" if shadow else ""
    items.append(f"drawtext=fontfile={font}:textfile={p}:fontsize={size}:fontcolor={color}:x={x}:y={yy}:alpha='{a}'"
                 f":enable='between(t\\,{t0}\\,{t1})'{sh}" + (f":line_spacing={spacing}" if spacing else ""))
def line(t0, t1, y, wmax=520, color="0x3B95A9"):
    # growing hairline (drawbox width cannot animate; emulate with 8 steps)
    for k in range(1, 9):
        a = t0 + (k - 1) * 0.05
        wk = int(wmax * k / 8)
        items.append(f"drawbox=x=(iw-{wk})/2:y={y}:w={wk}:h=3:color={color}@0.95:t=fill:enable='between(t\\,{a:.2f}\\,{t1})'")
# 0-3 s: kicker
text("k1", "F U K U O K A   ×   N A K A   R I V E R", LATL, 40, 0.6, 3.0, y="h*0.47", rise=0)
line(0.9, 3.0, 590, 420)
# 3-7 s: title + tagline
text("t1", "NAKAGAWA", MIN, 150, 3.0, 7.0, y="h*0.30", rise=40)
text("t2", "RIVER NIGHTS", MIN, 150, 3.25, 7.0, y="h*0.30+165", rise=40)
text("t3", "川が、夜のステージになる。", MIN, 52, 4.3, 7.0, y="h*0.30+360", rise=20)
# 7-10.5 s: beat-synced keywords (one per beat = 0.5 s)
for i, w in enumerate(["LIVE", "JAZZ", "CIRCUS", "ART", "DJ", "MARCHE"]):
    t0 = 7.0 + i * 0.5
    text(f"w{i}", w, LATB, 210, t0, t0 + 0.5, rise=0, fin=0.06, fout=0.08)
text("w9", "4 STAGES  ON  THE  RIVER", LATB, 64, 10.0, 10.9, y="h*0.42", rise=10, fin=0.15)
text("w10", "水上ステージ ・ 屋形船 ・ アート ・ マルシェ", GOT, 40, 10.15, 10.9, y="h*0.42+90", rise=10, fin=0.15)
# 10.9-13 s: date + place
text("d1", "2027.3.14 SUN — 3.22 MON", LATB, 120, 10.95, 13.0, y="h*0.36", rise=30)
text("d2", "那珂川　春吉橋〜西大橋エリア　｜　17:30–22:00", GOT, 44, 11.3, 13.0, y="h*0.36+160", rise=16)
line(11.2, 13.0, 640, 760)
# 13-15 s: end card
text("e1", "NAKAGAWA RIVER NIGHTS", MIN, 96, 13.1, 15.0, y="h*0.38", rise=20, fout=0.01)
text("e2", "COMING SOON", LATL, 46, 13.6, 15.0, y="h*0.38+130", rise=10, fout=0.01)
# persistent small notes
text("n1", "TEASER  /  EXPERIMENTAL", LATL, 24, 0.3, 15.0, x="60", y="50", rise=0, fout=0.01, shadow=False)
text("n2", "※タイトル・日程は仮", GOT, 22, 0.3, 15.0, x="w-text_w-60", y="h-80", rise=0, fout=0.01, shadow=False)
pre = ("[0:v]format=yuv420p,eq=brightness='-0.12*clip((t-2.8)/0.4\\,0\\,1)"
       "-0.08*clip((t-12.9)/0.5\\,0\\,1)':eval=frame,vignette=PI/4.5")
chain = pre + "," + ",".join(items) + ",fade=t=in:st=0:d=0.6[v]"
open(OUT, "w").write(chain)
print(len(items), "layers")
