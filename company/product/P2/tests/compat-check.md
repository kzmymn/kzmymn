# P2 原価率計算シート — 互換性の検査結果

- 対象: `dist/genka-keisan.xlsx`
- 実行日時: 2026-10-11 10:23
- 方法: xlsx（zip）内の XML を直接読み、全セルの数式・入力規則・条件付き書式を走査（`tests/compat_check.py`）
- 許可リスト: AND, IF, IFERROR, INDEX, ISBLANK, MATCH, OR, ROUND, ROUNDDOWN, ROUNDUP, SUM, SUMPRODUCT, VLOOKUP

## 判定: OK（問題なし）

- 数式の数: 2682（入力規則の式を含む）
- 使っている関数: AND（100）, IF（5080）, IFERROR（2190）, OR（810）, ROUND（870）, ROUNDUP（30）, SUM（30）, VLOOKUP（1350）
- 入力規則: 2 件、条件付き書式のルール: 2 件

| 確認項目 | 結果 |
|---|---|
| 許可リスト外の関数が無い | OK |
| 新しい関数（XLOOKUP, LET, LAMBDA, FILTER など。_xlfn 付き）が無い | OK |
| 配列数式・動的配列が無い | OK |
| 外部参照・構造化参照（[ を含む式）が無い | OK |
| マクロ・テーブル・外部データ接続のパーツが無い | OK |
| 名前付き範囲が無い | OK |
| シート保護・ブック保護（パスワード）が無い | OK |
| 入力規則のリストはセル範囲の参照だけ | OK |
| 条件付き書式は単純なセル値の条件だけ | OK |

## 入力規則と条件付き書式の中身

- xl/worksheets/sheet2.xml 入力規則（リスト） E5:E104 → '設定'!$B$11:$B$12
- xl/worksheets/sheet3.xml 入力規則（リスト） B7:B21 B32:B46 B57:B71 B82:B96 B107:B121 B132:B146 B157:B171 B182:B196 B207:B221 B232:B246 B257:B271 B282:B296 B307:B321 B332:B346 B357:B371 B382:B396 B407:B421 B432:B446 B457:B471 B482:B496 B507:B521 B532:B546 B557:B571 B582:B596 B607:B621 B632:B646 B657:B671 B682:B696 B707:B721 B732:B746 → '材料マスタ'!$B$5:$B$104
- xl/worksheets/sheet3.xml 条件付き書式 E4:E754: セルの値 equal "超過"
- xl/worksheets/sheet4.xml 条件付き書式 H5:H34: セルの値 equal "超過"

## この環境で行った検査と、行っていない検査

- **行った**: 上の静的検査（全数式の関数名を許可リストと照合）と、LibreOffice での再計算テスト（`tests/result.md`）。
- **行っていない**: Microsoft Excel と Google スプレッドシートでの実機確認。この環境にはどちらも無いため、実際に開いて同じ値になるかは未確認。手順は `device-check.md`（創業者が5分で確認）。
- 補足: 許可リストの関数は、Excel と Google スプレッドシートの両方の公式関数一覧にある基本関数（Excel: https://support.microsoft.com/en-us/office/excel-functions-alphabetical-b3944572-255d-4efb-bb96-c6d90033e188 、Google: https://support.google.com/docs/table/25273?hl=en ）。実際に使っているのは上の「使っている関数」だけ。ROUNDUP は依頼の例示リストに無いが、推奨売価の10円単位の切り上げに使うため許可リストに加えた（Google スプレッドシートにもある）。
- 出典 URL の確認方法: この環境からは上の URL を開けず（プロキシで拒否）、本文は未閲覧。関数の選定は一般的な知識と検索結果に基づく。URL の生存と内容は未確認【要確認】。
- 補足: 同梱ファイルは openpyxl で作るため、計算結果の値をファイルに保存していない（開いたときに再計算させる設定 fullCalcOnLoad を付けている）。Excel と Google スプレッドシートでは開くと計算されるが、スマホのファイルプレビューなど計算しないビューアでは数式のセルが空に見える。
