# EP01｜携帯がない時代、待ち合わせに遅れたらどうしてた？

チャンネル軸（作業名）「スマホや携帯がなかった、ついこの前の暮らし」の初回。v3（テンポ重視）台本を v3.1 に整え、音声付きの全編を作った。**未公開**。

## 成果物（`out/`）

| ファイル | 内容 |
|---|---|
| `EP01-full.mp4` | 完成版の全編。1920×1080・30fps・H.264／AAC、**3分07秒**、-16 LUFS |
| `EP01-opening-45s.mp4` | 冒頭45秒（確認用。全編の冒頭と同じ映像） |
| `narration.wav` | ナレーション単体（48kHz・モノラル・-16 LUFS／ピーク -1.5 dBFS） |
| `EP01.ja.srt` | 日本語字幕（YouTubeにアップロード可。画面の字幕と同じ区切り・時刻） |
| `EP01-thumbnail.jpg` | サムネイル 1280×720 |
| `EP01-storyboard.jpg` | 全46ビートの静止画一覧（時刻と場面名つき） |
| `narration-timing.json` | ビートごとの開始・終了時刻、読み（カナ） |
| `asr-check.txt` | 音声認識による聞き取り検査の結果 |
| `narration-openjtalk-compare.m4a` | 比較用：別エンジン（Open JTalk）で読んだ同じ台本。未採用 |

文書（`docs/`）
- `script-v3.1.md` — 台本全文、v3からの変更点、各文と画面の対応、史実／架空の境界の検査
- `publish-pack.md` — タイトル案、概要欄（チャプター付き）、出典、使用ツールの権利、**公開前に人が確認すること**

## 作り方（編集可能なソース）

```
src/beats.py        台本の正本。1ビート＝字幕1枚＝音声1区間＝画面の1変化
src/narration.py    beats → 音声合成 → narration.wav ＋ timing.json
src/draw.py         線画の部品（人物・時計・公衆電話・家・駅・伝言板・矢印…）
src/render.py       timing に合わせて14場面を描き、MP4を書き出す
src/make_srt.py     timing → 字幕SRT
src/thumbnail.py    サムネイル
src/check_audio.py  音声認識で台本との一致を検査（人の耳の代わりではない）
fonts/              Noto Sans JP（SIL OFL）
```

台本を直したときの再生成（Linux／Mac共通。数分で終わる）:

```bash
cd EP01/src
python3 narration.py --model <Kokoroのモデルを置いたフォルダ>   # 音声と時刻表
python3 render.py --stills       # 各ビートの静止画を out/stills/ に（確認用）
python3 render.py                # 全編 out/EP01-full.mp4
python3 render.py --until 45 --name EP01-opening-45s
python3 make_srt.py
```

文言だけ直して読みを変えたいときは `beats.py` の `say` に読みやすい表記（ひらがな・漢数字）を書く。画面の字幕は `text` のまま。尺は音声から自動で決まり、画面の動き（矢印が伸びる、札が出る等）は「何という語を言い始めたか」に合わせて自動で動く（`render.py` の `S.at(k, "語")`）。

### 必要なもの（すべて無料）

- Python 3.10以上、FFmpeg
- `pip install pycairo pillow numpy soundfile pyopenjtalk kokoro-onnx jaconv mojimoji` と `pip install --no-deps misaki`
  （misaki の日本語処理が要求する fugashi/unidic は使わず、`narration.py` 内で Open JTalk に置き換えている）
- Kokoro のモデル2つ（約350MB、リポジトリには入れていない）:
  `kokoro-v1.0.onnx` と `voices-v1.0.bin` — https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0
- 検査を使う場合のみ: `pip install sherpa-onnx` と音声認識モデル `sherpa-onnx-zipformer-ja-reazonspeech-2024-08-01`
  — https://github.com/k2-fsa/sherpa-onnx/releases/tag/asr-models

検証済みの版：kokoro-onnx 0.6.1／misaki 0.7.4／pyopenjtalk 0.4.1／pycairo 1.29.2／sherpa-onnx 1.13.8。

## この制作環境について

- 作業はクラウド上のLinuxコンテナ（Claude Code）で行った。Macには接続していない
- 引き継ぎで添付されたはずの `EP01-Fast-v3.zip`（40秒見本・render_fast.py 等）と `EP01-Assets-v2.zip` はこの環境に届いていなかったため、**見本動画・旧コードは見ていない**。引き継ぎ文に全文があった v3 台本と画面設計表から作り直した
- リポジトリにあった `IMG_6300.jpg`（線画の人物）は出所が不明なため、素材として使っていない
- 有料サービス・API・契約は使っていない
