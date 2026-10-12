"""テストケース（入力と、手で計算した主要な期待値）。

各ケースの全セルは model.py（Python の独立計算）でも期待値を作り、
LibreOffice で再計算したセル値と照合する。ここの「checks」は model.py 自体の検算を兼ねる。

check の書き方:
  ("mat:1:J", 1000)          材料1行目の J 列（税抜仕入価格）
  ("menu:1:line:2:F", 0.13)  メニュー1の材料2行目の F 列（原価）
  ("menu:1:rate", 0.1)       メニュー1の原価率（total, target, tax, net, rate, diff, judge, rec）
  ("list:1:judge", "超過")   一覧シート1行目（name, price, total, rate, target, diff, judge, rec）
  "" は空欄の期待値。
"""
S = {"target": 0.30, "sales_tax": 0.10, "purchase_tax": 0.08}

#           名前, 仕入単位, 価格, 税区分, 税率, 内容量, 単位, 歩留まり
CASES = [
    dict(id="T01", title="通常：税込の仕入価格を8%で割り戻す",
         materials=[("材料A", "1kg", 1080, "税込", None, 1000, "g", None)],
         menus=[("品A", 1100, None, None, [("材料A", 100)])],
         checks=[("mat:1:J", 1000), ("mat:1:K", 1), ("mat:1:L", 1), ("mat:1:M", "OK"),
                 ("menu:1:line:1:F", 100), ("menu:1:net", 1000), ("menu:1:rate", 0.1),
                 ("menu:1:diff", -0.2), ("menu:1:judge", "目標内"), ("menu:1:rec", 370)]),
    dict(id="T02", title="税区分が税抜なら割り戻さない",
         materials=[("材料B", "500g", 1000, "税抜", None, 500, "g", None)],
         menus=[("品B", 1100, None, None, [("材料B", 50)])],
         checks=[("mat:1:J", 1000), ("mat:1:K", 2), ("menu:1:line:1:F", 100), ("menu:1:rate", 0.1)]),
    dict(id="T03", title="歩留まり80%（0.8で入力）",
         materials=[("材料C", "1kg", 1000, "税抜", None, 1000, "g", 0.8)],
         menus=[("品C", 1100, None, None, [("材料C", 100)])],
         checks=[("mat:1:K", 1), ("mat:1:L", 1.25), ("menu:1:line:1:F", 125), ("menu:1:rate", 0.125)]),
    dict(id="T04", title="歩留まりを「85」と数字で入力（85%として扱う）",
         materials=[("材料D", "1kg", 850, "税抜", None, 1000, "g", 85)],
         menus=[("品D", 550, None, None, [("材料D", 200)])],
         checks=[("mat:1:K", 0.85), ("mat:1:L", 1), ("menu:1:line:1:F", 200), ("menu:1:rate", 0.4),
                 ("menu:1:judge", "超過"), ("menu:1:diff", 0.1), ("menu:1:rec", 740)]),
    dict(id="T05", title="税率を「10」と入力（容器など10%の品）",
         materials=[("容器", "50枚", 1100, "税込", 10, 50, "枚", None)],
         menus=[("品E", 1100, None, None, [("容器", 1)])],
         checks=[("mat:1:J", 1000), ("mat:1:K", 20), ("menu:1:line:1:F", 20), ("menu:1:rate", 0.02)]),
    dict(id="T06", title="空欄：仕入価格が空欄（エラーを出さず、チェック列に文字）",
         materials=[("材料F", "1kg", None, "税込", None, 1000, "g", None),
                    ("材料G", "1kg", 1000, "税抜", None, 1000, "g", None)],
         menus=[("品F", 1100, None, None, [("材料F", 100), ("材料G", 100)])],
         checks=[("mat:1:J", ""), ("mat:1:K", ""), ("mat:1:L", ""), ("mat:1:M", "価格を入力"),
                 ("menu:1:line:1:E", ""), ("menu:1:line:1:F", ""), ("menu:1:line:1:G", "材料マスタを確認"),
                 ("menu:1:total", 100), ("menu:1:rate", 0.1)]),
    dict(id="T07", title="内容量0（#DIV/0! を出さない）",
         materials=[("材料H", "1袋", 500, "税抜", None, 0, "g", None)],
         menus=[("品H", 1100, None, None, [("材料H", 10)])],
         checks=[("mat:1:J", 500), ("mat:1:K", ""), ("mat:1:L", ""), ("mat:1:M", "内容量を入力"),
                 ("menu:1:line:1:F", ""), ("menu:1:total", 0), ("menu:1:rate", 0), ("menu:1:rec", "")]),
    dict(id="T08", title="歩留まり0（#DIV/0! を出さない）",
         materials=[("材料I", "1kg", 1000, "税抜", None, 1000, "g", 0)],
         menus=[],
         checks=[("mat:1:K", 1), ("mat:1:L", ""), ("mat:1:M", "歩留まりが0")]),
    dict(id="T09", title="0円の材料（自家製・もらい物など）",
         materials=[("材料J", "1L", 0, "税込", None, 1000, "ml", None)],
         menus=[("品J", 330, None, None, [("材料J", 200)])],
         checks=[("mat:1:J", 0), ("mat:1:K", 0), ("mat:1:L", 0), ("menu:1:line:1:F", 0),
                 ("menu:1:total", 0), ("menu:1:rate", 0), ("menu:1:judge", "目標内"), ("menu:1:rec", "")]),
    dict(id="T10", title="販売価格が空欄・0円（原価率は空欄、判定は「売価を入力」）",
         materials=[("材料K", "1kg", 1000, "税抜", None, 1000, "g", None)],
         menus=[("品K1", None, None, None, [("材料K", 100)]),
                ("品K2", 0, None, None, [("材料K", 100)])],
         checks=[("menu:1:net", ""), ("menu:1:rate", ""), ("menu:1:diff", ""), ("menu:1:judge", "売価を入力"),
                 ("menu:2:net", 0), ("menu:2:rate", ""), ("menu:2:judge", "売価を入力"),
                 ("list:1:rate", ""), ("list:1:judge", "売価を入力"), ("list:1:rec", 370)]),
    dict(id="T11", title="未登録の材料名・使用量の空欄（#N/A を出さない）",
         materials=[("材料L", "1kg", 1000, "税抜", None, 1000, "g", None)],
         menus=[("品L", 1100, None, None, [("存在しない材料", 100), ("材料L", None), ("材料L", 30)])],
         checks=[("menu:1:line:1:D", ""), ("menu:1:line:1:E", ""), ("menu:1:line:1:F", ""),
                 ("menu:1:line:1:G", "未登録の材料"), ("menu:1:line:2:F", ""), ("menu:1:line:2:G", "使用量を入力"),
                 ("menu:1:line:3:F", 30), ("menu:1:total", 30)]),
    dict(id="T12", title="端数の丸め：税抜仕入は小数2位、単価は小数4位",
         materials=[("材料M", "7個", 1001, "税込", None, 7, "個", None)],
         menus=[("品M", 1000, None, None, [("材料M", 3)])],
         checks=[("mat:1:J", 926.85), ("mat:1:K", 132.4071), ("menu:1:line:1:F", 397.22),
                 ("menu:1:net", 909.09), ("menu:1:rate", 0.4369)]),
    dict(id="T13", title="端数の丸め：ちょうど0.5の境目は切り上げ（0.125円→0.13円）",
         materials=[("材料N", "8g", 1, "税抜", None, 8, "g", None)],
         menus=[("品N", 110, None, None, [("材料N", 1)])],
         checks=[("mat:1:K", 0.125), ("menu:1:line:1:F", 0.13), ("menu:1:rate", 0.0013)]),
    dict(id="T14", title="推奨売価：割り切れるときは切り上げない（300円÷30%×1.1＝1,100円）",
         materials=[("材料O", "1kg", 1000, "税抜", None, 1000, "g", None)],
         menus=[("品O", 1000, None, None, [("材料O", 300)])],
         checks=[("menu:1:total", 300), ("menu:1:rec", 1100), ("menu:1:judge", "超過"),
                 ("menu:1:rate", 0.33), ("menu:1:diff", 0.03)]),
    dict(id="T15", title="メニューごとの目標（「25」と入力）と売価の税率8%（持ち帰り）",
         materials=[("材料P", "1kg", 1000, "税抜", None, 1000, "g", None)],
         menus=[("品P", 540, 25, 0.08, [("材料P", 100)])],
         checks=[("menu:1:target", 0.25), ("menu:1:tax", 0.08), ("menu:1:net", 500), ("menu:1:rate", 0.2),
                 ("menu:1:diff", -0.05), ("menu:1:rec", 440), ("list:1:target", 0.25)]),
    dict(id="T16", title="15行すべて使う（合計の範囲）",
         materials=[("材料Q", "1kg", 1000, "税抜", None, 1000, "g", None)],
         menus=[("品Q", 3300, None, None, [("材料Q", 10 * (k + 1)) for k in range(15)])],
         checks=[("menu:1:total", 1200), ("menu:1:net", 3000), ("menu:1:rate", 0.4), ("menu:1:rec", 4400)]),
    dict(id="T17", title="30品目のメニューと一覧（最後のブロックまで計算される）",
         materials=[("材料R", "1kg", 1000, "税抜", None, 1000, "g", None)],
         menus=[(f"品R{k + 1}", 1100, None, None, [("材料R", 10 * (k + 1))]) for k in range(30)],
         checks=[("menu:30:total", 300), ("menu:30:rate", 0.3), ("menu:30:judge", "目標内"),
                 ("list:30:name", "品R30"), ("list:30:rate", 0.3), ("list:29:rate", 0.29),
                 ("list:30:rec", 1100)]),
    dict(id="T18", title="目標と同じ原価率は「目標内」、メニュー名が空欄の一覧行は空欄",
         materials=[("材料S", "1kg", 1000, "税抜", None, 1000, "g", None)],
         menus=[("品S", 1100, None, None, [("材料S", 300)])],
         checks=[("menu:1:rate", 0.3), ("menu:1:judge", "目標内"), ("menu:1:diff", 0),
                 ("list:2:name", ""), ("list:2:rate", ""), ("list:2:judge", ""), ("menu:2:judge", "")]),
]


def sample_case():
    """dist の見本データそのもの（見本の架空の数値）"""
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import build
    return dict(id="S01", title="同梱ファイルの見本データ（dist/genka-keisan.xlsx そのもの）",
                materials=build.SAMPLE_MATERIALS, menus=build.SAMPLE_MENUS,
                settings=build.SAMPLE_SETTINGS, checks=[], use_dist=True)
