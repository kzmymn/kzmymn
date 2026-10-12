"""ナレーション生成：beats.py の各ビートを音声合成し、1本のWAVとタイミング表にする。

音声: Kokoro-82M (Apache-2.0) の日本語ボイス jf_alpha を kokoro-onnx で実行。
読み: Open JTalk (pyopenjtalk) の読み推定 → misaki の仮名→音素変換。
      misaki は fugashi + unidic を要求するが、ここでは pyopenjtalk で代替する。

使い方:
  python3 narration.py --model DIR [--voice jf_alpha] [--engine kokoro|jtalk] [--out ../out]
  DIR には kokoro-v1.0.onnx と voices-v1.0.bin を置く
  （https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0）
"""
import argparse, json, os, re, sys, types

import numpy as np
import pyopenjtalk
import soundfile as sf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from beats import BEATS

SR_OUT = 48000


# --- fugashi の代役（misaki.ja.JAG2P が使う属性だけ持つ） ---
class _Feat:
    def __init__(self, pron):
        self.pron = pron
        self.kana = pron


class _Word:
    def __init__(self, surface, pron, char_type):
        self.surface, self.feature, self.char_type, self.is_unk = surface, _Feat(pron), char_type, False


class _Tagger:
    def __init__(self, *a, **k):
        pass

    def __call__(self, text):
        out = []
        for n in pyopenjtalk.run_frontend(text):
            surf, pron = n["string"], n["pron"].replace("’", "")
            punct = n["pos"] == "記号"
            out.append(_Word(surf, surf if punct else pron, 3 if punct else 6))
        return out


_fg = types.ModuleType("fugashi")
_fg.Tagger = _Tagger
sys.modules.setdefault("fugashi", _fg)


def kanji_num(n):
    """整数を漢数字に（例: 1990 → 千九百九十）。"""
    d = "〇一二三四五六七八九"
    if n == 0:
        return d[0]
    out = ""
    for v, u in ((1000, "千"), (100, "百"), (10, "十")):
        q, n = divmod(n, v)
        if q:
            out += ("" if q == 1 else d[q]) + u
    return out + (d[n] if n else "")


def digits_to_kanji(text):
    # misaki の数字処理は「2時」を「に・とき」と分けてしまうため、先に漢数字へ
    return re.sub(r"\d+", lambda m: kanji_num(int(m.group())), text)


def spoken(beat):
    return beat.get("say") or beat["text"].replace("\n", "")


def reading(text):
    """確認用のカタカナ読み。"""
    return "".join(n["pron"].replace("’", "") for n in pyopenjtalk.run_frontend(text))


class KokoroTTS:
    def __init__(self, model_dir, voice):
        from kokoro_onnx import Kokoro
        from misaki import ja
        self.k = Kokoro(os.path.join(model_dir, "kokoro-v1.0.onnx"), os.path.join(model_dir, "voices-v1.0.bin"))
        self.g2p = ja.JAG2P()
        self.voice = voice

    def __call__(self, text):
        a, sr = self.k.create(self.g2p(digits_to_kanji(text)), voice=self.voice, speed=1.0, lang="ja", is_phonemes=True)
        return a.astype(np.float32), sr


class JTalkTTS:
    def __call__(self, text):
        a, sr = pyopenjtalk.tts(text)
        return (a / 32768.0).astype(np.float32), sr


def resample(a, sr):
    if sr == SR_OUT:
        return a
    x = np.arange(int(len(a) * SR_OUT / sr)) * sr / SR_OUT
    return np.interp(x, np.arange(len(a)), a).astype(np.float32)


def trim(a, thresh=0.01, keep=0.03):
    idx = np.where(np.abs(a) > thresh)[0]
    if len(idx) == 0:
        return a
    k = int(keep * SR_OUT)
    a = a[max(0, idx[0] - k): idx[-1] + k].copy()
    f = int(0.01 * SR_OUT)
    a[:f] *= np.linspace(0, 1, f)
    a[-f:] *= np.linspace(1, 0, f)
    return a


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="/tmp/claude-0/kokoro")
    ap.add_argument("--voice", default="jf_alpha")
    ap.add_argument("--engine", default="kokoro", choices=["kokoro", "jtalk"])
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "out"))
    ap.add_argument("--lead", type=float, default=0.5, help="冒頭の無音（秒）")
    args = ap.parse_args()

    tts = KokoroTTS(args.model, args.voice) if args.engine == "kokoro" else JTalkTTS()
    os.makedirs(args.out, exist_ok=True)

    parts = [np.zeros(int(args.lead * SR_OUT), np.float32)]
    t = args.lead
    timing = []
    for i, b in enumerate(BEATS):
        a, sr = tts(spoken(b))
        a = trim(resample(a, sr))
        dur = len(a) / SR_OUT
        timing.append(dict(i=i, scene=b["scene"], start=round(t, 3), end=round(t + dur, 3),
                           text=b["text"], say=spoken(b), reading=reading(spoken(b))))
        parts += [a, np.zeros(int(b["pause"] * SR_OUT), np.float32)]
        t += dur + b["pause"]
        print(f"{i:02d} {timing[-1]['start']:7.2f}-{timing[-1]['end']:7.2f} {spoken(b)}")

    audio = np.concatenate(parts)
    audio *= 0.89 / max(1e-6, np.abs(audio).max())  # ピークを -1 dBFS に
    name = "narration" if args.engine == "kokoro" else "narration-openjtalk"
    raw = os.path.join(args.out, name + "-raw.wav")
    sf.write(raw, audio, SR_OUT, subtype="PCM_16")
    # 音量を -16 LUFS / ピーク -1.5 dBFS にそろえる（長さは変わらない）
    import subprocess
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                    "-ar", str(SR_OUT), "-ac", "1", os.path.join(args.out, name + ".wav")], check=True)
    os.remove(raw)
    with open(os.path.join(args.out, name + "-timing.json"), "w", encoding="utf-8") as f:
        json.dump(dict(duration=round(len(audio) / SR_OUT, 3), engine=args.engine,
                       voice=args.voice if args.engine == "kokoro" else "mei_normal", beats=timing),
                  f, ensure_ascii=False, indent=1)
    print("total", len(audio) / SR_OUT)


if __name__ == "__main__":
    main()
