# コンセプト1枚スライド（A4横）

| ファイル | 内容 | Illustratorでの扱い |
|---|---|---|
| `slide.pdf` | 完成スライド（A4横）。「土台 × 本事業が加えるもの ＝ 文化景観」の式を軸に構成。文字・図形はベクター、挿絵は画像 | 開いて文字・図形をそのまま編集可 |
| `slide.png` | プレビュー画像 | — |
| `hero.png` | three.js（WebGL）で描いた3Dビジュアル（透過PNG・2400×1100） | 配置画像として使用 |
| `hero-vector.svg` | 同じ3Dシーンを three.js の SVGRenderer でベクター書き出し | 線・図形を個別に編集可（パス数が多いので重め） |
| `venn.svg` / `venn.pdf` | コンセプトの構造図（円の重なり） | 色・文字を編集可 |

再生成：`node render-hero.js hero.html <three.module.js> hero.png`、
ベクター版は `node render-hero.js hero-vector.html <three.module.js> hero-vector.svg <three/examples/jsm>`。

※ `hero*.png/svg`・`venn.*` は前の版の素材。現行の `slide.pdf` では使っていない。
