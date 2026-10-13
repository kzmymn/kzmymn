# Synthesized placeholder BGM (royalty-free, stdlib only): 120 BPM, 15 s
import math, random, struct, wave, sys
SR, DUR, BPM = 44100, 15.0, 120
N = int(SR * DUR); beat = 60 / BPM
L = [0.0] * N; R = [0.0] * N
random.seed(1)
def add(i, v, pan=0.0):
    if 0 <= i < N:
        L[i] += v * (1 - pan) * 0.5 * 2 ** 0.5; R[i] += v * (1 + pan) * 0.5 * 2 ** 0.5
def midi(n): return 440 * 2 ** ((n - 69) / 12)
# chords (jazzy): Cmaj7, Am9, Dm9, G13 - 2 beats each, loop
chords = [[48, 55, 59, 64, 67], [45, 52, 55, 59, 60], [50, 57, 60, 64, 65], [43, 53, 57, 59, 64]]
bass   = [36, 33, 38, 31]
# pad (soft saw-ish via few harmonics, slow attack), enters at 0.5 s
for b in range(30):
    t0 = b * beat * 2
    if t0 >= DUR: break
    ch = chords[b % 4]
    for n in ch:
        f = midi(n + 12)
        for k in range(int(SR * beat * 2)):
            i = int(t0 * SR) + k; t = k / SR
            if i >= N: break
            env = min(1, t / 0.25) * (0.75 + 0.25 * math.cos(2 * math.pi * 0.5 * t))
            v = sum(math.sin(2 * math.pi * f * h * t + h) / h for h in (1, 2, 3)) * 0.018 * env
            add(i, v, pan=0.3 * math.sin(n))
# drums from 1.0 s (bar 1 intro is pad only)
for b in range(30):
    t0 = b * beat
    if t0 < 2 * beat or t0 >= 13.5: continue
    s = int(t0 * SR)
    for k in range(int(SR * 0.35)):          # kick
        t = k / SR; f = 50 + 90 * math.exp(-t * 30)
        add(s + k, math.sin(2 * math.pi * f * t) * math.exp(-t * 9) * 0.55)
    if b % 2 == 1:                           # clap / snare
        for k in range(int(SR * 0.18)):
            t = k / SR; add(s + k, (random.random() * 2 - 1) * math.exp(-t * 22) * 0.18, pan=0.1)
    hs = int((t0 + beat / 2) * SR)           # off-beat hat
    for k in range(int(SR * 0.05)):
        t = k / SR; add(hs + k, (random.random() * 2 - 1) * math.exp(-t * 90) * 0.12, pan=0.35)
# bass from 1.0 s
for b in range(30):
    t0 = b * beat
    if t0 < 2 * beat or t0 >= 13.5: continue
    f = midi(bass[(b // 2) % 4]); s = int(t0 * SR)
    for k in range(int(SR * beat * 0.9)):
        t = k / SR; env = min(1, t / 0.01) * math.exp(-t * 2.5)
        add(s + k, (math.sin(2 * math.pi * f * t) + 0.3 * math.sin(4 * math.pi * f * t)) * 0.22 * env)
# riser into the date section (10.0-10.5 s) and final chime at 13.0 s
for k in range(int(SR * 0.5)):
    t = k / SR; add(int(10.0 * SR) + k, (random.random() * 2 - 1) * (t / 0.5) ** 2 * 0.15)
for n in (72, 76, 79, 83, 86):
    f = midi(n)
    for k in range(int(SR * 2.0)):
        t = k / SR; add(int(13.0 * SR) + k, math.sin(2 * math.pi * f * t) * math.exp(-t * 1.6) * 0.06, pan=(n - 79) / 10)
# simple echo, fades, normalize
d = int(SR * beat * 0.75)
for i in range(d, N):
    L[i] += R[i - d] * 0.22; R[i] += L[i - d] * 0.22
for i in range(N):
    t = i / SR; g = min(1, t / 0.4) * min(1, (DUR - t) / 1.2)
    L[i] *= g; R[i] *= g
peak = max(max(abs(x) for x in L), max(abs(x) for x in R)) or 1
out = sys.argv[1] if len(sys.argv) > 1 else "bgm.wav"
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(b"".join(struct.pack("<hh", int(L[i] / peak * 0.85 * 32767), int(R[i] / peak * 0.85 * 32767)) for i in range(N)))
print("wrote", out)
