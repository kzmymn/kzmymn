#!/usr/bin/env python3
"""販売ページ（listing.md）と同梱物（MANIFEST / dist / zip）が一致するかを検査する。全商品共通。

使い方:
    python3 company/ops/scripts/check_listing.py <商品ID>      例: P2

検査すること:
1. MANIFEST.md が今の dist と一致している（古くない）。zip の中身も dist と同じ。
2. listing.md の「## 同梱物」セクションの箇条書きのファイル名が、MANIFEST と過不足なく一致する。
   箇条書きの書式:  - `genka-keisan.xlsx` — 説明
3. listing.md の本文に、dist に無い形式が書かれていない。
   - 拡張子の記述（.pdf, .csv, .xlsx など）→ その拡張子のファイルが dist にあること
   - 形式・ソフト名（PDF, CSV, Excel, Google スプレッドシート, Word, PowerPoint, HTML, PNG, JPEG）
     → 対応する拡張子のファイルが dist にあること
   「PDF は付いていません」のような否定の文は、行末に <!-- check_listing: ignore --> を付けると検査から外せる。

終了コード: 0 = OK、1 = NG（不一致あり）、2 = ファイルが無いなど実行できない
"""
from __future__ import annotations

import os
import re
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_manifest import PRODUCT_DIR, ROOT, file_info  # noqa: E402

CONTENT_DIR = os.path.join(ROOT, "company", "content")
IGNORE = "check_listing: ignore"

KNOWN_EXT = ["xlsx", "xlsm", "xls", "ods", "csv", "tsv", "pdf", "html", "htm", "txt", "md", "json",
             "png", "jpg", "jpeg", "svg", "webp", "docx", "doc", "pptx", "zip"]
EXT_RE = re.compile(r"\.(" + "|".join(KNOWN_EXT) + r")(?![A-Za-z0-9])", re.I)
# 形式・ソフト名 → それを名乗るなら dist に必要な拡張子（どれか1つ）
KEYWORDS = [
    (re.compile(r"PDF"), {"pdf"}, "PDF"),
    (re.compile(r"CSV"), {"csv"}, "CSV"),
    (re.compile(r"Excel|エクセル"), {"xlsx", "xlsm", "xls"}, "Excel"),
    (re.compile(r"Google\s*スプレッドシート|Googleスプレッドシート|Google Sheets|スプシ"),
     {"xlsx", "xls", "ods", "csv"}, "Google スプレッドシート"),
    (re.compile(r"(?<![A-Za-z])Word(?![A-Za-z])|ワード文書"), {"docx", "doc"}, "Word"),
    (re.compile(r"PowerPoint|パワーポイント"), {"pptx"}, "PowerPoint"),
    (re.compile(r"(?<![A-Za-z])HTML(?![A-Za-z])"), {"html", "htm"}, "HTML"),
    (re.compile(r"(?<![A-Za-z])PNG(?![A-Za-z])"), {"png"}, "PNG"),
    (re.compile(r"JPE?G"), {"jpg", "jpeg"}, "JPEG"),
]


def parse_manifest(path):
    names = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^\|\s*`([^`]+)`\s*\|", line)
            if m:
                names.append(m.group(1))
    return names


def parse_bundle_section(text):
    """「## 同梱物」セクションの箇条書きから (行番号, ファイル名 or None, 行) を返す"""
    lines = text.splitlines()
    out, inside, found = [], False, False
    for i, line in enumerate(lines, start=1):
        if re.match(r"^##\s", line):
            inside = bool(re.match(r"^##\s*同梱物", line))
            found = found or inside
            continue
        if inside and re.match(r"^\s*[-*]\s+", line):
            m = re.search(r"`([^`]+)`", line)
            out.append((i, m.group(1).strip() if m else None, line.strip()))
    return found, out


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    pid = argv[1]
    pdir = os.path.join(PRODUCT_DIR, pid)
    manifest = os.path.join(pdir, "MANIFEST.md")
    listing = os.path.join(CONTENT_DIR, pid, "listing.md")
    for p in (manifest, listing):
        if not os.path.isfile(p):
            print(f"実行できません: {os.path.relpath(p, ROOT)} がありません"
                  + ("（先に build_manifest.py を実行）" if p == manifest else ""))
            return 2

    ng = []
    # 1. MANIFEST と dist・zip の一致
    mnames = parse_manifest(manifest)
    current = file_info(pid)
    cur_names = [r["name"] for r in current]
    with open(manifest, encoding="utf-8") as f:
        mtext = f.read()
    stale = sorted(set(mnames) ^ set(cur_names))
    stale += [r["name"] for r in current if r["name"] in mnames and f"`{r['sha']}`" not in mtext]
    if stale:
        ng.append("MANIFEST.md が今の dist と一致しません（build_manifest.py を再実行）: " + ", ".join(sorted(set(stale))))
    zpath = os.path.join(pdir, f"{pid}.zip")
    if not os.path.isfile(zpath):
        ng.append(f"{pid}.zip がありません（build_manifest.py を実行）")
    else:
        with zipfile.ZipFile(zpath) as z:
            znames = sorted(n for n in z.namelist() if not n.endswith("/"))
        if znames != sorted(cur_names):
            ng.append(f"{pid}.zip の中身が dist と違います: zip={znames} dist={sorted(cur_names)}")

    # 2. 同梱物セクション
    with open(listing, encoding="utf-8") as f:
        text = f.read()
    found, items = parse_bundle_section(text)
    if not found:
        ng.append("listing.md に「## 同梱物」セクションがありません")
    listed = []
    for ln, name, raw in items:
        if name is None:
            ng.append(f"listing.md {ln}行目: 同梱物の行にファイル名（`...`）がありません: {raw}")
        else:
            listed.append(name)
    dup = sorted({n for n in listed if listed.count(n) > 1})
    if dup:
        ng.append("同梱物に同じファイルが2回書かれています: " + ", ".join(dup))
    missing_in_listing = sorted(set(mnames) - set(listed))
    not_in_dist = sorted(set(listed) - set(mnames))
    if missing_in_listing:
        ng.append("販売ページに書かれていない同梱ファイル: " + ", ".join(missing_in_listing))
    if not_in_dist:
        ng.append("販売ページにあるが同梱されていないファイル: " + ", ".join(not_in_dist))

    # 3. 形式・拡張子の記述
    exts = {os.path.splitext(n)[1].lower().lstrip(".") for n in mnames}
    for ln, line in enumerate(text.splitlines(), start=1):
        if IGNORE in line:
            continue
        for m in EXT_RE.finditer(line):
            e = m.group(1).lower()
            if e not in exts and not (e in ("jpg", "jpeg") and exts & {"jpg", "jpeg"}) \
                    and not (e in ("htm", "html") and exts & {"htm", "html"}):
                ng.append(f"listing.md {ln}行目: 「.{m.group(1)}」とあるが、dist に .{e} のファイルがありません: {line.strip()}")
        for rx, need, label in KEYWORDS:
            if rx.search(line) and not (need & exts):
                ng.append(f"listing.md {ln}行目: 「{label}」とあるが、dist に対応する形式"
                          f"（{', '.join('.' + x for x in sorted(need))}）がありません: {line.strip()}")

    print(f"商品 {pid}: dist {len(cur_names)} ファイル / MANIFEST {len(mnames)} / 販売ページの同梱物 {len(listed)}")
    if ng:
        print("NG")
        for n in ng:
            print("  -", n)
        return 1
    print("OK: 販売ページの同梱物と形式の記述は、同梱ファイルと一致しています")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
