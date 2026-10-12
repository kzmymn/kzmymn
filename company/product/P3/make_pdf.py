#!/usr/bin/env python3
"""「お客様用」シートの印刷見本 PDF を LibreOffice で作る。

使い方:  python3 company/product/P3/make_pdf.py [ページ範囲（既定 1）]

1. dist/allergen-ichiran.xlsx を一時フォルダにコピーし、「お客様用」以外のシートを非表示にする
   （非表示のシートは印刷されない。数式の参照先としては残る）。
2. soffice --headless --convert-to pdf で PDF にする（見本は 3 品なので 1 ページ目だけ）。
3. dist/allergen-ichiran-print-sample.pdf に保存する。
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build  # noqa: E402

PDF = os.path.join(build.DIST, "allergen-ichiran-print-sample.pdf")


def make_pdf(xlsx=build.OUT, out=PDF, pages="1"):
    work = tempfile.mkdtemp(prefix="p3pdf_")
    try:
        src = os.path.join(work, "customer.xlsx")
        wb = openpyxl.load_workbook(xlsx)
        for ws in wb.worksheets:
            if ws.title != build.CUST_SHEET:
                ws.sheet_state = "hidden"
        wb.active = wb.sheetnames.index(build.CUST_SHEET)
        wb.save(src)
        opts = {"PageRange": {"type": "string", "value": pages}} if pages else {}
        filt = "pdf:calc_pdf_Export:" + json.dumps(opts) if opts else "pdf"
        subprocess.run(["soffice", "--headless", "--norestore", "--convert-to", filt, "--outdir", work, src],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
        shutil.copy(os.path.join(work, "customer.pdf"), out)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return out


if __name__ == "__main__":
    print(make_pdf(pages=sys.argv[1] if len(sys.argv) > 1 else "1"))
