# ジャンル調査 (2) メガロドン・サメ / (3) 深海 — YouTube市場リサーチ

調査日: 2026-10-03
担当: リサーチサブエージェント

---

## 0. 調査の制約(最初に読んでください)

この調査は**データの取得に大きな制約があった**ため、数字の網羅性は低いです。

- この環境のネットワーク方針で、`youtube.com` / `m.youtube.com`、socialblade、playboard、noxinfluencer、vidiq、hypeauditor、speakrj、viewstats、outlierkit、similarchannels、yutura、reddit、wikipedia、web.archive.org、invidious、r.jina.ai、ladbible、unilad が **WebFetch でも curl でもすべてブロック**されました(egress proxy から 403)。そのため ytInitialData の取得はできていません。
- 使えたのは WebSearch の検索結果スニペットだけです。その WebSearch もセッション全体の上限(200回)に途中で達し、**日本語の検索はほとんどできていません**。
- 以下の表では次のように区別しています。
  - **確認済み**: 検索スニペットや報道記事に数字が出ていたもの(出典URLあり)
  - **未確認**: 動画の存在とタイトルは確認できたが、再生数・登録者数・公開日などは取れなかったもの
  - **推論**: 筆者の分析・仮説。データではありません
- 依頼の重点だった「(b) 登録者2万人未満の小規模チャンネルによる外れ値」は、**数字の裏付けが取れた事例は見つかりませんでした**。これは「存在しない」という意味ではありません。調べられなかった、という意味です。次の段階で、YouTubeを直接見られる環境(人の手による閲覧、または YouTube Data API キー)で §8 の手順に沿って再調査してください。

---

## 1. 確認済みの数字(ファクトシート)

| # | 対象 | 種別 | 数字 | 時点/出典 |
|---|---|---|---|---|
| F1 | Discovery「Megalodon: The Monster Shark Lives」(2013、Shark Week) | 大手TV(偽ドキュメンタリー) | TV視聴者 **480万人**。当時のShark Week史上最多。事後のオンライン投票で **73%** が「メガロドンは今も生きている」と信じたと報じられた | https://en.wikipedia.org/wiki/Megalodon:_The_Monster_Shark_Lives / https://www.realclearscience.com/lists/top_junk_science_of_2013/megalodon_mermaids.html |
| F2 | 同番組の YouTube 再アップ版「Megalodon: The Shark Lives」 | 再アップ | **700万回超**。2025年1月に「また拡散している」と報道 | https://www.ladbible.com/news/animals/megalodon-do-they-still-exist-discovery-channel-934332-20250120 |
| F3 | 2014「Megalodon: The New Evidence」→ 2015年にDiscovery社長 Rich Ross が「フェイク番組をやめる」と約束 | 業界の文脈 | — | https://www.foxnews.com/entertainment/discovery-channel-defends-its-decision-to-air-dramatized-megalodon.amp / https://www.npr.org/2014/08/30/344562317/when-wildlife-documentaries-jump-the-shark / https://www.southernfriedscience.com/we-were-wrong-about-megalodon-lessons-learned-from-10-years-combating-fake-science-in-popular-media/ |
| F4 | MetaBallStudios(Alvaro Gracia Montoya) | 大手(3D比較アニメ) | 登録者 **約196.5万人**(2026年9月時点のスニペット) | https://hypeauditor.com/youtube/UCQwFuQLnLocj5F7ZcmcuWYQ/ |
| F5 | MetaBallStudios「⚓ SHIPWRECKS Depth Comparison ⚓ (3D)」 | 大手 | **15,966,037回**。2021年公開 | https://www.youtube.com/watch?v=aGPiQ47ahsE |
| F6 | MetaBallStudios「Ocean DEPTH Comparison 🌊 (3D Animation)」 | 大手 | 再生数は**未確認**。ただし公開から数年たっても、2024年2月(UNILAD Tech)、2025年1月(UNILAD)、2025年3月(LADbible)と**何度もバイラル記事になっている**。メディアが繰り返し取り上げる、寿命の長い動画 | https://www.uniladtech.com/science/news/youtube-video-showing-scale-of-ocean-763752-20240228 / https://www.ladbible.com/entertainment/youtube/how-deep-sea-is-3d-animation-metaballstudios-189318-20250314 / https://www.unilad.com/news/us-news/video-shows-how-deep-ocean-is-giving-anxiety-838726-20250110 / https://nerdist.com/article/how-deep-oceans-go-ocean-depth-comparison-video-metaball-studios/ |
| F7 | **AiTelly「Titan潜水艇の圧壊」3Dアニメ**(2023年6〜7月) | **中規模チャンネルの外れ値** | 投稿時の登録者 **26.7万人** → **13日で約1,000万回**(12日時点で600万回)。3人チームが Blender で**約12時間**で制作。公開情報(OceanGateのサイトなど)から寸法を割り出した | https://www.unilad.com/news/world-news/titan-sub-implosion-animation-video-viral-949148-20230713 / https://www.dailyo.in/news/titanic-submersible-implosion-3d-animation-is-now-a-viral-video-with-10-million-views-40593 / https://www.newsweek.com/titan-sub-implosion-animation-viewed-5-million-times-1812486 / https://www.boston25news.com/news/trending/animation-explaining-titan-subs-implosion-has-more-than-6-million-views/642IZGJAWBF6BNAMHNB6WUIMYI/ |
| F8 | Neal Agarwal「The Deep Sea」(neal.fun、2019年12月) | YouTube外(下にスクロールして潜る体験型サイト) | 数日で100万、短期間で300万ビュー超 | https://www.cbc.ca/news/canada/windsor/deep-sea-interactive-uwindsor-researcher-1.5396328 / https://x.com/nealagarwal/status/1203725171531669504 |
| F9 | Kurzgesagt「What's Hiding at the Most Solitary Place on Earth? The Deep Sea」 | 大手 | 公開日 **2019-09-15**。再生数は**未確認**(同動画への「リアクション動画」が作られるほど定番化している) | https://www.imdb.com/title/tt10960198/ / https://www.youtube.com/watch?v=lHo531H8FTE |
| F10 | Zack D. Films | 大手(3D Shorts) | 登録者 **2,860万人**、総再生 **約774億回**、1億回超のShortsが23本(fandomスニペット、時点不明) | https://zackdfilms.fandom.com/wiki/Zack_D._Films |
| F11 | The Infographics Show | 大手 | 1本あたり平均 **約110万回**、直近30日で3,779万回(vidiqスニペット、時点不明)。「MEGALODON vs MODERN DAY SHARK」という動画がある | https://vidiq.com/youtube-stats/channel/@theinfographicsshow/ / https://www.facebook.com/TheInfographicsShow/videos/megalodon-vs-modern-day-shark-how-do-they-actually-compare/1160149861126441/ |
| F12 | Bedtime Stories(実話怪談・未解決ミステリー、Richard While) | 大手 | 2024-12-27 に登録者100万人を達成。海の怪物回(メガロドン・モササウルスに言及)あり | https://youtube.fandom.com/wiki/Bedtime_Stories |
| F13 | 「メガロドンがオーストラリアの島に打ち上げられた」AI生成動画(2025年) | AIフェイクのバイラル | TikTok / Instagram / X で拡散し、ファクトチェック機関が「AI生成」と判定 | https://srilanka.factcrescendo.com/english/viral-video-of-megalodon-on-an-australian-island-is-ai-generated/ / https://www.latestly.com/social-viral/fact-check/was-a-megalodon-found-on-australia-beach-fact-check-reveals-ai-generated-clip-going-viral-with-netizens-believing-it-to-be-true-7013820.html |
| F14 | CGIアーティスト Aleksey(@aleksey__n)の「現代のメガロドンが船やヘリを襲う」CG | 個人CG作家 | TikTokで大手アカウントが転載して拡散(再生数は未確認) | https://www.tiktok.com/@slash/video/7213973681343679787 |

---

## 2. 英語圏: 主要動画とフォーマット別の整理

### 2-1. (a) 大手チャンネル主導のヒット

| タイトル | チャンネル | 登録者 | 再生数 | 公開 | 尺 | フォーマット/勝因(推論) |
|---|---|---|---|---|---|---|
| ⚓ SHIPWRECKS Depth Comparison ⚓ (3D) | MetaBallStudios | 約196.5万 | **1,597万** | 2021 | 未確認 | 「知っている物(自由の女神・エッフェル塔・タイタニック)」と並べて深さを比べ続ける。ナレーションなし・BGMだけなので言語の壁がない。「どこまで行くのか」が気になって最後まで見てしまう |
| Ocean DEPTH Comparison 🌊 (3D Animation) | MetaBallStudios | 同上 | 未確認(数千万規模と推定、**未確認**) | 未確認 | 未確認 | アゾフ海(水深約7m)から始め、40地点以上を経てチャレンジャー海淵(約10,900m)で終わる。浅い所から始めて深くなる一方向の構成。報道で何度も再燃する(F6) |
| The Deep Sea | Kurzgesagt | 2,400万超(Wikipediaスニペット。時点未確認) | 未確認 | 2019-09-15 | 未確認(約9分と記憶、**未確認**) | 海面からチャレンジャー海淵まで1本の縦スクロールで降りる。「最も孤独な場所」という情緒的なフレーミング |
| MEGALODON vs MODERN DAY SHARK | The Infographics Show | 未確認 | 未確認 | 未確認 | 未確認 | 比較もの。チャンネル平均は約110万回/本 |
| What If Megalodon Sharks Never Went Extinct? | What If(Underknown) | 未確認 | 未確認 | 未確認 | 未確認 | 「もしも」ものの元祖格 https://www.youtube.com/watch?v=-ajB0KahjkA / https://whatifshow.com/what-if-megalodon-sharks-never-went-extinct/ |
| Megalodon Shorts 各種 | Zack D. Films | 2,860万 | 未確認 | — | <60秒 | 3DCGの短いショッカー(「もし〜したら」型)。巨大チャンネルの Shorts 量産ライン |
| Megalodon: The Shark Lives(再アップ) | 第三者による再アップ | 未確認 | **700万+** | 元は2013年放送 | 約1.5時間(**未確認**) | 「本物の映像に見える」偽ドキュメンタリー。真偽をめぐる論争そのものがクリックを生む |

### 2-2. (b) 外れ値候補(登録者に比べて再生が突出)

| タイトル | チャンネル | 登録者(当時) | 再生数 | 倍率 | 備考 |
|---|---|---|---|---|---|
| Titan sub implosion 3D animation | **AiTelly** | 26.7万 | 13日で約1,000万 | **約37倍(13日時点)** | **確認済みの唯一の強い外れ値**。条件は ①ニュースの直後 ②「何が起きたのか」を3Dで具体的に見せる ③低コスト(12時間、Blender)。登録者10万未満という条件には当てはまらないが、フォーマットの再現性が高い |
| 小規模チャンネル(<2万)のメガロドン/深海外れ値 | — | — | — | — | **未確認**。動画の存在は多数確認できたが(下記)、登録者数・再生数が取れず、外れ値かどうか判定できなかった |

### 2-3. 直近1〜2年に投稿が集中しているメガロドン長尺(飽和の証拠)

検索スニペットの「○日前」表記から並べると、**メガロドンのドキュメンタリー/解説の長尺が、ここ1年で少なくとも7本以上、似たタイトルで投稿されています**。再生数はすべて未確認です。

| タイトル | URL | 検索時点での経過 |
|---|---|---|
| Megalodon: We Were Wrong About Earth's Greatest Ocean Predator \| Full Documentary | https://www.youtube.com/watch?v=frr9AdZXrJc | 36日前 |
| MEGALODON: Life and Fall / The Full Story of the Ocean's Greatest Predator | https://www.youtube.com/watch?v=DIzTRT9wK8U | 145日前 |
| We Were Completely WRONG About Megalodon | https://www.youtube.com/watch?v=fC4LtXFAa1M | 169日前 |
| MEGALODON: The Ocean's Greatest Predator | https://www.youtube.com/watch?v=RlMQEL3NyQU | 231日前 |
| MEGALODON: The Apex Predator Of the Ocean | https://www.youtube.com/watch?v=q4-i6ke8Un0 | 271日前 |
| We Were Wrong About Megalodon | https://www.youtube.com/watch?v=7FUbwlfSIWQ | 284日前 |
| Ocean's Deadliest Predator Returns | https://www.youtube.com/watch?v=SVgld8pTnv0 | 624日前 |
| Megalodon Was Even Bigger Than We Feared - And the Ocean Still Hides Giants | https://www.youtube.com/watch?v=n9hkzVbYo4M | 未確認 |
| What If The Megalodon Never Stopped Evolving? | https://www.youtube.com/watch?v=5DR2Q2TzHbg | 未確認 |
| Why People Still Think Megalodon Survived | https://www.youtube.com/watch?v=MRND0U3yZOs | 未確認 |
| Megalodon As You Know It Never Existed, Experts Say | https://www.youtube.com/watch?v=wZ_KPAe58uE | 未確認 |
| What If the Megalodon Shark Never Went Extinct? | https://www.youtube.com/watch?v=7MC2rhedZAc | 未確認 |
| What If Megalodon Sharks Didn't Go Extinct? | https://www.youtube.com/watch?v=H3Un_gx2fqU | 未確認 |
| Megalodon Documentary - King of the Seas (Full Documentary) | https://www.youtube.com/watch?v=k_XJ1cUiCDk | 未確認 |
| Finding Megalodon - Prehistoric Nature Documentary(CG、1年以上かけて制作) | https://www.youtube.com/watch?v=YOTdsaWbfB8 / https://tidewaterteddy.com/2021/11/05/finding-megalodon-new-prehistoric-life-documentary/ | 2021年 |

サイズ比較(3D)系も多数あります。
- 「Unbelievable 3D Shark Species Weight And Size Comparison」(約1,115日前)https://www.youtube.com/watch?v=KITo_Sww3_o
- 「Sea Monsters 3D Size Comparison: Bloop vs Megalodon」(約750日前)https://www.youtube.com/watch?v=mMq8aubbBfU
- 「Megalodon vs. Human: Mind-Blowing Size Comparison」(約425日前)https://www.youtube.com/watch?v=DiBQwCg4Iiw
- Shorts「Megalodon Size Comparison 🤯」(約592日前)https://www.youtube.com/shorts/fnsdE-beKtk
- 「3D Sea Monsters Size Comparison」https://www.youtube.com/watch?v=ehLoBMni0pE

**推論**: 「We Were (Completely) Wrong About Megalodon」という型だけで、確認できた範囲で4本以上あります。もともとは「最新研究で常識がひっくり返る」という切り口ですが、それ自体がテンプレ化しています。WatchMojoも記事化しており(https://www.watchmojo.com/articles/what-if-megalodon-sharks-didn-t-go-extinct)、「What if megalodon still existed」は**英語圏では明らかに飽和**しています。

### 2-4. 深海(英語)の主要トピック

| トピック | 確認できた動画例 | 所見(推論) |
|---|---|---|
| マリアナ海溝 | 「What Exists in the Deepest Place on Earth?」https://www.youtube.com/watch?v=aDAcZCHbVcM 、「The Deepest Dive Humanly Possible」https://www.youtube.com/watch?v=w9k7_wCUq_4 、「New Footage From the Mariana Trench Shows Something That Shouldn't Exist」https://www.youtube.com/watch?v=JV0l6rHmWvA 、「They found something terrible at the bottom of Mariana Trench」https://www.youtube.com/watch?v=Jjy7iXZZOP8 、「Scientists Explored the Mariana Trench—What They Found Is More Terrifying Than Space!」https://www.youtube.com/watch?v=zYwiYcDQ49E 、BBC「Record-breaking journey to the bottom of the ocean」https://www.youtube.com/watch?v=LKXvdyNz6L8 、Shorts「Real-Life Mermaid Recorded by Divers in Mariana Trench」https://www.youtube.com/shorts/2n_kBM4hAjI | 釣りタイトル(「あってはならないもの」「宇宙より恐ろしい」)や捏造系のShortsが多い。**誠実さそのものが差別化になる** |
| Bloop | 「The Bloop: Solving the Ocean's Greatest Mystery」https://www.youtube.com/watch?v=4OCMnrz9ia4 、「What Made This Sound in the Ocean?」https://www.youtube.com/watch?v=wnYjSkVLzlg 、found footage系「The Bloop 2024」https://www.youtube.com/watch?v=sU3UFQWv82c | NOAAが「氷山が割れる音(icequake)」と結論済みであることを最後に明かす型が定番。found footage(フィクション)も混在 |
| Titan潜水艇 | AiTelly(F7) | ニュースが出た直後の72時間に、3Dで「何が起きたか」を出す。賞味期限は短いが、爆発力は最大 |
| 深さスケール | MetaBallStudios(F5、F6)、neal.fun(F8)、Kurzgesagt(F9) | 「下へ下へ」という一方向の構成は、離脱しにくい最強の型。すでに複数の大手が持っている |

---

## 3. 日本語圏: 確認できた動画

再生数・登録者はすべて**未確認**です(日本語の検索は1回しかできず、その後に上限に達したため)。

| タイトル | URL | 型 |
|---|---|---|
| もし、メガロドンが今でも存在していたら？ | https://www.youtube.com/watch?v=PV_MW5I1niY | 「もしも」型(英語動画の吹き替え・翻訳版の可能性あり、**未確認**) |
| 【ゆっくり解説】メガロドンも生きていた？！その証拠の数々とは？！ | https://www.youtube.com/watch?v=7rKpv7uws10 | ゆっくり解説 × 生存説 |
| 【生存説】メガロドンはまだ生きてる！？古代の巨大ザメが絶滅してない10の証拠 | https://www.youtube.com/watch?v=XFAygQA8kTc | 【】タグ × 数字リスト × 生存説 |
| メガロドン絶滅は嘘だった？超巨大ザメの生存説を徹底解説！【古代ザメ】【MEG】 | https://www.youtube.com/watch?v=67iqqMMq1jU (関連ブログ https://www.board-gill.com/megalodon_still_alive_or_not/ ) | 疑問形 × 徹底解説 × 映画MEGのキーワード |
| 【リマスタ総集編】メガロドンの真実｜巨大化・生存説・最新研究で迫る最強捕食者 | https://www.youtube.com/watch?v=DXdrM3Ufd4k | 総集編・リマスタ(長尺の再編集) |

**日本語圏のタイトルの傾向(推論)**
- 「生存説」「〜は嘘だった？」「〜の真実」「徹底解説」が中心です。「もしも(What if)」型よりも、**「生きているかもしれない」というミステリー寄りの切り口**が多くなっています。
- 【ゆっくり解説】【】タグ、数字リスト(10の証拠)、映画『MEG ザ・モンスター』への便乗が目立ちます。
- 高品質なシネマティックCGやAI映像で作る大人向けの日本語ドキュメンタリーは、検索した範囲では**目立っていません**(ただし網羅的な検索はできていないため**未確認**)。

---

## 4. パターン分析(推論。上記データと一般的な知見にもとづく)

### 4-1. タイトルのパターン

| 型 | 英語の例 | 日本語の例 | 飽和度 |
|---|---|---|---|
| もしも型 | What If Megalodon Never Went Extinct? | もしメガロドンが今も存在していたら？ | **英語は飽和**、日本語は中程度 |
| 常識が覆る型 | We Were (Completely) Wrong About Megalodon | 〜は嘘だった？ | 英語ではすでにテンプレ化 |
| 最新研究型 | Megalodon Was Even Bigger Than We Feared | 最新研究で迫る | 中程度。研究ニュースに連動するため、タイミングが大事 |
| 生存説・ミステリー型 | Why People Still Think Megalodon Survived | 生存説、10の証拠 | 日本語で特に強い |
| 比較型 | Megalodon vs Human / Bloop vs Megalodon | 〜vs〜 | Shorts・3Dで飽和 |
| スケール・深さ型 | Ocean DEPTH Comparison | 深さ比較 | 大手の定番。後発は差別化が必要 |
| 事件再現型 | Titan sub implosion animation | — | ニュースが出たときだけ爆発する |

### 4-2. サムネイルのパターン(推論。画像は確認できていない)
- 巨大なメガロドンと小さな人間・船・ダイバーを並べた「スケール対比」
- 暗い青から黒へのグラデーション、深淵、発光生物
- 赤い矢印・赤丸、「???」
- 深さのものなら縦のスケールバーや数字(10,935m)
- **日本語版は文字量が多く**、黄色・白の太字ふち取り文字が一般的(ゆっくり系の慣習)

### 4-3. 冒頭の作り方(推論)
- **Discovery型**: 「本物らしく見える映像」で冒頭から「これは本当なのか？」と思わせる。倫理的な問題が大きい。
- **MetaBall型**: ナレーションなしで、最初の1カット目からすぐに始める。
- **Kurzgesagt型**: 「ここは地球で最も孤独な場所」という感情の掴み。
- **What If型**: 「1隻の漁船のソナーに、15mの影が映った」のような再現ドラマから入り、すぐに「ではどうなるか」へつなげる。
- **AiTelly型**: 「何が起きたのか、1秒ずつ見ていく」。

### 4-4. 尺(推論)
- 深さスケールのもの: 5〜12分
- What If型: 8〜15分
- フルドキュメンタリー: 30分〜1時間超。睡眠用は2〜3時間(睡眠用ドキュメンタリーの具体的な実績は**未確認**)
- Shorts: 30〜60秒

---

## 5. 科学的な前提(制作上の注意。筆者の訓練知識によるもので、一次文献で要確認)

- メガロドン(Otodus megalodon)の絶滅は約360万年前とされる(Boessenecker et al. 2019)。ファクトチェック記事でも同じ数字が使われている(F13の出典)。
- 2024年の研究(Sternes, Shimada ら、Palaeontologia Electronica)で、「ホホジロザメを大きくした姿」ではなく、**より細長い体型だった**とする説が出ている。「Megalodon As You Know It Never Existed」という動画はこの流れを扱ったものと推測される(**未確認**)。
- 歯のエナメル質の亜鉛同位体による栄養段階の研究(2022年)で、**ホホジロザメとの競合**が絶滅要因の一つとされている。
- 「深海に潜んでいる」という生存説は、①歯の化石記録が途絶えている ②メガロドンは浅い暖かい海の生き物だった ③大型の恒温性捕食者を維持できるだけの餌が深海にない、という理由で否定できる。

**推論**: これらは「最新研究で姿が変わったメガロドン」「生存説を科学で検証する」という、**大人向けの切り口として使える材料**です。

---

## 6. 英語圏と日本語圏の違い(推論)

| 観点 | 英語圏 | 日本語圏 |
|---|---|---|
| 主な担い手 | 3DCG大手(MetaBall、Zack D.)、What If、Infographics、Kurzgesagt | ゆっくり解説、テロップ解説、翻訳・吹き替え |
| 好まれる切り口 | もしも、vs、スケール、事件の再現 | 生存説、真実、徹底解説、総集編 |
| 映像の品質 | 高品質3DCGがすでに標準 | 静止画とテキストが中心(推測、**未確認**) |
| 飽和度(メガロドン「もしも」) | **非常に高い** | 中程度(上位動画の再生数は**未確認**) |
| AI映像に対する視聴者の反応 | AIフェイク(F13)への警戒が高まっている | 未確認 |

---

## 7. 機会と隙間(シネマティック × 科学的に厳密 × AI映像 × 大人向け)

1. **「フィクションと事実の分離」を売りにする**
   Discoveryの偽ドキュメンタリー(視聴者480万人、73%が信じた)や、AIフェイク動画(F13)が拡散する中で、「AIで作った映像だと明示したうえで、科学的に正しく再現する」こと自体がブランドになり得ます。概要欄や画面に、出典と「再現映像」の表示を必ず入れる。
2. **最新研究版のメガロドン**
   「細長かったメガロドン」で現代の海を描く。まだ旧来の姿でAI映像を作っている大多数の動画と、見た目だけで差がつきます。
3. **深海は「下へ降りる」型 × 生き物ドキュメンタリー**
   MetaBall型の1本道構成に、Kurzgesagt型の情緒と高品質映像を足す。日本語では隙間がある可能性があります(**未確認**)。
4. **ニュース連動の再現(AiTelly型)**
   潜水艇の事故、新種の発見、深海探査のニュースが出たら、72時間以内に3D・AIで再現する。小規模チャンネルが爆発できる、確認済みの唯一の型です。
5. **日本語で大人向け・高品質**
   日本語圏はゆっくり系が中心と推測されるため、映像品質で差別化できる可能性があります(要検証)。
6. **英語の睡眠用・長尺**
   「深海を3時間かけて降りていく」など。需要の数字は**未確認**のため、要検証。

---

## 8. 次の段階でやるべき検証(YouTubeを直接見られる環境で)

1. YouTubeで「what if megalodon」「megalodon still alive」「メガロドン 生きていたら」「深海 ゆっくり解説」「マリアナ海溝」「深海生物」を検索し、フィルタを「今年」にする。上位50本について、再生数・登録者数・公開日・尺を記録する。
2. 「再生数 ÷ 登録者数 ≥ 10」かつ「登録者 < 10万」の動画を外れ値として抽出する。
3. 2-3節の各URLについて、再生数・チャンネルの登録者数を確認する。
4. 日本語の上位5本について、サムネイルの文字量、尺、冒頭30秒を書き起こす。
5. YouTube Data API キーがあれば、`search.list`(q=megalodon, publishedAfter=2023-10-01, order=viewCount)と `videos.list` / `channels.list` で一括取得するのが最も効率的。

---

## 9. 結論:「もしメガロドンが現代の海に生きていたら」は最初の1本として適切か(推論)

**判定: そのままの形ではおすすめしません。切り口を変えれば可。**

**理由(マイナス)**
- 英語圏では、What If、Infographics、Zack D.、WatchMojo、そして直近1年だけで7本以上のドキュメンタリーがあり、**検索流入は大手が押さえています**。
- 「AIで作ったメガロドン映像」は、すでにフェイク動画(F13)の代名詞になりつつあり、「またAIのメガロドンか」と思われるリスクがあります。
- 新しいチャンネルの1本目は、検索流入もおすすめ流入もほぼ期待できません。1本目の役割は「チャンネルの方向性を示す名刺」です。

**理由(プラス)**
- 需要は常にあります(Discovery番組の再アップが今も700万回超、2025年にも再燃)。
- 日本語圏では「もしも」型の飽和は英語ほどではない可能性があります(**未確認**)。

**おすすめの切り口(推論)**
- 「最新研究の細長いメガロドンが、もし現代の海にいたら」
  → 見た目の差別化と、科学的な厳密さの両方を示せる。
- 「メガロドンは本当に深海で生きられるのか — 生存説を科学で検証する」
  → 日本語圏で強い「生存説」の需要に乗りながら、最後は「生きられない理由」で締める。
- **1本目を深海(下へ降りる型)にし、メガロドンは2〜3本目に回す**
  → 深海の映像美で「シネマティック」というブランドを先に作る。

---

## 出典一覧

- https://en.wikipedia.org/wiki/Megalodon:_The_Monster_Shark_Lives
- https://www.realclearscience.com/lists/top_junk_science_of_2013/megalodon_mermaids.html
- https://www.ladbible.com/news/animals/megalodon-do-they-still-exist-discovery-channel-934332-20250120
- https://www.foxnews.com/entertainment/discovery-channel-defends-its-decision-to-air-dramatized-megalodon.amp
- https://www.npr.org/2014/08/30/344562317/when-wildlife-documentaries-jump-the-shark
- https://www.npr.org/sections/thetwo-way/2013/08/07/209791960/shark-week-roundup-new-sharkcat-video-fake-documentary
- https://www.southernfriedscience.com/we-were-wrong-about-megalodon-lessons-learned-from-10-years-combating-fake-science-in-popular-media/
- https://hypeauditor.com/youtube/UCQwFuQLnLocj5F7ZcmcuWYQ/
- https://www.youtube.com/watch?v=aGPiQ47ahsE
- https://www.uniladtech.com/science/news/youtube-video-showing-scale-of-ocean-763752-20240228
- https://www.ladbible.com/entertainment/youtube/how-deep-sea-is-3d-animation-metaballstudios-189318-20250314
- https://www.unilad.com/news/us-news/video-shows-how-deep-ocean-is-giving-anxiety-838726-20250110
- https://nerdist.com/article/how-deep-oceans-go-ocean-depth-comparison-video-metaball-studios/
- https://www.mentalfloss.com/article/651042/how-deep-is-ocean
- https://laughingsquid.com/ocean-depth-comparison/
- https://www.unilad.com/news/world-news/titan-sub-implosion-animation-video-viral-949148-20230713
- https://www.dailyo.in/news/titanic-submersible-implosion-3d-animation-is-now-a-viral-video-with-10-million-views-40593
- https://www.newsweek.com/titan-sub-implosion-animation-viewed-5-million-times-1812486
- https://www.boston25news.com/news/trending/animation-explaining-titan-subs-implosion-has-more-than-6-million-views/642IZGJAWBF6BNAMHNB6WUIMYI/
- https://www.cbc.ca/news/canada/windsor/deep-sea-interactive-uwindsor-researcher-1.5396328
- https://x.com/nealagarwal/status/1203725171531669504
- https://www.imdb.com/title/tt10960198/
- https://zackdfilms.fandom.com/wiki/Zack_D._Films
- https://vidiq.com/youtube-stats/channel/@theinfographicsshow/
- https://youtube.fandom.com/wiki/Bedtime_Stories
- https://srilanka.factcrescendo.com/english/viral-video-of-megalodon-on-an-australian-island-is-ai-generated/
- https://www.latestly.com/social-viral/fact-check/was-a-megalodon-found-on-australia-beach-fact-check-reveals-ai-generated-clip-going-viral-with-netizens-believing-it-to-be-true-7013820.html
- https://www.tiktok.com/@slash/video/7213973681343679787
- https://www.watchmojo.com/articles/what-if-megalodon-sharks-didn-t-go-extinct
- https://whatifshow.com/what-if-megalodon-sharks-never-went-extinct/
- https://tidewaterteddy.com/2021/11/05/finding-megalodon-new-prehistoric-life-documentary/
- https://www.board-gill.com/megalodon_still_alive_or_not/
- 各YouTube動画URLは本文の表に記載
