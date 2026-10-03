# v2: "では、もっと巨大な水槽なら？" -> ジンベエザメ30年 vs ホホジロザメ198日 の展開を追加
import os, sys, subprocess
import render02 as R
from PIL import Image

L, E, view = R.L, R.E, R.view
R.IMG['I6'] = R.load('images/I6_whaleshark_tank.png')
R.DUR = 44.5
R.SHOTS = [
    (0.0, 4.0,   lambda t, d: view('I1', L(.50, .49, E(t/d)), L(.50, .47, E(t/d)), L(1.00, 1.08, t/d))),
    (4.0, 8.5,   lambda t, d: view('I2', L(.48, .52, t/d), .50, L(1.00, 1.06, t/d))),
    (8.5, 14.0,  lambda t, d: view('I2', L(.52, .56, t/d), L(.50, .43, E(t/d)), L(1.06, 1.20, t/d))),
    (14.0, 19.0, lambda t, d: view('A', .5, .476, L(1.15, 1.17, t/d))),
    (19.0, 22.0, lambda t, d: view('B1', .5, .476, 1.15)),
    (22.0, 25.5, lambda t, d: view('B2', .5, .476, L(1.15, 1.17, t/d))),
    (25.5, 29.0, lambda t, d: view('I1', .49, .47, L(1.10, 1.00, E(t/d)), dark=.55)),
    (29.0, 33.5, lambda t, d: view('I6', L(.50, .52, t/d), L(.46, .44, t/d), L(1.00, 1.07, t/d))),
    (33.5, 37.5, lambda t, d: view('I1', .49, L(.47, .44, t/d), L(1.00, 1.12, t/d))),
    (37.5, 44.5, lambda t, d: view('I5', .50, L(.56, .42, E(t/d)), L(1.10, 1.16, t/d))),
]
R.TAGS = [(0, 14, '仮想シーン／AI生成'), (14, 25.5, '模式図（縮尺はおおむね正確）'), (25.5, 29, '仮想シーン／AI生成'),
          (29, 33.5, 'イメージ（AI生成）'), (33.5, 37.5, 'もしも（想像）／AI生成'), (37.5, 44.5, 'イメージ（実際の展示とは異なります）')]
R.SUBS = [
    (0.3, 3.9, 'メガロドンは、\n水族館で飼えるのか？', 'sub'),
    (4.3, 8.3, '実は、ホホジロザメでさえ\n難しい。', 'sub'),
    (8.7, 11.6, '2016年、沖縄で展示された\n約3.5mのホホジロザメは、', 'sub'),
    (11.8, 13.9, '3日で死んだ。', 'big'),
    (14.3, 16.6, 'メガロドンは、生まれた時点で\n約3.6〜3.9m。', 'sub'),
    (16.7, 18.8, 'そのホホジロザメと、\nほぼ同じ大きさ。', 'sub'),
    (19.2, 21.9, '大人は、推定16m。', 'sub'),
    (22.2, 25.3, '最大で、約24m。', 'sub'),
    (25.8, 28.8, '結論：\nかなり厳しい。', 'sub'),
    (29.3, 33.2, '8.8mのジンベエザメでも、\n長さ35mの巨大水槽。', 'sub'),
    (33.8, 35.3, 'メガロドンを飼うなら――', 'sub'),
    (35.4, 37.3, '湾をまるごと、\n水槽にするしかない。', 'sub'),
    (37.9, 40.6, '現実に“飼える”メガロドンは、\n1頭だけ。', 'sub'),
    (40.8, 43.4, '埼玉の博物館の、\n天井に。', 'sub'),
]
R.LOGO = (42.5, 44.5, 'ロストジャイアント')

if __name__ == '__main__':
    O = R.OUT
    if len(sys.argv) > 1 and sys.argv[1] == 'still':
        for t in map(float, sys.argv[2:]): Image.fromarray(R.frame(t)).save(os.path.join(O, f'v2_still_{t:04.1f}.png'))
        sys.exit()
    R.srt(os.path.join(O, 'aquarium_megalodon_v2.srt')); wav = os.path.join(O, 'ambience_v2.wav'); R.audio(wav)
    silent = os.path.join(O, 'aquarium_megalodon_v2_silent.mp4')
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{R.W}x{R.H}', '-r', str(R.FPS),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p',
                          '-movflags', '+faststart', silent], stdin=subprocess.PIPE)
    for i in range(int(R.DUR*R.FPS)): p.stdin.write(R.frame(i/R.FPS).tobytes())
    p.stdin.close(); p.wait()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', silent, '-i', wav, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                    '-shortest', os.path.join(O, 'aquarium_megalodon_v2.mp4')], check=True)
    print('done')
