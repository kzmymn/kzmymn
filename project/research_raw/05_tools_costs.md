# 05. 制作ツールと費用調査（古代生物・海洋生物ドキュメンタリー風YouTube／6〜7分／日本語→英語展開）

調査日: 2026-10-03
調査方法: WebSearch（2026年時点の情報を優先）。ただしこの環境では公式料金ページへの直接アクセス（WebFetch）がプロキシで遮断されたため、**数値の多くは2026年付の二次情報（比較・レビューサイト）経由**。公式URLは「確認先」として併記した。契約前に必ず公式ページで最終確認すること。
為替の目安: **1 USD ≈ 150円**で換算（未確認・概算）。

凡例: 【確度高】複数ソースで一致／【確度中】二次情報1〜2件／**未確認**＝ソース間で食い違い、または検証できず

---

## 0. まず押さえるべき2026年の大きな変化（重要）

| 変化 | 内容 | 影響 |
|---|---|---|
| **OpenAI Sora 終了** | 2026-03-24 発表、Web/アプリは 2026-04-26 終了、**APIは 2026-09-24 終了**【確度高】 | 選択肢から除外。 [OpenAI Help](https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation) / [Axios](https://www.axios.com/2026/03/24/openai-discontinue-sora-video-app) |
| **Udio ダウンロード停止** | 2025-10 の UMG 提携以降、音源・ステムのDLが無効。2026年9月時点でも再開していない、との報道【確度中】 | YouTube用BGMとしては実質使えない。 [Udio Help](https://help.udio.com/en/articles/12683565-changes-associated-with-the-universal-music-group-umg-partnership) |
| **にじボイス 終了** | 2026-02-04 サービス終了（日本俳優連合の削除要請を受けて）【確度高】 | 除外。 [Algomatic告知](https://algomatic.jp/news/notice_nijivoice_20251121/) / [PC Watch](https://pc.watch.impress.co.jp/docs/news/2065958.html) |
| **YouTube Inspiration タブ廃止へ** | 2026年8月から段階的に廃止、Ask Studio に移行【確度中】 | ネタ出しは Ask Studio を使う。 [YouTube Help](https://support.google.com/youtube/answer/15575509?hl=en) |
| **YouTube「inauthentic content」方針の明確化** | 2026-07 に「AIスロップ」対策の収益化方針を明確化。対象は「汎用・反復・テンプレ量産」「不快な内容」「AIペルソナでの健康/金融等センシティブ話題」【確度高】 | AI映像そのものはOK。**人の手による構成・独自解説・編集の価値**が必須。 [TechCrunch](https://techcrunch.com/2026/07/20/youtube-clarifies-policies-around-ai-slop-and-upsetting-videos/) |
| **Suno のDL上限** | 2026年9月の規約改定で商用利用は月間DL枠（Pro 20曲／Premier 60曲）に制限、との情報【確度中・未確認寄り】 | BGM用途なら十分だが要確認。 |

---

## 1. AI動画生成

### 1-1. 比較表（2026年10月時点の概算）

| ツール/モデル | 月額プラン（USD） | 1秒あたりの目安コスト(1080p) | 最大クリップ長 | 解像度 | 参照画像/一貫性 | 透かし・商用 | 生物・水中のリアルさ（評判） |
|---|---|---|---|---|---|---|---|
| **Google Veo 3.1**（Flow / Gemini / Google AI Pro・Ultra） | AI Plus $4.99 / **AI Pro $19.99（日本 2,900円）** / **AI Ultra（日本 36,400円、初回3か月18,000円）**。US Ultraは$99.99〜$249.99の複数表記あり＝**未確認** | API: Lite $0.08/s, Fast $0.12/s, Standard $0.40/s（4K: Fast $0.30/s, Std $0.60/s）。Flow: Lite 10cr、Fast 20cr（Ultraは10cr）、Quality 100cr／1クリップ | 4/6/8秒（4Kは8秒固定）、Scene Extensionで延長可 | 720p/1080p/**4K**（2026-01更新） | **Ingredients to Video（参照画像最大4枚）**、First/Last frame | **Flowの可視透かしはUltraとAPIのみ外れる**【確度中】。SynthID（不可視）は全出力に付与 | 自然光・屋外・大気感・リアリズムで最上位評価。ネイティブ音声付き |
| **Kling 3.0**（Kuaishou） | Standard $8.80（初月$6.99, 660cr）/ **Pro $32.56（3,000cr）** / Premier $80.96（8,000cr）/ Ultra 約$160〜180（26,000cr）。年払いで約34%引 | 1080p無音 8cr/s、音声付 12cr/s、720p無音 6cr/s、4K 30cr/s → Proで約$0.087/s。API $0.112/s | 最長15秒、マルチショット | 720p/1080p/4K | Elements（被写体参照）・マルチショットで一貫性強い | **無料は透かし＋商用不可＋720p**、有料は透かし無し・商用可【確度高】 | 長尺・シネマティック・キャラ一貫性に強い。動物の動きも安定との評価 |
| **Seedance 2.0**（ByteDance／Dreamina・CapCut） | Dreamina: Basic約$14.5、Standard約$32.9（5,775cr）、Advanced約$65.7（12,840cr）。表記ゆれ大＝**未確認** | 年払いSuper: Fast/Mini $0.041/s、Pro $0.086/s（720p）。**2026-09-23〜10-09キャンペーン: Fast $0.008/s、Pro $0.016/s**。API目安 約$0.14/s（1元/秒） | 最長15秒、マルチショット・音声同時生成 | 720p〜（1080p/2Kは上位） | **参照入力最大12点**、一貫性トップクラス | 実在人物の顔はブロック、不可視透かしあり。日本では2026-03-31からCapCut経由で提供 | Artificial Analysis Video Arenaで2026年上位（T2V/I2Vとも1位との報道）【確度中】。物語・マルチショットに最強 |
| **Runway Gen-4.5** | Standard $12（年払い, 625cr）/ Pro $28（2,250cr）/ Max $76（9,500cr） | 12cr/s → Pro約$0.15/s、Max約$0.10/s | 5〜10秒 | 1080p | References、Act系、編集機能が充実 | 有料は透かし無し・商用可 | 液体・毛・布の質感が改善。編集/ポスプロ的機能が強み |
| **Gemini Omni Flash**（Google, 2026-06登場, 8/27 GA） | AI Plus以上でGemini/Flowから利用 | API: 720p $0.10/s、1080p $0.152/s、4K $0.304/s | 未確認 | 〜4K | テキスト/画像/動画入力、対話的編集 | SynthID | Arena上位との報道。対話で修正できるのが利点【確度中】 |
| **Hailuo（MiniMax 2.3 等）** | Standard $7.99（1,000cr）/ Pro $24.99（4,500cr）/ Master $63.99 / Max $199.99 | API $0.08/s（768p）、$0.13/s（2K） | 6〜10秒 | 768p〜1080p | 被写体参照あり | 無料は透かし＋商用不可、有料は可 | 動きの物理表現が良く安価。高精細さはVeo/Klingに劣る評価 |
| **Luma（Ray3 / Ray 3.14）** | Plus $30 / Pro $90 / Ultra $300 | 未確認 | 5〜10秒 | 1080p、HDR | キーフレーム、参照 | 無料は透かし＋商用不可、Plus以上で商用可 | 映像美は高いがコスパは中 |
| **Midjourney Video（V1系）** | Basic $10 / Standard $30 / **Pro $60・Mega $120（Relaxで動画無制限）** | 動画1本 ≈ 画像8枚分のGPU時間 | 5秒＋4秒×4回延長＝最長21秒 | SD/HD（低め） | MJ画像からI2V＝絵柄統一しやすい | 商用可（年商$1M超はPro以上） | 美しいが写実ドキュメンタリーには解像度・物理が弱い。イメージB-roll向け |
| **Pika 2.5** | Standard $10（月払い, 700cr）/ Pro $28 / Fancy $76 | 1080p 5秒=40cr | 5〜10秒 | 〜1080p | 限定的 | 無料は480p・透かし・商用不可 | エフェクト系。リアル生物ドキュメンタリーには不向き |
| **Wan（Alibaba, オープン）** | 無料（ローカルGPU）。Wan 2.2はApache 2.0。**Wan 3.0（2026-08公開ベータ、30秒1パス）のオープンウェイト有無はソース間で矛盾＝未確認**。Wan 2.5/2.6はAPIのみ | 電気代＋GPU。クラウドGPUなら時間課金 | 2.2: 5秒前後、3.0: 最大30秒（主張） | 480p〜1080p | LoRA学習で生物デザイン固定が可能 | 自前運用なら透かし無し | 品質は上位商用モデルに一歩譲る。RTX 4090/24GB級が必要（14B） |
| ~~OpenAI Sora 2~~ | **2026-09-24 API終了。利用不可** | — | — | — | — | — | — |

主な出典:
- Google AI プラン（公式確認先）: https://one.google.com/about/google-ai-plans/ ／日本価格: [helentech](https://helentech.jp/google-ai-plans-comparison/), [AI総研 Flowガイド](https://www.ai-souken.com/article/what-is-flow), [mj-lab 2026年8月](https://mj-lab.com/veo-3-1-practical-guide/)
- Flowクレジット: [costgoat Google Flow](https://costgoat.com/pricing/google-flow), [saascrmreview](https://saascrmreview.com/google-flow-pricing/)
- Veo API単価（公式）: https://ai.google.dev/gemini-api/docs/pricing ／ [veo3gen](https://www.veo3gen.app/blog/veo-3-1-pricing-plans)
- Veo 3.1 4K・Ingredients: [the-decoder](https://the-decoder.com/google-deepmind-updates-veo-3-1-with-reference-image-function-for-more-dynamic-videos/), [superprompt](https://superprompt.com/blog/google-veo-3-1-update-4k-vertical-video-ingredients)
- Veo透かし: [BGR](https://www.bgr.com/tech/those-amazing-veo-3-videos-will-finally-tell-you-they-were-made-with-ai/), [aifreeapi SynthID](https://www.aifreeapi.com/en/posts/veo-3-1-watermarks-synthid)
- Kling（公式確認先）: https://app.klingai.com/global/membership/membership-plan ／ [magichour](https://magichour.ai/blog/kling-ai-pricing), [cloudzero](https://www.cloudzero.com/blog/kling-ai-pricing/), [atlascloud](https://www.atlascloud.ai/blog/tips/kling-ai-pricing)
- Seedance/Dreamina（公式）: https://dreamina.capcut.com/seedance/seedance-2-0-pricing ／ [TechCrunch CapCut](https://techcrunch.com/2026/03/26/bytedances-new-ai-video-generation-model-dreamina-seedance-2-0-comes-to-capcut/), [CapCut X 日本提供](https://x.com/capcutapp/status/2038806148934189070)
- Runway（公式）: https://runwayml.com/pricing ／ [eesel](https://www.eesel.ai/blog/runway-ai-pricing), [stacksheriff](https://stacksheriff.com/ai-tools/runway-pricing/)
- Gemini Omni: [eesel](https://www.eesel.ai/blog/gemini-omni-1-1-flash-pricing), [buildfastwithai](https://blog.buildfastwithai.com/gemini-omni-flash-review-google-ai-video-model-2026)
- Hailuo（公式）: https://hailuoai.video/subscribe ／ [costbench](https://costbench.com/software/ai-video-generators/hailuo-ai/)
- Luma（公式）: https://lumalabs.ai/pricing ／ [eesel](https://www.eesel.ai/blog/luma-ai-pricing)
- Midjourney（公式）: https://docs.midjourney.com/hc/en-us/articles/27870484040333-Comparing-Midjourney-Plans ／ [TechCrunch V1](https://techcrunch.com/2025/06/18/midjourney-launches-its-first-ai-video-generation-model-V1)
- Pika（公式）: https://pika.art/pricing ／ [flowith](https://flowith.io/blog/pika-art-pricing-2026-free-vs-basic-vs-pro/)
- Wan: [localaimaster Wan 2.7](https://localaimaster.com/blog/wan-2-7-open-source), [wan27.org Wan 3.0](https://wan27.org/blog/wan-3-open-source), [kingy Wan 3.0](https://kingy.ai/blog/wan-3-0-analysis/)
- ランキング: [techsy Arena順位](https://techsy.io/en/blog/best-ai-video-models), [3daistudio 比較](https://www.3daistudio.com/blog/best-ai-video-generator-2026)

### 1-2. 用途別のおすすめ

- **写実的な海洋生物・水中光（コースティクス、浮遊物、青の減衰）**: **Veo 3.1（Quality/Fast）** が第一候補。自然光・大気感・プロンプト忠実度で評価が高い。
- **同じ古代生物を複数カットで一貫させる**: **Seedance 2.0（参照12点・マルチショット）** と **Kling 3.0（Elements・15秒・マルチショット）**。Veo 3.1のIngredients（参照4枚）も可。
- **I2V（静止画キーフレーム→動画）で絵作りを固定**: Kling / Veo（First/Last frame）/ Seedance いずれも可。**「まず静止画で生物デザインを確定→I2V」が最も安定**。
- **最安で秒数を稼ぐ**: Seedance 2.0 Fast（年払い$0.041/s、キャンペーン中はさらに安い）、Hailuo、Veo 3.1 Lite API（$0.08/s）。
- **自前GPUがある場合**: Wan 2.2（Apache 2.0）＋生物デザインLoRA。ただし最終品質はクラウド上位モデルが有利。
- **避ける/補助**: Pika（エフェクト寄り）、Midjourney Video（低解像度、イメージ用B-rollなら可）。

---

## 2. AI画像生成（キーフレーム・サムネイル）

| ツール | 料金 | 強み | 注意 |
|---|---|---|---|
| **Nano Banana Pro（Gemini 3 Pro Image）** | Google AI Pro/Ultraに含まれる（Gemini/Flow）。API $0.134/枚（1K/2K）、$0.24（4K）。2026-06 GA | **参照画像による同一生物の再現・編集**、文字入れ（サムネ）に強い | SynthID付与。【確度中】 |
| **Midjourney V8.x**（V8.2が2026-07-24にデフォルト） | Basic $10 / Standard $30 / Pro $60 / Mega $120（年払い20%引） | シネマティックな質感・ライティング・スタイル参照（--sref）、キャラ参照 | 年商$1M超はPro以上。写実の解剖学的正確さは要チェック |
| **GPT Image 2（ChatGPT Images 2.0）** | 2026-04-21 API公開、全ChatGPTプランで利用可 | 推論してから描くため指示追従・文字精度が高い→**サムネの日本語文字** | 写実の質感はMJ/Nano Bananaと好みが分かれる |
| **FLUX.2** | API: klein $0.014〜、Pro $0.03、Flex $0.05、Max $0.07/枚 | 安価・高品質、ローカル運用（dev/klein）可、LoRAで生物デザイン固定 | ライセンスはモデルごとに異なる（dev系は非商用条件あり＝要確認） |
| **Ideogram 3** | Plus $15〜20 / Pro $42〜60。API $0.03〜0.09 | タイポグラフィ（英語サムネ） | 写実生物は他に劣る |
| **Imagen 4**（Google） | Gemini/Flow/Vertex経由 | 写実的 | 2026年はNano Banana系が主力。単体価格は未確認 |

出典: [Midjourney Version docs](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version), [releasebot MJ](https://releasebot.io/updates/midjourney), [openrouter Nano Banana Pro](https://openrouter.ai/google/gemini-3-pro-image), [pixmind](https://www.pixmind.io/posts/nano-banana-pro-pricing-guide-2026), [OpenAI gpt-image-2](https://developers.openai.com/api/docs/models/gpt-image-2), [BFL pricing](https://docs.bfl.ml/quick_start/pricing), [eesel Ideogram](https://www.eesel.ai/blog/ideogram-pricing)

**推奨**: キーフレーム＝**Nano Banana Pro（AI Proに込み）＋必要ならMidjourney Standard**。サムネ文字＝GPT Image 2 か Nano Banana Pro（日本語文字）。最終的な文字はCanva/Photoshop等で人手入れが安全。

---

## 3. 日本語ナレーション（TTS）

| 選択肢 | 料金 | 日本語品質 | 商用・クレジット |
|---|---|---|---|
| **自分の声（推奨候補）** | マイク 1〜2万円程度（一回）。無料 | 最も自然・信頼性高い。YouTubeの「独自性」面でも有利 | 権利問題なし。英語版はElevenLabs PVC/吹替で自分の声を流用可 |
| **ElevenLabs（Eleven v3）** | Free（商用不可）/ **Starter $5〜6（3万クレジット≈3万文字）** / **Creator $22（10万〜12.1万）** / Pro $99 | v3（2026年2月正式版）で日本語のピッチアクセント・抑揚が大幅改善、との日本語レビュー多数【確度中】。v3は1リクエスト5,000文字上限 | **Starter以上で商用可**。Creator以上でPro Voice Clone（自分の声のクローン）。英語版にも同一声で展開可 |
| **Fish Audio（OpenAudio S1/S2）** | Plus $11（年）/$15（月）≈200分、Pro $75 | 日本語対応、低価格。品質は良好との評価だが個体差 | 有料で商用可（自分が権利を持つ声に限る） |
| **VOICEVOX** | 無料 | キャラ声（ずんだもん等）。ドキュメンタリーの落ち着いたナレーションには不向きなキャラが多い | **概要欄に「VOICEVOX:キャラ名」表記で収益化可**。キャラごとに追加規約あり。クレジット無し商用は1キャラ40万円＋税の契約 |
| **CoeFont** | Free（非商用・クレジット要）/ **Standard 3,300円/月（約8万文字）** / Plus 55,000円 | 日本製、日本語自然。ナレーター系ボイスあり | Standard以上で商用・YouTube収益化可、クレジット不要 |
| **Google Cloud TTS（Chirp 3 HD）** | $30/100万文字（無料枠あり） | 日本語HD声は自然だが感情表現は控えめ | 商用可（GCP規約） |
| **Azure Neural TTS** | Neural $15/100万文字、HD $22/100万文字 | ja-JP Neural/HD。SSMLで細かい調整可 | 商用可 |
| **OpenAI gpt-4o-mini-tts** | 入力$2.50/1Mトークン、出力$10〜12/1Mトークン | 日本語は可だが英語ほど自然ではない（未確認） | 商用可（AI音声である旨の開示を求める規約あり） |
| ~~にじボイス~~ | **2026-02-04終了** | — | — |

文字量の目安: 日本語ナレーション約300〜350字/分 → **6.5分 ≈ 2,000〜2,300字**。リテイク込みで3倍見ても約7,000字/本 → **ElevenLabs Starterで月4本まで収まる計算**。

出典: [ElevenLabs pricing（公式）](https://elevenlabs.io/pricing), [flexprice](https://flexprice.io/blog/elevenlabs-pricing-breakdown), [uravation ElevenLabs 2026年10月](https://uravation.com/media/elevenlabs-complete-guide-2026/), [uiux.tokyo v3](https://uiux.tokyo/page/elevenlabs-v3-2026/), [Fish Audio（公式）](https://fish.audio/plan/), [VOICEVOX規約まとめ castcraft](https://castcraft.live/blog/527/), [VOICEVOX公式](https://voicevox.hiroshiba.jp/), [CoeFont topvox](https://www.topvox.jp/blog/review-coefont/), [Google TTS（公式）](https://cloud.google.com/text-to-speech/pricing), [Azure texttolab](https://texttolab.com/blog/azure-text-to-speech-pricing), [costgoat OpenAI TTS](https://costgoat.com/pricing/openai-tts)

**推奨**: 日本語版＝**自分の声** または **ElevenLabs v3（Starter→Creator）**。英語版＝ElevenLabsで同じ声（自分の声のPVCクローン or 同一ストックボイス）で一貫性を保つ。

---

## 4. 音楽・効果音（Content IDリスク込み）

| 選択肢 | 料金 | 商用/Content ID | 備考 |
|---|---|---|---|
| **YouTube Audio Library** | 無料 | YouTube上は安全。一部は帰属表示必須 | 曲数・質は限定的。最低予算の基本 |
| **Epidemic Sound** | Creator $9.99/月（年払い）/ $17.99（月払い） | 1チャンネル/プラットフォームで収益化可。**Content IDを事前ホワイトリスト化**（自社権利保有） | ドキュメンタリー向けシネマティック曲・SFXが豊富。解約後の新規アップロードは要注意（契約中公開分は有効） |
| **Artlist** | Music&SFX Social $9.99〜、Unlimited 約$16.6（年$199）、Max $33.25 | 永久ライセンス型（契約中DLした曲は解約後も使用可） | Content ID対応あり |
| **Suno（v5.5）** | Pro $10（年$8）/ Premier $30（年$24）。WMG提携後 | 有料で商用・YouTube収益化可。**2026-09規約で月間DL枠（Pro 20／Premier 60）**【確度中】 | AI曲は他者のContent ID（類似曲）誤検知リスク・規約変更リスクあり。**AI曲を自分でContent ID登録しない**こと |
| ~~Udio~~ | — | **DL不可（2026年9月時点）** | 除外 |
| **ElevenLabs SFX v2 / Eleven Music v2** | ElevenLabs有料プランのクレジット共用（Music 900cr/分） | 有料プランで商用可、Musicはライセンス済みデータ学習（Merlin/Kobalt）。※セルフサーブはFilm/TV等除外 | 水中の泡、深海の低周波、生物の鳴き声（創作）など**存在しない生物の声作りに最適** |

Content IDの実務: ライブラリ曲でも誤クレームはあり得るので、**ライセンス証明（DL履歴・ライセンスID）を保存**し、異議申し立てで解除する運用にする。

出典: [Epidemic Sound pricing（公式）](https://www.epidemicsound.com/pricing/), [photutorial Epidemic](https://photutorial.com/epidemic-sound-pricing/), [photutorial Artlist](https://photutorial.com/artlist-pricing/), [Suno pricing（公式）](https://suno.com/pricing), [eesel Suno review](https://www.eesel.ai/blog/suno-review), [dynamoi Suno rights](https://dynamoi.com/learn/ai-music-distribution/suno-commercial-rights-explained), [Udio help](https://help.udio.com/en/articles/12683565-changes-associated-with-the-universal-music-group-umg-partnership), [ElevenLabs Music docs](https://elevenlabs.io/docs/overview/capabilities/music), [mindstudio Eleven Music](https://www.mindstudio.ai/blog/elevenlabs-music-v2-commercial-content-licensed-ai-music), [YouTube Audio Library](https://studio.youtube.com/channel/UC/music)

---

## 5. 編集・アップスケール・字幕

| ツール | 料金 | ポイント |
|---|---|---|
| **DaVinci Resolve（無料版）** | 無料 | **UHD 3840×2160/60fpsまで書き出し可**（8bit H.264/H.265）。カラーグレーディング最強。Fairlightで音声も完結。Studio版（約$295買い切り）は10bit・ノイズ除去・AI機能（Magic Mask/字幕自動生成等） |
| **CapCut** | 無料 / Pro（日本 1,200円/月・9,000円/年 との情報、他にも価格表記ゆれ＝**未確認**） | **2025-06の規約改定でユーザーコンテンツへの広範なライセンス条項が議論に**。また**Proでも素材ごとに「非商用」「商用可」ラベルがあり、Pro＝包括的商用ライセンスではない**。収益化チャンネルの本編編集は Resolve 推奨、CapCutは使うなら素材ラベル確認を徹底 |
| **Premiere Pro** | 約$22.99/月（単体、未確認） | Adobe Firefly連携、生成拡張。既に使い慣れていれば |
| **Topaz Video（旧Video AI）** | **サブスクのみ**: Personal $299/年（年商$1M未満の商用可、クラウドクレジット25/月）、Pro $699/年。Topaz Studio $399/年（全部入り、$45/月年契約） | 720p/1080p生成→4Kアップスケール、フレーム補間。AI映像の質感を揃えるのに有効 |
| **字幕** | Resolve Studio自動字幕 / Whisper系（無料、ローカル）/ YouTube自動字幕＋手直し | 日本語→英語字幕は Claude/ChatGPT で翻訳→SRT。英語版は別アップロードか**YouTubeの多言語音声トラック**を検討 |

出典: [toolfarm Resolve free vs Studio](https://www.toolfarm.com/tutorial/in-depth-davinci-resolve-studio-vs-the-free-version/), [davinciresolve21.com 4K](https://davinciresolve21.com/blog/davinci-resolve-free-version-4k-export-limit-myth-explained), [Blackmagic公式](https://www.blackmagicdesign.com/products/davinciresolve), [CapCut legal（公式）](https://www.capcut.com/trust/legal), [dpreview CapCut規約](https://www.dpreview.com/news/1239418455/capcut-video-editing-app-s-new-terms-spark-rights-concerns-we-asked-a-lawyer-for-guidance/), [toolproven CapCut商用](https://toolproven.com/blog/capcut-commercial-license), [opentherank CapCut国別価格](https://opentherank.com/photo-video-pricing/capcut/), [Topaz Studio（公式）](https://www.topazlabs.com/studio), [costbench Topaz](https://costbench.com/software/ai-video-generators/topaz-video-ai/)

---

## 6. 台本・リサーチ

| ツール | 料金（目安） | 使い方 |
|---|---|---|
| **Claude（Pro）** | 約$20/月（年払い$17）※2026年価格は**未確認** | 構成・台本執筆、日本語の語り口調整、英語版ローカライズ。長文資料の読み込み |
| **ChatGPT（Plus）** | $20/月（※Go等の廉価プランは国により異なる、**未確認**） | 台本・GPT Image 2・Deep Research |
| **Perplexity（Pro）** | 約$20/月（**未確認**）／無料版でも出典付き検索可 | 最新の古生物学ニュース・論文の出典付き検索 |
| **NotebookLM** | 無料（上限あり）／Google AI Proで上限拡張 | 論文・博物館資料・Wikipediaなどを読み込ませて**ソース限定のファクトチェック**。Audio Overviewで構成確認 |
| **Gemini（Deep Research）** | Google AI Proに含まれる | 網羅的下調べ |

**ファクトチェック方針**: 古代生物は学説が更新されやすい（体長推定・外見・生息年代）。台本の数値はすべて一次資料（論文・博物館・国立科学博物館等）で裏取りし、「〜と推定されている」と幅を持たせる。復元が推測であることを動画内で明示すると信頼性が上がる。

---

## 7. 分析・ネタ出し

| ツール | 料金 | 備考 |
|---|---|---|
| **YouTube Studio（Ask Studio／Analytics）** | 無料 | Inspirationタブは2026年8月から段階的廃止→**Ask Studio**で企画相談。タイトルA/Bテスト（Test & Compare）も無料 |
| **vidIQ** | Free / Boost $199/年（月払い$39） 他 | キーワード・競合分析、AIクレジット2,000/月（Boost） |
| **TubeBuddy** | Pro 約$3.6〜4.5/月、Legend 約$23〜29/月 | サムネA/B、タグ。安価 |

出典: [YouTube Help Inspiration](https://support.google.com/youtube/answer/15575509?hl=en), [YouTube Blog](https://blog.youtube/news-and-events/youtube-studio-made-on-youtube-2025/), [1of10 vidIQ](https://1of10.com/blog/vidiq-pricing/), [1of10 TubeBuddy](https://1of10.com/blog/tubebuddy-pricing-review/)

**推奨**: 最初は無料（YouTube Studio＋vidIQ無料版）で十分。月4本体制になったらvidIQ Boost（年払い）を検討。

---

## 8. 1本あたりの必要尺・生成量の試算

前提: 完成尺 6.5分 = **390秒**

| 項目 | 構成案A「フルAI映像」 | 構成案B「ハイブリッド（推奨・低予算）」 |
|---|---|---|
| AI動画で埋める尺 | 約300〜330秒（残りはタイトル・地図・図解・テキスト） | 約180〜200秒（ヒーローショット中心） |
| 静止画＋カメラワーク（Ken Burns/2.5Dパララックス） | 少量 | 約120〜150秒（Nano Banana/MJ画像を動かす） |
| 1クリップ長 | 6〜8秒（実際に使うのは3〜6秒） | 同左 |
| 使用クリップ数 | 約45〜60カット | 約30〜35カット |
| **リテイク倍率** | ×3〜4 | ×3 |
| **生成秒数/本** | **約1,000〜1,300秒** | **約550〜650秒** |

### 1秒あたり単価別のAI動画コスト/本（概算）

| 単価 | 例 | 案A（1,150秒） | 案B（600秒） |
|---|---|---|---|
| $0.04/s | Seedance 2.0 Fast（Dreamina年払い, 720p→アップスケール） | 約$46（≈7,000円） | 約$25（≈3,700円） |
| $0.08〜0.09/s | Kling 3.0 1080p（Pro/Premier）、Veo 3.1 Lite API | 約$95〜105（≈15,000円） | 約$50（≈7,500円） |
| $0.12/s | Veo 3.1 Fast API 1080p | 約$140（≈21,000円） | 約$72（≈11,000円） |
| $0.40/s | Veo 3.1 Standard API | 約$460（≈69,000円） | 約$240（≈36,000円） |
| 定額 | **Google AI Ultra（Flow）**: Fast 10cr/クリップ、Quality 100cr/クリップ、月25,000cr | 4本/月でも Fast中心＋Quality要所 で収まる計算（Quality 8秒×250本=2,000秒分、Fastなら約2万秒分） | 同左 |

※Flowの「クリップ単位クレジット」は8秒クリップ前提の推定。Pro（1,000cr＋日次50cr）ならFast(20cr)で約50〜75クリップ≒400〜600秒/月だが、**Pro以下ではFlow出力に可視透かし「Veo」が入る**ため本編には不向き（プレビズ・テスト用）。

---

## 9. 推奨スタック

### 9-1. 最低予算スタック（月2本・ハイブリッド構成B）

| 役割 | ツール | 月額 |
|---|---|---|
| 動画生成（主力） | **Kling Pro**（3,000cr ≈ 1080p無音で375秒／720pで500秒） | $32.56（≈4,900円） |
| 動画生成（秒数補充） | **Dreamina（Seedance 2.0）商用可プラン**（約$18〜33、表記ゆれ＝未確認）またはVeo 3.1 Lite/Fast APIを従量 | 約$18〜33（≈2,700〜5,000円） |
| 画像・リサーチ・プレビズ | **Google AI Pro**（Nano Banana Pro、Gemini Deep Research、NotebookLM拡張、Flowでテスト） | 2,900円 |
| ナレーション | **自分の声**（無料）または **ElevenLabs Starter** | $0〜6（≈0〜900円） |
| 音楽・SFX | **YouTube Audio Library（無料）**＋ElevenLabs SFX（Starter内）※必要に応じSuno Pro $10 | 0〜1,500円 |
| 編集 | **DaVinci Resolve 無料版** | 0円 |
| 台本 | Claude または ChatGPT（無料版でも可、有料なら$20） | 0〜3,000円 |
| 分析 | YouTube Studio（Ask Studio）＋vidIQ無料 | 0円 |
| **合計** | | **約1.1万〜1.8万円/月**（≈$75〜120） |

- 生成秒数の実質: Kling 375〜500秒＋Seedance/Veo Lite 数百秒 ≒ **約800〜1,100秒/月** → 構成B（600秒/本）で**月2本がぎりぎり**。
- **1本あたり実費 ≈ 5,500〜9,000円**（AI動画分 約4,000〜7,500円＋その他按分）。
- 初月は Kling の初月割引（Standard $6.99 / Pro $25.99）、Google AI Pro 初月無料、Seedanceキャンペーン（〜10/9）を活用してテスト。

### 9-2. 品質重視スタック（月2〜4本・フルAI構成A対応）

| 役割 | ツール | 月額 |
|---|---|---|
| 動画生成（主力・透かし無し・4K） | **Google AI Ultra**（Veo 3.1 Quality/Fast、Ingredients、4Kアップスケール50cr、月25,000cr。Nano Banana Pro、Gemini、NotebookLM上限も最大） | 36,400円（初回3か月 18,000円） |
| 動画生成（一貫性・長尺・マルチショット） | **Kling Pro**（またはSeedance 2.0 Standard） | $32.56（≈4,900円） |
| キーフレーム美術 | **Midjourney Standard**（V8.x、スタイル/キャラ参照） | $30（≈4,500円） |
| ナレーション | **自分の声**＋**ElevenLabs Creator**（PVCで自分の声クローン→英語版、SFX、Music） | $22（≈3,300円） |
| 音楽 | **Epidemic Sound Creator**（Content ID事前クリア） | $9.99〜17.99（≈1,500〜2,700円） |
| アップスケール | **Topaz Video Personal**（$299/年） | ≈$25（≈3,700円） |
| 編集 | DaVinci Resolve（無料→必要ならStudio $295買い切り） | 0円（Studio按分≈1,000円） |
| 台本・リサーチ | Claude Pro ＋ Perplexity（無料版）＋NotebookLM | ≈$20（≈3,000円） |
| 分析 | vidIQ Boost（年払い） | ≈$16.6（≈2,500円） |
| **合計** | | **約6万〜6.5万円/月**（Ultra初回割引期間は約4.3万円） |

- 生成量: Ultra単体で Fast中心＋Quality要所なら**月4本のフルAI構成でも収まる**見込み（Quality 100cr/クリップを1本あたり約60クリップ使うと6,000cr、Fast 10cr×300クリップ＝3,000cr → 1本約9,000cr、月2〜3本分。4本ならFast比率を上げる）。
- **1本あたり実費 ≈ 1.5万〜3万円**（月4本なら約1.5万円、月2本なら約3万円）。
- 品質のコア: Veo 3.1で写実的な水中・光、Kling/Seedanceで同一生物の連続カット、Topazで4K化、Epidemicで安全なBGM。

### 9-3. 代替・追加オプション
- **Runway Gen-4.5（Pro $28）**: 編集系機能（参照・リライティング等）を使いたい場合の代替主力。
- **Veo 3.1 Fast API従量（$0.12/s）**: Ultraを契約せず透かし無しVeoを使う方法。月1本なら Ultra より安い（案Bで約1.1万円）。Vertex AI経由ならGoogleの補償（indemnification）対象の情報あり（未確認）。
- **Wan 2.2/3.0ローカル**: 24GB級GPUを持っているなら秒単価ほぼゼロ。LoRAで生物デザイン固定。

---

## 10. AIリアリズムの制作Tips（古代生物・海洋）

### 10-1. 生物デザインの一貫性
1. **「生物デザインシート」を最初に作る**: Nano Banana Pro / Midjourneyで、側面・正面・上面・口元アップ・全身（スケール比較付き）を同一シードやスタイル参照で生成し、1枚に確定。体色・模様・ヒレの数・歯列を**文章仕様（スペック表）**としても保存し、毎回プロンプトに貼る。
2. **I2V（画像→動画）を基本にする**: T2Vは毎回デザインがブレる。確定キーフレーム→Veo（Ingredients/First frame）、Kling（Elements）、Seedance（参照最大12点）。
3. **ショットごとに参照を固定**: 同じ参照画像セットを使い回す。体色は照明で変わるので、水深ごとの「色見本」も作る。
4. **カット尺を短く**: AI映像は3〜5秒目以降に崩れやすい。8秒生成して良い3〜4秒だけ使う。
5. **崩れやすい要素を避ける**: 口の開閉、ヒレの本数、群れの個体同士の融合、捕食シーンの接触。→ 接触直前でカット、泡・砂煙・暗転でつなぐ。

### 10-2. 不気味さ（uncanny）回避
- **カメラはドキュメンタリーの文法**: 望遠レンズ風、ゆっくりしたトラッキング、ダイバー目線の手持ち揺れ、ROV/深海探査機のライト。プロンプトに「documentary footage, BBC natural history style, telephoto, shallow depth of field」等。ただし実在番組名・ブランドは出力に出ないよう注意（プロンプトに番組名を入れない方が安全）。
- **動きは控えめ・自然に**: 「slow, gliding, subtle tail movement」。速い動き・急旋回は破綻しやすい。
- **完璧すぎる質感を汚す**: フィルムグレイン、浮遊物（マリンスノー）、レンズの微かな歪み、軽いピントのズレを後処理で統一 → 生成元が違うクリップの質感が揃う。
- **目の表現**: 目のハイライトと瞳孔の向きが不自然になりがち。アップは少なく、ミドル〜ワイド中心。

### 10-3. スケール感（巨大さ）の出し方
- **比較対象を画面に入れる**: ダイバー（小さく、背中側・顔を映さない）、潜水艇、現生の魚群（イワシ・マグロ）、サンゴ、海面の光芒。
- **大気（水）遠近法**: 遠いほど青く霞む。巨大生物は輪郭の一部が霧に溶ける。
- **ゆっくり動かす**: 巨大なものほど動きは遅く見える。カメラの移動距離に対して生物が画面を長く横切る。
- **図解インサート**: 人間・バス・シロナガスクジラとのサイズ比較図（静止画・モーショングラフィックス）を挟むと説得力が増す。

### 10-4. 水中ライティング
- **水深で色を変える**: 浅場＝コースティクス（揺れる光の網目）と光芒（god rays）、中層＝青緑で赤が抜ける、深海＝ほぼ真っ暗＋生物発光＋探査ライトのスポット。
- **赤の減衰**: 10m以深では赤が失われる。赤い体色は深場では黒っぽく見えるのが自然。
- **浮遊粒子とバックスキャッター**: ライトの前に粒子が光ると「本物の水中撮影」感が出る。
- **カラーグレーディングで統一**: DaVinci ResolveでLUT/ノードを作り、全クリップに同一グレードを当てる。

### 10-5. 制作フローとプラットフォーム対応
- **ワークフロー**: 台本（Claude/ChatGPT）→ファクトチェック（NotebookLM/Perplexity＋一次資料）→ショットリスト（秒数・構図・参照画像ID）→キーフレーム生成→I2V生成（×3〜4）→選別→Resolveで編集・グレード→ナレーション・BGM・SFX→Topazで4K化（任意）→字幕→アップロード。
- **YouTubeの開示**: 写実的なAI映像（実在しない生物の「実写風」映像）は「改変または合成コンテンツ」にチェックを入れるのが安全。開示は収益化や表示に影響しないと YouTube は説明。説明欄に「映像はAIによる復元イメージ」と明記。
- **独自性（inauthentic content対策）**: 自分の解説・構成・考察を中心に据え、テンプレ量産にしない。シリーズでも毎回の切り口・調査量を変える。
- **英語展開**: 同一映像に英語ナレーション（ElevenLabsで同じ声）を差し替え、YouTubeの多言語音声トラックまたは別チャンネル。サムネ文字は差し替え。
- **素材管理**: 生成プロンプト・シード・使用ツール・ライセンス（プラン名・日付）をスプレッドシートで記録（権利主張・異議申し立て時の証拠）。

---

## 11. 未確認事項・リスク一覧
- Google AI Ultra の米国価格（$99.99〜$249.99で表記ゆれ）、Ultra内の段階プランの有無 → 公式 https://one.google.com/about/google-ai-plans/ で確認
- Flow（AI Pro）出力の可視透かしの有無と扱い（ソース上はUltra/APIのみ透かし無し）
- Dreamina（Seedance 2.0）の正確なプラン名・価格・商用条件・1080p単価
- Wan 3.0 のオープンウェイト公開状況（ソース矛盾）
- Suno 2026年9月規約の「DL枠」内容
- CapCut Pro の日本価格（1,200円/月 説と約2,180円/月 説）
- Claude / ChatGPT / Perplexity の2026年10月時点の月額
- Kling Ultra の価格（$159.99〜$180で表記ゆれ）
- 為替（1USD=150円で概算）
