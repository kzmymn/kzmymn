"""音声の機械検査：ビートごとに切り出して日本語音声認識にかけ、台本との一致率を出す。

人の耳による聞きやすさ検査の代わりにはならない。読み間違い・欠落の発見用。
使い方: python3 check_audio.py WAV TIMING_JSON ASR_MODEL_DIR
ASR: sherpa-onnx-zipformer-ja-reazonspeech-2024-08-01
  (https://github.com/k2-fsa/sherpa-onnx/releases/tag/asr-models)
"""
import difflib, json, re, sys

import numpy as np
import sherpa_onnx
import soundfile as sf

wav, timing, d = sys.argv[1], sys.argv[2], sys.argv[3].rstrip("/") + "/"
rec = sherpa_onnx.OfflineRecognizer.from_transducer(
    encoder=d + "encoder-epoch-99-avg-1.int8.onnx", decoder=d + "decoder-epoch-99-avg-1.onnx",
    joiner=d + "joiner-epoch-99-avg-1.int8.onnx", tokens=d + "tokens.txt", num_threads=4)
a, sr = sf.read(wav, dtype="float32")
T = json.load(open(timing, encoding="utf-8"))


def kana(s):
    import pyopenjtalk
    return re.sub(r"[、。？！「」\s]", "", "".join(n["pron"].replace("’", "") for n in pyopenjtalk.run_frontend(s)))


scores = []
for b in T["beats"]:
    pad = np.zeros(sr, np.float32)  # 隣のビートを混ぜず、前後を1秒の無音で挟む
    seg = np.concatenate([pad, a[int((b["start"] - 0.12) * sr): int((b["end"] + 0.12) * sr)], pad])
    s = rec.create_stream(); s.accept_waveform(sr, seg); rec.decode_stream(s)
    hyp = s.result.text
    r = difflib.SequenceMatcher(None, kana(b["say"]), kana(hyp)).ratio()  # 読み（カナ）で比較
    scores.append(r)
    flag = "  " if r >= 0.9 else "!!"
    print(f"{flag}{b['i']:02d} {r:.2f} {hyp}")
print(f"mean {np.mean(scores):.3f}  min {np.min(scores):.2f}  below0.9 {sum(x < 0.9 for x in scores)}")
