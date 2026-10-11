"""P3 アレルゲン一覧表のテストケース。

各ケース:
  id, title  … 識別子と内容
  shop       … 店名（None なら空欄）
  menus      … 入力シートの行（上から順。None は空行）。
               dict(name, values={品目名: 値}, date, who, note)
  checks     … 手で書いた期待値 [(キー, 値)]。キーは run_tests.addr() を参照
  use_dist   … True なら dist の同梱ファイルそのものを使う
  edit_list  … dist をコピーし、品目リストを書き換える {セル: 値}
期待値は手書きの checks に加え、run_tests.model_checks() が全50行・全セルについて独立に計算する。
"""
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import build  # noqa: E402

C, N, Q = build.CONTAINS, build.NOTCONTAIN, build.UNKNOWN
NAMES = [it[1] for it in build.ITEMS]
D = datetime.date(2026, 10, 11)


def vals(default=N, **over):
    """全品目を default にし、over（品目名→値）で上書きする。値 None は空欄"""
    v = {n: default for n in NAMES}
    v.update(over.get("o", {}))
    return v


def menu(name, values, date=D, who="山田", note=None):
    return dict(name=name, values=values, date=date, who=who, note=note)


CASES = [
    dict(id="T01", title="○だけ（29品目すべて含む・確認日と確認者あり）→ 確認済み",
         shop="テスト店",
         menus=[menu("全部入り", vals(C))],
         checks=[("in:1:status", "確認済み"), ("in:1:ncont", 29), ("in:1:nunk", 0),
                 ("cu:1:item:えび", C), ("cu:1:item:りんご", C), ("cu:1:note", ""),
                 ("in:sum_unk", 0), ("in:sum_todo", 0)]),
    dict(id="T02", title="－だけ（含む品目なし）→ 確認済み・含む0",
         shop="テスト店",
         menus=[menu("白ごはん", vals(N))],
         checks=[("in:1:status", "確認済み"), ("in:1:ncont", 0), ("in:1:nunk", 0),
                 ("cu:1:item:小麦", N), ("cu:1:name", "白ごはん")]),
    dict(id="T03", title="○と－の混在 → 確認済み、お客様用に同じ記号",
         shop="テスト店",
         menus=[menu("天ぷら", vals(N, o={"えび": C, "小麦": C, "卵": C}), note="揚げ油を共用")],
         checks=[("in:1:status", "確認済み"), ("in:1:ncont", 3),
                 ("cu:1:item:えび", C), ("cu:1:item:かに", N), ("cu:1:item:卵", C),
                 ("cu:1:note", "揚げ油を共用"), ("cu:1:date", D)]),
    dict(id="T04", title="？が1つ残る → 未確認あり、お客様用は ？ と「※未確認あり。」",
         shop="テスト店",
         menus=[menu("サラダ", vals(N, o={"乳": Q, "ごま": C}), note="ドレッシングは市販品")],
         checks=[("in:1:status", "未確認あり"), ("in:1:nunk", 1), ("in:1:ncont", 1),
                 ("cu:1:item:乳", Q), ("cu:1:item:ごま", C),
                 ("cu:1:note", "※未確認あり。ドレッシングは市販品"), ("in:sum_unk", 1), ("in:sum_todo", 1)]),
    dict(id="T05", title="空欄が1つ残る → 未確認あり、お客様用は ？",
         shop="テスト店",
         menus=[menu("スープ", vals(N, o={"ゼラチン": None}))],
         checks=[("in:1:status", "未確認あり"), ("in:1:nunk", 1), ("cu:1:item:ゼラチン", Q),
                 ("cu:1:note", "※未確認あり。")]),
    dict(id="T06", title="メニュー名だけで品目がすべて空欄 → 未確認あり（29）、お客様用は全部 ？",
         shop="テスト店",
         menus=[menu("新メニュー", vals(None), date=None, who=None)],
         checks=[("in:1:status", "未確認あり"), ("in:1:nunk", 29), ("in:1:ncont", 0),
                 ("cu:1:item:えび", Q), ("cu:1:item:りんご", Q), ("cu:1:date", "")]),
    dict(id="T07", title="確認日なし（品目はすべて確定）→ 確認日なし、お客様用の確認日は空欄",
         shop="テスト店",
         menus=[menu("冷奴", vals(N, o={"大豆": C}), date=None)],
         checks=[("in:1:status", "確認日なし"), ("cu:1:date", ""), ("cu:1:item:大豆", C),
                 ("cu:1:note", ""), ("in:sum_unk", 0), ("in:sum_todo", 1)]),
    dict(id="T08", title="確認者なし → 確認者なし",
         shop="テスト店",
         menus=[menu("焼き鮭", vals(N, o={"さけ": C}), who=None)],
         checks=[("in:1:status", "確認者なし"), ("cu:1:item:さけ", C), ("cu:1:date", D)]),
    dict(id="T09", title="品目は入っているがメニュー名が空欄 → メニュー名なし、お客様用には出ない",
         shop="テスト店",
         menus=[dict(name=None, values=vals(N, o={"えび": C}), date=D, who="山田", note="メモ")],
         checks=[("in:1:status", "メニュー名なし"), ("cu:1:name", ""), ("cu:1:item:えび", ""),
                 ("cu:1:note", ""), ("in:sum_todo", 1)]),
    dict(id="T10", title="○－？以外の値（半角 - と o、空白）→ 入力値エラー、お客様用は ？",
         shop="テスト店",
         menus=[menu("貼り付けた行", vals(N, o={"えび": "-", "かに": "o", "くるみ": " "}))],
         checks=[("in:1:status", "入力値エラー"), ("cu:1:item:えび", Q), ("cu:1:item:かに", Q),
                 ("cu:1:item:くるみ", Q), ("cu:1:item:小麦", N), ("cu:1:note", "※未確認あり。")]),
    dict(id="T11", title="途中に空行（1行目と3行目だけ入力）→ 空行は状態もお客様用も空欄",
         shop="テスト店",
         menus=[menu("A定食", vals(N, o={"小麦": C})), None, menu("B定食", vals(N, o={"そば": C}))],
         checks=[("in:2:status", ""), ("in:2:ncont", ""), ("in:2:nunk", ""), ("cu:2:name", ""),
                 ("cu:2:item:えび", ""), ("cu:2:date", ""), ("cu:2:note", ""),
                 ("in:3:status", "確認済み"), ("cu:3:item:そば", C)]),
    dict(id="T12", title="50品すべて入力（最終行まで計算されるか）。うち8品は？あり",
         shop="テスト店",
         menus=[menu(f"メニュー{k + 1}",
                     vals(N, o={NAMES[k % 29]: C, NAMES[(k + 5) % 29]: (Q if k % 7 == 0 else N)}))
                for k in range(50)],
         checks=[("in:50:status", "未確認あり"), ("in:49:status", "確認済み"), ("cu:50:name", "メニュー50"), ("cu:50:item:" + NAMES[49 % 29], C),
                 ("in:1:status", "未確認あり"), ("in:sum_unk", 8), ("in:sum_todo", 8)]),
    dict(id="T13", title="店名が空欄 → お客様用の表題は「アレルゲン一覧表」",
         shop=None,
         menus=[menu("おにぎり", vals(N))],
         checks=[("cu:title", "アレルゲン一覧表")]),
    dict(id="T14", title="品目リストを1件書き換える（同梱ファイルの C12「落花生（ピーナッツ）」→「ピーナッツ」、B14「アーモンド」の区分「推奨」→「義務」）"
                       "→ 入力・お客様用の見出しに反映",
         use_dist=True,
         edit_list={"C12": "ピーナッツ", "B14": "義務"},
         checks=[("in:head:8", "ピーナッツ"), ("cu:head:8", "ピーナッツ"),
                 ("in:kubun:10", "義務"), ("cu:kubun:10", "義務"),
                 ("in:head:1", "えび"), ("cu:head:29", "りんご")]),
    dict(id="T15", title="同梱ファイル（見本3品）そのもの → 確認済み／未確認あり／確認日なし",
         use_dist=True,
         checks=[("cu:title", "〇〇食堂（見本）　アレルゲン一覧表"),
                 ("in:1:status", "確認済み"), ("in:2:status", "未確認あり"), ("in:3:status", "確認日なし"),
                 ("cu:2:item:乳", Q), ("cu:1:item:鶏肉", C), ("cu:1:item:えび", N),
                 ("cu:2:note", "※未確認あり。" + build.SAMPLE_NOTE),
                 ("in:sum_unk", 1), ("in:sum_todo", 2), ("cu:4:name", "")]),
]
