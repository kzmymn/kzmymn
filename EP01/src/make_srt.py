"""タイミング表から字幕SRTを作る（画面の字幕と同じ表示区間）。"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "out", "narration-timing.json")
dst = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "out", "EP01.ja.srt")
T = json.load(open(src, encoding="utf-8"))
bs = T["beats"]


def ts(x):
    ms = int(round(x * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


with open(dst, "w", encoding="utf-8") as f:
    for i, b in enumerate(bs):
        nxt = bs[i + 1]["start"] if i + 1 < len(bs) else T["duration"]
        f.write(f"{i + 1}\n{ts(max(0, b['start'] - 0.08))} --> {ts(min(nxt - 0.1, b['end'] + 0.7))}\n{b['text']}\n\n")
print("->", dst)
