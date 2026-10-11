#!/usr/bin/env python3
"""xlsx の互換性検査（Excel と Google スプレッドシートの両方で動かすための静的チェック）。

xlsx（zip）の XML を直接読み、次を確認する。
- セルの数式・入力規則・条件付き書式で使っている関数が、許可リストの中だけか
- 新しい関数（_xlfn. / _xlws. 付き）、外部参照（[1]Sheet!A1 など）、構造化参照（テーブル参照）が無いか
- マクロ（vbaProject.bin）、外部リンク、テーブル、外部データ接続が無いか
- 名前付き範囲が無いか（印刷タイトル・印刷範囲の組み込み名だけは許す）、シート保護（パスワード）が無いか
- 入力規則のリストはセル範囲の参照だけか（文字列を直接並べたリストは使わない）
- 条件付き書式は単純なセル値の条件（cellIs）だけか

使い方:  python3 company/product/P3/tests/compat_check.py [xlsx のパス]
結果は tests/compat-check.md に書く。問題があれば終了コード 1。
"""
from __future__ import annotations

import collections
import datetime
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT = os.path.join(os.path.dirname(HERE), "dist", "allergen-ichiran.xlsx")

# 依頼の許可リスト（SUM, COUNTIF, COUNTBLANK, IF, IFERROR, INDEX, MATCH, AND, OR, ISBLANK）
ALLOWED = {"SUM", "COUNTIF", "COUNTBLANK", "IF", "IFERROR", "INDEX", "MATCH", "AND", "OR", "ISBLANK"}
BUILTIN_NAMES = {"_xlnm.Print_Titles", "_xlnm.Print_Area"}
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
FUNC_RE = re.compile(r"(?<![A-Za-z0-9_.])([A-Za-z_][A-Za-z0-9_.]*)\s*\(")
STR_RE = re.compile(r'"(?:[^"]|"")*"')
QSHEET_RE = re.compile(r"'(?:[^']|'')*'!")


def strip(formula: str) -> str:
    """文字列リテラルとシート名（'...'!）を除いて、関数名だけを拾えるようにする"""
    return QSHEET_RE.sub("S!", STR_RE.sub('""', formula))


def main(path):
    problems = []
    notes = []
    funcs = collections.Counter()
    n_formulas = 0
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        bad_parts = [n for n in names if re.search(r"vbaProject|externalLink|/tables/|connections\.xml|"
                                                   r"activeX|ctrlProps|/queryTables/", n, re.I)]
        for n in bad_parts:
            problems.append(f"禁止されたパーツがある: {n}")
        ct = z.read("[Content_Types].xml").decode("utf-8")
        if "macroEnabled" in ct:
            problems.append("マクロ有効ブックの形式になっている")
        wbxml = ET.fromstring(z.read("xl/workbook.xml"))
        dn = wbxml.findall(".//m:definedNames/m:definedName", NS)
        user_dn = [d for d in dn if d.get("name") not in BUILTIN_NAMES]
        if user_dn:
            problems.append("名前付き範囲がある: " + ", ".join(d.get("name") for d in user_dn))
        for d in dn:
            if d.get("name") in BUILTIN_NAMES:
                notes.append(f"印刷設定の組み込み名 {d.get('name')} → {d.text}")
                if "[" in d.text or "#REF!" in d.text:
                    problems.append(f"印刷設定の組み込み名が不正: {d.text}")
        if wbxml.find(".//m:workbookProtection", NS) is not None:
            problems.append("ブックの保護が設定されている")
        sheets = {s.get("name"): s for s in wbxml.findall(".//m:sheets/m:sheet", NS)}
        sheet_parts = sorted(n for n in names if re.match(r"xl/worksheets/sheet\d+\.xml$", n))
        per_sheet = []
        dv_count = cf_count = 0

        def check_formula(text, where):
            nonlocal n_formulas
            n_formulas += 1
            if re.search(r"_xl(fn|ws|udf)\.", text):
                problems.append(f"{where}: 新しい関数（_xlfn 等）: {text[:80]}")
            s = strip(text)
            if "[" in s:
                problems.append(f"{where}: 外部参照または構造化参照の可能性（[ を含む）: {text[:80]}")
            if "#REF!" in s:
                problems.append(f"{where}: #REF! を含む: {text[:80]}")
            for fn in FUNC_RE.findall(s):
                funcs[fn.upper()] += 1
                if fn.upper() not in ALLOWED:
                    problems.append(f"{where}: 許可リスト外の関数 {fn}: {text[:80]}")

        for part in sheet_parts:
            root = ET.fromstring(z.read(part))
            cnt = 0
            for c in root.findall(".//m:sheetData/m:row/m:c", NS):
                f = c.find("m:f", NS)
                if f is not None and f.text:
                    cnt += 1
                    check_formula(f.text, f"{part}!{c.get('r')}")
                if c.get("t") == "array" or (f is not None and f.get("t") == "array"):
                    problems.append(f"{part}!{c.get('r')}: 配列数式")
            if root.find("m:sheetProtection", NS) is not None:
                problems.append(f"{part}: シート保護が設定されている")
            for dv in root.findall(".//m:dataValidations/m:dataValidation", NS):
                dv_count += 1
                f1 = dv.find("m:formula1", NS)
                txt = f1.text if f1 is not None else ""
                if dv.get("type") == "list":
                    if txt.startswith('"'):
                        problems.append(f"{part}: 入力規則のリストが文字列の直接指定: {txt}")
                    elif not re.fullmatch(r"('(?:[^']|'')*'|[^!]+)!\$?[A-Z]+\$?\d+:\$?[A-Z]+\$?\d+", txt):
                        problems.append(f"{part}: 入力規則のリストがセル範囲の参照ではない: {txt}")
                    else:
                        notes.append(f"{part} 入力規則（リスト） {dv.get('sqref')} → {txt}")
                else:
                    problems.append(f"{part}: リスト以外の入力規則: {dv.get('type')}")
                if txt:
                    check_formula(txt, f"{part} 入力規則")
            for cf in root.findall(".//m:conditionalFormatting", NS):
                for rule in cf.findall("m:cfRule", NS):
                    cf_count += 1
                    if rule.get("type") != "cellIs":
                        problems.append(f"{part}: 単純なセル値条件ではない条件付き書式: {rule.get('type')}")
                    for fx in rule.findall("m:formula", NS):
                        notes.append(f"{part} 条件付き書式 {cf.get('sqref')}: セルの値 {rule.get('operator')} {fx.text}")
            per_sheet.append((part, cnt))
        rels = z.read("xl/_rels/workbook.xml.rels").decode("utf-8")
        if "externalLink" in rels or 'TargetMode="External"' in rels:
            problems.append("ブックの関係に外部リンクがある")

    # シート名と part の対応（表示用）
    lines = [
        "# P3 アレルゲン一覧表 — 互換性の検査結果",
        "",
        f"- 対象: `{os.path.relpath(path, os.path.dirname(HERE))}`",
        f"- 実行日時: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "- 方法: xlsx（zip）内の XML を直接読み、全セルの数式・入力規則・条件付き書式を走査（`tests/compat_check.py`）",
        f"- 許可リスト: {', '.join(sorted(ALLOWED))}",
        "",
        f"## 判定: {'OK（問題なし）' if not problems else 'NG（' + str(len(problems)) + ' 件）'}",
        "",
        f"- 数式の数: {n_formulas}（入力規則の式を含む）",
        f"- 使っている関数: " + ", ".join(f"{k}（{v}）" for k, v in sorted(funcs.items())),
        f"- 入力規則: {dv_count} 件、条件付き書式のルール: {cf_count} 件",
        "",
        "| 確認項目 | 結果 |",
        "|---|---|",
    ]
    def has(word):
        return any(word in p for p in problems)
    items = [
        ("許可リスト外の関数が無い", not has("許可リスト外")),
        ("新しい関数（XLOOKUP, LET, LAMBDA, FILTER など。_xlfn 付き）が無い", not has("新しい関数")),
        ("配列数式・動的配列が無い", not has("配列数式")),
        ("外部参照・構造化参照（[ を含む式）が無い", not has("[ を含む") and not has("外部リンク")),
        ("マクロ・テーブル・外部データ接続のパーツが無い", not has("禁止されたパーツ") and not has("マクロ")),
        ("名前付き範囲が無い（印刷タイトル・印刷範囲の組み込み名を除く）", not has("名前付き範囲")),
        ("シート保護・ブック保護（パスワード）が無い", not has("保護")),
        ("入力規則のリストはセル範囲の参照だけ", not has("入力規則")),
        ("条件付き書式は単純なセル値の条件だけ", not has("条件付き書式")),
    ]
    for label, ok in items:
        lines.append(f"| {label} | {'OK' if ok else '**NG**'} |")
    if problems:
        lines += ["", "## 問題の一覧", ""] + [f"- {p}" for p in problems[:200]]
    lines += ["", "## 入力規則と条件付き書式の中身", ""] + [f"- {n}" for n in notes]
    lines += [
        "",
        "## この環境で行った検査と、行っていない検査",
        "",
        "- **行った**: 上の静的検査（全数式の関数名を許可リストと照合）と、LibreOffice での再計算テスト（`tests/result.md`）。",
        "- **行っていない**: Microsoft Excel と Google スプレッドシートでの実機確認。この環境にはどちらも無いため、"
        "実際に開いて同じ値になるかは未確認。手順は `device-check.md`（創業者が5分で確認）。",
        "- 補足: 許可リストの関数は、Excel 2010 以降・Google スプレッドシート・LibreOffice のいずれにもある基本関数。"
        "実際に使っているのは上の「使っている関数」だけ。",
        "- 補足: 「お客様用」シートの印刷タイトル（各ページに1〜5行目を印刷）と印刷範囲は、Excel の組み込み名（_xlnm.Print_Titles / _xlnm.Print_Area）として保存される。"
        "利用者が作る名前付き範囲ではないため許可した。Google スプレッドシートはこの設定を読まない可能性がある【推測・要実機確認】ため、印刷時に「固定行を繰り返す」をオンにする手順を `使い方` シートと `device-check.md` に書いた。",
        "- 補足: 品目名の見出しは縦書き（文字の向き＝縦。xlsx の textRotation=255）。LibreOffice の PDF では縦に並ぶことを確認した。Excel・Google スプレッドシートでの見え方は実機確認の項目。",
        "- 補足: 同梱ファイルは openpyxl で作るため、計算結果の値をファイルに保存していない（開いたときに再計算させる設定 fullCalcOnLoad を付けている）。"
        "Excel と Google スプレッドシートでは開くと計算されるが、スマホのファイルプレビューなど計算しないビューアでは数式のセルが空に見える。",
    ]
    with open(os.path.join(HERE, "compat-check.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("OK" if not problems else "NG")
    for p in problems[:50]:
        print(" ", p)
    print(f"formulas={n_formulas} funcs={dict(funcs)}")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT))
