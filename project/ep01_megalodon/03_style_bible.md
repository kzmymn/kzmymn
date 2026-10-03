# Ep.01 スタイルバイブル（全カット共通の映像・音のルール）

AI映像で一番崩れやすいのは「カットごとに生物の姿・色味・質感がバラバラになること」です。
ここで決めたルールを全カットのプロンプトと編集に当てはめてください。

---

## 1. メガロドンのデザインを固定する（最初の1日でやること）

### 1-1. 採用する復元モデル
- **Shimada et al. 2025（*Palaeontologia Electronica* 28(1):a12）の「細長い体型」**を採用する。
  - 体の長さに対する太さの比率は、現生のレモンザメに近い。ずんぐりしたホホジロザメ型にはしない。
  - 頭は体に比べてやや小さく、尾部は長め（16.4mの個体で頭部約1.8m、尾部約3.6m）。
  - ひれの細かい形は化石からわかっていない。そのため、大型のネズミザメ目の一般的な形にとどめる（第1背びれは大、第2背びれは小、三日月形の尾びれ）。
- 画面上では「復元の一案」と明記する（台本の第2章）。
- 比較用に、旧来の「巨大ホホジロザメ型」のシルエットも1枚だけ作る（第2章の比較カットで使う）。

### 1-2. デザインシートの生成プロンプト（Nano Banana Pro / Midjourney / GPT Image）
```
Scientific paleoart character model sheet of Otodus megalodon, reconstructed as a SLENDER, elongated
fusiform shark: body length-to-girth proportions similar to a lemon shark (Negaprion brevirostris)
scaled up to 16 meters, relatively small conical snout, wide jaw with rows of large triangular
serrated teeth, large first dorsal fin, small second dorsal fin, crescent-shaped caudal fin,
long pectoral fins. Dark slate-grey dorsal skin with subtle bronze tint, sharp countershading
to off-white belly, faint old scars on the flank, matte skin texture with fine dermal denticles.
Orthographic views: side view, top view, front view, three-quarter view, close-up of mouth.
Neutral mid-grey studio background, even lighting, photorealistic, museum-grade scientific
illustration, no text, no labels.
```
- 生成した中から1案を決め、**側面・正面・3/4・口元の4枚**を「MEG_REF」として保存する。この4枚は以後すべての I2V（画像から動画）とキーフレーム生成の参照画像に使う。
- 旧来型（比較用）のプロンプト:「same sheet, but bulky great-white-shark proportions, oversized head, thick torpedo body」

### 1-3. 現生の生物も参照画像を固定する
- ザトウクジラ親子（HUMP_REF）、シャチ（ORCA_REF）、ホホジロザメ（GWS_REF）。それぞれ側面1枚を作って固定する。

---

## 2. 映像トーン

| 項目 | ルール |
|---|---|
| 画面比 | 16:9、1080pで書き出す（余裕があれば4K） |
| フレームレート | 24fps（生成時も24fpsを指定） |
| カメラ | ゆっくり動かす。手持ち風の揺れはNG。水中ではドリーとクレーンのような滑らかな移動のみ |
| 水中の光 | 水深で分ける。浅い場所（0〜20m）は揺れる光の網目と光芒、中層（20〜200m）は赤が抜けた青緑、深い場所は暗い青で輪郭の光だけ |
| 粒子 | 浮遊粒子（マリンスノー）を常に少量入れる。スケール感が出て、AIの破綻も隠せる |
| スケール感 | 大きさを見せたいカットには必ず比較対象を入れる（魚群、ダイバー、ボート、クジラ）。遠くの物ほど青く霞ませる |
| 色 | 「事実」パート：ニュートラルでややウォーム。「もしも」パート：彩度をやや落とした青、シネマスコープ風の上下黒帯（2.39:1）を足す |
| 質感統一 | 全カットに同じLUT＋フィルムグレイン（強さ10〜15%）を当て、ツールごとの質感差を消す |
| AIで崩れやすい動き | 噛みつく瞬間、口の開閉、生物同士の接触は直接見せない。泡、砂煙、影、カットの切り替えで「起きた」と分からせる（ドキュメンタリーの文法） |
| 残酷描写 | 血や捕食の瞬間は見せない（YouTubeの「視聴者を不快にさせるコンテンツ」方針に配慮。大人向けでも品よく） |

### 共通プロンプト末尾（全映像プロンプトの最後に付ける）
```
STYLE: photorealistic wildlife documentary cinematography, shot on large-format cinema camera
in underwater housing, natural light, gentle suspended particles, physically accurate water
caustics and light falloff, subtle film grain, 24fps, no text, no watermark, no subtitles.
```
各カットのプロンプト中の `[STYLE]` は、この文を意味する。

---

## 3. 画面上のグラフィック（毎回同じものを使う＝チャンネルの「型」）

| 要素 | 仕様 |
|---|---|
| 区分ラベル | 左上に表示。【事実】白地に黒文字、【推定】琥珀（#E0A526）、【もしも】青（#3A7BD5）。角丸、フォントは Noto Sans JP Bold |
| AI透かし | 右下に常時「AI生成の再現映像」（白50%）。実写や写真のカットでは外す |
| 出典カード | 数値を出すカットでは、画面下に小さく「出典: Shimada et al. 2025」のように表示（3秒以上） |
| 数値テロップ | 大きな数字＋単位。例「約24 m」。数字は Noto Serif JP、単位は小さく |
| 字幕 | 全編に日本語字幕（YouTube字幕ファイル .srt を別途アップロード。焼き込まない） |
| 章タイトル | 中央に細めの明朝体。例「第1章　私たちは、全身を見たことがない」 |

---

## 4. 音楽（BGM）キュー

すべて **YouTube オーディオライブラリ（無料・Content ID の問題なし）** で探せる種類を指定する。品質を上げたい場合は Epidemic Sound で同じキーワードを検索する。

| キュー | 使う場所 | 雰囲気 | 検索キーワード |
|---|---|---|---|
| M1 Abyss | コールドオープン | 低いドローン、サブベース、ほぼ無旋律 | "dark ambient", "drone", "underwater" |
| M2 Wonder | イントロ、第1章 | ピアノと柔らかい弦。好奇心 | "cinematic piano", "documentary", "inspiring calm" |
| M3 Evidence | 第2章（数字の部分） | 控えめなパルス、マリンバかピチカート | "minimal", "science", "pulse" |
| M4 Ancient Seas | 第2章後半〜第3章 | オーケストラのゆっくりした盛り上がり | "epic orchestral slow", "nature documentary" |
| M5 What-if | 第4章 | 低い打楽器とシンセ。緊張感 | "suspense", "tension cinematic", "dark percussion" |
| M6 Ending | 第5章後半〜エンディング | ピアノ独奏から弦へ。郷愁 | "emotional piano", "nostalgic", "reflective" |

- ナレーションの下では BGM を **−20〜−24 LUFS 相当**に下げる（ナレーションは −14 LUFS 前後に合わせる）
- 曲名とライセンスは必ず記録する（`06_production_log` に残す）

## 5. 効果音（SE）
- ElevenLabs Sound Effects で生成するか、YouTube オーディオライブラリの効果音を使う。
- 基本セット: 水中の環境音（低いゴボゴボ音）、泡、ザトウクジラの歌（実録音を使う場合は NOAA の公開音源を確認し、出典を表示する）、遠くのソナー音、低い衝撃音（ブーム）、紙をめくる音（図鑑）、化石を置く音（石）、時計の針の音。
