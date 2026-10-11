# progress.md — 第3週のハンドオフ（2026-10-11）

## 要約

最初の商品3点（P1 多言語メニュー、P2 原価率計算シート、P3 アレルゲン一覧表）を作り、販売ページ・出品計画まで用意した。
計算テスト（P2 19/19、P3 15/15）と同梱物の一致チェックは全部合格。ただし **QA は3点とも未合格**（2回目：修正を依頼＋証拠不足）。
残る証拠不足は、BOOTH 規約・消費者庁・J-PlatPat の公式ページがこの環境から開けないこと、と Excel／Google の実機確認で、**AI では解消できない**。ゲートは緩めず、出品承認キューには載せていない。
AI 利用料が想定を超えたとの連絡を受け、修正2回目の後の QA 再審査は行わずに区切った。

## 会社

| 状態 | ノード |
|---|---|
| 完了 | リサーチ（BOOTH 規約〔抜粋ベース〕、競合・アレルゲン制度・互換性）、制作（P1〜P3）、コンテンツ（販売ページ3・同梱 README 3）、マーケ（出品計画・価格案）、組織（10月の見直し） |
| 実行中 | 品質ゲート（修正2回目まで実施。QA の3回目の再審査が未実施） |
| ブロック中 | 出品（A1〜A3 未処理）、QA 合格（A6〜A10：規約・品目・商標・実機の確認） |

## 出力

- 調査：`company/research/platform-rules.md`（BOOTH 規約。本文未閲覧）、`company/research/2026-10-11-first-products.md`
- 商品：`company/product/P1/`、`P2/`、`P3/`（同梱物は各 `dist/`、配布用 zip は各 `<ID>.zip`、`MANIFEST.md`、`names.md`、テストは `tests/`、実機確認手順は `device-check.md`）
- 販売ページ：`company/content/P1/listing.md`、`P2/listing.md`、`P3/listing.md`
- 出品計画：`company/marketing/2026-10-11-listing-plan.md`
- 検査スクリプト：`company/ops/scripts/build_manifest.py`、`check_listing.py`
- 組織見直し：`company/org/review-2026-10.md`（`.claude/agents/*.md` に反映）
- 週次レポート：`company/reports/2026-10-11.md`

## 意思決定

- 過去の QA 指摘4点を先回りで潰す仕組みを入れた：規約は `platform-rules.md` に一次資料URLと確認日、固有名詞は `names.md`、同梱物は `dist/`＋自動生成の `MANIFEST.md`＋`check_listing.py`、xlsx は LibreOffice 再計算＋関数の許可リスト検査。
- 見本の店名は「〇〇食堂（見本）」に統一（実在店の検索で一致なし。商標は未確認）。
- 新しい役職は採用しない（recruiter の結論。不足は役職でなく証拠の置き場所だった）。recruiter の Web ツールは残す。
- 販売ページには、検証した事実だけを書く（「Excel 対応」「スマホ対応」「最新」「法令対応」は使わない）。
- 規約本文を読めないため、AI 利用は安全側で自主開示する（販売ページの「仕様・制作について」と README 冒頭）。
- P1 の辞書の見出し語「落花生」は、既存 CSV との互換のため変えない（P3 は「落花生（ピーナッツ）」）。
- 利用料の超過を受け、QA の3回目は次回に回した。運用ルールの上限（修正ラウンド2回・サブエージェント10体）は、オーケストレーターの提案として A11 に載せた（創業者の承認後に `ops/weekly-routine.md` に反映）。

## 創業者からの承認（必要）

`approvals.md` の A1〜A4（初期設定）に加えて：
- **A6**（推奨）：ネットワーク許可（booth.pm、caa.go.jp、j-platpat など6ドメイン）。または A7・A8 を自分で確認
- **A9**：J-PlatPat で「MenuBridge」「〇〇食堂」の商標検索
- **A10**：Excel／Google スプレッドシートで P2・P3 を開く実機確認（各 device-check.md）
- **A11**：運用ルールの上限を入れるかどうか

## 次のアクション（次回の Routine で実行）

1. qa：P1〜P3 を再審査（3回目）。2回目の修正（README の商標注記の文言、names.md、compat-check の記述、device-check）が解消したかを確認する。
2. researcher：A6 が済んでいれば、BOOTH 規約・消費者庁の品目・J-PlatPat を一次資料で確認し、`platform-rules.md` と各 `names.md` を更新する。
3. writer／engineer：A7〜A10 の結果を反映する（実機確認が済めば「対応ソフト」の表記を差し替え、品目が変わっていれば P1・P3 を直す）。
4. qa が合格したものを `approvals.md` の「出品・公開の承認」に載せる（価格は出品計画の案）。
5. 新商品は作らない（3点の出品準備を優先）。

ブロッカー継続：はい（A1〜A3 が未処理。来週も未処理で「はい」なら、停止条件により Routine を止めて報告だけにする）
