#!/usr/bin/env python3
"""P2「原価率計算シート」の xlsx を生成する。

使い方:
    python3 company/product/P2/build.py            # dist/genka-keisan.xlsx を作る（見本データ入り）

tests/ からは build_workbook(path, materials, menus, settings) を呼び、
テスト用の入力を入れたブックを作る（数式は同じ）。

互換性の方針（Excel と Google スプレッドシート）:
- 関数は SUM, IF, IFERROR, ROUND, ROUNDUP, VLOOKUP, OR, AND のみ使う。
- 名前付き範囲・テーブル（構造化参照）・マクロ・外部リンク・シート保護は使わない。
- 入力規則のリストは「設定」シートのセル範囲を参照する（直接文字列のリストは使わない）。
- 条件付き書式は「セルの値が "超過" に等しい」だけ。判定は必ず文字でも表示する。
"""
from __future__ import annotations

import os
import sys

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.workbook.properties import CalcProperties
from openpyxl.worksheet.datavalidation import DataValidation

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "dist")
OUT = os.path.join(DIST, "genka-keisan.xlsx")

# ---- レイアウト定数（tests からも参照する） ----
MAT_SHEET = "材料マスタ"
MENU_SHEET = "メニュー原価"
LIST_SHEET = "一覧"
SET_SHEET = "設定"
HOWTO_SHEET = "使い方"

MAT_FIRST = 5            # 材料マスタのデータ開始行
MAT_ROWS = 100           # 材料の最大数
MAT_LAST = MAT_FIRST + MAT_ROWS - 1

MENU_COUNT = 30          # メニューの最大数
LINES = 15               # 1メニューあたりの材料行
BLOCK = 25               # 1メニューのブロック行数（空行を含む）
MENU_FIRST = 4           # 最初のブロックの開始行

# ブロック内の相対位置
OFF_NAME = 0
OFF_PRICE = 1
OFF_HEAD = 2
OFF_LINE1 = 3
OFF_TOTAL = OFF_LINE1 + LINES          # 18
OFF_TARGET = OFF_TOTAL + 1             # 19 目標原価率（適用値）
OFF_TAX = OFF_TOTAL + 2                # 20 売価の税率（適用値）
OFF_NET = OFF_TOTAL + 3                # 21 税抜売価
OFF_RATE = OFF_TOTAL + 4               # 22 原価率・判定
OFF_DIFF = OFF_TOTAL + 5               # 23 目標との差
OFF_REC = OFF_TOTAL + 6                # 24 推奨売価

# 設定シートのセル
SET_TARGET = f"'{SET_SHEET}'!$C$4"
SET_SALES_TAX = f"'{SET_SHEET}'!$C$5"
SET_PURCHASE_TAX = f"'{SET_SHEET}'!$C$6"
SET_TAXKIND_RANGE = f"'{SET_SHEET}'!$B$11:$B$12"


def block_start(i: int) -> int:
    """i 番目（0始まり）のメニューブロックの先頭行"""
    return MENU_FIRST + i * BLOCK


# ---- 見本データ（見本の架空の数値） ----
SAMPLE_SETTINGS = {"target": 0.30, "sales_tax": 0.10, "purchase_tax": 0.08}

# (材料名, 仕入単位, 仕入価格, 税区分, 税率, 内容量, 単位, 歩留まり)
SAMPLE_MATERIALS = [
    ("豚こま切れ肉", "1kgパック", 1280, "税込", None, 1000, "g", None),
    ("鶏もも肉", "2kgパック", 1980, "税抜", None, 2000, "g", 0.9),
    ("玉ねぎ", "3kg袋", 698, "税込", None, 3000, "g", 0.9),
    ("じゃがいも", "1kg袋", 298, "税込", None, 1000, "g", 0.85),
    ("卵", "10個パック", 248, "税込", None, 10, "個", None),
    ("米", "10kg袋", 4980, "税込", None, 10000, "g", None),
    ("キャベツ", "1玉", 198, "税込", None, 1200, "g", 0.8),
    ("しょうゆ", "1.8Lボトル", 498, "税込", None, 1800, "ml", None),
    ("マヨネーズ", "1kg袋", 598, "税抜", None, 1000, "g", None),
    ("持ち帰り容器", "50枚入り", 1100, "税込", 0.10, 50, "枚", None),
]

# (メニュー名, 販売価格（税込）, 目標原価率, 売価の税率, [(材料名, 使用量), ...])
SAMPLE_MENUS = [
    ("豚のしょうが焼き定食（見本）", 980, None, None,
     [("豚こま切れ肉", 120), ("玉ねぎ", 50), ("キャベツ", 60), ("しょうゆ", 15), ("米", 150)]),
    ("親子丼（見本）", 780, None, None,
     [("鶏もも肉", 100), ("卵", 2), ("玉ねぎ", 40), ("しょうゆ", 15), ("米", 150)]),
    ("ポテトサラダ 持ち帰り（見本）", 380, 0.25, 0.08,
     [("じゃがいも", 120), ("玉ねぎ", 15), ("マヨネーズ", 25), ("持ち帰り容器", 1)]),
]

# ---- スタイル ----
F_TITLE = Font(name="Meiryo", size=14, bold=True)
F_BOLD = Font(name="Meiryo", bold=True)
F_NORMAL = Font(name="Meiryo")
F_NOTE = Font(name="Meiryo", size=9, color="555555")
FILL_INPUT = PatternFill("solid", fgColor="FFF6CC")   # 入力欄（見出しにも【入力】と書く）
FILL_HEAD = PatternFill("solid", fgColor="DDE6F0")
FILL_CALC = PatternFill("solid", fgColor="F2F2F2")
FILL_OVER = PatternFill("solid", fgColor="F8CBAD")
THIN = Side(style="thin", color="999999")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")


def _cell(ws, ref, value=None, font=F_NORMAL, fill=None, fmt=None, border=False, align=None):
    c = ws[ref]
    if value is not None:
        c.value = value
    c.font = font
    if fill:
        c.fill = fill
    if fmt:
        c.number_format = fmt
    if border:
        c.border = BORDER
    if align:
        c.alignment = align
    return c


# ---------------------------------------------------------------- 使い方
HOWTO_LINES = [
    ("原価率計算シート（個人経営の飲食店向け）", F_TITLE),
    ("", None),
    ("■ このファイルでできること", F_BOLD),
    ("・材料の仕入価格から、1g・1ml・1個あたりの単価を自動で計算します（歩留まりも考慮）。", None),
    ("・メニューごとに材料と使用量を入れると、1品の原価・原価率・目標との差・推奨売価が出ます。", None),
    ("・「一覧」シートで全メニュー（最大30品）の原価率を並べて確認できます。", None),
    ("", None),
    ("■ 使う順番", F_BOLD),
    ("1. 「設定」シートで、目標原価率と消費税率を確認します（初期値：目標30%、売価10%、仕入8%）。", None),
    ("2. 「材料マスタ」に材料を登録します（最大100件）。黄色のセル＝入力欄です（見出しに【入力】と書いてあります）。", None),
    ("   ・仕入価格は、レシートどおりの金額を入れ、「税込」か「税抜」を選びます（空欄は税込として扱います）。", None),
    ("   ・税率は空欄なら「設定」の仕入の税率（8%）を使います。容器など食品以外は10%を入れてください。", None),
    ("   ・内容量は、単位（g・ml・個・枚など）とそろえて数字で入れます。例：1kg袋なら 1000（単位 g）。", None),
    ("   ・歩留まりは、皮・骨・筋などを除いて実際に使える割合です。空欄は100%として扱います。85% または 85 と入力できます。", None),
    ("3. 「メニュー原価」に、メニュー名・販売価格（税込）を入れ、材料を選んで使用量を入れます（1品15行まで）。", None),
    ("   ・材料名はリストから選びます。使用量は材料マスタの単位（g・ml・個など）で入れます。", None),
    ("   ・目標原価率・売価の税率は、空欄なら「設定」の値を使います。持ち帰り（8%）の品だけ変える、などができます。", None),
    ("4. 「一覧」で全メニューを確認します。目標を超えた品は「超過」と表示されます。", None),
    ("", None),
    ("■ 計算のきまり", F_BOLD),
    ("・原価も売価も「税抜」でそろえて原価率を計算します（税込の仕入価格は税率で割り戻します）。", None),
    ("・税抜仕入価格は小数第2位、単価は小数第4位、1行の原価は小数第2位で四捨五入します。原価率は小数第4位（0.01%単位）で四捨五入します。", None),
    ("・推奨売価（税込）＝ 合計原価 ÷ 目標原価率 ×（1＋売価の税率）を、10円単位で切り上げた金額です。", None),
    ("・入力が足りないところは空欄のまま表示し、エラー（#DIV/0! など）は出ないようにしています。", None),
    ("・材料マスタの「チェック」列、メニューの「チェック」列に、入力の不足（例：内容量を入力、未登録の材料）を文字で表示します。", None),
    ("", None),
    ("■ 見本データについて", F_BOLD),
    ("・最初に入っている店名「〇〇食堂（見本）」、材料、メニュー、金額は、すべて見本の架空の数値です。実在の店や商品の価格ではありません。", None),
    ("・自分の店で使うときは、見本の行を消すか上書きしてください（数式の入っている灰色の列は消さないでください）。", None),
    ("", None),
    ("■ 対応ソフト", F_BOLD),
    ("・Microsoft Excel（デスクトップ版）、Google スプレッドシート（Googleドライブにアップロードして開く）を想定しています。", None),
    ("・マクロ・外部リンク・新しい関数（XLOOKUP など）は使っていません。", None),
    ("", None),
    ("■ ご注意", F_BOLD),
    ("・計算結果は入力した数字に基づく目安です。価格の決定は、ご自身の判断で行ってください。", None),
]


def _howto(ws):
    ws.column_dimensions["A"].width = 120
    for i, (text, font) in enumerate(HOWTO_LINES, start=1):
        c = ws.cell(row=i, column=1, value=text)
        c.font = font or F_NORMAL
        c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.sheet_view.showGridLines = False


# ---------------------------------------------------------------- 設定
def _settings(ws, s):
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 34
    ws.column_dimensions["C"].width = 14
    ws.column_dimensions["D"].width = 60
    _cell(ws, "B1", "設定", F_TITLE)
    _cell(ws, "B2", "店名：〇〇食堂（見本）", F_NORMAL)
    _cell(ws, "B3", "項目", F_BOLD, FILL_HEAD, border=True)
    _cell(ws, "C3", "【入力】値", F_BOLD, FILL_HEAD, border=True)
    _cell(ws, "D3", "説明", F_BOLD, FILL_HEAD, border=True)
    rows = [
        (4, "目標原価率", s["target"], "メニューごとに空欄のときに使う目標。30% または 30 と入力できます。"),
        (5, "売価の消費税率", s["sales_tax"], "販売価格（税込）を税抜に直すときの税率。店内飲食は10%。"),
        (6, "仕入の消費税率（初期値）", s["purchase_tax"], "材料マスタの税率が空欄のときに使う税率。食品は8%。"),
    ]
    for r, label, val, note in rows:
        _cell(ws, f"B{r}", label, border=True)
        _cell(ws, f"C{r}", val, fill=FILL_INPUT, fmt="0%", border=True)
        _cell(ws, f"D{r}", note, F_NOTE, border=True, align=WRAP)
    _cell(ws, "B9", "見本の数値はすべて架空です。", F_NOTE)
    _cell(ws, "B10", "税区分のリスト（消さないでください）", F_NOTE)
    _cell(ws, "B11", "税込")
    _cell(ws, "B12", "税抜")


# ---------------------------------------------------------------- 材料マスタ
MAT_HEADERS = [
    ("A", "No", 5, None),
    ("B", "【入力】材料名", 22, FILL_INPUT),
    ("C", "【入力】仕入単位（メモ）", 14, FILL_INPUT),
    ("D", "【入力】仕入価格（円）", 12, FILL_INPUT),
    ("E", "【入力】税区分（税込／税抜）", 12, FILL_INPUT),
    ("F", "【入力】税率（空欄=設定値）", 11, FILL_INPUT),
    ("G", "【入力】内容量", 10, FILL_INPUT),
    ("H", "【入力】単位", 7, FILL_INPUT),
    ("I", "【入力】歩留まり（空欄=100%）", 12, FILL_INPUT),
    ("J", "税抜仕入価格（円）［自動］", 13, FILL_CALC),
    ("K", "単位あたり単価（税抜・円）［自動］", 14, FILL_CALC),
    ("L", "歩留まり後の単価（税抜・円）［自動］", 15, FILL_CALC),
    ("M", "チェック［自動］", 16, FILL_CALC),
]


def mat_formulas(r: int) -> dict:
    rate = f"IF(F{r}=\"\",{SET_PURCHASE_TAX},IF(F{r}>=1,F{r}/100,F{r}))"
    yld = f"IF(I{r}=\"\",1,IF(I{r}>1,I{r}/100,I{r}))"
    return {
        "J": f'=IF(OR(B{r}="",D{r}=""),"",IFERROR(IF(E{r}="税抜",D{r},ROUND(D{r}/(1+{rate}),2)),""))',
        "K": f'=IFERROR(IF(OR(J{r}="",G{r}="",G{r}=0),"",ROUND(J{r}/G{r},4)),"")',
        "L": f'=IFERROR(IF(K{r}="","",IF({yld}=0,"",ROUND(K{r}/{yld},4))),"")',
        "M": (f'=IF(B{r}="","",IF(D{r}="","価格を入力",IF(OR(G{r}="",G{r}=0),"内容量を入力",'
              f'IF(AND(I{r}<>"",I{r}=0),"歩留まりが0",IF(L{r}="","入力を確認","OK")))))'),
    }


def _materials(ws, materials):
    _cell(ws, "A1", "材料マスタ", F_TITLE)
    _cell(ws, "A2", "黄色＝入力欄（見出しに【入力】）、灰色＝自動計算（数式。消さないでください）。"
          "見本の行は見本の架空の数値です。", F_NOTE)
    _cell(ws, "A3", "仕入価格はレシートどおりに入れ、税込か税抜かを選びます。空欄は税込として扱います。", F_NOTE)
    for col, title, width, fill in MAT_HEADERS:
        _cell(ws, f"{col}4", title, F_BOLD, FILL_HEAD, border=True, align=Alignment(wrap_text=True, vertical="center"))
        ws.column_dimensions[col].width = width
    ws.row_dimensions[4].height = 48
    for i in range(MAT_ROWS):
        r = MAT_FIRST + i
        _cell(ws, f"A{r}", i + 1, border=True)
        for col, _, _, fill in MAT_HEADERS[1:9]:
            _cell(ws, f"{col}{r}", fill=FILL_INPUT, border=True)
        ws[f"D{r}"].number_format = "#,##0"
        ws[f"F{r}"].number_format = "0%"
        ws[f"G{r}"].number_format = "#,##0.##"
        ws[f"I{r}"].number_format = "0%"
        for col, f in mat_formulas(r).items():
            _cell(ws, f"{col}{r}", f, fill=FILL_CALC, border=True)
        ws[f"J{r}"].number_format = "#,##0.00"
        ws[f"K{r}"].number_format = "#,##0.0000"
        ws[f"L{r}"].number_format = "#,##0.0000"
    for i, m in enumerate(materials):
        r = MAT_FIRST + i
        for col, v in zip("BCDEFGHI", m):
            if v is not None:
                ws[f"{col}{r}"].value = v
    dv = DataValidation(type="list", formula1=SET_TAXKIND_RANGE, allow_blank=True)
    dv.error = "「税込」か「税抜」を選んでください"
    dv.errorTitle = "税区分"
    ws.add_data_validation(dv)
    dv.add(f"E{MAT_FIRST}:E{MAT_LAST}")
    ws.freeze_panes = f"C{MAT_FIRST}"


# ---------------------------------------------------------------- メニュー原価
def menu_cells(i: int) -> dict:
    """i 番目のメニューの主要セル番地"""
    s = block_start(i)
    return {
        "name": f"C{s + OFF_NAME}",
        "price": f"C{s + OFF_PRICE}",
        "target_in": f"E{s + OFF_PRICE}",
        "tax_in": f"G{s + OFF_PRICE}",
        "line_first": s + OFF_LINE1,
        "line_last": s + OFF_LINE1 + LINES - 1,
        "total": f"C{s + OFF_TOTAL}",
        "target": f"C{s + OFF_TARGET}",
        "tax": f"C{s + OFF_TAX}",
        "net": f"C{s + OFF_NET}",
        "rate": f"C{s + OFF_RATE}",
        "judge": f"E{s + OFF_RATE}",
        "diff": f"C{s + OFF_DIFF}",
        "rec": f"C{s + OFF_REC}",
    }


def line_formulas(r: int) -> dict:
    mrange = f"'{MAT_SHEET}'!$B${MAT_FIRST}:$L${MAT_LAST}"
    return {
        "D": f'=IF(B{r}="","",IFERROR(VLOOKUP(B{r},{mrange},7,FALSE)&"",""))',
        "E": f'=IF(B{r}="","",IFERROR(VLOOKUP(B{r},{mrange},11,FALSE),""))',
        "F": f'=IF(OR(B{r}="",C{r}=""),"",IFERROR(ROUND(C{r}*E{r},2),""))',
        "G": (f'=IF(B{r}="","",IFERROR(IF(VLOOKUP(B{r},{mrange},11,FALSE)="","材料マスタを確認",'
              f'IF(C{r}="","使用量を入力","OK")),"未登録の材料"))'),
    }


def _menus(ws, menus):
    _cell(ws, "A1", "メニュー原価", F_TITLE)
    _cell(ws, "A2", "黄色＝入力欄（【入力】）、灰色＝自動計算。原価・売価とも税抜で原価率を計算します。"
          "見本のメニューと金額は見本の架空の数値です。", F_NOTE)
    for col, w in zip("ABCDEFG", (11, 34, 14, 22, 16, 13, 18)):
        ws.column_dimensions[col].width = w
    mrange_names = f"'{MAT_SHEET}'!$B${MAT_FIRST}:$B${MAT_LAST}"
    dv = DataValidation(type="list", formula1=mrange_names, allow_blank=True)
    dv.error = "材料マスタに登録した材料名を選んでください"
    dv.errorTitle = "材料名"
    dv.showErrorMessage = False   # 未登録の名前も入力でき、チェック列に「未登録の材料」と出す
    ws.add_data_validation(dv)

    for i in range(MENU_COUNT):
        s = block_start(i)
        c = menu_cells(i)
        _cell(ws, f"A{s}", f"メニュー{i + 1}", F_BOLD, FILL_HEAD, border=True)
        _cell(ws, f"B{s}", "【入力】メニュー名", F_BOLD, border=True)
        _cell(ws, c["name"], fill=FILL_INPUT, border=True)
        ws.merge_cells(f"C{s}:G{s}")
        p = s + OFF_PRICE
        _cell(ws, f"B{p}", "【入力】販売価格（税込・円）", border=True)
        _cell(ws, c["price"], fill=FILL_INPUT, fmt="#,##0", border=True)
        _cell(ws, f"D{p}", "【入力】目標原価率（空欄=設定値）", F_NOTE, border=True, align=WRAP)
        _cell(ws, c["target_in"], fill=FILL_INPUT, fmt="0%", border=True)
        _cell(ws, f"F{p}", "【入力】売価の税率（空欄=設定値）", F_NOTE, border=True, align=WRAP)
        _cell(ws, c["tax_in"], fill=FILL_INPUT, fmt="0%", border=True)
        h = s + OFF_HEAD
        for col, t in zip("ABCDEFG", ("No", "【入力】材料名（リストから選ぶ）", "【入力】使用量",
                                       "単位［自動］", "単価（税抜・円/単位）［自動］", "原価（円）［自動］",
                                       "チェック［自動］")):
            _cell(ws, f"{col}{h}", t, F_BOLD, FILL_HEAD, border=True, align=Alignment(wrap_text=True))
        ws.row_dimensions[h].height = 32
        for k in range(LINES):
            r = c["line_first"] + k
            _cell(ws, f"A{r}", k + 1, border=True)
            _cell(ws, f"B{r}", fill=FILL_INPUT, border=True)
            _cell(ws, f"C{r}", fill=FILL_INPUT, fmt="#,##0.##", border=True)
            for col, f in line_formulas(r).items():
                _cell(ws, f"{col}{r}", f, fill=FILL_CALC, border=True)
            ws[f"E{r}"].number_format = "#,##0.0000"
            ws[f"F{r}"].number_format = "#,##0.00"
        dv.add(f"B{c['line_first']}:B{c['line_last']}")

        lf, ll = c["line_first"], c["line_last"]
        tin, xin = c["target_in"], c["tax_in"]
        price = c["price"]
        formulas = [
            (OFF_TOTAL, "合計原価（税抜・円）", f"=SUM(F{lf}:F{ll})", "#,##0.00"),
            (OFF_TARGET, "目標原価率（適用値）",
             f'=IF({tin}="",{SET_TARGET},IF({tin}>1,{tin}/100,{tin}))', "0.0%"),
            (OFF_TAX, "売価の税率（適用値）",
             f'=IF({xin}="",{SET_SALES_TAX},IF({xin}>=1,{xin}/100,{xin}))', "0%"),
            (OFF_NET, "税抜売価（円）",
             f'=IF({price}="","",IFERROR(ROUND({price}/(1+{c["tax"]}),2),""))', "#,##0.00"),
            (OFF_RATE, "原価率",
             f'=IFERROR(IF(OR({c["net"]}="",{c["net"]}=0),"",ROUND({c["total"]}/{c["net"]},4)),"")', "0.00%"),
            (OFF_DIFF, "目標との差（＋は目標超過）",
             f'=IF({c["rate"]}="","",ROUND({c["rate"]}-{c["target"]},4))', "+0.00%;-0.00%;0.00%"),
            (OFF_REC, "推奨売価（税込・円／目標原価率から逆算、10円単位で切り上げ）",
             (f'=IFERROR(IF(OR({c["total"]}=0,{c["target"]}=0),"",'
              f'ROUNDUP(ROUND({c["total"]}/{c["target"]}*(1+{c["tax"]}),2)/10,0)*10),"")'), "#,##0"),
        ]
        for off, label, f, fmt in formulas:
            r = s + off
            _cell(ws, f"B{r}", label, F_BOLD if off in (OFF_TOTAL, OFF_RATE, OFF_REC) else F_NORMAL,
                  border=True, align=Alignment(wrap_text=True))
            _cell(ws, f"C{r}", f, F_BOLD, FILL_CALC, fmt=fmt, border=True)
        rr = s + OFF_RATE
        _cell(ws, f"D{rr}", "判定［自動］", border=True)
        _cell(ws, c["judge"],
              (f'=IF({c["rate"]}="",IF({c["name"]}="","","売価を入力"),'
               f'IF({c["rate"]}>{c["target"]},"超過","目標内"))'),
              F_BOLD, FILL_CALC, border=True)
        ws.row_dimensions[s + OFF_REC].height = 30

    ws.conditional_formatting.add(
        f"E{MENU_FIRST}:E{block_start(MENU_COUNT - 1) + BLOCK}",
        CellIsRule(operator="equal", formula=['"超過"'], fill=FILL_OVER))

    for i, (name, price, target, tax, lines) in enumerate(menus):
        c = menu_cells(i)
        ws[c["name"]].value = name
        if price is not None:
            ws[c["price"]].value = price
        if target is not None:
            ws[c["target_in"]].value = target
        if tax is not None:
            ws[c["tax_in"]].value = tax
        for k, (mat, qty) in enumerate(lines):
            r = c["line_first"] + k
            if mat is not None:
                ws[f"B{r}"].value = mat
            if qty is not None:
                ws[f"C{r}"].value = qty
    ws.freeze_panes = "A4"


# ---------------------------------------------------------------- 一覧
LIST_FIRST = 5
LIST_COLS = [
    ("A", "No", 5, None, "name"),
    ("B", "メニュー名", 34, None, "name"),
    ("C", "販売価格（税込・円）", 12, "#,##0", "price"),
    ("D", "合計原価（税抜・円）", 12, "#,##0.00", "total"),
    ("E", "原価率", 10, "0.00%", "rate"),
    ("F", "目標原価率", 10, "0.0%", "target"),
    ("G", "目標との差", 10, "+0.00%;-0.00%;0.00%", "diff"),
    ("H", "判定", 10, None, "judge"),
    ("I", "推奨売価（税込・円）", 12, "#,##0", "rec"),
]


def _list(ws):
    _cell(ws, "A1", "一覧（全メニューの原価率）", F_TITLE)
    _cell(ws, "A2", "このシートは自動で表示されます（入力は不要）。判定が「超過」の品は、目標原価率を超えています。", F_NOTE)
    _cell(ws, "A3", "店名：〇〇食堂（見本）／見本の数値はすべて架空です。", F_NOTE)
    for col, title, w, _, _ in LIST_COLS:
        _cell(ws, f"{col}4", title, F_BOLD, FILL_HEAD, border=True, align=Alignment(wrap_text=True, vertical="center"))
        ws.column_dimensions[col].width = w
    ws.row_dimensions[4].height = 32
    m = f"'{MENU_SHEET}'!"
    for i in range(MENU_COUNT):
        r = LIST_FIRST + i
        c = menu_cells(i)
        name = f"{m}{c['name']}"
        _cell(ws, f"A{r}", i + 1, border=True)
        for col, _, _, fmt, key in LIST_COLS[1:]:
            ref = f"{m}{c[key]}"
            if key == "name":
                f = f'=IF({name}="","",{name})'
            else:
                f = f'=IF({name}="","",IF({ref}="","",{ref}))'
            _cell(ws, f"{col}{r}", f, fmt=fmt, border=True)
    ws.conditional_formatting.add(
        f"H{LIST_FIRST}:H{LIST_FIRST + MENU_COUNT - 1}",
        CellIsRule(operator="equal", formula=['"超過"'], fill=FILL_OVER))
    ws.freeze_panes = f"C{LIST_FIRST}"


# ---------------------------------------------------------------- 全体
def build_workbook(path, materials=None, menus=None, settings=None):
    materials = SAMPLE_MATERIALS if materials is None else materials
    menus = SAMPLE_MENUS if menus is None else menus
    settings = SAMPLE_SETTINGS if settings is None else settings
    wb = Workbook()
    ws_howto = wb.active
    ws_howto.title = HOWTO_SHEET
    _howto(ws_howto)
    _materials(wb.create_sheet(MAT_SHEET), materials)
    _menus(wb.create_sheet(MENU_SHEET), menus)
    _list(wb.create_sheet(LIST_SHEET))
    _settings(wb.create_sheet(SET_SHEET), settings)
    # Excel で開いたときに全数式を再計算させる（openpyxl は計算結果を保存しないため）
    wb.calculation = CalcProperties(fullCalcOnLoad=True)
    wb.security = None   # 空の workbookProtection 要素も書かない（保護は使わない）
    wb.properties.creator = "MenuBridge"
    wb.properties.title = "原価率計算シート"
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    wb.save(path)
    return path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else OUT
    print(build_workbook(out))
