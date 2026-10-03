# Ep.01 カット表（絵コンテ・映像生成指示・編集指示）

- 全 **52カット**、本編 約7分58秒＋エンドカード20秒
- 素材の種類
  - **[V]** Veo 3.1（文章から動画。キーフレームの指定も可）
  - **[K]** Kling 3.0 I2V（MEG_REF などの参照画像から動画）
  - **[S]** 静止画を生成し、DaVinci でゆっくりズーム／パンをかける
  - **[G]** 図解・グラフィック（DaVinci の Fusion／Canva で作る）
  - **[P]** 実写写真（自分で撮影するか、ライセンスを確認した画像）
- `[STYLE]` は `03_style_bible.md` の共通プロンプト末尾を指す
- 生成はすべて 8秒（Kling は 5〜10秒）で行い、良い3〜6秒を切り出して使う
- AI生成の目安: 映像系（V/K）約34カット、合計約230秒 → リテイク3倍で**約700秒を生成**

---

## コールドオープン（0:00–0:35）　BGM: M1 Abyss　ラベル【もしも】

### C01｜0:00–0:05（5秒）｜[V]
- **映像**: 海面の真下から見上げる。太陽光の光芒が揺れ、画面いっぱいの青。
- **プロンプト**: `Looking straight up from 10 meters below the ocean surface in the open Pacific, shimmering sunlight god rays piercing deep blue water, gentle surface ripples, tiny particles drifting, calm and vast. Slow upward tilt. [STYLE]`
- **N**: 太平洋。日本の南の海。
- **テロップ**: 画面上部に小さく「この映像は、科学研究をもとにした仮想のシミュレーションです」（5秒）＋左上に【もしも】
- **SE**: 水中の環境音、低いゴボゴボ音
- **編集**: 黒から1秒かけてフェードイン。M1 は無音から立ち上げる

### C02｜0:05–0:12（7秒）｜[K] HUMP_REF
- **映像**: ザトウクジラの母子が横切る。子は母の胸びれの近くを泳ぐ。
- **プロンプト**: `A humpback whale mother and her calf swimming slowly side by side from left to right, 50 meters depth feel, soft blue light, calf close to mother's long pectoral fin, graceful tail strokes, camera tracking alongside at a respectful distance. [STYLE]`
- **N**: 水深およそ50メートル。ザトウクジラの親子が、北へ向かっています。
- **SE**: ザトウクジラの鳴き声（遠く、小さく）
- **編集**: 速度を95%に落として重さを出す

### C03｜0:12–0:17（5秒）｜[V]
- **映像**: クジラの親子を真上から見下ろす。その下は暗い青に溶けていく。
- **プロンプト**: `Top-down underwater view of a humpback whale mother and calf as small silhouettes, the water beneath them fading into dark blue abyss, enormous empty space below, ominous calm. Slow descending camera. [STYLE]`
- **N**: その、さらに下に。
- **編集**: カメラが下がる動きに合わせて M1 の低音を少し上げる

### C04｜0:17–0:23（6秒）｜[K] MEG_REF
- **映像**: はるか下の暗がりを、細長い巨大な影がゆっくり横切る。輪郭だけ見える。
- **プロンプト**: `Deep below in dim blue water, the enormous slender silhouette of a giant shark glides slowly across the frame, only its outline and the faint gleam of its pale belly visible, a small school of fish scatters near it for scale, the shape is at least three times longer than a bus. Static camera. [STYLE]` ＋参照画像 MEG_REF（側面）
- **N**: 影がある。
- **SE**: 低い「ブーン」という持続音（サブベース）
- **編集**: 影が画面の中央を通るときにナレーションを当てる

### C05｜0:23–0:26（3秒）｜[V]
- **映像**: 子クジラの目のクローズアップ。何かに気づいたような間。
- **プロンプト**: `Extreme close-up of a humpback whale calf's eye underwater, gentle light, the eye shifts slightly downward. [STYLE]`
- **N**: （なし。2秒の間）
- **SE**: すべての音を一瞬消す（無音の0.8秒）
- **編集**: 無音にして、次のナレーションを際立たせる

### C06｜0:26–0:31（5秒）｜[S]
- **映像**: 画面が暗転し、中央に小さく1本の化石の歯が浮かぶ（黒背景、スポットライト）。
- **プロンプト（静止画）**: `A single fossil Otodus megalodon tooth, dark grey-brown enamel with fine serrations, lit by a single spotlight against pure black, museum photography, ultra detailed, no text`
- **N**: ……もちろん、これは現実の映像ではありません。この影の持ち主は、およそ360万年前に、地球から姿を消しました。
- **テロップ**: 「約360万年前に絶滅」【事実】
- **編集**: ゆっくりズームイン（100%→108%）

### C07｜0:31–0:35（4秒）｜[G]＋[K]
- **映像**: 歯の画像から、現代の海に泳ぐメガロドンの正面のシルエットへディゾルブし、タイトルを出す。
- **プロンプト（背景映像）**: `Front view of a slender giant shark slowly approaching the camera out of deep blue gloom, mouth closed, calm and immense, only partially lit from above. [STYLE]` ＋MEG_REF（正面）
- **N**: でも、もしも――いまの海に、生きていたら。
- **テロップ**: タイトル「もしメガロドンが今の海に生きていたら」（明朝・白・中央）
- **SE**: 低い衝撃音（ブーム）をタイトルと同時に
- **編集**: タイトルは2.5秒表示。ここで M1 を切る

---

## イントロ（0:35–1:03）　BGM: M2 Wonder

### C08｜0:35–0:41（6秒）｜[S]
- **映像**: 古い図鑑の見開き（架空の図鑑。サメの挿絵と大きな歯の絵）。子どもの手がページをめくる。
- **プロンプト（静止画→Klingで手の動きを付ける）**: `A worn vintage Japanese children's encyclopedia open on a wooden desk at night, an illustrated page of a giant prehistoric shark and a huge triangular tooth drawn life-size, warm desk lamp light, a child's small hand touching the page, nostalgic film photography, no readable text`
- **N**: 子どもの頃、図鑑で見た「史上最大のサメ」。手のひらより大きな、三角形の歯。
- **SE**: ページをめくる音、遠くで時計の秒針
- **編集**: 暖色に色補正する（ここだけ懐かしい色味）

### C09｜0:41–0:47（6秒）｜[G]
- **映像**: 旧来のずんぐりしたシルエットが、細長いシルエットに滑らかに変わっていくモーフィング（線画）。
- **作り方**: デザインシートの旧来型と新型の側面図を線画化し、DaVinci の Fusion でディゾルブする（または同じ位置に重ねてクロスフェード）
- **N**: 実はこの数年で、その姿は大きく描き変えられつつあります。
- **SE**: 柔らかい「シュッ」という音

### C10｜0:47–0:58（11秒）｜[G]
- **映像**: 3つのラベルが順に出る。【事実】→化石の写真、【推定】→計算式風の線画、【もしも】→青い海の映像。
- **N**: この動画では、化石からわかっている「事実」、研究者が導き出した「推定」、そして私たちの「もしも」を、はっきり分けながら、
- **テロップ**: 3色のラベル（スタイルバイブル3章）
- **SE**: ラベルが出るたびに軽い「カチッ」
- **編集**: チャンネルの定番演出にする（毎回同じ動き・同じ音）

### C11｜0:58–1:03（5秒）｜[K] MEG_REF
- **映像**: 現代の海（遠くに船の底、ソナーのような光）を、メガロドンが通過していく。
- **プロンプト**: `A slender giant prehistoric shark swims past the camera in a modern ocean, far above on the surface the dark hull of a cargo ship is visible as a silhouette, sunlight beams, sense of two eras overlapping. [STYLE]`
- **N**: メガロドンを、現代の海に放ってみます。
- **SE**: 遠くの船のスクリュー音
- **編集**: 最後に1秒かけて黒へフェード

---

## 第1章「私たちは、全身を見たことがない」（1:03–2:20）　BGM: M2 Wonder → M3　ラベル【事実】

### C12｜1:03–1:07（4秒）｜[G]
- **映像**: 章タイトル「第1章　私たちは、全身を見たことがない」
- **SE**: 静かな「ポン」という余韻のある音

### C13｜1:07–1:15（8秒）｜[S]
- **映像**: 学名のテロップと、時間軸のバー（2,300万年前→360万年前）。
- **作り方**: 横長の時間軸を [G] で作る。背景は深海の静止画（ぼかす）
- **N**: メガロドン。学名、オトドゥス・メガロドン。生きていたのは、およそ2,000万年以上前から、360万年前まで。
- **テロップ**: *Otodus megalodon*／約2,300万年前〜約360万年前　出典: Boessenecker et al. 2019
- **編集**: 時間軸のバーが左から右へ伸びるアニメーション

### C14｜1:15–1:22（7秒）｜[S]
- **映像**: 博物館の暗い展示室。空っぽの展示台にスポットライトだけが当たっている（「全身はない」の比喩）。
- **プロンプト（静止画）**: `A dark natural history museum hall at night, a long empty display platform lit by a single spotlight, dust in the light beam, melancholic and quiet, cinematic, no people, no text`
- **N**: 意外かもしれませんが、私たちは、メガロドンの全身の骨格を、一度も見たことがありません。
- **編集**: ゆっくり前進するドリー（Ken Burns）

### C15｜1:22–1:29（7秒）｜[G]
- **映像**: サメの体の線画。軟骨部分が透けて消え、歯だけが残る。
- **N**: サメの骨格は、そのほとんどが軟骨。化石として、ほとんど残らないのです。
- **SE**: 砂がさらさらと崩れる音

### C16｜1:29–1:37（8秒）｜[V]
- **映像**: 海底の砂に、抜け落ちた歯がゆっくり沈んで積もっていく（古代の海）。
- **プロンプト**: `On an ancient shallow sea floor, large triangular shark teeth slowly sink and settle into the sand one after another, gentle current, sunlight dappling the seabed, time passing. Macro lens, slow motion. [STYLE]`
- **N**: 残ったのは、歯。サメは一生のあいだ、歯を生え替わらせ続けます。
- **SE**: 歯が砂に落ちる小さな音

### C17｜1:37–1:45（8秒）｜[S]＋[G]
- **映像**: 化石の歯と、スマートフォン（実物大）を並べた比較。
- **プロンプト（静止画）**: `A large fossil megalodon tooth about 18 cm tall placed next to a modern smartphone on a dark slate surface for size comparison, top-down studio product photography, soft light, no brand logos, no text`
- **N**: だからメガロドンの歯は、世界中の地層から大量に見つかっています。大きなものは、長さ18センチを超えます。
- **テロップ**: 「最大 約18 cm超」【事実】出典: Florida Museum
- **編集**: 数字のテロップを、歯の縁に沿った線とともに出す

### C18｜1:45–1:50（5秒）｜[P]または[S]
- **映像**: 椎骨が1列に並ぶ様子。
- **素材**: ベルギー王立自然史博物館の標本写真は権利の確認が必要。使えない場合はAI静止画で「椎骨141個を並べたイメージ」を作り、【イメージ】と表記する
- **プロンプト（静止画）**: `A long row of 141 fossilized shark vertebral centra laid out in a line on a museum table, disc-shaped, dark brown, dramatic side lighting, scientific specimen photography, no text`
- **N**: そして、まれな例外があります。ベルギーで見つかった、1頭分、141個の椎骨。
- **テロップ**: 「ベルギー王立自然史博物館 所蔵標本（IRSNB P 9893）」

### C19｜1:50–1:57（7秒）｜[S]＋[G]
- **映像**: 椎骨の断面に年輪のような成長の輪。46本の輪が順に光る。
- **プロンプト（静止画）**: `Cross-section of a fossil shark vertebra showing concentric growth rings like tree rings, macro photography, neutral background, high detail, no text`
- **N**: その断面に刻まれた成長の輪は、46本。この個体は、少なくとも46歳まで生きていたと考えられています。
- **テロップ**: 「成長輪 46本」【推定】出典: Shimada et al. 2021
- **編集**: 輪を外側から順にハイライトするアニメーション

### C20｜1:57–2:02（5秒）｜[G]
- **映像**: 地球儀がベルギーから日本へ回転する。
- **N**: もう一つの例外は、日本にあります。
- **SE**: 「シュッ」という回転音

### C21｜2:02–2:09（7秒）｜[P] 推奨
- **映像**: 荒川の河原（埼玉県深谷市付近）の現在の風景。
- **素材**: **自分で撮影する**のが理想（河川敷は撮影可。立ち入り禁止区域と化石採集のルールに注意）。難しければAI静止画を使い【イメージ】と表記する
- **プロンプト（代替の静止画）**: `A wide shallow river flowing over exposed layered sedimentary rock in the Japanese countryside in Saitama, autumn afternoon light, gravel banks, distant low mountains, realistic landscape photography, no text`
- **N**: 1986年。埼玉県、荒川の河原。
- **テロップ**: 「1986年　埼玉県（旧川本町・現深谷市）」

### C22｜2:09–2:16（7秒）｜[P] 推奨
- **映像**: 埼玉県立自然の博物館の歯の化石の展示。
- **素材**: **博物館に撮影と YouTube 掲載の許可を取り、自分で撮る**（下記「撮影メモ」参照）。許可が取れなければ、AI静止画「73本の歯の並び（イメージ）」で代替する
- **N**: 約1,000万年前の地層から、1頭分の歯が、73本まとまって見つかりました。1頭の歯がこれほどそろって見つかったのは、世界で初めてのことでした。
- **テロップ**: 「1頭分の歯 73本（世界初）」【事実】協力・出典: 埼玉県立自然の博物館

### C23｜2:16–2:20（4秒）｜[V]
- **映像**: 現在の荒川の風景が、1,000万年前の浅い海へディゾルブ（同じ構図で水が満ちていく）。
- **プロンプト**: `The same Japanese river valley landscape gradually transforms: water rises and the valley becomes a shallow ancient sea bay 10 million years ago, sunlight on the waves, seabirds, seamless transition. Locked-off camera. [STYLE]`
- **N**: 当時、このあたりは、海だったのです。
- **SE**: 川のせせらぎから波の音へ
- **編集**: 第1章のいちばんの見せ場。音楽を少し上げ、ナレーションのあとに2秒の間を取る

---

## 第2章「描き変えられた姿」（2:20–3:56）　BGM: M3 Evidence → M4　ラベル【推定】

### C24｜2:20–2:24（4秒）｜[G]
- **映像**: 章タイトル「第2章　描き変えられた姿」

### C25｜2:24–2:33（9秒）｜[K] 旧来型の参照
- **映像**: ずんぐりした旧来型のメガロドン（巨大ホホジロザメ型）が泳ぐ。少し古いCGのような質感。
- **プロンプト**: `A bulky, oversized great-white-shark-like giant shark with a massive head and thick torpedo body swims toward camera, classic 1990s documentary CGI look, slightly desaturated. [STYLE]` ＋旧来型の参照
- **N**: 長いあいだ、メガロドンは「巨大なホホジロザメ」として描かれてきました。太い胴体に、大きな頭。映画やゲームで、おなじみの姿です。
- **テロップ**: 「従来の復元」
- **編集**: 映像を4:3の枠に入れ、「古い資料映像」風に見せる

### C26｜2:33–2:39（6秒）｜[G]
- **映像**: 論文の表紙風のカード（誌名・年・著者を表示）。
- **N**: ところが2024年と2025年、研究者たちが別の可能性を示しました。
- **テロップ**: 「Sternes et al. 2024／Shimada et al. 2025　*Palaeontologia Electronica*」
- **編集**: 論文PDFの画面そのものは使わない（誌面の転載を避ける）。タイトル文字だけ自作で組む

### C27｜2:39–2:48（9秒）｜[G]
- **映像**: 現生のサメのシルエットが格子状に多数並ぶ（165種を表現）。中心に向かって集まり、細長いメガロドンの形になる。
- **N**: 現生と化石のサメ、165種の体のつくりを比べた結果――
- **SE**: 細かい「カチカチ」という音が連続する

### C28｜2:48–2:55（7秒）｜[K] MEG_REF
- **映像**: 新しい細長い体型のメガロドンが、真横を通り過ぎる（初めての全身ショット）。
- **プロンプト**: `Full side profile of a slender, elongated giant shark (lemon-shark-like proportions, 16 meters long) gliding slowly past the camera from right to left in clear blue mid-water, entire body visible, a school of mackerel for scale, sunlight rays from above, majestic and calm. [STYLE]` ＋MEG_REF（側面）
- **N**: メガロドンは、ホホジロザメよりもずっと細長い体をしていた可能性が高い。
- **テロップ**: 【推定】＋「体型は研究者の間で議論中。本映像は Shimada ほか（2025）にもとづく復元の一案」（常時5秒）
- **編集**: 本編で最も大事なカット。生成を多めに回し（6〜8回）、いちばん良いものを選ぶ

### C29｜2:55–3:04（9秒）｜[G]
- **映像**: 横から見たスケール比較。人、ホホジロザメ（6m）、バス（12m）、メガロドン16m、そして24mの輪郭線。最後にテニスコートが重なる。
- **N**: その推定では、ベルギーの個体は全長およそ16メートル。そして、いまの化石記録から考えうる最大のものは、およそ24メートル。テニスコートの長さと、ほぼ同じです。
- **テロップ**: 「約16.4 m」「最大 約24.3 m」【推定】出典: Shimada et al. 2025
- **編集**: 線が左から右へ伸びていく。24mの輪郭は点線にする（「最大の推定」であることを表す）

### C30｜3:04–3:12（8秒）｜[K]
- **映像**: 生まれたばかりのメガロドンの子が、浅い海を泳ぐ。そばにダイバー（比較用）。
- **プロンプト**: `A newborn giant prehistoric shark pup about 4 meters long swims through a sunlit shallow coastal bay with seagrass, a human scuba diver in the background for scale is clearly smaller than the pup, peaceful mood. [STYLE]` ＋MEG_REF
- **N**: 生まれたときの体長は、すでに3.6メートルから3.9メートル。大人の人間の、倍の大きさで生まれてきたことになります。
- **テロップ**: 「出生時 約3.6〜3.9 m」【推定】
- **注意**: ダイバーは比較のための演出なので、画面の隅に小さく「比較用の演出」と表示する

### C31｜3:12–3:20（8秒）｜[G]
- **映像**: 細長いモデルと旧来型のモデルを左右に並べ、中央に「？」。
- **N**: ただし、体の形については、研究者の間でまだ議論が続いています。ここから先の映像は、この新しい研究にもとづく「復元の一案」です。
- **テロップ**: 【論争中】（琥珀色）

### C32｜3:20–3:30（10秒）｜[G]＋[S]
- **映像**: 歯の断面と化学分析を表すグラフィック。サーモグラフィー風に、メガロドンの体の芯が周りの水より赤く光る。
- **プロンプト（静止画）**: `Thermal imaging style visualization of a giant slender shark in the ocean, the shark's core body glowing warmer orange-red than the surrounding cool blue water, scientific visualization, dark background, no text`
- **N**: 歯の化学分析からは、さらに二つのことがわかってきました。一つは、体温。メガロドンの体は、まわりの海水より7度ほど温かかったと推定されています。
- **テロップ**: 「周りの海水より 約+7℃」【推定】出典: Griffiths et al. 2023, PNAS

### C33｜3:30–3:44（14秒）｜[G]
- **映像**: 食物連鎖のピラミッド。プランクトン→小魚→大型魚→イルカ→…→最上段にメガロドン。現生のシャチやホホジロザメより上に置かれる。
- **N**: もう一つは、食物連鎖の中での位置。歯に残された窒素の記録は、メガロドンが、これまでに知られている海の生き物の中で、最も高い位置にいたことを示しています。
- **テロップ**: 「栄養段階 既知の海洋生物で最高水準」【推定】出典: Kast et al. 2022, Science Advances
- **編集**: ピラミッドが下から積み上がる

### C34｜3:44–3:56（12秒）｜[K]
- **映像**: メガロドンが画面奥から手前に向かって泳ぎ、カメラの上を通過していく（腹側が画面を覆う）。
- **プロンプト**: `Low-angle shot from below as a slender giant shark swims directly over the camera, its pale belly and long pectoral fins filling the frame, sunlight blocked as it passes, overwhelming scale. [STYLE]` ＋MEG_REF
- **N**: 捕食者を食べる捕食者を、さらに食べる。それが、メガロドンでした。
- **SE**: 通過に合わせて低い「ゴォッ」という水の圧力の音
- **編集**: M4 の盛り上がりをここに合わせる。腹が画面を覆った瞬間に暗転し、章を切り替える

---

## 第3章「なぜ、消えたのか」（3:56–4:43）　BGM: M4 → 静かに　ラベル【事実＋推定】

### C35｜3:56–4:00（4秒）｜[G]
- **映像**: 章タイトル「第3章　なぜ、消えたのか」

### C36｜4:00–4:10（10秒）｜[V]
- **映像**: 鮮新世の海。空から見た海岸線の時間経過。浅い海が後退し、陸が広がっていく。
- **プロンプト**: `Aerial time-lapse of an ancient coastline over thousands of years: shallow turquoise lagoons and coastal seas slowly shrink as sea level drops, land expands, the light turns colder and greyer, epic and quiet. [STYLE]`
- **N**: では、なぜこれほどの捕食者が、姿を消したのでしょうか。答えは、一つではありません。有力なのは、いくつもの変化が重なったという考え方です。
- **テロップ**: 【論争中】主な仮説：寒冷化／沿岸の海の減少／獲物の変化／競合

### C37｜4:10–4:18（8秒）｜[G]
- **映像**: 地球の気温グラフ（鮮新世の寒冷化の傾向を模式的に示す）と、浅い海の面積が縮む地図。
- **N**: 地球は少しずつ冷え、メガロドンが暮らしていた、暖かく浅い海が減っていきました。
- **テロップ**: 「鮮新世の海の大型動物：属の約36%が絶滅」出典: Pimiento et al. 2017
- **注意**: グラフは「模式図」と明記する（実データの曲線を描く場合は出典の数値を使う）

### C38｜4:18–4:24（6秒）｜[V]
- **映像**: 小型のヒゲクジラの群れが、冷たい色の海へ去っていく。
- **プロンプト**: `A small group of small baleen whales swimming away into colder, greener, murkier water, fading into the distance, melancholic. [STYLE]`
- **N**: 獲物となるクジラたちの顔ぶれも、変わっていきました。

### C39｜4:24–4:34（10秒）｜[K] GWS_REF
- **映像**: ホホジロザメが素早く旋回する（小回りのきく動き）。
- **プロンプト**: `A great white shark makes a quick agile turn in clear blue water, powerful tail stroke, sunlight dappling its back, close tracking shot. [STYLE]` ＋GWS_REF
- **N**: そして同じころ、同じ獲物を狙う、より小さく、小回りのきくライバルが、世界の海に広がっていました。ホホジロザメです。
- **テロップ**: 「競合説」【推定】出典: McCormack et al. 2022, Nature Communications

### C40｜4:34–4:43（9秒）｜[K]
- **映像**: 冷えた暗い海の中を、やせたメガロドンが1頭だけゆっくり泳いで、奥の闇に消えていく。
- **プロンプト**: `A lone giant slender shark swims slowly away from camera into dark, cold, greenish water, gradually disappearing into the gloom, sparse particles, sense of an ending era. [STYLE]` ＋MEG_REF
- **N**: 巨大な体と、温かい体。豊かな海では最強の武器だったものが、海が変わったとき、重すぎる「燃費」になったのかもしれません。
- **編集**: 消えきった後に2秒の暗転。M4 を消す。第3章から第4章への大きな区切り

---

## 第4章「もしも、いまの海にいたら」（4:43–6:39）　BGM: M5 What-if　ラベル【もしも】　画面: 青い色味＋上下に黒帯

### C41｜4:43–4:52（9秒）｜[G]＋[V]
- **映像**: 暗転から、青い現代の海へ。上下に黒帯が入る（2.39:1）。章タイトル「第4章　もしも、いまの海にいたら」。
- **プロンプト（背景）**: `Modern deep blue open ocean, sunlight rays, a distant container ship silhouette on the surface far above, quiet. [STYLE]`
- **N**: ここからは、想像の時間です。もしもメガロドンが、いまの海に生きていたら。
- **テロップ**: 画面上部に固定「ここから先は【もしも】― 研究をもとにした想像です」（この章の間ずっと表示）
- **SE**: ソナーの「ピン」という音

### C42｜4:52–5:06（14秒）｜[G]
- **映像**: 世界地図に海水温のグラデーション。極地と深海に×、温帯から熱帯の海に色が付く。日本の南を黒潮の流れが光る。
- **N**: まず、どこで暮らすのか。体を温める仕組みを持っていたとしても、冷たい極地の海や、餌の乏しい深海で生きるのは難しいはずです。現実的なのは、温帯から熱帯の海。日本の近くなら、たとえば黒潮が流れる海かもしれません。
- **テロップ**: 「推定される生息域（想像）」

### C43｜5:06–5:12（6秒）｜[K]
- **映像**: 黒潮の海。カツオの群れの横を、メガロドンが悠然と泳ぐ。
- **プロンプト**: `A slender giant shark cruising slowly through warm Kuroshio current waters off Japan, a huge shimmering school of skipjack tuna nearby, bright cobalt blue water, sunlight. [STYLE]` ＋MEG_REF
- **N**: （前のカットからの続き。ここは間として映像だけで見せる）

### C44｜5:12–5:28（16秒）｜[G]
- **映像**: 大きな数字「1日 約98,000 kcal」を出し、続けて「1年 ≒ 中型のクジラ1〜3頭分」をクジラのアイコンで見せる。
- **N**: 次に、どれだけ食べるのか。全長16メートルの個体が1日に必要とするエネルギーは、およそ9万8,000キロカロリーと推定されています。1年に直すと、中型のクジラ1頭から3頭分に相当する計算です。
- **テロップ**: 「約98,000 kcal/日」【推定】出典: Cooper et al. 2022　／「年に中型クジラ1〜3頭分」【試算】当チャンネルによる換算（仮定: クジラの組織1kgあたり1,000〜2,000kcal）
- **編集**: 試算の仮定は概要欄にも書く

### C45｜5:28–5:44（16秒）｜[V]＋[K]
- **映像**: (a) 巨大なシロナガスクジラの横で、メガロドンが小さく見える（4秒）→ (b) アシカの群れ、大型の魚、海底に沈んだクジラの骨（各3秒）。
- **プロンプト(a)**: `A blue whale, enormous and calm, swims in the foreground while a slender giant shark far behind looks small by comparison, scale contrast, deep blue water. [STYLE]`
- **プロンプト(b-1)**: `A playful group of sea lions darting through a kelp forest, sunlight. [STYLE]`
- **プロンプト(b-2)**: `A whale fall on the deep sea floor: a large whale skeleton resting on sediment, scavenging fish and crabs around it, dim blue light. [STYLE]`
- **N**: 狙うのは、おそらく大人のクジラではありません。体重が100トンを超えることもあるシロナガスクジラは、メガロドンにとっても大きすぎる。標的になりうるのは、クジラの子ども、アザラシやアシカ、大型の魚。そして、クジラの死骸です。
- **注意**: 狩りの瞬間・血は見せない（スタイルバイブル2章）

### C46｜5:44–5:50（6秒）｜[K] ORCA_REF
- **映像**: シャチの群れが、水面近くを編隊で泳いでくる。
- **プロンプト**: `A pod of five orcas swimming in tight formation toward the camera just below the surface, sunlight flickering on their black and white bodies, powerful and coordinated. [STYLE]` ＋ORCA_REF
- **N**: そして現代の海には、メガロドンが出会わなかった相手がいます。シャチです。
- **SE**: シャチの鳴き声（クリック音）
- **編集**: 「シャチです」の直後に音楽を一瞬止める

### C47｜5:50–6:08（18秒）｜[G]＋[V]
- **映像**: 上部の固定表示を一時的に【事実】へ切り替える（色も白へ）。カリフォルニア沖ファラロン諸島の地図→ホホジロザメが逃げる模式アニメ→南アフリカの地図。
- **背景用プロンプト**: `A great white shark swimming fast away from camera into the distance, tense mood, slightly murky coastal water. [STYLE]`
- **N**: これは、実際に観察されたことです。カリフォルニア沖では、シャチが現れると、ホホジロザメはその海域から逃げ出し、その季節のあいだ戻ってきませんでした。南アフリカでは、シャチがホホジロザメを狩り、栄養豊富な肝臓だけを食べていたことが記録されています。
- **テロップ**: 【事実】出典: Jorgensen et al. 2019, Scientific Reports／Towner et al. 2022, African Journal of Marine Science
- **編集**: 事実パートの間だけ黒帯を外し、色味をニュートラルに戻す（「ここだけ現実」を視覚で伝える）

### C48｜6:08–6:24（16秒）｜[K]
- **映像**: 【もしも】に戻る。(a) 浅い海で、メガロドンの子がシャチの群れに気づいて身をひるがえす（8秒）→ (b) 大人のメガロドンとシャチの群れが、深い青の中で距離を取ってすれ違う（8秒。接触はさせない）。
- **プロンプト(a)**: `In a sunlit shallow bay, a juvenile slender giant shark about 4 meters long notices a distant pod of orcas and turns away quickly, tense atmosphere. [STYLE]`
- **プロンプト(b)**: `In open deep blue water, a 16-meter slender giant shark and a pod of orcas pass each other at a distance, both cautious, circling slowly, no contact, ominous standoff. Wide shot. [STYLE]`
- **N**: もしも、そこにメガロドンがいたら。大人のメガロドンは、どのシャチよりもはるかに大きい。けれど、生まれたばかりの子どもは、群れで狩りをするシャチにとって、格好の獲物になるかもしれません。
- **テロップ**: 【もしも】

### C49｜6:24–6:39（15秒）｜[V]
- **映像**: 両者のシルエットが闇の中で円を描くように回る。カメラは真上から、ゆっくり引いていく。
- **プロンプト**: `Top-down view in deep dark blue water: the silhouettes of a giant slender shark and several orcas slowly circling each other, the camera slowly pulls away upward until they become tiny shapes, mysterious, unresolved. [STYLE]`
- **N**: 大人どうしが出会ったら、どうなるのか。それは――誰にも、わかりません。
- **編集**: 「それは――」のあと1秒の間。M5 をここで切り、無音で次の章へ

---

## 第5章「私たちは、気づくのか」（6:39–7:33）　BGM: 無音 → M6 Ending　ラベル【もしも】→【事実】

### C50｜6:39–7:03（24秒）｜[G]＋[V]
- **映像**: 現代の海の観測網のモンタージュ（各4〜5秒）。(1) 海底に積もる新しい白い歯、(2) クジラの体の巨大な噛み跡の線画（実写は使わない）、(3) 漁船と網、(4) サメに付けられた衛星タグと地図上の軌跡、(5) 研究船で海水を採取する様子（環境DNA）。
- **プロンプト(1)**: `Fresh white shark teeth scattered on a modern sandy seafloor, a curious fish passing by, clear water. [STYLE]`
- **プロンプト(3)**: `A Japanese fishing boat at dawn hauling in nets, ocean spray, realistic. [STYLE]`
- **プロンプト(5)**: `Marine scientists on a research vessel deck collecting seawater samples in bottles for environmental DNA analysis, overcast daylight, realistic documentary. [STYLE]`
- **N**: では、私たち人間は、その存在に気づくでしょうか。答えは、ほぼ確実に「気づく」です。生きていれば、抜け落ちた新しい歯が、海底に積もっていく。クジラの体には、見たこともない大きさの噛み跡が残る。漁師の網、衛星タグ、海の水に残されたDNA。いまの海は、私たちが思っている以上に、見張られています。
- **編集**: 項目ごとに小さなアイコンのテロップ（歯／噛み跡／網／タグ／DNA）

### C51｜7:03–7:33（30秒）｜[S]＋[V]
- **映像**: (a) 化石の歯（C06 と同じもの）を再び黒背景で見せる（10秒）→【事実】ラベルに戻り、上下の黒帯が外れる。(b) 大型の貨物船と、それに比べて小さな1頭のサメのシルエット（10秒）。(c) 網に絡まった現生のサメ（シルエットのみ、10秒）。
- **プロンプト(b)**: `View from below: the massive dark hull of a 200-meter cargo ship passing overhead, a giant shark silhouette far below it looks small, sunlight around the hull. [STYLE]`
- **プロンプト(c)**: `Silhouette of a shark entangled in a drifting fishing net in blue water, somber, no blood, documentary. [STYLE]`
- **N**: そして、この理屈は逆向きにも働きます。新しい歯は、一本も見つかっていない。巨大な噛み跡もない。だからこそ、科学者たちは言います。メガロドンは、もういない。　船が襲われる心配は？　メガロドンにとって人間は、小さすぎて割に合わない獲物です。むしろ心配すべきなのは、人間の網や船が、メガロドンを追い詰めることのほうかもしれません。
- **テロップ**: 「メガロドンは絶滅している」【事実】出典: NHM London／Boessenecker et al. 2019
- **編集**: 「もういない」で M6 を入れる。この動画でいちばん大事な一文なので、テロップは大きめに

---

## エンディング（7:33–7:58）＋エンドカード（7:58–8:18）　BGM: M6 Ending

### C52｜7:33–7:58（25秒）｜[V]＋[P]
- **映像**: (a) 古代の海を、最後の1頭が夕暮れの光の中で泳ぎ去る（8秒）→ (b) 地層の崖の断面に、歯の化石が埋まっているアップ（7秒）→ (c) 最初の図鑑のページが閉じられる（C08 と同じ机、10秒）。
- **プロンプト(a)**: `Golden hour light from the surface in an ancient warm sea, a single slender giant shark swims slowly toward the horizon of blue, peaceful and elegiac, wide shot. [STYLE]`
- **プロンプト(b)**: `Close-up of a layered sedimentary cliff face with a fossil shark tooth partially exposed in the rock, natural daylight, realistic. no text`
- **N**: 360万年前、最後のメガロドンが泳いだ海。その歯はいまも、世界中の地層の中で眠っていて、ときどき、私たちの前に姿を現します。子どもの頃、図鑑の向こうに見ていたあの海は、本当に、あったのです。　次回は、水深1万メートル。地球でいちばん深い海の底へ、降りていきます。
- **編集**: 図鑑が閉じる音で M6 を締める

### エンドカード（20秒）
- 背景: 暗い深海へ光が消えていく静止画（次回の予告：マリアナ海溝）
- YouTube の終了画面: 「次の動画（再生リスト）」＋「チャンネル登録」
- テロップ: 「参考文献は概要欄に」

---

## 撮影メモ（実写素材を自分で撮る場合）
- **埼玉県立自然の博物館（長瀞町）**: 1986年の歯の化石（県指定天然記念物）と約12mの復元模型を展示。特別展「古秩父湾」は **2026年10月12日まで**（調査時点の情報。公式サイトで要確認）。
  - 撮影の可否と、**YouTube（収益化チャンネル）への掲載許可**を事前に問い合わせる。許可が出たら、概要欄に「撮影協力」として記載する。
  - 許可が取れれば、AI映像の中に「本物」が入り、チャンネルの信頼性が大きく上がる。この動画で最も費用対効果の高い素材になる。
- 荒川の河川敷: 風景は撮影してよいが、化石を勝手に採集しないこと（天然記念物の指定区域や河川管理のルールを確認）。

## 生成量の見積もり
| 種類 | カット数 | 使う秒数 | 生成する秒数（リテイク込み） |
|---|---|---|---|
| [K] Kling（参照画像あり） | 16 | 約125秒 | 約400秒（C28 は8回分） |
| [V] Veo | 16 | 約105秒 | 約300秒 |
| [S] 静止画 | 12 | 約85秒 | 静止画40枚程度 |
| [G] 図解 | 15 | 約150秒 | DaVinci／Canva で作る |
| [P] 実写 | 2〜4 | 約20秒 | 自分で撮影 |
