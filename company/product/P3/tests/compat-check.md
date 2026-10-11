# P3 アレルゲン一覧表 — 互換性の検査結果

- 対象: `dist/allergen-ichiran.xlsx`
- 実行日時: 2026-10-11 10:23
- 方法: xlsx（zip）内の XML を直接読み、全セルの数式・入力規則・条件付き書式を走査（`tests/compat_check.py`）
- 許可リスト: AND, COUNTBLANK, COUNTIF, IF, IFERROR, INDEX, ISBLANK, MATCH, OR, SUM

## 判定: OK（問題なし）

- 数式の数: 1870（入力規則の式を含む）
- 使っている関数: AND（150）, COUNTBLANK（300）, COUNTIF（306）, IF（4951）, ISBLANK（201）, OR（100）
- 入力規則: 1 件、条件付き書式のルール: 5 件

| 確認項目 | 結果 |
|---|---|
| 許可リスト外の関数が無い | OK |
| 新しい関数（XLOOKUP, LET, LAMBDA, FILTER など。_xlfn 付き）が無い | OK |
| 配列数式・動的配列が無い | OK |
| 外部参照・構造化参照（[ を含む式）が無い | OK |
| マクロ・テーブル・外部データ接続のパーツが無い | OK |
| 名前付き範囲が無い（印刷タイトル・印刷範囲の組み込み名を除く） | OK |
| シート保護・ブック保護（パスワード）が無い | OK |
| 入力規則のリストはセル範囲の参照だけ | OK |
| 条件付き書式は単純なセル値の条件だけ | OK |

## 入力規則と条件付き書式の中身

- 印刷設定の組み込み名 _xlnm.Print_Titles → 'お客様用'!$1:$5
- 印刷設定の組み込み名 _xlnm.Print_Area → 'お客様用'!$A$1:$AF$55
- xl/worksheets/sheet3.xml 入力規則（リスト） C6:AE55 → '品目リスト'!$I$5:$I$7
- xl/worksheets/sheet3.xml 条件付き書式 C6:AE55: セルの値 equal "？"
- xl/worksheets/sheet3.xml 条件付き書式 C6:AE55: セルの値 equal "○"
- xl/worksheets/sheet3.xml 条件付き書式 AI6:AI55: セルの値 equal "未確認あり"
- xl/worksheets/sheet4.xml 条件付き書式 B6:AD55: セルの値 equal "？"
- xl/worksheets/sheet4.xml 条件付き書式 B6:AD55: セルの値 equal "○"

## この環境で行った検査と、行っていない検査

- **行った**: 上の静的検査（全数式の関数名を許可リストと照合）と、LibreOffice での再計算テスト（`tests/result.md`）。
- **行っていない**: Microsoft Excel と Google スプレッドシートでの実機確認。この環境にはどちらも無いため、実際に開いて同じ値になるかは未確認。手順は `device-check.md`（創業者が7分ほどで確認）。
- 補足: 許可リストの関数は、Excel と Google スプレッドシートの両方の公式関数一覧にある基本関数（Excel: https://support.microsoft.com/en-us/office/excel-functions-alphabetical-b3944572-255d-4efb-bb96-c6d90033e188 、Google: https://support.google.com/docs/table/25273?hl=en ）。実際に使っているのは上の「使っている関数」だけ。
- 出典 URL の確認方法: この環境からは上の URL を開けず（プロキシで拒否）、本文は未閲覧。関数の選定は一般的な知識と検索結果に基づく。URL の生存と内容は未確認【要確認】。
- 補足: 「お客様用」シートの印刷タイトル（各ページに1〜5行目を印刷）と印刷範囲は、Excel の組み込み名（_xlnm.Print_Titles / _xlnm.Print_Area）として保存される。利用者が作る名前付き範囲ではないため許可した。Google スプレッドシートはこの設定を読まない可能性がある【推測・要実機確認】ため、印刷時に「固定行を繰り返す」をオンにする手順を `使い方` シートと `device-check.md` に書いた。
- 補足: 品目名の見出しは縦書き（文字の向き＝縦。xlsx の textRotation=255）。LibreOffice の PDF では縦に並ぶことを確認した。Excel・Google スプレッドシートでの見え方は実機確認の項目。
- 補足: 同梱ファイルは openpyxl で作るため、計算結果の値をファイルに保存していない（開いたときに再計算させる設定 fullCalcOnLoad を付けている）。Excel と Google スプレッドシートでは開くと計算されるが、スマホのファイルプレビューなど計算しないビューアでは数式のセルが空に見える。
