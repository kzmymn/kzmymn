# progress.md — 第2週のハンドオフ

## 要約

創業者の方針（「自分は口座・アカウントだけ。手離れのいい事業を、AIの組織で自律的に」）に合わせて事業を切り替えた。
**小規模飲食店向けの業務テンプレートを BOOTH で販売する事業**に決め、7役職のAIエージェント組織と、週1回の自動実行の仕組みを作った。

## 会社

| 状態 | ノード |
|---|---|
| 完了 | リサーチ（手離れ型の事業選定）、組織設計（7役職の定義）、運用設計（週次 Routine） |
| 次に実行 | 制作（最初の商品3点） |
| ブロック中 | 出品（創業者の BOOTH 開設待ち：`approvals.md` A1〜A3） |
| 休止 | 店舗営業型の受託（創業者の営業が必要なため） |

## 出力

- `company/research/hands-off-selection.md` — 手離れ型事業の比較と選定
- `.claude/agents/*.md` — researcher, designer, writer, engineer, marketer, qa, recruiter
- `company/org/README.md` — 組織図と共通ルール
- `company/ops/weekly-routine.md` — CEO（週次 Routine）のプロンプト
- `company/approvals.md` — 創業者の承認キュー
- `company/state/index.md` — 成果物台帳
- `company/finance/sales.md` — 販売・財務台帳

## 意思決定

- 主力はデジタルテンプレート、集客は無料Webツール。KDPは第3候補として保留。
- AIストック素材・訪日アフィリエイト・LINEスタンプは不採用（受付終了、スパム対策、低単価）。
- BOOTHの大量出品規制に合わせ、新商品は週3点までにした。
- 制作と検査を分けた（QAは読み取り専用で、自分では直さない）。

## 創業者からの承認（必要）

`approvals.md` の初期設定 A1〜A4（BOOTH開設、口座、特商法表記、開業届の確認）。

## 次のアクション（次回の Routine で実行）

1. researcher：商品候補1〜3（多言語メニューのテンプレート、原価率計算シート、アレルゲン一覧表）の競合価格と不満点を調べる。
2. engineer／designer：商品1〜3のファイルを作る（第1週のデモを商品1に転用）。
3. writer：販売ページ文とマニュアルを書く。
4. marketer：BOOTH用のタイトル・タグ・価格を決める。
5. qa：判定し、合格したものを承認キューに載せる。

ブロッカー継続：いいえ（今週が初回）
