# P3 見本データで使った名前の一覧

- 作成：2026-10-11（engineer）
- 対象：`dist/` の allergen-ichiran.xlsx（全シート）、allergen-ichiran-print-sample.pdf、README.txt
- 確認の方法：`build.py` の見本データと文言を目で確認しました。また、PDF の文字を pdfplumber で取り出して確認しました。
- 結果：固有名詞は、見本の店名「〇〇食堂（見本）」の1件だけです。人名・住所・電話番号・実在の店名はありません。見本以外の固有名詞（対応ソフト名、ファイルの作成者「MenuBridge」、フォント名など）は末尾の確認記録の 0. を参照（2026-10-11 CEO 修正）。

## A. 固有名詞

| 名前 | 使った場所 | 種類 | 架空だとわかる理由 |
|---|---|---|---|
| 〇〇食堂（見本） | xlsx「入力」B2、「お客様用」A1 の表題（数式で表示）、print-sample.pdf の表題、README.txt、xlsx「使い方」 | 店名 | 名前の部分が伏せ字の「〇〇」で、「（見本）」と書いてある |

## B. 固有名詞ではないもの（念のため載せます）

| 名前 | 使った場所 | 種類 | 理由 |
|---|---|---|---|
| 鶏の唐揚げ | 「入力」「お客様用」1行目、PDF | 料理名 | 一般的な料理名 |
| 野菜サラダ（ごまドレッシング） | 「入力」「お客様用」2行目、PDF | 料理名 | 一般的な料理名 |
| ざるそば | 「入力」「お客様用」3行目、PDF | 料理名 | 一般的な料理名 |
| 店長（見本） | 「入力」の確認者（AG6・AG7） | 役職 | 人名ではなく役職に「（見本）」を付けたもの |
| 29品目の名前と訳（えび、Shrimp、虾、새우 など） | 「品目リスト」ほか | 食品の一般名 | 消費者庁の資料にある品目名と、その参考訳 |
| 消費者庁 | 「使い方」「品目リスト」「お客様用」の注意書き | 行政機関 | 出典として名前と URL を書いた。ロゴや書式は使っていない |

## C. テストだけで使った名前（購入者には渡しません）

`tests/cases.py` では「テスト店」「山田」「A定食」「メニュー1〜50」などを使っています。これらは一時ファイルの中だけで使い、`dist/` には入りません。

## 実在・商標の確認（researcher, 2026-10-11）

### 0. names.md に漏れていた名前（dist/ を見直した結果）

`dist/allergen-ichiran.xlsx`（openpyxl で全シートのセル・数式内の文字・入力規則・ヘッダー/フッター・コメント・ファイルのプロパティ）、`dist/README.txt`、`dist/allergen-ichiran-print-sample.pdf`（プロパティと埋め込みフォント）を確認しました。セル・入力規則・コメントには、上の表 A・B 以外の固有名詞はありませんでした（コメントはなし、フッターは「&Pページ」だけ）。次の名前が漏れていました。

| 名前 | 使った場所 | 種類 | 購入者から見えるか |
|---|---|---|---|
| MenuBridge | xlsx のファイルのプロパティ「作成者」（docProps/core.xml の dc:creator）、PDF のプロパティ「作成者（Author）」、README.txt「制作について」、listing「仕様・制作について」と根拠メモ（HTML コメント） | 当社の仮の社名 | README・listing は見える（本文）。プロパティはファイルのプロパティを開くと見える |
| Microsoft Excel／Excel | README.txt「同梱ファイル」（「Excel ブック」）・「対応ソフト」・「商標について」（「Microsoft Excel」の表記で商標の注記）、xlsx「使い方」A35、listing「対応ソフト・動作環境」・「よくある質問」・差し替え文と根拠メモ（HTML コメント） | 他社の製品名（登録商標） | 見える（本文）。※以前の版にあった「Windows、Mac」は、README・xlsx・listing のどこにも出てこないため、2026-10-11 にこの行から削除 |
| Google スプレッドシート、Google ドライブ | README.txt「対応ソフト」・「商標について」（商標の注記）、xlsx「使い方」A36・A44〜A45、listing「対応ソフト・動作環境」・「よくある質問」・差し替え文と根拠メモ（HTML コメント） | 他社の製品名（商標） | 見える（本文） |
| Microsoft（Microsoft グループ） | README.txt「商標について」（「Microsoft グループの」） | 他社の会社名 | 見える（本文）。商標の注記で権利者として名前を書いているだけ |
| Google LLC | README.txt「商標について」（「Google LLC の」） | 他社の会社名 | 見える（本文）。同上 |
| Microsoft Excel Compatible / Openpyxl 3.1.5 | xlsx の docProps/app.xml「Application」 | 作成ツール名（openpyxl が自動で書く） | ふつうは見えない |
| Calc、LibreOffice 24.2 | PDF のプロパティ「Creator」「Producer」 | 作成ツール名（自動） | PDF のプロパティで見える |
| Carlito、WenQuanYi Zen Hei、Inter | PDF の埋め込みフォント（pdffonts で確認） | フォント名 | PDF のプロパティで見える |
| LibreOffice（LibreOffice 24.2.7.2） | README.txt「制作について」（「LibreOffice での再計算テスト 15 項目」）・「対応ソフト」（「LibreOffice で再計算テストをしています」）、listing 本文「対応ソフト・動作環境」（2か所）・「仕様・制作について」（1か所）と HTML コメント（差し替え文・根拠メモ）。PDF のプロパティ（上の行）とは別に、本文で名前を出している | 他者のソフト名（The Document Foundation。商標） | 見える（本文） |
| メイリオ（Meiryo） | listing 本文「対応ソフト・動作環境」（3か所）、xlsx の指定フォント（xl/styles.xml の font name="Meiryo"。セルの文字の書式） | フォント名（Microsoft の製品。商標） | listing は見える。xlsx はフォント欄で見える |
| BOOTH | README.txt「お問い合わせ」（「BOOTH の商品ページ」「BOOTH のメッセージ機能」）、listing の見出し「P3 販売ページ（BOOTH）下書き」と根拠メモ（HTML コメント）。販売ページそのものも BOOTH 上に載る | 販売サイト名（ピクシブ株式会社のサービス。商標） | 見える（本文） |
| Microsoft 365 | listing の HTML コメント（実機確認後の差し替え文の例「例：Microsoft 365」）。今の公開文には出ない | 他社の製品名（商標） | 今は見えない。差し替え後に書けば見える |
| XLOOKUP、IF、COUNTIF、COUNTBLANK、ISBLANK、AND、OR | listing 本文「対応ソフト・動作環境」、README.txt「対応ソフト」 | 表計算の関数名 | 見える（本文）。一般的な関数名で、商品名としては使っていない |
| Calibri | xlsx の既定のフォント（xl/styles.xml。openpyxl が自動で入れる。値の入ったセルでは使っていない） | フォント名（Microsoft。商標） | ふつうは見えない |

- 追記（researcher、2026-10-11、QA 修正依頼1回目）：上の LibreOffice（本文）〜Calibri の6行を追加しました。`company/content/P3/listing.md` の本文（HTML コメントを含む）の英字の語と「メイリオ」「BOOTH」「消費者庁」を機械的に抜き出して確認し（grep）、xlsx の書式のフォント名は styles.xml から確認しました。上の表の Excel・Google スプレッドシート・Google ドライブ・MenuBridge も listing 本文で使っています（「対応ソフト・動作環境」「よくある質問」「仕様・制作について」）。Windows・Mac は listing・README・xlsx のどこにも出てきません（2026-10-11 に grep で確認し、この文から削除）。消費者庁は表 B のとおり、listing 本文でも出典として名前と URL を書いています。listing の根拠メモ（HTML コメント、公開しない）に出る「岡山県」は出典の説明で、購入者には見えません。
- 追記（researcher、2026-10-11、QA 修正依頼2回目）：README.txt「商標について」の欄を使用場所として各行に加え、そこで権利者として書いている「Microsoft（グループ）」「Google LLC」を表に加えました（以前は下の 3. の説明にしかありませんでした）。注記の文言は writer が修正中のため、文言ではなく欄（場所）として記録しています。Excel の行にあった「Windows、Mac」は、今の README・xlsx・listing に出てこないため削除しました。LibreOffice の行に README.txt「対応ソフト」を加えました。確認の方法：README.txt、xlsx の全シートのセル（openpyxl で文字列を全件出力）と入力規則、`company/content/P3/listing.md` を、Microsoft・Google・Excel・LibreOffice・BOOTH・MenuBridge・メイリオ・365・Windows・Mac・Apple・iPhone・Android・LLC・商標で grep。Windows・Mac・iPhone・Android は 0件、xlsx の「Apple」「Mac…」は品目リストの訳（りんご、さば、マカダミアナッツ）でした。
- 追加した名前の実在・商標の確認（J-PlatPat）は、下の 2. と同じ理由で未実施です。LibreOffice・メイリオ・BOOTH・Microsoft 365・Calibri は、対応環境・作成の説明・問い合わせ先として名前を書いているだけで、ロゴや商品名には使っていません。判断は下の 3.・4. と同じ（互換性・事実の説明の範囲。推測）。

### 1. 実在の店舗との一致（WebSearch、検索日 2026-10-11）

- 「〇〇食堂（見本）」は P1・P2 と同じ名前のため、検索の記録は `company/product/P1/names.md` と `company/product/P2/names.md` の「実在・商標の確認」を参照（一致する実在の店は見つからず、公的書類でも「○○食堂」は伏せ字として使われている）。
- P3 の用途での追加検索：`"〇〇食堂" 見本 アレルゲン一覧表` → 「〇〇食堂」という名の店・見本は見つからず。出てきたのは公的機関のアレルゲン献立表（島根県 https://www.pref.shimane.lg.jp/education/kyoiku/kikan/shonenshizen/shokudomenu2/shokudomenu08.html 、宮城県 https://www.pref.miyagi.jp/documents/50721/r7_8_allergy.pdf 、浦安市 https://www.city.urayasu.lg.jp/_res/projects/default_project/_page_/001/033/576/2026mikata.pdf など）だけ。
- 「店長（見本）」は役職名、料理名（表 B）は一般名詞のため、個別の検索はしていません。
- 限界：WebSearch は米国向けで、日本の個人店を網羅していません。「見つからなかった」は「存在しない」の証明ではありません。

### 2. 登録商標（J-PlatPat）

- J-PlatPat は環境から接続できませんでした（2026-10-11 に再試行）。
  - WebFetch `https://www.j-platpat.inpit.go.jp/` → `getaddrinfo ENOTFOUND www.j-platpat.inpit.go.jp`
  - curl（プロキシ経由）→ `curl: (56) CONNECT tunnel failed, response 403`（プロキシの記録は connect_rejected）
- 「〇〇食堂」：P1・P2 の代替検索の結果を参照（「〇〇食堂」「Sample Shokudo」そのものの登録は見つからず）。根拠は P1・P2 と同じ（伏せ字＋一般名詞、常に「（見本）」を併記、商品名・ロゴに使わない）。※推測を含み、J-PlatPat で直接確認したものではありません。
- 「MenuBridge」：P2 の「3. MenuBridge」を参照（WebSearch では商標登録・出願を示すページは見つからず、J-PlatPat は未確認）。P3 では xlsx に加えて PDF のプロパティにも入っています。屋号として使い続けるなら、創業者が J-PlatPat で確認してから使うのが安全です（推測）。プロパティを空欄にするかどうかの判断は創業者・engineer に任せます。

### 3. 他社の製品名（Excel、Google スプレッドシート、Google ドライブ）

これらは実在の他社の商標です（Microsoft・Excel は Microsoft、Google スプレッドシート・Google ドライブは Google）。※以前の版にあった Windows（Microsoft）・Mac（Apple）は、今の README・xlsx・listing に出てこないため、2026-10-11 に削除しました。P3 では「対応ソフト」と使い方の説明として本文で名前を書いているだけで、ロゴ・アイコン・画面写真は使っていません（xlsx・PDF・README を確認）。

- Microsoft の商標ガイドライン（WebFetch、2026-10-11）https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general
  - 互換性を正しく書くことは認めている（"Note if your product ... is interoperable or compatible with a Microsoft product"）。
  - 自社の商品名・社名に Microsoft の名前を入れるのは不可。提携・推奨されていると思わせる書き方も不可。
  - 自社の名前より目立たせない。商標の注記（"Microsoft ... are trademarks of the Microsoft group of companies."）を付けることを勧めている。
- Google（WebSearch、2026-10-11。about.google は WebFetch で `ENOTFOUND` となり本文は直接読めず）
  - 製品名を自社の商品名・社名に入れない。互換性を示す "for"／"compatible with" は可（Workspace Marketplace のガイドライン https://developers.google.com/workspace/marketplace/terms/branding ）。
  - 商標を使うときは「[製品名] is a trademark of Google LLC」の注記と、提携していないことの表示を勧めている（https://about.google/brand-resource-center/guidance/media 、使い方のルール https://about.google/brand-resource-center/rules ）。
- 判断（推測を含む）：README・使い方での「対応ソフト」としての記載は、互換性の説明の範囲で問題は小さいと考えます。ただし、
  - 商品名・出品タイトル・サムネイルに「Excel」「Google スプレッドシート」を入れる場合は、「Excel・Google スプレッドシート対応」のような互換性の表現にとどめ、ロゴは使わないこと。
  - README に商標の注記を入れる案は、README.txt「商標について」の欄として反映済みです（2026-10-11 確認。文言は writer が修正中）。
  - 出品タイトルは `company/marketing/2026-10-11-listing-plan.md` の担当（marketer）が上の点を確認する必要があります。

### 4. 作成ツール名・フォント名（自動で入ったもの）

- openpyxl・LibreOffice（Calc）は作成に使ったソフトの名前が自動で記録されたもので、商標として使っているわけではありません。問題は小さいと考えます（推測）。
- PDF の埋め込みフォントのライセンス（WebSearch、2026-10-11）：
  - Carlito：SIL Open Font License 1.1（https://www.fontsquirrel.com/license/carlito ）
  - Inter：SIL Open Font License 1.1（https://www.fontsquirrel.com/license/inter ）
  - WenQuanYi Zen Hei：GPL-2 にフォント埋め込みの例外付き（埋め込んだ文書は GPL の対象にならない）（https://metadata.ftp-master.debian.org/changelogs/main/f/fonts-wqy-zenhei/stable_copyright ）
  - どれも PDF への埋め込み・同梱は認められていると読めます（推測。各ライセンス本文の確認は engineer に任せます）。

### 未確認の点

- J-PlatPat での直接の検索（「〇〇食堂」「食堂」「MenuBridge」）。人が別の端末から確認する必要があります。
- Google の商標ガイドラインの本文（about.google）は環境から開けず、検索結果の要約での確認です。
- names.md の冒頭の「結果」は、上の 0. に合わせて CEO が修正済み（2026-10-11）。
