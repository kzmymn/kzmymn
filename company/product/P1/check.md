# P1 多言語メニューのテンプレート — 検証記録

- 実施日：2026-10-11（designer）
- 環境：Playwright（Node, グローバル導入版）＋ Chromium（/opt/pw-browsers, chromium-1194）。CJK フォントは WenQuanYi Zen Hei。
- 検証スクリプトはスクラッチパッドで実行（成果物には含めない）。

## 1. 自動チェック

| 項目 | 方法 | 結果 |
|---|---|---|
| 外部通信なし（実行時） | Playwright で4言語を開き、`file:` `blob:` `data:` 以外のリクエストを記録 | 0件 |
| 外部参照なし（ソース） | `grep -c -iE "https?://" dist/menu-template.html` | 0件。`<link>` `@import` `src=` `url(` もなし（`URL.createObjectURL` はCSV保存用のローカル処理） |
| JSエラー | `console.error` / `pageerror` を記録 | 0件 |
| 翻訳の欠け | HTML 内の自己チェック（画面の黄色い枠に表示） | 「9品 × 4言語、訳の欠けはありません」 |
| CSV 往復 | `menuToCSV(MENU)` → `csvToMenu()` が元データと一致するか | 一致（true） |
| CSV 取り込み（UI） | テキスト貼り付け／ファイル選択の両方で menu-data.csv を読み込み | 9品を読み込み、表示も正常 |
| CSV 取り込み（Shift_JIS） | Excel の「CSV（カンマ区切り）」相当の cp932 ファイルを選択 | 自動で Shift_JIS として読み直し、日本語は正常（中・韓の文字は Shift_JIS では保存できないため「?」になる。README で「CSV UTF-8」保存を案内） |
| スマホ 390px のはみ出し | `scrollWidth` と料理名・価格・説明の要素幅を比較 | 4言語とも横はみ出し0件（ページ幅 390 = 画面幅 390） |
| 印刷時の最小文字サイズ | 印刷メディアで、印刷される全テキストの computed font-size の最小値 | 4言語とも 13.33px = **10.0pt**（10pt 未満なし）。本文 10.5pt、料理名 11.5pt |
| 改ページ | 36品（見本の4倍）を CSV で読み込み A4 PDF 化 | 3ページ。料理の途中で改ページされない（`break-inside: avoid`）。見出しだけがページ末に残らない |
| CSV の BOM | `head -c3 \| od -tx1` | menu-data.csv / phrases.csv / README.txt とも `ef bb bf`（UTF-8 BOM 付き） |
| PDF | `pdfinfo` / `pdftotext` | sample-print.pdf：A4・4ページ（日・英・中・韓 各1ページ）。テキスト抽出で文字化けなし |

## 2. 目視確認（スクリーンショット）

保存先：`company/product/P1/screenshots/`

| ファイル | 内容 | 文字化け | はみ出し | 備考 |
|---|---|---|---|---|
| mobile-390-ja.png | スマホ 390px・日本語 | なし | なし | 編集用の黄色い枠が上に出る（印刷されない） |
| mobile-390-en.png | スマホ・英語 | なし | なし | 日本語名を小さく併記 |
| mobile-390-zh.png | スマホ・中国語簡体字 | なし | なし | |
| mobile-390-ko.png | スマホ・韓国語 | なし | なし | 長いラベル（알레르기 유발 성분）も折り返して収まる |
| print-a4-ja.png | A4 印刷（PDF の1ページ目を画像化） | なし | なし | 2段組み、1ページに収まる |
| print-a4-en.png | A4 印刷・英語 | なし | なし | |
| print-a4-zh.png | A4 印刷・中国語 | なし | なし | |
| print-a4-ko.png | A4 印刷・韓国語 | なし | なし | |

- 目印（おすすめ、辛さ、アルコール等）は枠付きの文字、アレルゲンは「アレルゲン: 小麦、大豆」の文字で表示。色だけで区別している情報はない（印刷時は白黒）。
- 選択中の言語ボタンは色に加えて「✓」と太字で示す。

## 3. 名前・権利の確認

- 見本の店名は「〇〇食堂（見本）」/「(Sample) ○○ Shokudo」/「（样本）○○食堂」/「(견본) ○○ 식당」。
- `grep -rn -E "麺処|さくら|Sakura|樱|사쿠라" company/product/P1` → 0件（第1週デモの店名は不使用）。
- 料理名は一般名のみ（唐揚げ定食、生姜焼き定食など）。画像・イラスト・外部素材は使っていない（サムネイルは自作HTMLのスクリーンショットと単色の図形のみ）。

## 4. 未解決・注意

- 中国語・韓国語（英語も）の訳はネイティブ未確認の参考訳。HTML の編集用枠と README.txt に明記済み。
- PDF には環境のフォント（WenQuanYi Zen Hei、Inter）がサブセット埋め込みされている。いずれもオープンなライセンス（WenQuanYi は GPL＋フォント例外、Inter は SIL OFL）だが、**推測**であり qa でライセンス確認を推奨。
- 実機（iPhone Safari / Android Chrome / Windows の Excel）では未検証。Chromium のみ。
- 購入者の環境では OS 標準フォントで表示されるため、見た目（字形・行の折り返し）はスクリーンショットと多少異なる。

## 5. PDF に埋め込まれたフォントのライセンス（追記）

確認の方法：環境に入っている Debian パッケージに同梱されたライセンス文書を読みました（`/usr/share/doc/<パッケージ>/copyright`）。`fc-query` の結果には copyright や license の項目が出なかったため、ここでは使っていません。

| フォント | ファイル | 同梱文書に書かれた権利者 | 同梱文書に書かれたライセンス |
|---|---|---|---|
| WenQuanYi Zen Hei | /usr/share/fonts/truetype/wqy/wqy-zenhei.ttc | 2007-2009, Qianqian Fang and The WenQuanYi Project Board of Trustees | 「GPL-2 with Font embedding exception and M+ FONTS License」（`/usr/share/doc/fonts-wqy-zenhei/copyright`） |
| Inter | /usr/share/fonts/opentype/inter/*.otf | 2016-2023 The Inter Project Authors | 「OFL-1.1 and Apache-2.0」。フォントファイル自体は OFL-1.1 の条文が同梱されている（`/usr/share/doc/fonts-inter/copyright`） |

- WenQuanYi Zen Hei：上の文書には GPL のフォント埋め込み例外の文（"As a special exception, if you create a document which uses this font, and embed this font or unaltered portions of this font into the document, this font does not by itself cause the resulting document to be covered by the GNU General Public License"）が含まれています。このため、PDF にサブセットを埋め込んでも、PDF そのものが GPL の対象になることはないと読めます。
- Inter：OFL-1.1 は、文書への埋め込みを認めています。
- 上の2点は、同梱文書を読んだうえでの解釈です。法的な最終判断ではありません。
- 4. に書いた「推測」は、この確認で置き換えます。

## 6. 未解決（追記）

- `designer.md` の更新で、`company/ops/scripts/build_manifest.py` を使って MANIFEST.md を生成することが求められています。
- しかし、このスクリプトはリポジトリにまだありません。そのため MANIFEST.md は生成していません（2026-10-11 時点）。
