# company/ops/scripts — 同梱物と販売ページの一致チェック

販売ページの記述と同梱物の不一致（QA 指摘）を機械的に防ぐためのスクリプト。全商品共通。Python 3 の標準ライブラリだけで動く。

## 決まりごと

- 購入者が受け取るファイルは、すべて `company/product/<ID>/dist/` に置く。dist 以外のものは同梱しない。
- 販売ページは `company/content/<ID>/listing.md`。中に「## 同梱物」セクションを作り、1ファイル1行で書く。

  ```markdown
  ## 同梱物
  - `genka-keisan.xlsx` — 原価率計算シート本体
  - `README.txt` — 同梱説明
  ```

## 1. build_manifest.py — 同梱物の一覧と配布用 zip を作る

```sh
python3 company/ops/scripts/build_manifest.py P2
```

- `company/product/P2/MANIFEST.md`：ファイル名・サイズ・SHA-256（先頭12桁）・形式
- `company/product/P2/P2.zip`：dist の中身だけ（フォルダ dist は入れない）。日本語のファイル名は UTF-8 で入れる
- dist に隠しファイル（`.DS_Store` など）があると、NG で止まる（終了コード 1）
- dist を変えたら、必ず再実行する

## 2. check_listing.py — 販売ページと同梱物を照合する

```sh
python3 company/ops/scripts/check_listing.py P2
echo $?   # 0 = OK、1 = NG、2 = ファイルが無く実行できない
```

確認すること:

1. MANIFEST.md と zip が、今の dist と同じか（古い MANIFEST のまま出品しない）
2. 「## 同梱物」の箇条書きのファイル名と、MANIFEST のファイル名が過不足なく一致するか
3. 販売ページ全体に、dist に無い形式が書かれていないか
   - 拡張子（`.pdf` `.csv` `.xlsx` など）→ その拡張子のファイルが dist にあるか
   - 形式・ソフト名（PDF、CSV、Excel、Google スプレッドシート、Word、PowerPoint、HTML、PNG、JPEG）→ 対応する形式のファイルがあるか
     （例：「Excel／Google スプレッドシート対応」には .xlsx などが必要。「PDF付き」には .pdf が必要）

NG のときは差分（販売ページにだけある／同梱物にだけある／どの行のどの記述か）を表示する。

「PDF は付いていません」のような否定の文で誤検知したら、その行の末尾に `<!-- check_listing: ignore -->` を付ける（使うのは必要なときだけ。QA が確認する）。

## 出品前の手順（CEO / QA）

1. `python3 company/ops/scripts/build_manifest.py <ID>`
2. `python3 company/ops/scripts/check_listing.py <ID>` が OK（終了コード 0）になることを確認
3. OK の出力を QA の判定の証拠に付け、承認キュー（`company/approvals.md`）に載せる。出品にアップロードするのは `<ID>.zip`
