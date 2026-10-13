# NAKAGAWA RIVER NIGHTS 告知動画（実験版・15秒・横型1920×1080）

| ファイル | 役割 |
|---|---|
| `scene.py` | Blender（EEVEE）で夜の那珂川を3D生成。橋・ステージの光は120BPMのビートで明滅 |
| `titles.py` | ffmpeg の drawtext でモーションタイポグラフィ（タイトル・キーワード・日付・エンドカード） |
| `bgm.py` | 仮BGMをPython標準ライブラリだけで合成（120BPM、権利フリー） |
| `build.sh` | 上記をまとめて mp4 に書き出す |

必要なもの：Blender 4.x、xvfb-run（画面のない環境でEEVEEを動かすため）、ffmpeg、python3。
本番では BGM をプロの楽曲に差し替える前提。タイトル・日程は仮。
