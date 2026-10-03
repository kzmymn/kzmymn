# YouTube市場調査 01：恐竜・絶滅巨大生物ジャンル（英語圏 / 日本語圏）

調査日: 2026-10-03
担当: リサーチエージェント（WebSearchベース）

---

## 0. 調査の制約（必ず先に読むこと）

- **このセッションの環境では youtube.com、socialblade、playboard、noxinfluencer、vidIQ、yutura、medium、reddit、wikipedia が egress プロキシで遮断**されていた（WebFetch と curl はどちらも 403 / EGRESS_BLOCKED）。ytInitialData を直接取ることはできなかった。
- データは **WebSearch の検索結果スニペット**（playboard / vidIQ / yutura / youtubers.me / speakrj / tuber-town / digitalcreators などの集計サイトが索引されたもの）だけから取っている。調査の途中でセッション共通の WebSearch 上限（200回）に達したため、個別動画の再生数はほとんど取れていない。
- そのため本レポートでは数値を3種類に分けて書く。
  - **【確認済】** 検索スニペットで数値を確認できたもの（出典URL付き）
  - **【一部確認】** 動画の存在・タイトル・おおよその公開時期は確認できたが、再生数は取れていないもの
  - **【未確認】** 筆者の事前知識による参考情報。必ず実データで検証すること
- 「小規模チャンネルの外れ値（登録者10万未満で再生数が登録者の10倍以上）」は、**数値付きで確認できた例がほぼゼロ**だった。§5 に検証用の候補リストと手順をまとめた。ここは追加調査が必要な最重要項目。

---

## 1. 結論サマリー

1. **英語圏は大型ブランドと中堅のフェイスレス・ドキュメンタリーの二層構造。** PBS Eons、Ben G Thomas（76万人）、Moth Light Media（51万人）、Curious Archive（145万人）などが「科学的に正確な解説」の座をすでに取っている。中でも Moth Light Media は **171本で総再生8,900万＝1本あたり約52万再生**【確認済】で、制作頻度が低くても質の高い長尺ドキュメンタリーが勝てることを示している。
2. **2025〜26年は英語圏で「睡眠用ドキュメンタリー（Documentary for Sleep / To Fall Asleep To）」の古生物版が急増。** "Forgotten Creatures of Prehistoric Earth"、"What Was Earth Like 65 Million Years Ago?"、"What a T-REX Actually Did All Day"、"3 Hours Of Extinct Animals Facts To Fall Asleep To" などが確認できた【一部確認】。一方で AI 量産の "Boring History for Sleep" 系が大量に流入しているという報道があり（Slashdot 2025-09）、反動として **"No AI"（人間が台本と声を担当）を売りにするチャンネルも現れている**（Lights Out Library）。
3. **AI映像の短尺（Veo 3 系）は爆発的。** 2025年7月開設のチャンネルが3ヶ月・20本で6,100万再生（トップは「先史時代の人間が蛇に襲われる」映像）。2026年2月開設の "Hasan Ai 202" は1ヶ月未満・53本で約1,500万再生（POV視点の動物映像）【確認済：二次情報（Medium / vuela.ai の記事）】。ただし中身はスペクタクル型で、科学的な厳密さはない。
4. **日本語圏はゆっくり解説・ずんだもん解説がほぼ独占。** ただし主要チャンネルでも登録者は10〜18万人規模に留まる。成熟した長寿チャンネルには直近の失速を示すデータがある。例えば 生物ロマン【ゆっくり解説】は登録者16.3万人・1,189本だが、**直近15本の平均は約8,740再生**【確認済】。一方、少数精鋭型の 古代生物ちゃんねる は **39本で870万再生（1本平均約22万）**【確認済】。本数より1本の質が効くことを示している。
5. **空白地帯（新チャンネルの機会）**
   - 日本語圏には「映画的な映像 × 学術的な厳密さ × 大人向けナレーション（合成音声ではなく人間の声、または高品質TTS）」の古生物ドキュメンタリーが事実上存在しない。
   - 日本語の「睡眠用古生物ドキュメンタリー」は "【睡眠用・ゆっくり解説】" という形で需要が確認できる【一部確認】。しかしシネマティックな映像で作られた本格的な睡眠用ドキュメンタリーは見当たらない。
   - 英語圏では "AI slop" への反発が強まっている。「AI映像だが論文に基づく・出典を明示・古生物学的に正しい復元」というポジションには差別化の余地がある。

---

## 2. 英語圏：チャンネル規模データ

| チャンネル | 登録者 | 総再生 | 本数 | 1本平均（計算値） | 形式 | 状態 | 出典 |
|---|---|---|---|---|---|---|---|
| PBS Eons | 未確認（数百万規模と推定） | — | — | — | 実写素材＋イラスト、ホスト付き解説 | 最多再生は "Why Megalodon (Definitely) Went Extinct" 670万再生【確認済】 | https://www.speakrj.com/audit/report/eons/youtube |
| Ben G Thomas | 76.3万 | 1億7,935万 | 877 | 約35.5万（集計サイト値） | 顔出しあり、古生物と現生動物、週1本 | 【確認済】 | https://playboard.co/en/channel/UCDSzwZqgtJEnUzacq3ddoOQ |
| Moth Light Media | 50.7万 | 約8,900万 | 171 | **約52万** | フェイスレスの進化・恐竜ドキュメンタリー、英国、2017年開設 | 【確認済】 | https://vidiq.com/youtube-stats/channel/UCOh5Ht3eB4914hMUfJkKa9g/ |
| Curious Archive | 145万 | 1億7,944万 | 133 | 約135万 | 思弁生物学・古生物・神話。フェイスレスのナレーション | 【確認済】 | https://playboard.co/en/channel/UCweDKPSF65wRw5VHFUJYiow |
| Clint's Reptiles | 91.9万 | 1億4,902万 | 592 | 約25万 | 顔出しあり、爬虫類と進化（恐竜含む） | 【確認済】 | https://vidiq.com/youtube-stats/channel/UCH18915fTE6yZzKrqdea8RQ/ |
| melodysheep | 未確認 | — | — | — | "Timelapse of the Future" 5,000万再生超・Webby賞2回【確認済】。宇宙系だが「タイムラプス」形式の参考例 | — | https://www.melodysheep.com/timelapse-of-the-future |
| Prehistoric Documentary | 未確認 | — | — | — | 生命史を通史で扱うドキュメンタリー | 存在のみ確認 | https://www.youtube.com/channel/UCNTKVFbvSi_dT0n4x1SyB1A |
| Prehistoric Tales Hub | 未確認 | — | — | — | AI生成。人類進化と先史生命 | 存在のみ確認 | https://www.youtube.com/channel/UCPRWd8E8nCpphYXvbRxxOvw |

**分類**
- (a) 規模で回っている大型チャンネル：PBS Eons、Curious Archive、Kurzgesagt、BBC Earth、Nat Geo、Bright Side（後ろ3つは今回未計測）
- (b) 中規模だが1本あたりの効率が高いチャンネル：Moth Light Media（1本約52万）、Curious Archive（1本約135万）。どちらも**低頻度・高品質・フェイスレス**型

---

## 3. 英語圏：動画例

### 3-1. 確認できた具体例

| タイトル | チャンネル | 再生数 | 公開時期 | 尺 | 形式・特徴 | 出典 |
|---|---|---|---|---|---|---|
| Why Megalodon (Definitely) Went Extinct | PBS Eons | **670万**【確認済】 | 未確認（2019年前後と推定） | 未確認（10分前後と推定） | 「絶滅の理由」型。"(Definitely)" という言い切りで好奇心を突く | speakrj（上記） |
| 3 Hours Of Extinct Animals Facts To Fall Asleep To | 未確認 | 未確認 | 2024年12月頃（索引時点で約650日前） | 3時間 | 睡眠用・事実の羅列 | https://www.youtube.com/watch?v=jL-Pi233SaE |
| 3 Hours of Mind-Blowing Facts About Prehistory to Help You Fall Asleep | 未確認 | 未確認 | 未確認 | 3時間 | 地球誕生から恐竜までの睡眠用通史 | https://www.youtube.com/watch?v=C__chRHkprA |
| Forgotten Creatures of Prehistoric Earth | 未確認 | 未確認 | 2025年10月頃（約344日前） | 長尺（睡眠用） | 説明文は "a slow and calming journey through a forgotten world — not dinosaurs or mammoths, but stranger beings"。**知名度の低い生物**を前面に出している | https://www.youtube.com/watch?v=ggrWRr3zYlY |
| Forgotten Oceans of Prehistoric Earth | 同系列と推定 | 未確認 | 未確認 | 長尺 | 恐竜以前の海を扱う睡眠用 | https://www.youtube.com/watch?v=4jsNfWBJGFQ |
| Why Prehistoric Oceans Get Creepier the Deeper You Go | 未確認 | 未確認 | 未確認 | 長尺 | 睡眠用 × 「深くなるほど怖い」構造（iceberg 型） | https://www.youtube.com/watch?v=OL6d6z3a6Ic |
| Prehistoric Sea Monsters That Made Megalodon Look Like a Toy | 未確認 | 未確認 | 未確認 | 未確認 | 有名生物（メガロドン）と比べて格上げする型 | https://www.youtube.com/watch?v=W4vXGspyqms |
| The World Before Dinosaurs — The Creatures That Almost Became Us | 未確認 | 未確認 | 未確認 | 未確認 | ペルム紀の単弓類。「私たちの祖先」として自分ごと化 | https://www.youtube.com/watch?v=F7HbIuNRaLk |
| Prehistoric Mystery: What Really Killed the Giant Insects? | 未確認 | 未確認 | 未確認 | 未確認 | 石炭紀の巨大昆虫を謎解き型で扱う | https://www.youtube.com/watch?v=mct97FzIEGs |
| What Was Earth Like 65 Million Years Ago? | 未確認 | 未確認 | 2026年1月頃（約271日前） | 長尺（睡眠用） | 「白亜紀最後の日々へ旅する」二人称の没入型 | https://www.youtube.com/watch?v=pnFZvo8JbDo |
| What a T-REX Actually Did All Day | 未確認 | 未確認 | 2026年8月頃（約53日前） | 未確認 | **「Day in the life」型**。1頭の T. rex の24時間を追う | https://www.youtube.com/watch?v=CPltHN7PYrQ |
| 66 Million Years Ago, Something Survived That Shouldn't Have | 未確認 | 未確認 | 未確認 | 未確認 | ミステリー型のタイトル | https://www.youtube.com/watch?v=Jq4NDY4h7JE |
| We Brought Back a T. Rex. Here's What Happened in the First 24 Hours. | 未確認 | 未確認 | 未確認 | 未確認 | What-if × 24時間の時系列型 | https://www.youtube.com/watch?v=AKhF5W4MQ54 |
| What If the Dinosaurs Never Died — Would They Have Built Cities? | 未確認 | 未確認 | 未確認 | 未確認 | What-if 型（同種タイトルが多数あり、レッドオーシャン） | https://www.youtube.com/watch?v=PzHA3eeU_UU |
| How Dinosaurs Could Have Evolved If They Never Went Extinct | 未確認 | 未確認 | 未確認 | 未確認 | 思弁進化型 | https://www.youtube.com/watch?v=OwSomQ-eSO0 |

### 3-2. AI映像の短尺・外れ値（二次情報）

| チャンネル | 開設 | 実績 | 内容 | 出典 |
|---|---|---|---|---|
| 名称未確認（Medium記事で紹介） | 2025年7月 | **3ヶ月・20本で6,100万再生**。1本は1ヶ月で4,000万再生 | Veo 3 生成。「先史時代の人間 vs 虎や蛇」のサバイバル映像 | https://medium.com/write-a-catalyst/this-3-month-old-ai-channel-got-60-million-views-and-how-anyone-can-do-it-f0c332cfaf81 |
| Hasan Ai 202 | 2026年2月 | 1ヶ月未満・53本で約1,500万再生 | 動物の POV 視点映像 | https://vuela.ai/blog/ai-animal-video-14-million-views-ai-generated |

→ 新規チャンネルでも登録者ゼロから桁違いの再生を取れる「外れ値」の実例。ただしショート・スペクタクル型で、収益化ポリシー（後述）のリスクは高い。

### 3-3. 参考：過去の小規模チャンネルのバイラル例

- The Prehistoric Channel（2015年）：子どもが作る恐竜フィギュア動画。Reddit の r/videos がきっかけで、3日間で**登録者22人→8.8万人**。https://www.tubefilter.com/2015/10/27/the-prehistoric-channel-subscribers-reddit/
  - 示唆：外部コミュニティ（Reddit、X）への露出が小規模チャンネルの起爆剤になる。

---

## 4. 日本語圏

### 4-1. チャンネル規模データ

| チャンネル | 登録者 | 総再生 | 本数 | 1本平均（計算値） | 備考 | 出典 |
|---|---|---|---|---|---|---|
| ゆっくり生物チャンネル【ゆっくり解説】 | 18.1万 | 5,657万 | 816 | 約6.9万 | 2021年開設。30日で約306万再生（時点により変動） | https://yutura.net/channel/60379/ ・ https://us.youtubers.me/2f497a26-8791-43e7-8902-8f2b1a3714c0/youtube-videos-stats |
| 生物ロマン【ゆっくり解説】 | 16.3万 | 7,576万 | 1,189 | 約6.4万 | **直近15本の平均は約8,740再生**、30日で約71万再生。量産型の失速を示す | https://digitalcreators.jp/channel/UCrs0gXDTUAFzlV3IYCSqwpQ/ |
| 進化生物学ch【ゆっくり解説】 | 11.5万 | 1,674万 | 122 | 約13.7万 | 学術寄り。「生命の歴史」シリーズ | https://yutura.net/channel/54089/ |
| 【ゆっくり解説】古代生物ちゃんねる | 10.5〜11.2万 | 870万 | **39** | **約22.3万** | 少数精鋭。2020年2月開設 | https://www.youtube.com/@kodaiseibutuch |
| ずんだもん生物解説 / 生物ずんだもん / 動物ずんだもん | 未確認 | — | — | — | ずんだもん（VOICEVOX）系が並立していることを確認 | https://www.youtube.com/channel/UCDKewf4yaD4TqaW2WDtqWZQ |
| 福井県立恐竜博物館（公式） | 未確認 | — | — | — | 公的機関 | https://www.youtube.com/user/FukuiDinosaurs |
| 恐竜チャンネル / ティラノがやってくる！ / ティラノサウルス牧場 | 未確認 | — | — | — | **子ども向け**が多い | 検索結果 |

### 4-2. 日本語圏の動画例

| タイトル | チャンネル | 再生数 | 公開日 | 備考 | 出典 |
|---|---|---|---|---|---|
| 古代生物の絶滅理由まとめ（総集編） | ゆっくり生物チャンネル | **111万**【確認済】 | 2023-07-22 | 「絶滅理由」×総集編（長尺） | yutura（上記） |
| 生物進化の謎まとめ（総集編） | ゆっくり生物チャンネル | **163万**【確認済】 | 未確認 | 総集編の長尺 | yutura |
| 【ゆっくり解説】ミトコンドリアと真核生物の起源：生物進化最大のミッシングリンク【生命の歴史⑥】 | 進化生物学ch | **58万**【確認済】 | 未確認 | 学術的テーマでも伸びている | yutura |
| 【ゆっくり解説】死滅回遊魚の正体 | 進化生物学ch | 102万【確認済】 | 未確認 | 古生物ではないが同チャンネルの最多 | yutura |
| 【睡眠用・ゆっくり解説】様々な古生物Part7 カルノタウルス/パキケファロサウルス/カンブロパキコーペ など【途中広告なし】 | 未確認 | 未確認 | 未確認 | **日本語の睡眠用古生物の需要がある証拠**。「途中広告なし」を明記 | https://www.youtube.com/watch?v=hBKKWzHLOc4 |
| 【ゆっくり解説】恐竜研究が激変中！最新発表で覆った"４つの常識"とは？【新作＋傑作選３本】 | 未確認 | 未確認 | 未確認 | 「新作＋傑作選」で尺を水増しする型 | https://www.youtube.com/watch?v=NSj3kTnDWHw |
| 【ゆっくり解説】まさかの弱体化！？新説で評価が変わった古代生物６選 | 未確認 | 未確認 | 未確認 | 「新説で常識が覆る」×ランキング | https://www.youtube.com/watch?v=gefyVhxgIh4 |
| 【ゆっくり解説】最新の科学で判明…想像していたのと違っていた「古代生物」7選 | 古代生物ちゃんねる | 未確認 | 未確認 | 同上 | https://www.youtube.com/watch?v=sZ3A-QhRZV8 |
| 【ゆっくり解説】謎生物ハルキゲニアの最新情報！ついに食事が判明！ | 未確認 | 未確認 | 未確認 | 最新論文をフックにしている | https://www.youtube.com/watch?v=geflO6CYdwU |
| 古代生物水族館｜AIが蘇らせた太古の海の記憶 Ancient Creature Aquarium | 未確認 | 未確認 | 未確認 | **日本語のAI映像古生物の先行例** | https://www.youtube.com/watch?v=1IdiwA-Y_HA |
| 「間違いなくティラノサウルスだった」アフリカで目撃された恐竜型UMA【総集編】 | 生物ロマン | 未確認 | 未確認 | 恐竜 × UMA のクロスオーバー | https://www.youtube.com/watch?v=iir81JUseF0 |

### 4-3. 日本語圏の特徴【一部確認＋分析】

- **ゆっくり・ずんだもん系が主流**であることを確認した。上位の古生物・生物チャンネルはすべて合成音声＋静止画やイラストの構成。
- タイトルの定番：【ゆっくり解説】の接頭辞、「〇選」、「最新の科学で判明」、「まさかの」「ヤバい」、「総集編」「傑作選」、【睡眠用】【途中広告なし】。
- 登録者の天井は低め（10〜20万）。英語圏との差は約5倍。市場規模の差に加え、ゆっくり形式そのものが視聴者層を限定している可能性がある。
- 量産型は失速が見える（生物ロマン：直近平均 8,740再生）。少数精鋭型は1本あたりの効率が高い（古代生物ちゃんねる：39本で平均22万）。
- 子ども向け（恐竜フィギュア、アニメ）の恐竜チャンネルは別市場。**大人向けのシネマティックな古生物ドキュメンタリーは日本語でほぼ空白**（ただし網羅的には未検証）。

---

## 5. 小規模チャンネルの外れ値：検証用の候補と手順（追加調査が必要）

今回の環境では、登録者10万未満で10倍以上の再生がある具体例を数値で確認できなかった。以下は検証すべき候補。

**候補（存在は確認済み、数値は未確認）**
1. "What a T-REX Actually Did All Day"（2026年8月公開）：新しい Day-in-the-life 型。チャンネル規模を確認する
2. "Forgotten Creatures of Prehistoric Earth" / "Forgotten Oceans of Prehistoric Earth"：睡眠用の新興チャンネルの可能性
3. "What Was Earth Like 65 Million Years Ago?"：睡眠用
4. "Why Prehistoric Oceans Get Creepier the Deeper You Go"
5. "Prehistoric Sea Monsters That Made Megalodon Look Like a Toy"
6. "We Brought Back a T. Rex. Here's What Happened in the First 24 Hours."
7. 古代生物水族館（AI、日本語）
8. 【睡眠用・ゆっくり解説】様々な古生物 シリーズ

**検証手順（youtube.com にアクセスできる環境で実施）**
- vidIQ の Outliers、1of10.com、viewstats.com で「dinosaur / prehistoric / extinct / megafauna / for sleep」を検索する。条件は「登録者 < 100k、views / subs ≥ 10」。
- YouTube 検索で、フィルタ「今年」「20分以上」「再生回数順」をかける。キーワードは "documentary for sleep prehistoric"、"before dinosaurs"、"ice age megafauna documentary"、「古生物 睡眠用」「絶滅動物 総集編」。

**【未確認】事前知識に基づく参考（要検証）**
- 英語の睡眠用ドキュメンタリーは、"Sleepless Historian"、"Boring History for Sleep"、"Bedtime Stories" 系が2024〜25年に急成長した（主に歴史ジャンル）。古生物版はまだ供給が少ないと推定。
- Kurzgesagt の恐竜関連動画（例："What if dinosaurs..."）は1本で数千万再生級だが、(a) 規模型の典型。
- Ice Age・メガファウナ系は恐竜系より供給が少ない。テラーバード、パラケラテリウム、アースロプレウラなど「知名度は中程度で見た目のインパクトが大きい」生物が外れ値になりやすい傾向がある（推定）。

---

## 6. パターン分析

### 6-1. タイトルの型（英語圏）

| 型 | 例 | 効く理由 |
|---|---|---|
| 睡眠用・長尺 | "3 Hours of … To Fall Asleep To"、"… (Documentary for Sleep)" | 総再生時間が極端に長い。夜に定期的に再生される |
| 忘れられた・知られざる | "Forgotten Creatures of…"、"Creatures That Almost Became Us" | 恐竜疲れした層を取り込む。新奇性 |
| 有名生物と比べる | "…Made Megalodon Look Like a Toy" | 既存の検索需要に乗れる |
| Actually / Really | "What a T-REX Actually Did All Day" | 映画のイメージを覆す。大人向けの知的好奇心 |
| 一日・24時間 | "Day in the life"、"First 24 Hours" | 物語の骨格が自動的にできる。没入感 |
| What-if | "What If Dinosaurs Never Went Extinct" | 供給過多でレッドオーシャン |
| 深くなるほど | "…Get Creepier the Deeper You Go" | iceberg 型で離脱を防ぐ |
| 断定・謎 | "Why Megalodon (Definitely) Went Extinct"、"Something Survived That Shouldn't Have" | 答えを知りたい欲求を刺激する |

### 6-2. タイトルの型（日本語圏）

【ゆっくり解説】＋「〇選」＋「最新研究で判明」＋煽り（ヤバい／まさか）＋【総集編】【睡眠用】【途中広告なし】

### 6-3. サムネイル（【未確認】一般的傾向。実物は未取得）

- 英語の大型・中堅：CG や復元画1体の大写し＋人間や現生動物とのサイズ比較＋短い文字（2〜4語）。暗い背景に生物を浮かび上がらせる。
- 睡眠用：暗く落ち着いた色調、風景が主役で、文字は少ないか無し。
- 日本語ゆっくり系：キャラ立ち絵＋生物画像＋大きな縁取り文字。赤と黄色が多い。

### 6-4. 冒頭フック（推定。文字起こしは未取得）

- 睡眠用は「Tonight, we travel back…」のような二人称で穏やかに誘導する（説明文の文体から推定）。
- 解説型は「常識の否定」（"Everything you know about T. rex is wrong"）、「スケール提示」（全長、体重、人間との比較）、「謎の提示」（なぜ絶滅したのか）。

### 6-5. 尺

- 解説型：10〜25分
- 睡眠用：1.5〜3時間以上（"3 Hours" が定番）
- 日本語の総集編：30分〜2時間
- AI短尺：ショート（60秒以内）

### 6-6. 競合の強さ

| 領域 | 競合の強さ | コメント |
|---|---|---|
| 英語・恐竜一般解説 | 非常に強い | PBS Eons、Ben G Thomas、Kurzgesagt、BBC など |
| 英語・What-if 恐竜 | 非常に強い（供給過多） | 同じタイトルが乱立 |
| 英語・睡眠用古生物 | 中（急増中） | AI 量産が流入。品質で差別化できる余地あり |
| 英語・AI短尺スペクタクル | 強い（参入容易・量産） | ポリシーリスクが高い |
| 日本語・ゆっくり古生物 | 中〜強（ただし失速傾向） | 天井は20万人程度 |
| 日本語・シネマティック大人向け古生物 | **弱い（ほぼ空白）** | 最大の機会 |
| 日本語・睡眠用古生物（映像重視） | **弱い** | ゆっくり睡眠用のみ |

---

## 7. リスク

- **YouTube パートナープログラムの「inauthentic content（旧 repetitious content）」ポリシー**（2025年7月更新）【未確認：事前知識】。AI量産・テンプレ量産は収益化を剥奪されるリスクがある。対策：台本のオリジナリティ、出典の明示、人間による編集・ナレーション、シリーズとしての一貫した作家性。
- AI slop への視聴者の反発（Slashdot 2025-09 報道、"No AI" を売りにする競合の出現）。https://news.slashdot.org/story/25/09/03/2028206/ai-generated-boring-history-videos-are-flooding-youtube-drowning-out-real-history
- 古生物ファン層は復元の正確さに厳しい（羽毛、唇、姿勢など）。AIは不正確な復元をしやすく、炎上要因になる。

---

## 8. 新チャンネル（シネマティック・学術厳密・AI映像・大人向け）の機会

1. **日本語の「映画的な古生物ドキュメンタリー」で先行者になる。** ゆっくり形式に飽きた大人層と、NHKスペシャルや Prehistoric Planet を好む層を取り込む。
2. **睡眠用の長尺（1〜3時間）を主力にし、通常尺（15〜25分）でフックを作る二段構え。** 長尺は総再生時間と RPM の点で有利。日本語では「途中広告なし」「穏やかなナレーション」が刺さることを確認した。
3. **英語圏は「知られざる生物」と「Actually」型で攻める。** 恐竜一般や What-if は避け、ペルム紀の単弓類、石炭紀の巨大節足動物、カンブリア紀、新生代のメガファウナ（テラーバード、パラケラテリウム、ティタノボア、ダンクルオステウス）に特化する。
4. **Day-in-the-life ＋ 科学的注釈。** 1個体の一日を物語として描き、画面上で「論文ベース／推定」を区別して表示する。「Scientifically accurate AI」というポジションを取る。
5. **出典リストを概要欄に置き、"Paleoart reviewed" を打ち出す。** 反AI感情への対策であり、権威性にもなる。
6. **外れ値の起爆剤**：最新の論文ニュース（新種発表など）に1週間以内に反応する動画。Reddit の r/Paleontology や X の古生物クラスタへの露出。
7. **JP/EN の同時展開**：同じ映像素材を使い、ナレーションだけを差し替える。日本語は空白市場、英語は大きな市場、という役割分担。

---

## 9. 出典一覧

- PBS Eons 統計：https://www.speakrj.com/audit/report/eons/youtube
- Ben G Thomas：https://playboard.co/en/channel/UCDSzwZqgtJEnUzacq3ddoOQ
- Moth Light Media：https://vidiq.com/youtube-stats/channel/UCOh5Ht3eB4914hMUfJkKa9g/
- Curious Archive：https://playboard.co/en/channel/UCweDKPSF65wRw5VHFUJYiow
- Clint's Reptiles：https://vidiq.com/youtube-stats/channel/UCH18915fTE6yZzKrqdea8RQ/
- melodysheep：https://www.melodysheep.com/timelapse-of-the-future
- AI チャンネル 6,100万再生：https://medium.com/write-a-catalyst/this-3-month-old-ai-channel-got-60-million-views-and-how-anyone-can-do-it-f0c332cfaf81
- Hasan Ai 202：https://vuela.ai/blog/ai-animal-video-14-million-views-ai-generated
- AI Boring History の流入：https://news.slashdot.org/story/25/09/03/2028206/ai-generated-boring-history-videos-are-flooding-youtube-drowning-out-real-history
- Lights Out Library（No AI）：https://open.spotify.com/episode/6MOl51zDb3CximhHI7g2Po
- The Prehistoric Channel：https://www.tubefilter.com/2015/10/27/the-prehistoric-channel-subscribers-reddit/
- ゆっくり生物チャンネル：https://yutura.net/channel/60379/popular/ ・ https://us.youtubers.me/2f497a26-8791-43e7-8902-8f2b1a3714c0/youtube-videos-stats
- 進化生物学ch：https://yutura.net/channel/54089/popular/
- 生物ロマン：https://digitalcreators.jp/channel/UCrs0gXDTUAFzlV3IYCSqwpQ/
- 古代生物ちゃんねる：https://www.youtube.com/@kodaiseibutuch
- 各動画URLは本文の表を参照
