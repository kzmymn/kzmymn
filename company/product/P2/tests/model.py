"""原価率計算シートの計算を、数式とは独立に Python で再現する（期待値の計算用）。

仕様（使い方シートの「計算のきまり」と同じ）:
- 税抜仕入価格 = 税抜なら仕入価格、税込（空欄含む）なら ROUND(仕入価格 / (1+税率), 2)
  税率は空欄なら設定の仕入税率。1以上の値は % とみなし 100 で割る。
- 単価 = ROUND(税抜仕入価格 / 内容量, 4)。内容量が空欄か 0 なら空欄。
- 歩留まり後単価 = ROUND(単価 / 歩留まり, 4)。歩留まり空欄は 1、1を超える値は 100 で割る、0 なら空欄。
- 1行の原価 = ROUND(使用量 × 歩留まり後単価, 2)
- 合計原価 = 行原価の合計
- 税抜売価 = ROUND(販売価格 / (1+売価税率), 2)
- 原価率 = ROUND(合計原価 / 税抜売価, 4)。税抜売価が空欄か 0 なら空欄。
- 目標との差 = ROUND(原価率 - 目標, 4)
- 推奨売価 = 切り上げ(ROUND(合計原価 / 目標 × (1+売価税率), 2) / 10) × 10。合計原価0なら空欄。

丸めは Excel の ROUND と同じ「四捨五入（0から遠い方）」を Decimal で行う。
"""
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING

BLANK = ""


def D(x):
    return Decimal(str(x))


def rnd(x, n):
    return float(D(x).quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP))


def is_blank(v):
    return v is None or v == ""


def material_row(m, settings):
    name, unit_memo, price, kind, rate, qty, unit, yld = m
    out = {}
    if is_blank(name) or is_blank(price):
        J = BLANK
    else:
        r = settings["purchase_tax"] if is_blank(rate) else (rate / 100 if rate >= 1 else rate)
        J = float(price) if kind == "税抜" else rnd(D(price) / (1 + D(r)), 2)
    if J == BLANK or is_blank(qty) or qty == 0:
        K = BLANK
    else:
        K = rnd(D(J) / D(qty), 4)
    y = 1 if is_blank(yld) else (yld / 100 if yld > 1 else yld)
    if K == BLANK or y == 0:
        L = BLANK
    else:
        L = rnd(D(K) / D(y), 4)
    if is_blank(name):
        M = BLANK
    elif is_blank(price):
        M = "価格を入力"
    elif is_blank(qty) or qty == 0:
        M = "内容量を入力"
    elif not is_blank(yld) and yld == 0:
        M = "歩留まりが0"
    elif L == BLANK:
        M = "入力を確認"
    else:
        M = "OK"
    out.update(J=J, K=K, L=L, M=M, unit=unit)
    return out


def compute(materials, menus, settings):
    mats = {}
    mat_rows = []
    for m in materials:
        row = material_row(m, settings)
        mat_rows.append(row)
        if not is_blank(m[0]) and m[0] not in mats:   # VLOOKUP は最初の一致
            mats[m[0]] = row
    menu_out = []
    for name, price, target_in, tax_in, lines in menus:
        target = settings["target"] if is_blank(target_in) else (target_in / 100 if target_in > 1 else target_in)
        tax = settings["sales_tax"] if is_blank(tax_in) else (tax_in / 100 if tax_in >= 1 else tax_in)
        line_out = []
        total = Decimal(0)
        for mat, qty in lines:
            if is_blank(mat):
                line_out.append(dict(D=BLANK, E=BLANK, F=BLANK, G=BLANK))
                continue
            row = mats.get(mat)
            if row is None:
                dd, ee, gg = BLANK, BLANK, "未登録の材料"
            else:
                dd = "" if is_blank(row["unit"]) else str(row["unit"])
                ee = row["L"]
                gg = "材料マスタを確認" if ee == BLANK else ("使用量を入力" if is_blank(qty) else "OK")
            if is_blank(qty) or ee == BLANK:
                ff = BLANK
            else:
                ff = rnd(D(qty) * D(ee), 2)
                total += D(ff)
            line_out.append(dict(D=dd, E=ee, F=ff, G=gg))
        total = float(total)
        net = BLANK if is_blank(price) else rnd(D(price) / (1 + D(tax)), 2)
        rate = BLANK if (net == BLANK or net == 0) else rnd(D(total) / D(net), 4)
        diff = BLANK if rate == BLANK else rnd(D(rate) - D(target), 4)
        if rate == BLANK:
            judge = BLANK if is_blank(name) else "売価を入力"
        else:
            judge = "超過" if rate > target else "目標内"
        if total == 0 or target == 0:
            rec = BLANK
        else:
            x = rnd(D(total) / D(target) * (1 + D(tax)), 2)
            rec = float((D(x) / 10).quantize(Decimal(1), rounding=ROUND_CEILING) * 10)
        menu_out.append(dict(name=name, price=price, lines=line_out, total=total, target=target,
                             tax=tax, net=net, rate=rate, diff=diff, judge=judge, rec=rec))
    return mat_rows, menu_out
