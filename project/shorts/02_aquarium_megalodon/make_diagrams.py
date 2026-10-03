# Scale diagrams for "メガロドンは水族館で飼育できるのか？" (1080x1920, accurate to scale)
from PIL import Image, ImageDraw, ImageFont
import os
D=os.path.dirname(os.path.abspath(__file__))
FONT='/tmp/claude-0/-home-user-kzmymn/3e7f1713-6c7b-55bd-b789-3923738060fb/scratchpad/short/noto/Sans/OTF/Japanese/NotoSansCJKjp-Bold.otf'
FM=FONT.replace('Bold','Medium')
W,H=1080,1920; BG=(6,16,34)
TANK_L,TANK_D=35.0,10.0          # 沖縄美ら海水族館「黒潮の海」35m x 27m x 深さ10m（公式）
PX=900/TANK_L                    # px per metre
X0=(W-900)//2; Y0=560            # tank top-left
fl=lambda s,f=FONT: ImageFont.truetype(f,s)

def shark(d,x,y,L,fill,outline,label=None,lab_col=(255,255,255),lab_pos='above'):
    """side-view shark silhouette, snout at right; (x,y)=tail tip x / body centre-line y; length L metres"""
    l=L*PX; h=l*0.16
    P=lambda u,v:(x+u*l,y+v*h)
    top=[(0.00,-0.95),(0.06,-0.55),(0.12,-0.12),(0.20,-0.30),(0.30,-0.48),(0.40,-0.62),(0.44,-1.02),(0.50,-1.05),(0.53,-0.66),
         (0.62,-0.70),(0.72,-0.66),(0.82,-0.55),(0.90,-0.38),(0.96,-0.18),(1.00,0.00)]
    bot=[(0.97,0.20),(0.90,0.36),(0.80,0.46),(0.70,0.50),(0.66,0.75),(0.60,0.52),(0.48,0.50),(0.36,0.42),(0.28,0.55),(0.25,0.38),
         (0.16,0.20),(0.10,0.10),(0.03,0.60),(0.07,0.05)]
    d.polygon([P(u,v) for u,v in top+bot],fill=fill,outline=outline,width=2)
    if label:
        f=fl(30,FM); tw=f.getlength(label)
        ty = y-h*1.3-44 if lab_pos=='above' else y+h*1.0+10
        d.text((max(X0, min(x+l/2-tw/2, X0+900-tw)),ty),label,font=f,fill=lab_col)

def base(title):
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im,'RGBA')
    # water
    d.rectangle([X0,Y0,X0+900,Y0+TANK_D*PX],fill=(20,70,120,170),outline=(200,225,245),width=3)
    d.line([X0,Y0+8,X0+900,Y0+8],fill=(150,200,235,140),width=2)
    f=fl(28,FM)
    d.text((X0,Y0-48),'国内最大級の水槽（長さ35m・深さ10m）',font=f,fill=(210,225,240))
    # human for scale
    hx=X0+900-40; hy=Y0+TANK_D*PX
    d.ellipse([hx-6,hy-44,hx+6,hy-32],fill=(230,235,240)); d.rectangle([hx-5,hy-32,hx+5,hy],fill=(230,235,240))
    d.text((hx-90,hy+8),'人（1.7m）',font=fl(24,FM),fill=(200,210,225))
    pass  # tag is drawn by the video renderer
    return im,d

# A: great white 3.5m vs newborn megalodon 3.6-3.9m
im,d=base('A')
mid=Y0+TANK_D*PX/2
shark(d,X0+380,Y0+TANK_D*PX*0.33,3.5,(200,210,220,235),(255,255,255),'ホホジロザメ 約3.5m',lab_pos='above')
shark(d,X0+380,Y0+TANK_D*PX*0.72,3.8,(224,165,38,230),(255,230,170),'生まれたてのメガロドン 約3.6〜3.9m（推定）',(255,225,160),lab_pos='below')
im.save(os.path.join(D,'diagram_A_newborn.png'))

# B1: adult 16m
im,d=base('B1')
shark(d,X0+60,Y0+TANK_D*PX*0.5,16.0,(224,165,38,215),(255,230,170))
d.text((X0+60,Y0+TANK_D*PX+60),'大人のメガロドン 約16m（推定）',font=fl(34,FM),fill=(240,190,90))
im.save(os.path.join(D,'diagram_B1_adult16m.png'))
# B2: max estimate 24.3m
im,d=base('B2')
shark(d,X0+60,Y0+TANK_D*PX*0.5,24.3,(224,120,38,200),(255,200,150))
d.text((X0+60,Y0+TANK_D*PX+60),'最大推定 約24.3m',font=fl(34,FM),fill=(240,150,90))
d.text((X0+60,Y0+TANK_D*PX+108),'水槽の長さの約7割',font=fl(30,FM),fill=(220,200,190))
im.save(os.path.join(D,'diagram_B2_max24m.png'))
print('ok')
