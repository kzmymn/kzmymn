# P1 見本データで使った名前の一覧

- 作成：2026-10-11（designer）
- 確認の方法：`dist/` の menu-template.html、menu-data.csv、phrases.csv、README.txt と、sample-print.pdf を `pdftotext` で文字にしたものを grep しました。検索した文字は次のとおりです。
  - 店名の記号：〇〇／○○、(Sample)、（样本）、(견본)
  - 電話番号の形：数字-数字-数字
  - 住所の手がかり：〒、都道府県・市区町村＋数字
  - 人名の手がかり：様、さん、Mr.、Ms.
  - 会社・ブランドの手がかり：株式会社、有限会社、®、™、@
- 結果：
  - 固有名詞は、下の表 A の見本の店名（4言語）だけです。
  - 人名・住所・電話番号・メールアドレス・実在の店名・ブランド名・商標は 0件です。
  - 「様」にヒットしたのは「お客様」「お一人様」などの敬称で、人名ではありません。
  - 「@」にヒットしたのは CSS の `@media` と `@page` です。
  - 第1週のデモの店名（麺処 さくら など）は 0件です（`check.md` の 3. を参照）。

## A. 固有名詞（見本の店名）

| 名前 | 使った場所（ファイルと言語） | 種類 | 架空である根拠 |
|---|---|---|---|
| 〇〇食堂（見本） | menu-template.html（日）、sample-print.pdf 1ページ目（日）、README.txt | 店名 | 名前の部分が伏せ字の「〇〇」で、「（見本）」と明記している |
| (Sample) ○○ Shokudo | menu-template.html（英）、sample-print.pdf 2ページ目（英） | 店名 | 伏せ字と "(Sample)" の明記 |
| （样本）○○食堂 | menu-template.html（中）、sample-print.pdf 3ページ目（中） | 店名 | 伏せ字と「样本」（＝見本）の明記 |
| (견본) ○○ 식당 | menu-template.html（韓）、sample-print.pdf 4ページ目（韓） | 店名 | 伏せ字と「견본」（＝見本）の明記 |

## B. 料理名（固有名詞ではありません。一般名であることの確認のため載せています）

どの料理名も、どこの店でも使われる一般的な名前です。特定の店の商品名やブランド名は含めていません。場所は、どれも menu-template.html・menu-data.csv・sample-print.pdf の4言語です。

| 名前（日） | 英 / 中 / 韓 | 種類 | 根拠 |
|---|---|---|---|
| 鶏の唐揚げ定食 | Fried Chicken Set Meal / 日式炸鸡套餐 / 닭튀김 정식 | 料理名（一般名） | 一般的な料理名 |
| 焼き魚定食（さば） | Grilled Mackerel Set Meal / 烤青花鱼套餐 / 고등어구이 정식 | 料理名（一般名） | 同上 |
| 豚の生姜焼き定食 | Ginger Pork Set Meal / 姜汁烧猪肉套餐 / 돼지고기 생강구이 정식 | 料理名（一般名） | 同上 |
| 麻婆豆腐定食 | Mapo Tofu Set Meal / 麻婆豆腐套餐 / 마파두부 정식 | 料理名（一般名） | 料理のジャンル名。人名に由来するとされるが、一般名として定着している |
| だし巻き卵 | Japanese Rolled Omelet / 日式高汤蛋卷 / 일본식 계란말이 | 料理名（一般名） | 一般的な料理名 |
| 枝豆 | Edamame / 毛豆 / 풋콩 | 料理名（一般名） | 同上 |
| ざるそば | Chilled Soba Noodles / 日式冷荞麦面 / 냉 메밀국수 | 料理名（一般名） | 同上 |
| ウーロン茶 | Oolong Tea / 乌龙茶 / 우롱차 | 飲み物（一般名） | 茶の種類の名前。商品名ではない |
| 生ビール（中） | Draft Beer (Medium) / 生啤酒（中杯） / 생맥주 (중) | 飲み物（一般名） | 銘柄は書いていない |

## C. 定型文（phrases.csv）

- 全25文に、固有名詞（店名・人名・地名・ブランド）はありません。
- 「300円」「30分」は、店に合わせて書き換える例の数字です（note_ja 列に「お店に合わせて変更」と書いています）。

## D. 名前以外の文字で、上の検索にヒットしうるもの

- menu-template.html の CSS `font-family` に、OS に入っているフォントの名前を書いています（Hiragino Sans、Meiryo、Microsoft YaHei、Malgun Gothic、Noto Sans、WenQuanYi Zen Hei など）。
- これは閲覧する端末のフォントを指定するためのもので、見本データではありません。フォントのファイルは同梱していません。

## 実在・商標の確認（researcher, 2026-10-11）

対象は表 A の店名（4言語）です。表 B の料理名・飲み物名は一般名詞のため、個別の検索はしていません。

### 1. 実在の店舗との一致（WebSearch、検索日 2026-10-11）

| 検索語 | 対象 | 該当の有無 | 主な結果とURL |
|---|---|---|---|
| `"〇〇食堂"` | 〇〇食堂（見本） | 「〇〇食堂」という名の店は見つからず | 「地名＋食堂」型の店名の例（まいどおおきに食堂 https://ranking.net/items/05d66c ）、食べログの「食堂」一覧（https://tabelog.com/tw/R8708/rstLst/teishoku/38/ ）だけ |
| `"○○食堂" 店舗` | 同上 | 同上 | 熊本市の助成金申請書の記載例で「○○食堂」が伏せ字として使われている（https://www.city.kumamoto.jp/kiji0034849/5_4849_351222_up_RY2407HD.pdf ）。ほかは別名の店（食堂くく https://hamoni.jp/shop/0PqbMKJCcs3v29kLekfB 、最強食堂 https://aumo.jp/articles/45315 など） |
| `"まるまる食堂"` | 「〇〇」の読み | 完全一致の店は見つからず | 似た名前の別店（まるみ食堂 https://retty.me/restaurant/100001346910/ 、まるは食堂 https://epark.jp/shopinfo/jsp629799/ ） |
| `"Sample" "Shokudo" restaurant name trademark` | (Sample) ○○ Shokudo | 一致なし | "Shokudo" を含む米国の登録商標（下の 2.）が出ただけ |
| `"样本" "○○食堂"` | （样本）○○食堂 | 一致なし | 上の熊本市の記載例と、「食堂」の辞書の説明（https://hbreader.org/words/10388.html ）だけ |
| `"○○ 식당" 견본` | (견본) ○○ 식당 | 一致なし | 飲食店のチラシ・メニューのテンプレート集（https://carat.im/de/prompt-gallery/restaurant-flyer など）だけ |

- 判断：4言語のどれも、一致する実在の店は検索の範囲では見つかりませんでした。
- 限界：WebSearch は米国向けの検索で、日本・中国・韓国の個人店を網羅していません。「見つからなかった」は「存在しない」の証明ではありません。

### 2. 登録商標（J-PlatPat）

- J-PlatPat は環境から接続できませんでした（2026-10-11）。
  - WebFetch `https://www.j-platpat.inpit.go.jp/` → `getaddrinfo ENOTFOUND www.j-platpat.inpit.go.jp`
  - curl（プロキシ経由）→ `curl: (56) CONNECT tunnel failed, response 403`
- 代替の WebSearch（2026-10-11）：
  - `"〇〇食堂" 商標登録 J-PlatPat` → 商標の情報は出ず、「食堂」の辞書の説明だけ（https://kotobank.jp/word/食堂 ）。
  - `"Sample" "Shokudo" restaurant name trademark` → 米国の登録例（HONOLULU SHOKUDO https://trademark.justia.com/863/83/honolulu-86383109.html 、SHINYA SHOKUDO https://trademark.justia.com/900/73/shinya-90073094.html ）では "SHOKUDO" の部分は一般語として権利の対象から外されている（ディスクレーム）。「〇〇食堂」「Sample Shokudo」そのものの登録は見つからず。
- 根拠（商標の問題がないと考える理由）：
  - 「〇〇／○○」は伏せ字の記号で、特定の名前を指しません。「食堂／Shokudo／식당」は一般名詞です。
  - 4言語とも「（見本）／(Sample)／（样本）／(견본)」を常に併記しています。
  - 商品名・ロゴ・出品タイトルには使いません。
  - ※以上は推測を含みます。J-PlatPat で直接確認したものではありません。

### 未確認の点

- J-PlatPat での直接の検索（「〇〇食堂」「食堂」）。人が別の端末から確認する必要があります。
- 中国・韓国の商標データベースは調べていません。
