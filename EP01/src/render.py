"""EP01 全編レンダラー：ナレーションのタイミング表に合わせて線画アニメーションを描き、MP4を書き出す。

使い方:
  python3 render.py                       # 全編（out/EP01-full.mp4）
  python3 render.py --until 45 --name EP01-opening   # 冒頭だけ
  python3 render.py --stills              # 各ビートの静止画（確認用）
必要: Python3, pycairo, Pillow, numpy, pyopenjtalk, FFmpeg
"""
import argparse, json, math, os, subprocess, sys, tempfile
from functools import lru_cache
from multiprocessing import Pool

import cairo
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from beats import BEATS
from draw import *  # noqa

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "out")
FPS = 30
LEAD = 0.12   # 画面の変化を声よりわずかに先行させる


# ---------------------------------------------------------------------------
# タイミング
# ---------------------------------------------------------------------------
def load_timing(path):
    T = json.load(open(path, encoding="utf-8"))
    for b, src in zip(T["beats"], BEATS):
        b["head"] = src.get("head")
    scenes = []
    for b in T["beats"]:
        if not scenes or scenes[-1]["id"] != b["scene"]:
            scenes.append(dict(id=b["scene"], beats=[]))
        scenes[-1]["beats"].append(b)
    for i, s in enumerate(scenes):
        s["start"] = 0.0 if i == 0 else s["beats"][0]["start"] - 0.15
    for i, s in enumerate(scenes):
        s["end"] = scenes[i + 1]["start"] if i + 1 < len(scenes) else T["duration"]
    return T, scenes


@lru_cache(maxsize=None)
def _kana_len(s):
    import pyopenjtalk
    if not s:
        return 0
    return len("".join(n["pron"].replace("’", "") for n in pyopenjtalk.run_frontend(s)).replace("、", ""))


class S:
    """場面内の時間計算。k は場面内のビート番号。"""

    def __init__(self, t, scene):
        self.t, self.sc, self.B = t, scene, scene["beats"]

    def s(self, k):
        return self.B[k]["start"] - LEAD

    def e(self, k):
        return self.B[k]["end"]

    def p(self, k, delay=0.0, dur=0.4):
        return clamp((self.t - self.s(k) - delay) / dur)

    def at(self, k, sub):
        """ビート k の中で sub を言い始める推定時刻（読みの長さに比例）。"""
        say = self.B[k]["say"]
        i = say.find(sub)
        if i < 0:
            return self.s(k)
        frac = _kana_len(say[:i]) / max(1, _kana_len(say))
        return self.B[k]["start"] + (self.B[k]["end"] - self.B[k]["start"]) * frac - LEAD

    def pa(self, k, sub, dur=0.35, delay=0.0):
        return clamp((self.t - self.at(k, sub) - delay) / dur)

    def span(self, k, sub0=None, sub1=None):
        """sub0 から sub1 を言う間の進み 0-1。"""
        t0 = self.at(k, sub0) if sub0 else self.s(k)
        t1 = self.at(k, sub1) if sub1 else self.e(k)
        return clamp((self.t - t0) / max(0.1, t1 - t0))

    def since(self, k):
        return self.t - self.s(k)

    def on(self, k):
        return self.t >= self.s(k)


GROUND = 830


def ground(pen, x0=120, x1=1800, y=GROUND):
    pen.line(x0, y, x1, y, GRAY, 5, seed=999)


def pop_in(p):
    return ease_back(p), clamp(p * 2.5)


# ---------------------------------------------------------------------------
# 場面
# ---------------------------------------------------------------------------
def sc_hook(pen, S):
    t = S.t
    ground(pen)
    m = 30 * ease_io(S.span(0, None, None))
    k2 = ease_io(S.p(2, dur=0.7))
    # 時計：30分ぶん赤く塗る → 左上へ縮む
    cx, cy, r = lerp(640, 330, k2), lerp(460, 330, k2), lerp(200, 110, k2)
    sc_, al = pop_in(S.p(0, dur=0.5))
    clock(pen, cx, cy, r, 2, m, s=sc_, sector=(0, m))
    if m > 1:
        pen.text(f"+{int(round(m))}分", cx, cy + r + 50, int(lerp(56, 40, k2)), color=RED, alpha=al)
    # 遅れる人（走ってくる）
    run = ease_out(S.p(0, delay=0.1, dur=1.2))
    bx = lerp(2150, 1300, run)
    bx = lerp(bx, 1450, k2)
    pose = "run" if run < 1 and k2 == 0 else "stand"
    person(pen, bx, GROUND, 1.05, B_COL, "worry", pose, t, flip=True, hair="short", seed=1)
    if run > 0.5:
        sweat(pen, bx - 60, GROUND - 300, 1.0, alpha=clamp((run - 0.5) * 3))
    # 「ごめん、遅れる」→ 送れない
    p1 = S.p(1, dur=0.35)
    if p1 > 0:
        sc_, al = pop_in(p1)
        bubble(pen, lerp(1250, 1400, k2), lerp(360, 380, k2), "ごめん、遅れる", 46, tail=(1, 1), s=sc_, alpha=al)
        cr = S.pa(1, "送れません", dur=0.4)
        if cr > 0:
            pen.line(lerp(1060, 1210, k2), lerp(360, 380, k2), lerp(1060, 1210, k2) + 380 * cr,
                     lerp(360, 380, k2), RED, 12)
            tag(pen, lerp(1250, 1400, k2), lerp(250, 270, k2), "送れない", 36, bg=RED, fg=WHITE,
                s=ease_back(cr), alpha=cr)
    # 待つ側と、届かない線
    if k2 > 0:
        person(pen, lerp(260, 470, k2), GROUND, 1.05, A_COL, "worry", "stand", t, seed=2, alpha=k2)
        arrow(pen, 600, 560, 1300, 560, p=ease_out(S.p(2, delay=0.3, dur=0.9)), color=GRAY, width=7,
              dash=[18, 16], head=False, seed=3)
        cp = S.p(2, delay=0.6, dur=0.4)
        if cp > 0:
            cellphone(pen, 950, 560, 0.8, alpha=cp)
            cross(pen, 950, 560, 70, p=S.p(2, delay=0.8, dur=0.4))
            tag(pen, 950, 700, "携帯なし", 34, bg=WHITE, s=ease_back(cp), alpha=cp)


def sc_phone(pen, S):
    t = S.t
    ground(pen)
    # 公衆電話と遅れる人
    sc_, al = pop_in(S.p(0, dur=0.45))
    payphone(pen, 300, GROUND, 0.95 * sc_, alpha=al)
    person(pen, 470, GROUND, 0.9, B_COL, "worry", "phone" if S.p(0, 0.3) > 0 else "stand", t,
           flip=True, hair="short", seed=11, alpha=al)
    if not S.on(1):
        q = S.p(0, delay=0.4)
        bubble(pen, 560, 330, "公衆電話なら？", 42, tail=(-1, 1), s=ease_back(q), alpha=q)
    # 家（相手はもう外）と駅
    p1 = S.p(1, dur=0.45)
    if p1 > 0:
        sc_, al = pop_in(p1)
        ring_p = 0.0
        if S.on(2):
            ring_p = t - S.at(2, "鳴らしても") if t > S.at(2, "鳴らしても") else 0.0
            ring_p = ring_p if t < S.at(2, "駅で待つ") + 0.8 else 0.0
        house(pen, 960, GROUND, 0.9 * sc_, alpha=al, door_open=True, phone_ring=ring_p, label="相手の家")
        station(pen, 1580, GROUND, 0.62 * sc_, alpha=al)
        walk = ease_io(S.p(1, delay=0.3, dur=1.6))
        ax = lerp(1060, 1600, walk)
        person(pen, ax, GROUND + 5, 0.72, A_COL, "normal", "run" if 0 < walk < 1 else "stand", t,
               seed=12, alpha=al)
        if walk >= 1:
            tag(pen, 960, 470, "留守", 36, bg=WHITE, s=ease_back(S.p(1, delay=1.9)), alpha=S.p(1, delay=1.9))
    # 電話 → 家 → 本人には届かない
    if S.on(2):
        arrow(pen, 360, 470, 860, 620, p=ease_out(S.p(2, dur=0.8)), color=RED, bend=-90, seed=13)
        t_stop = S.at(2, "駅で待つ")
        pst = clamp((t - t_stop) / 0.9)
        arrow(pen, 1080, 640, 1520, 640, p=pst, color=RED, dash=[20, 14], stop=0.62, seed=14)
    # 電話はある / 本人がいない
    if S.on(3):
        check(pen, 300, 330, 44, p=S.p(3, dur=0.4))
        tag(pen, 300, 250, "電話はある", 34, bg=WHITE, s=ease_back(S.p(3)), alpha=S.p(3))
        cp = S.pa(3, "でも", dur=0.4)
        cross(pen, 960, 690, 60, p=cp)
        tag(pen, 960, 470, "本人がいない", 36, bg=RED, fg=WHITE, s=ease_back(cp), alpha=cp)
    # 今との違い：当時は「場所」に、今は「人」にかける
    p4 = S.p(4, dur=0.45)
    if p4 > 0:
        c = pen.c
        c.set_source_rgba(*PAPER, 0.93 * p4); c.rectangle(0, 0, W, H); c.fill()
        rows = [("当時", "電話は「場所」にかける", lambda x, y, a: house(pen, x, y + 90, 0.55, alpha=a), 0),
                ("今", "電話は「人」にかける", lambda x, y, a: (phone_modern(pen, x - 40, y, 0.45, alpha=a),
                                                     person(pen, x + 70, y + 110, 0.5, A_COL, "happy", "phone", 0, alpha=a)), 0.5)]
        for i, (lab, txt, icon, dl) in enumerate(rows):
            pp = S.p(4, delay=dl, dur=0.4)
            if pp <= 0:
                continue
            y = 380 + i * 250
            sc_, al = pop_in(pp)
            tag(pen, 470, y, lab, 44, bg=YELLOW if i == 0 else rgb("#BDE7A5"), s=sc_, alpha=al)
            icon(700, y, al)
            pen.text(txt, 1250, y, 64, alpha=al, scale=sc_)


def sc_recon(pen, S):
    t = S.t
    ground(pen, 500, 1420)
    p = S.p(0, dur=0.5)
    sc_, al = pop_in(p)
    pen.text("再現", 960, 230, 96, color=INK, alpha=al, scale=sc_)
    tag(pen, 960, 345, "1980年代後半を想定・架空の人物", 40, bg=WHITE, s=sc_, alpha=al, weight="medium")
    for i, (x, col, lab, hair, fl) in enumerate([(700, A_COL, "待つ側", "bob", False),
                                                 (1220, B_COL, "遅れる側", "short", True)]):
        q = S.p(0, delay=0.4 + i * 0.35, dur=0.4)
        if q > 0:
            s2, a2 = pop_in(q)
            person(pen, x, GROUND, 1.0 * s2, col, "normal", "stand", t, flip=fl, hair=hair, seed=21 + i, alpha=a2)
            tag(pen, x, GROUND - 340, lab, 34, bg=col, fg=WHITE, alpha=a2)


def station_map(pen, alpha=1.0, s=1.0, ox=0, oy=0, clock_spot=False, clock_p=1.0):
    """駅の見取り図（上から見た簡略図。特定の駅ではない）。"""
    a = push(pen, ox, oy, s, alpha)
    pen.rrect(560, 280, 800, 420, 24, seed=201); pen.fill(WHITE, preserve=True); pen.stroke(width=6)
    # ホームと線路
    pen.line(600, 330, 1320, 330, GRAY, 6, seed=202)
    pen.line(600, 345, 1320, 345, GRAY, 6, dash=[6, 18], seed=203)
    pen.text("ホーム", 960, 380, 30, color=GRAY)
    # 改札
    for i in range(5):
        gx = 860 + i * 50
        pen.rrect(gx - 10, 455, 20, 46, 4, seed=204 + i); pen.fill(rgb("#D9DEE6"), preserve=True); pen.stroke(width=4)
    pen.line(600, 478, 845, 478, INK, 6, seed=210)
    pen.line(1075, 478, 1320, 478, INK, 6, seed=211)
    pen.text("改札", 960, 430, 30)
    # 出口
    for x, lab in ((560, "西口"), (1360, "東口")):
        pen.c.new_path(); pen.c.rectangle(x - 12, 580, 24, 90); pen.fill(PAPER)
        pen.text(lab, x + (-70 if x < 900 else 70), 625, 36)
    if clock_spot and clock_p > 0:
        clock(pen, 1290, 600, 34, 2, 0, s=ease_back(clock_p), seed=212)
    pop(pen, a)


MAP_POS = {"inside": (760, 400), "outside": (960, 600), "west": (560, 625), "east": (1360, 625),
           "clock": (1290, 640)}


def sc_plan(pen, S):
    t = S.t
    if not S.on(2):
        ground(pen)
        p = S.p(0, dur=0.45)
        sc_, al = pop_in(p)
        station(pen, 960, GROUND, 1.0 * sc_, alpha=al, clock_t=(2, 0))
        tag(pen, 960, 300, "約束：午後2時・駅", 40, bg=YELLOW, s=sc_, alpha=al)
        face = "worry" if S.on(1) else "happy"
        person(pen, 470, GROUND, 0.9, A_COL, face, "stand", t, seed=31, alpha=al)
        person(pen, 1450, GROUND, 0.9, B_COL, face, "stand", t, flip=True, hair="short", seed=32, alpha=al)
        if S.on(1):
            q = S.pa(1, "駅で", dur=0.35)
            bubble(pen, 470, 470, "駅の、どこ？", 40, tail=(-1, 1), s=ease_back(q), alpha=q, think=True)
            q2 = S.p(1, delay=0.6)
            bubble(pen, 1450, 470, "？", 48, tail=(1, 1), s=ease_back(q2), alpha=q2, think=True)
        return
    # 見取り図
    k3 = ease_io(S.p(3, dur=0.5)) if not S.on(4) else ease_io(1 - S.p(4, dur=0.5))
    mx = lerp(0, -380, k3)
    msc = lerp(1.0, 0.8, k3)
    station_map(pen, s=msc, ox=mx + 960 * (1 - msc), oy=540 * (1 - msc) - 40, clock_spot=S.on(4),
                clock_p=S.pa(4, "時計の下", dur=0.4))

    def mp(name):
        x, y = MAP_POS[name]
        return mx + 960 * (1 - msc) + x * msc, 540 * (1 - msc) - 40 + y * msc

    if not S.on(4):
        for sub, name, lab in (("改札の中", "inside", "改札の中？"), ("外", "outside", "外？"),
                               ("東口", "east", "東口？"), ("西口", "west", "西口？")):
            q = S.pa(2, sub, dur=0.3)
            x, y = mp(name)
            if name == "east":
                x, y = x + 40 * msc, y + 120 * msc
            if name == "west":
                x, y = x - 40 * msc, y + 120 * msc
            tag(pen, x, y, lab, int(40 * msc + 4), bg=YELLOW, s=ease_back(q), alpha=q)
    # 今なら写真を送れる → できない
    if S.on(3) and not S.on(4):
        q = S.p(3, dur=0.45)
        phone_modern(pen, 1500, 540, 1.0 * ease_back(q), alpha=q,
                     msgs=[("ここにいる", "r", S.p(3, 0.3), 0)])
        # 写真（簡略）
        if S.p(3, 0.5) > 0:
            pp = S.p(3, 0.5)
            pen.rrect(1410, 460, 180, 120, 10, seed=301); pen.fill(rgb("#BFD6EA"), alpha=pp, preserve=True); pen.stroke(width=4, alpha=pp)
            pin(pen, 1500, 550, 0.6, alpha=pp)
        cross(pen, 1500, 540, 150, p=S.pa(3, "でも", dur=0.45))
    # 東口の改札を出て、時計の下
    if S.on(4):
        x0, y0 = mp("outside")
        x1, y1 = mp("clock")
        arrow(pen, 960, 500, x1 - 40, y1 - 20, p=ease_out(S.pa(4, "東口", dur=0.7)), color=RED, bend=60, seed=302)
        ring(pen, x1, y1 - 20, 90, 90, p=S.pa(4, "時計の下", dur=0.6), seed=303)
        q = S.pa(4, "決めました", dur=0.35)
        tag(pen, x1 + 20, y1 + 110, "約束の場所", 40, bg=RED, fg=WHITE, s=ease_back(q), alpha=q)


def sc_missed(pen, S):
    t = S.t
    ground(pen)
    if not S.on(1):
        # ホームと発車する電車
        pen.line(120, GROUND - 4, 1800, GROUND - 4, INK, 8, seed=401)
        go = ease_io(S.p(0, delay=0.3, dur=2.6))
        train(pen, lerp(780, 2300, go) - 330, GROUND - 40, 1.0)
        pen.c.new_path(); pen.c.rectangle(0, GROUND - 40, W, 40); pen.fill(LIGHT)
        pen.line(0, GROUND - 40, W, GROUND - 40, INK, 6, seed=402)
        run = ease_out(S.p(0, delay=0.2, dur=1.4))
        bx = lerp(-150, 520, run)
        person(pen, bx, GROUND - 40, 1.0, B_COL, "surprise" if run >= 1 else "worry", "run" if run < 1 else "stand",
               t, hair="short", seed=41)
        if run >= 1:
            sweat(pen, bx + 64, GROUND - 330, 1.0)
            tag(pen, bx, GROUND - 400, "乗り遅れ！", 40, bg=RED, fg=WHITE, s=ease_back(S.p(0, 1.4)), alpha=S.p(0, 1.4))
        return
    # 時計の下で待つ
    mins = lerp(0, 10, ease_io(S.p(1, dur=2.2)))
    if S.on(2):
        mins = lerp(10, 15, ease_io(S.p(2, dur=2.5)))
    station_clock(pen, 760, GROUND, 2, mins)
    person(pen, 920, GROUND, 1.0, A_COL, "worry" if S.on(2) else "normal", "stand", t, seed=42, look=-0.5)
    tag(pen, 760, GROUND - 450, f"2:{int(mins):02d}", 34, bg=WHITE)
    if not S.on(2):
        q = S.p(1, dur=0.4)
        bubble(pen, 1250, 380, "……", 52, tail=(-1, 1), s=ease_back(q), alpha=q)
        tag(pen, 1250, 520, "連絡なし", 36, bg=WHITE, s=ease_back(S.p(1, 0.5)), alpha=S.p(1, 0.5))
    else:
        for i, (sub, lab) in enumerate((("遅れている", "遅れてる？"), ("場所を", "場所まちがい？"), ("忘れた", "忘れた？"))):
            q = S.pa(2, sub, dur=0.35)
            bubble(pen, 1290 + (i % 2) * 120, 300 + i * 150, lab, 40, tail=(-1, 1), s=ease_back(q), alpha=q, think=True)


def sc_dilemma(pen, S):
    t = S.t
    station_map(pen, oy=10, clock_spot=True)
    ex, ey = MAP_POS["clock"]
    wx, wy = MAP_POS["west"]
    ey += 10; wy += 10
    # 待つ側（小）
    k0 = ease_io(S.p(0, delay=0.6, dur=1.6))
    if S.on(1):
        k0 = 1.0
    if S.on(2):
        # 二人とも回る：A は西口→東口、B は東口→西口へ、すれ違う
        cyc = (S.since(2) * 0.35) % 1.0
        ax = lerp(wx + 60, ex, ease_io(cyc)); ay = wy + 120 + 30 * math.sin(cyc * math.pi)
        bx = lerp(ex, wx + 60, ease_io(cyc)); by = ey - 60 - 30 * math.sin(cyc * math.pi)
        arrow(pen, wx + 60, wy + 120, ex, ey + 120, p=1, color=A_COL, width=6, dash=[12, 12], bend=-40, head=False, seed=501)
        arrow(pen, ex, ey - 60, wx + 60, wy - 60, p=1, color=B_COL, width=6, dash=[12, 12], bend=-40, head=False, seed=502)
        person(pen, ax, ay + 60, 0.38, A_COL, "worry", "run", t, seed=503)
        person(pen, bx, by + 60, 0.38, B_COL, "worry", "run", t, flip=True, hair="short", seed=504)
        q = S.p(2, delay=0.6)
        tag(pen, 1560, 420, "すれ違い", 48, bg=RED, fg=WHITE, s=ease_back(q), alpha=q)
        return
    arrow(pen, ex - 30, ey + 40, wx + 60, wy + 40, p=ease_out(S.p(0, dur=0.8)), color=A_COL, width=7,
          dash=[16, 12], bend=-90, seed=505)
    ax, ay = lerp(ex, wx + 60, k0), lerp(ey, wy, k0) + 60 + 70 * math.sin(k0 * math.pi)
    person(pen, ax, ay + 60, 0.42, A_COL, "worry", "run" if 0 < k0 < 1 else "stand", t, seed=506)
    if S.on(1):
        q = S.p(1, dur=0.8)
        bx, by = lerp(960, ex, ease_io(q)), lerp(500, ey, ease_io(q))
        person(pen, bx, by + 60, 0.42, B_COL, "worry", "run" if q < 1 else "stand", t, flip=True, hair="short", seed=507)
        ring(pen, ex, ey + 20, 70, 70, p=S.pa(1, "来たら", dur=0.5), seed=508)
        q2 = S.pa(1, "来たら", dur=0.35)
        tag(pen, ex + 120, ey - 150, "入れ違い", 40, bg=RED, fg=WHITE, s=ease_back(q2), alpha=q2)
    else:
        q = S.pa(0, "会えるかも", dur=0.4)
        bubble(pen, 760, 790, "西口かも？", 38, tail=(-1, -1), s=ease_back(q), alpha=q, think=True)


def sc_relay(pen, S):
    t = S.t
    ground(pen)
    payphone(pen, 230, GROUND, 0.8, label=True)
    person(pen, 380, GROUND, 0.78, B_COL, "worry", "phone", t, flip=True, hair="short", seed=61)
    house(pen, 900, GROUND, 0.8, roof=B_COL, label="遅れる側の家", phone_ring=0.0)
    person(pen, 1080, GROUND, 0.7, GRAY, "normal", "phone" if t < S.e(0) + 0.5 else "stand", t, hair="short", seed=62)
    station(pen, 1620, GROUND, 0.55)
    person(pen, 1560, GROUND + 5, 0.72, A_COL, "worry", "stand", t, seed=63)
    arrow(pen, 300, 520, 790, 560, p=ease_out(S.pa(0, "自分の家", dur=0.8)), color=RED, bend=-80, seed=64)
    q = S.pa(0, "伝言", dur=0.35)
    bubble(pen, 1050, 420, "伝言：30分遅れる", 34, tail=(1, 1), s=ease_back(q), alpha=q, weight="medium")
    if S.on(1):
        # 伝言は家に置かれたまま。待つ側が電話すれば受け取れる。
        q = S.pa(1, "待つ側", dur=0.6)
        arrow(pen, 1500, 560, 1150, 520, p=q, color=GRAY, width=7, dash=[14, 12], bend=60, seed=65)
        tag(pen, 1450, 320, "待つ側が電話すれば…", 32, bg=WHITE, s=ease_back(q), alpha=q, weight="medium")
        cp = S.pa(1, "届きません", dur=0.4)
        if cp > 0:
            tag(pen, 1450, 400, "かけなければ届かない", 34, bg=RED, fg=WHITE, s=ease_back(cp), alpha=cp)
    if S.on(2):
        q = S.p(2, dur=0.45)
        c = pen.c
        c.set_source_rgba(*PAPER, 0.85 * q); c.rectangle(0, 0, W, H); c.fill()
        sc_, al = pop_in(q)
        pen.rrect(560, 300, 800, 300, 22, seed=66); pen.fill(WHITE, alpha=al, preserve=True); pen.stroke(width=6, alpha=al)
        pen.text("事前の相談", 960, 380, 56, alpha=al, scale=sc_)
        pen.text("「遅れたら家に電話して」", 960, 480, 44, "medium", alpha=al, scale=sc_)
        cross(pen, 1300, 380, 42, p=S.pa(2, "なければ", dur=0.4))
        q2 = S.pa(2, "保証", dur=0.35)
        tag(pen, 960, 680, "なければ、伝わる保証なし", 40, bg=RED, fg=WHITE, s=ease_back(q2), alpha=q2)


BOARD_LINES = ["東口で待っています", "先に喫茶店へ行きます"]


def sc_board(pen, S):
    t = S.t
    ground(pen)
    gate(pen, 380, GROUND, 1.7, alpha=S.p(0, dur=0.3))
    q = S.p(0, delay=0.15, dur=0.5)
    sc_, al = pop_in(q)
    l1 = S.span(2, "東口で", "あるいは") if S.on(2) else 0
    l2 = S.span(2, "先に", None) if S.on(2) else 0
    blackboard(pen, 1080, 470, sc_ * 1.0, alpha=al, lines=[(BOARD_LINES[0], l1), (BOARD_LINES[1], l2)])
    if S.on(1):
        for sub, x, y, lab in (("改札横", 560, 560, "改札横"), ("待合室", 1480, 700, "待合室にも")):
            qq = S.pa(1, sub, dur=0.35)
            tag(pen, x, y, lab, 38, bg=YELLOW, s=ease_back(qq), alpha=qq)
        arrow(pen, 600, 520, 790, 480, p=ease_out(S.pa(1, "改札横", 0.5)), color=RED, width=7, seed=701)
    if S.on(2):
        qq = S.p(2, 0.3)
        pen.text("※文面は説明用の例です", 1080, 700, 28, "medium", color=GRAY, alpha=qq)
    if S.on(3):
        qq = S.p(3, dur=0.6)
        person(pen, lerp(1950, 1640, ease_out(qq)), GROUND, 0.85, B_COL, "happy" if S.t > S.at(3, "居場所") else "normal",
               "read", t, flip=True, hair="short", seed=702, alpha=clamp(qq * 2), look=-1)
        arrow(pen, 1380, 420, 1560, 330, p=ease_out(S.pa(3, "居場所", dur=0.5)), color=GREEN, width=8, seed=703)
        q2 = S.pa(3, "居場所", dur=0.35)
        tag(pen, 1640, 290, "東口だ！", 38, bg=GREEN, fg=WHITE, s=ease_back(q2), alpha=q2)


def sc_compare(pen, S):
    t = S.t
    q = S.p(2, dur=0.4)
    # 左：伝言板、右：今のメッセージ
    blackboard(pen, 520, 470, 0.72, lines=[(BOARD_LINES[0], 1), (BOARD_LINES[1], 1)])
    read = S.pa(0, "既読", dur=0.35)
    phone_modern(pen, 1420, 540, 0.95, msgs=[("東口で待ってる", "r", 1, read)], notif=S.p(0, dur=0.4))
    # 通知なし・既読なし
    pp = S.p(0, dur=0.4)
    bell(pen, 330, 760, 1.0, alpha=pp, crossed=pp > 0.5)
    tag(pen, 470, 760, "通知なし", 34, bg=WHITE, s=ease_back(pp), alpha=pp)
    rp = S.pa(0, "既読", dur=0.35)
    tag(pen, 720, 760, "既読なし", 34, bg=WHITE, s=ease_back(rp), alpha=rp)
    if rp > 0:
        pen.line(650, 760, 650 + 140 * rp, 760, RED, 7)
    # 周りの人にも読める
    if S.on(1):
        for i, (x, y) in enumerate(((200, 330), (850, 300), (210, 560))):
            qq = S.p(1, delay=i * 0.15, dur=0.3)
            eye(pen, x, y, 1.1, alpha=qq)
        qq = S.p(1, 0.3)
        tag(pen, 1420, 850, "読むのは本人だけ", 32, bg=rgb("#BDE7A5"), s=ease_back(qq), alpha=qq)
    if q > 0:
        pen.line(960, 200, 960, 880, GRAY, 5, dash=[14, 14], alpha=q)
        tag(pen, 520, 175, "当時：伝言板", 40, bg=YELLOW, s=ease_back(q), alpha=q)
        tag(pen, 1420, 175, "今：メッセージ", 40, bg=rgb("#BDE7A5"), s=ease_back(q), alpha=q)


def sc_reunion(pen, S):
    t = S.t
    ground(pen)
    if S.on(2) and not S.on(3):
        # もしも：待つ側が別の出口へ行っていたら
        station_clock(pen, 860, GROUND, 2, 30)
        person(pen, 1000, GROUND, 1.0, B_COL, "worry", "stand", t, flip=True, hair="short", seed=81)
        g = ease_io(S.p(2, delay=0.2, dur=1.6))
        person(pen, lerp(720, 200, g), GROUND, 1.0, A_COL, "worry", "run" if g < 1 else "stand", t, seed=82, alpha=0.45)
        arrow(pen, 700, 560, 260, 560, p=ease_out(S.p(2, 0.2, 1.0)), color=GRAY, width=7, dash=[14, 12], seed=83)
        q = S.p(2, dur=0.35)
        tag(pen, 960, 230, "もしも…", 48, bg=GRAY, fg=WHITE, s=ease_back(q), alpha=q)
        bubble(pen, 1250, 400, "いない…", 40, tail=(-1, 1), s=ease_back(S.p(2, 0.9)), alpha=S.p(2, 0.9))
        return
    if S.on(3):
        # 出かける前の約束（チェックリスト）
        q = S.p(3, dur=0.45)
        sc_, al = pop_in(q)
        pen.rrect(560, 230, 800, 520, 24, seed=84); pen.fill(WHITE, alpha=al, preserve=True); pen.stroke(width=6, alpha=al)
        pen.text("出かける前の約束", 960, 310, 54, alpha=al, scale=sc_)
        items = (("場所", "場所"), ("時間", "時間"), ("会えなかった", "会えなかった場合の行動"))
        for i, (sub, lab) in enumerate(items):
            qq = S.pa(4, sub, dur=0.35) if S.on(4) else 0
            y = 430 + i * 105
            pen.rrect(640, y - 32, 64, 64, 10, seed=85 + i); pen.fill(WHITE, alpha=al, preserve=True); pen.stroke(width=5, alpha=al)
            check(pen, 672, y, 30, p=qq)
            pen.text(lab, 740, y, 46, alpha=max(0.25 * al, qq), ax=0)
        return
    # 再会
    station_clock(pen, 860, GROUND, 2, 30 * ease_io(S.p(0, dur=1.0)) if True else 30)
    person(pen, 720, GROUND, 1.0, A_COL, "happy" if S.p(0, 1.0) > 0 else "worry", "wave" if S.p(0, 1.0) > 0 else "stand", t, seed=86)
    run = ease_out(S.p(0, delay=0.2, dur=1.0))
    bx = lerp(2050, 1060, run)
    person(pen, bx, GROUND, 1.0, B_COL, "happy" if run >= 1 else "worry", "run" if run < 1 else "stand", t,
           flip=True, hair="short", seed=87)
    if run >= 1 and not S.on(1):
        bubble(pen, 1240, 380, "ごめん！", 42, tail=(-1, 1), s=ease_back(S.p(0, 1.2)), alpha=S.p(0, 1.2))
        bubble(pen, 520, 380, "よかった！", 42, tail=(1, 1), s=ease_back(S.p(0, 1.5)), alpha=S.p(0, 1.5))
    tag(pen, 860, GROUND - 450, "2:30", 34, bg=WHITE)
    if S.on(1):
        ring(pen, 760, GROUND - 10, 140, 50, p=S.p(1, dur=0.6), seed=88)
        pin(pen, 600, GROUND - 330, 0.9, alpha=S.p(1, 0.2))
        q = S.pa(1, "動かなかった", dur=0.35)
        tag(pen, 480, GROUND - 420, "動かなかった", 40, bg=RED, fg=WHITE, s=ease_back(q), alpha=q)


def sc_caveat(pen, S):
    t = S.t
    if not S.on(1):
        for i, (sub, lab) in enumerate((("時代", "時代"), ("地域", "地域"), ("人", "人"))):
            q = S.pa(0, sub, dur=0.35)
            x = 560 + i * 400
            sc_, al = pop_in(q)
            pen.circle(x, 470, 130, seed=601 + i); pen.fill(WHITE, alpha=al, preserve=True); pen.stroke(width=6, alpha=al)
            if i == 0:
                clock(pen, x, 470, 70, 10, 10, s=sc_, alpha=al)
            elif i == 1:
                for k in range(3):
                    pin(pen, x - 50 + k * 50, 510 - (k % 2) * 40, 0.55 * sc_, alpha=al, color=(RED, BLUE, GREEN)[k])
            else:
                person(pen, x - 40, 540, 0.36 * sc_, A_COL, "normal", "stand", t, seed=602, alpha=al)
                person(pen, x + 40, 540, 0.36 * sc_, B_COL, "normal", "stand", t, flip=True, hair="short", seed=603, alpha=al)
            pen.text(lab, x, 660, 52, alpha=al, scale=sc_)
        q = S.pa(0, "違います", dur=0.35)
        tag(pen, 960, 800, "使った方法は、さまざま", 42, bg=YELLOW, s=ease_back(q), alpha=q)
        return
    ground(pen)
    for i, (x, has) in enumerate(((560, True), (1360, False))):
        q = S.pa(1, "あった" if has else "なかった", dur=0.4)
        sc_, al = pop_in(q)
        station(pen, x, GROUND, 0.75 * sc_, alpha=al)
        if has:
            blackboard(pen, x + 270, GROUND - 170, 0.3 * sc_, alpha=al, lines=[("…", 1)], label=False)
        tag(pen, x, GROUND + 60, "伝言板あり" if has else "伝言板なし", 36, bg=WHITE, s=sc_, alpha=al)


TL_Y = 560
TL_X = {"80": 420, "90": 960, "00": 1500}


def timeline(pen, alpha=1.0):
    pen.line(220, TL_Y, 1700, TL_Y, INK, 7, alpha=alpha, seed=801)
    for k, lab in (("80", "1980年代"), ("90", "1990年前後"), ("00", "2000年代")):
        x = TL_X[k]
        pen.line(x, TL_Y - 16, x, TL_Y + 16, INK, 7, alpha=alpha)
        pen.text(lab, x, TL_Y + 60, 36, alpha=alpha)


def sc_history(pen, S):
    t = S.t
    timeline(pen)
    # 伝言板（帯）
    pen.rrect(300, TL_Y - 150, 1100, 50, 10, seed=802); pen.fill(BOARD, 0.85)
    pen.text("駅の伝言板", 420, TL_Y - 125, 30, color=CHALK, ax=0)
    fade = 0.0
    if S.on(2):
        fade = S.pa(2, "撤去", dur=1.0) if S.on(2) else 0
        # 1990年前後から一部で撤去：帯の右側を薄く（点線）
        pen.c.set_source_rgba(*PAPER, 0.55 * fade); pen.c.rectangle(TL_X["90"], TL_Y - 160, 500, 70); pen.c.fill()
    q = S.pa(0, "ポケベル", dur=0.35)
    pager(pen, TL_X["90"] + 120, TL_Y - 260, 0.9 * ease_back(q), alpha=q)
    q = S.pa(0, "携帯", dur=0.35)
    cellphone(pen, TL_X["00"], TL_Y - 280, 0.9 * ease_back(q), alpha=q)
    q = S.pa(0, "全国一斉", dur=0.35)
    if q > 0 and not S.on(1):
        tag(pen, 960, 830, "全国一斉に消えた？", 44, bg=WHITE, s=ease_back(q), alpha=q)
        cross(pen, 1210, 830, 40, p=S.pa(0, "わけでは", dur=0.4))
    # 出典カード
    if S.on(1) and not S.on(2):
        q = S.p(1, dur=0.45)
        sc_, al = pop_in(q)
        pen.c.set_source_rgba(*PAPER, 0.85 * q); pen.c.rectangle(0, 0, W, H); pen.c.fill()
        doc_icon(pen, 560, 520, 1.2 * sc_, alpha=al)
        pen.text("片山雅木（2016）\n「伝言板から見る鉄道と社会の変化」\n日本地理学会 秋季学術大会 発表要旨", 1100, 520, 40, "medium",
                 alpha=al, scale=sc_)
    if S.on(2):
        q = S.pa(2, "千九百九十年", dur=0.4)
        pin(pen, TL_X["90"], TL_Y - 10, 1.0 * ease_back(q), alpha=q)
        tag(pen, TL_X["90"], 830, "一部の鉄道会社で撤去が始まる", 40, bg=RED, fg=WHITE,
            s=ease_back(S.pa(2, "撤去", dur=0.35)), alpha=S.pa(2, "撤去", dur=0.35))
    if S.on(3):
        q = S.p(3, dur=0.45)
        pen.c.set_source_rgba(*PAPER, 0.88 * q); pen.c.rectangle(0, 0, W, H); pen.c.fill()
        sc_, al = pop_in(q)
        pen.text("携帯の普及", 560, 420, 60, alpha=al, scale=sc_)
        pen.text("＝", 820, 420, 72, alpha=al, scale=sc_)
        pen.text("伝言板が消えた理由？", 1240, 420, 60, alpha=al, scale=sc_)
        cross(pen, 820, 420, 46, p=S.p(3, 0.6, 0.4))
        q2 = S.pa(3, "説明できない", dur=0.35)
        tag(pen, 960, 600, "それだけでは説明できない", 48, bg=YELLOW, s=ease_back(q2), alpha=q2)


def sc_now(pen, S):
    t = S.t
    ground(pen)
    if not S.on(1):
        q = S.p(0, dur=0.45)
        person(pen, 520, GROUND, 1.0, A_COL, "normal", "stand", t, seed=91)
        person(pen, 1400, GROUND, 1.0, B_COL, "normal", "run", t, flip=True, hair="short", seed=92)
        phone_modern(pen, 610, GROUND - 150, 0.22)
        phone_modern(pen, 1310, GROUND - 150, 0.22)
        arrow(pen, 1280, 450, 650, 450, p=ease_out(S.p(0, 0.3, 0.7)), color=GREEN, bend=-60, seed=93)
        arrow(pen, 650, 520, 1280, 520, p=ease_out(S.p(0, 0.8, 0.7)), color=GREEN, bend=-60, seed=94)
        tag(pen, 960, 300, "外にいても、つながる", 42, bg=rgb("#BDE7A5"), s=ease_back(q), alpha=q)
        return
    rel = S.on(2)
    person(pen, 600, GROUND, 1.0, A_COL, "happy" if rel else "normal", "stand", t, seed=95)
    phone_modern(pen, 1100, 520, 1.15, msgs=[("あと5分", "l", S.pa(1, "あと", 0.3), 0),
                                             ("店に入ってる", "l", S.pa(1, "店に", 0.3), 0),
                                             ("了解！", "r", S.p(1, 1.6, 0.3), S.p(1, 1.9, 0.3))])
    if rel:
        q = S.pa(2, "不安", dur=0.35)
        tag(pen, 600, 300, "不安が減る", 44, bg=rgb("#BDE7A5"), s=ease_back(q), alpha=q)


def sc_cta(pen, S):
    t = S.t
    ground(pen)
    if not S.on(1):
        q = S.p(0, dur=0.45)
        person(pen, 560, GROUND, 1.0, A_COL, "normal", "read", t, seed=96, alpha=q)
        for i, lab in enumerate(("改札前？", "時計の下？", "お店？")):
            qq = S.p(0, delay=0.4 + i * 0.3)
            pin(pen, 1000 + i * 260, 560, 0.9 * ease_back(qq), alpha=qq, color=(RED, BLUE, GREEN)[i])
            tag(pen, 1000 + i * 260, 640, lab, 34, bg=WHITE, s=ease_back(qq), alpha=qq)
        q2 = S.p(0, 1.6)
        tag(pen, 1260, 760, "コメントで教えてください", 36, bg=YELLOW, s=ease_back(q2), alpha=q2)
        return
    q = S.p(1, dur=0.45)
    m = 60 * ease_io(clamp(S.since(1) / 3.5)) if S.since(1) > 0.3 else 0
    clock(pen, 760, 500, 200, 2, m, sector=(0, m), s=ease_back(q), alpha=q)
    person(pen, 1300, GROUND, 1.0, B_COL, "surprise", "stand", t, flip=True, hair="short", seed=97)
    pen.text(f"{int(m)}分", 760, 760, 54, color=RED, alpha=q)
    bubble(pen, 1300, 420, "何分まで\n待てる？", 44, tail=(-1, 1), s=ease_back(S.p(1, 0.4)), alpha=S.p(1, 0.4))


SCENES = dict(hook=sc_hook, phone=sc_phone, recon=sc_recon, plan=sc_plan, missed=sc_missed,
              dilemma=sc_dilemma, relay=sc_relay, board=sc_board, compare=sc_compare, reunion=sc_reunion,
              caveat=sc_caveat, history=sc_history, now=sc_now, cta=sc_cta)


# ---------------------------------------------------------------------------
# 共通の上乗せ：大見出し・字幕・「架空の再現」表示
# ---------------------------------------------------------------------------
def headline_at(T, t):
    cur, since = "", 0.0
    for b in T["beats"]:
        if b["start"] - LEAD > t:
            break
        if b["head"] is not None:
            cur, since = b["head"], b["start"] - LEAD
    return cur, since


def draw_headline(pen, T, t):
    h, since = headline_at(T, t)
    if not h:
        return
    p = clamp((t - since) / 0.25)
    tw, th = pen.text_size(h, 66)
    c = pen.c
    # 蛍光ペン風の帯
    c.save()
    c.set_source_rgba(*YELLOW, 0.75)
    c.rectangle(960 - tw / 2 - 16, 120 + 4, (tw + 32) * ease_out(p), 34)
    c.fill()
    c.restore()
    pen.text(h, 960, 112, 66, alpha=p, scale=lerp(0.94, 1.0, ease_out(p)))


def subtitle_at(T, t):
    bs = T["beats"]
    for i, b in enumerate(bs):
        nxt = bs[i + 1]["start"] if i + 1 < len(bs) else T["duration"]
        if b["start"] - 0.08 <= t < min(nxt - 0.02, b["end"] + 0.7):
            return b["text"]
    return None


def draw_subtitle(pen, T, t):
    s = subtitle_at(T, t)
    if not s:
        return
    tw, th = pen.text_size(s, 46, "medium")
    c = pen.c
    y = 1010
    pen.c.save()
    c.set_source_rgba(1, 1, 1, 0.9)
    x0, y0, w, h = 960 - tw / 2 - 28, y - th - 2, tw + 56, th + 14
    r = 16
    c.new_sub_path()
    c.arc(x0 + w - r, y0 + r, r, -math.pi / 2, 0); c.arc(x0 + w - r, y0 + h - r, r, 0, math.pi / 2)
    c.arc(x0 + r, y0 + h - r, r, math.pi / 2, math.pi); c.arc(x0 + r, y0 + r, r, math.pi, 1.5 * math.pi)
    c.close_path(); c.fill()
    pen.c.restore()
    pen.text(s, 960, y + 6, 46, "medium", ax=0.5, ay=1.0)


def draw_fiction_chip(pen, T, scenes, t):
    ids = [s["id"] for s in scenes]
    on = next(s["start"] for s in scenes if s["id"] == "recon")
    off = next(s["start"] for s in scenes if s["id"] == "caveat")
    if on + 0.3 <= t < off:
        tag(pen, 150, 52, "架空の再現", 28, bg=WHITE, weight="medium")


# ---------------------------------------------------------------------------
def render_frame(ctx, bg, T, scenes, f):
    t = f / FPS
    ctx.set_source_surface(bg, 0, 0)
    ctx.paint()
    pen = Pen(ctx, f, FPS)
    sc = next(s for s in scenes if s["start"] <= t < s["end"]) if t < scenes[-1]["end"] else scenes[-1]
    SCENES[sc["id"]](pen, S(t, sc))
    draw_headline(pen, T, t)
    draw_fiction_chip(pen, T, scenes, t)
    draw_subtitle(pen, T, t)


def _worker(args):
    timing, f0, f1, path = args
    T, scenes = load_timing(timing)
    bg, _keep = paper_background()
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                           "-crf", "18", "-pix_fmt", "yuv420p", "-g", str(FPS * 2), path], stdin=subprocess.PIPE)
    for f in range(f0, f1):
        render_frame(ctx, bg, T, scenes, f)
        surf.flush()
        ff.stdin.write(surf.get_data())
    ff.stdin.close()
    ff.wait()
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timing", default=os.path.join(OUT, "narration-timing.json"))
    ap.add_argument("--audio", default=os.path.join(OUT, "narration.wav"))
    ap.add_argument("--until", type=float, default=None, help="この秒数までで切る（冒頭版）")
    ap.add_argument("--name", default="EP01-full")
    ap.add_argument("--jobs", type=int, default=os.cpu_count())
    ap.add_argument("--stills", action="store_true")
    a = ap.parse_args()

    T, scenes = load_timing(a.timing)
    if a.stills:
        bg, _k = paper_background()
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        ctx = cairo.Context(surf)
        d = os.path.join(OUT, "stills"); os.makedirs(d, exist_ok=True)
        for b in T["beats"]:
            if a.until and b["start"] > a.until:
                break
            f = int((b["end"] - 0.05) * FPS)
            render_frame(ctx, bg, T, scenes, f)
            surf.write_to_png(os.path.join(d, f"beat{b['i']:02d}.png"))
        print("stills ->", d)
        return

    dur = min(T["duration"], a.until) if a.until else T["duration"]
    n = int(math.ceil(dur * FPS))
    tmp = tempfile.mkdtemp(dir=OUT)
    k = a.jobs
    jobs = [(a.timing, n * i // k, n * (i + 1) // k, os.path.join(tmp, f"part{i}.mp4")) for i in range(k)]
    with Pool(k) as pool:
        parts = pool.map(_worker, jobs)
    lst = os.path.join(tmp, "list.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    out = os.path.join(OUT, a.name + ".mp4")
    af = ["-af", f"afade=t=out:st={dur - 0.4:.2f}:d=0.4"] if a.until else []
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                    "-i", a.audio, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-t", f"{dur:.3f}", *af, "-movflags", "+faststart", out], check=True)
    for p in parts:
        os.remove(p)
    os.remove(lst); os.rmdir(tmp)
    print("->", out)


if __name__ == "__main__":
    main()
