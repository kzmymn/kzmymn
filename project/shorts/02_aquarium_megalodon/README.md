# Short 02「メガロドンは、水族館で飼育できるのか？」制作指示書（Runway 用）

- 縦9:16、1080×1920、約38秒。ナレーションなし（字幕のみ）
- 字幕は Runway で生成する映像には焼き込まず、編集の段階で入れる
- 字幕は白の太字ゴシック、最大2行・1行12〜14字程度。画面の中央からやや下に置き、右端と最下部（操作表示）を避ける
- 左上に小さくラベル（「仮想シーン／AI生成」「模式図」「イメージ」）を表示する

## 素材
| ID | ファイル | 判定 | 用途 |
|---|---|---|---|
| I1 | images/I1_megalodon_tank.png | 採用 | 冒頭・サムネイル・結論の背景 |
| I2 | images/I2_greatwhite_tank.png | 採用（v2） | ホホジロザメのパート |
| I5 | images/I5_museum_ceiling.png | 採用 | オチ |
| A | diagram_A_newborn.png | 採用（縮尺は正確） | 生まれたてのメガロドンとホホジロザメの比較 |
| B1 | diagram_B1_adult16m.png | 採用（縮尺は正確） | 大人 約16m |
| B2 | diagram_B2_max24m.png | 採用（縮尺は正確） | 最大推定 約24.3m |
| — | images/x_*_unused.png | 不採用 | 理由は下記 |

## タイムライン
| 秒 | 素材 | Runway の動き | 字幕 | ラベル |
|---|---|---|---|---|
| 0.0〜4.0 | I1 | 画像から動画を作る：`slow push-in toward the shark, the shark glides slowly to the left, light ripples on the water surface, visitors stay still, no morphing` | メガロドンは、<br>水族館で飼えるのか？ | 仮想シーン／AI生成 |
| 4.0〜8.5 | I2 | `the shark swims slowly from left to right along the acrylic wall, the visitor stays still, gentle camera drift, no morphing` | 実は、ホホジロザメでさえ<br>難しい。 | 仮想シーン／AI生成 |
| 8.5〜14.0 | I2（拡大） | 動画はそのままで、編集でゆっくり拡大する | 2016年、沖縄で展示された<br>約3.5mのホホジロザメは、 → 3日で死んだ。（文字を切り替える） | 同上 |
| 14.0〜18.5 | I2（暗く） | 静止画をゆっくり拡大する | ホホジロザメは、泳ぎ続けて呼吸する。<br>飼育は極めて難しい。 | 同上 |
| 18.5〜23.5 | A | 動かさない（図をフェードイン） | メガロドンは、生まれた時点で<br>約3.6〜3.9m。 → そのホホジロザメと、<br>ほぼ同じ大きさ。 | 模式図 |
| 23.5〜26.5 | B1 | B1 → B2 へクロスフェード | 大人は、推定16m。 | 模式図 |
| 26.5〜30.0 | B2 | 動かさない | 最大で、約24m。 | 模式図 |
| 30.0〜33.0 | I1（暗く） | 静止画を逆方向にゆっくりズームアウト | 答え：今の技術では、<br>まず不可能。 | 仮想シーン／AI生成 |
| 33.0〜38.0 | I5 | `slow upward tilt toward the hanging shark model, visitors move slightly, warm museum light, the model stays completely still` | ただし1頭だけ、<br>"飼える"メガロドンがいる。 → 埼玉の博物館の、<br>天井に。 | イメージ（実際の展示とは異なります） |

- 最後の0.5秒は黒にフェードアウトする。ロゴを入れる場合は小さく「ロストジャイアント」。
- 映像が冒頭と同じ「巨大なサメ」で終わるので、繰り返し再生されてもつながりが自然になる。

## 科学・事実の確認（2026-10-03 確認済み）
| 字幕 | 根拠 |
|---|---|
| 2016年、沖縄で展示された約3.5mのホホジロザメは、3日で死んだ | 沖縄美ら海水族館の公式発表。2016年1月5日に展示、1月8日に死亡。体長約3.5mのオス。https://oki-churaumi.jp/topics/news160131/ ／ 琉球新報 https://ryukyushimpo.jp/news/entry-200469.html |
| 泳ぎ続けて呼吸する／飼育は極めて難しい | 同上の発表と報道（死因そのものは断定しない。字幕でも死因とは言っていない） |
| 国内最大級の水槽（長さ35m・深さ10m） | 美ら海水族館「黒潮の海」35m×27m×深さ10m、7,500m³ https://churaumi.okinawa/area/the-kuroshio/kuroshio/ |
| 生まれた時点で約3.6〜3.9m | Shimada et al. 2025, *Palaeontologia Electronica* 28(1):a12（推定） |
| 大人は推定16m、最大で約24m | 同上（ベルギーの標本は約16.4m、最大推定は約24.3m） |
| 埼玉の博物館の天井 | 埼玉県立自然の博物館のエントランスに、全長約12mの復元模型が吊るされている https://shizen.spec.ed.jp/ |

- 字幕では水族館の名前を出さず「沖縄で」にとどめる。画像も特定の施設に見えないものを使う。
- 「まず不可能」はチャンネルとしての結論（意見）。

## 不採用・作り直しの理由
- **x_tank_diagram（Gemini の水槽図）**: 水槽の縦横比が約1.6:1。実際の35m×10mは3.5:1なので、数字を載せると嘘の図になる。人の大きさも合っていない。→ 縮尺が正確な図（A／B1／B2）を別に作った。
- **x_diver_newborn（ダイバーとサメ）**: サメが大人のホホジロザメ（8m以上）に見え、「生まれたて約4m」と矛盾する。→ 図 A で代替する。
- **I2 v1（x_greatwhite_tank_v1_unused、水槽のホホジロザメ）**: 来館者に比べてサメが巨大に見え、メガロドンの画像（I1）と区別がつかない。「たった3.5mでも3日しか生きられなかった」という対比が弱まる。

### I2 作り直しに使ったプロンプト（Gemini）→ v2 を採用
```
Vertical 9:16. Inside a large public aquarium, eye-level view along the acrylic wall. A single great white shark about 3.5 meters long swims right next to the acrylic, parallel to it, while an adult visitor stands at the glass in silhouette in the same plane, so the shark is clearly only about twice the visitor's height in length. Blue tank lighting, a few small fish, generic aquarium with no logos or signage, slightly uneasy mood, photorealistic, no text.
```
