#!/usr/bin/env python3
"""同梱物の一覧（MANIFEST.md）と配布用 zip を作る。全商品共通。

使い方:
    python3 company/ops/scripts/build_manifest.py <商品ID>      例: P2

入力:  company/product/<ID>/dist/ の全ファイル（dist の中身＝購入者が受け取るものすべて）
出力:  company/product/<ID>/MANIFEST.md   ファイル名・サイズ・SHA-256（先頭12桁）・形式
       company/product/<ID>/<ID>.zip      dist の中身だけ（フォルダ dist 自体は入れない）。ファイル名は UTF-8

隠しファイルや OS のゴミファイル（.DS_Store など）が dist にあると、購入者に届いてしまうので
エラーで止める（終了コード 1）。
"""
from __future__ import annotations

import datetime
import hashlib
import os
import sys
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PRODUCT_DIR = os.path.join(ROOT, "company", "product")

FORMATS = {
    ".xlsx": "Excel ブック（xlsx）", ".xlsm": "マクロ有効 Excel ブック（xlsm）", ".xls": "Excel 97-2003 ブック（xls）",
    ".ods": "OpenDocument スプレッドシート（ods）", ".csv": "CSV（テキスト）", ".tsv": "TSV（テキスト）",
    ".pdf": "PDF", ".html": "HTML", ".htm": "HTML", ".css": "CSS", ".js": "JavaScript",
    ".txt": "テキスト", ".md": "Markdown（テキスト）", ".json": "JSON",
    ".png": "PNG 画像", ".jpg": "JPEG 画像", ".jpeg": "JPEG 画像", ".svg": "SVG 画像", ".webp": "WebP 画像",
    ".docx": "Word 文書（docx）", ".pptx": "PowerPoint（pptx）", ".zip": "ZIP",
}
JUNK = {".DS_Store", "Thumbs.db", "desktop.ini"}


def fmt_of(name: str) -> str:
    ext = os.path.splitext(name)[1].lower()
    return FORMATS.get(ext, f"その他（{ext or '拡張子なし'}）")


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def list_dist(pid: str):
    """dist の全ファイルを (相対パス, 絶対パス) で返す（相対パスは / 区切り、名前順）"""
    dist = os.path.join(PRODUCT_DIR, pid, "dist")
    if not os.path.isdir(dist):
        raise SystemExit(f"エラー: {os.path.relpath(dist, ROOT)} がありません")
    out = []
    for d, dirs, files in os.walk(dist):
        dirs.sort()
        for fn in sorted(files):
            full = os.path.join(d, fn)
            rel = os.path.relpath(full, dist).replace(os.sep, "/")
            out.append((rel, full))
    return sorted(out)


def file_info(pid: str):
    rows = []
    for rel, full in list_dist(pid):
        rows.append(dict(name=rel, size=os.path.getsize(full), sha=sha256(full)[:12], fmt=fmt_of(rel), path=full))
    return rows


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    pid = argv[1]
    pdir = os.path.join(PRODUCT_DIR, pid)
    rows = file_info(pid)
    bad = [r["name"] for r in rows if os.path.basename(r["name"]) in JUNK
           or any(part.startswith(".") for part in r["name"].split("/"))]
    if bad:
        print("NG: dist に隠しファイル・不要ファイルがあります（購入者に届いてしまいます）。消してから再実行してください:")
        for b in bad:
            print("  -", b)
        return 1
    if not rows:
        print("NG: dist が空です")
        return 1

    zpath = os.path.join(pdir, f"{pid}.zip")
    with zipfile.ZipFile(zpath, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for r in rows:
            t = datetime.datetime.fromtimestamp(os.path.getmtime(r["path"])).timetuple()[:6]
            zi = zipfile.ZipInfo(r["name"], date_time=max(t, (1980, 1, 1, 0, 0, 0)))
            zi.flag_bits |= 0x800          # ファイル名は UTF-8（日本語名の文字化け防止）
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(r["path"], "rb") as f:
                z.writestr(zi, f.read())
    zsize, zsha = os.path.getsize(zpath), sha256(zpath)[:12]

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# MANIFEST — {pid}",
        "",
        f"`company/ops/scripts/build_manifest.py {pid}` が自動で作るファイル。手で直さない（dist を変えたら再実行する）。",
        "",
        f"- 生成日時: {now}",
        f"- 対象: `company/product/{pid}/dist/`（購入者が受け取るファイルすべて）",
        f"- ファイル数: {len(rows)}",
        f"- 配布用 zip: `{pid}.zip`（{zsize:,} バイト、SHA-256 先頭12桁 `{zsha}`）",
        "",
        "| ファイル名 | サイズ（バイト） | SHA-256（先頭12桁） | 形式 |",
        "|---|---:|---|---|",
    ]
    for r in rows:
        lines.append(f"| `{r['name']}` | {r['size']:,} | `{r['sha']}` | {r['fmt']} |")
    with open(os.path.join(pdir, "MANIFEST.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"OK: {os.path.relpath(os.path.join(pdir, 'MANIFEST.md'), ROOT)}（{len(rows)} ファイル）")
    print(f"OK: {os.path.relpath(zpath, ROOT)}（{zsize:,} バイト）")
    for r in rows:
        print(f"  {r['name']}  {r['size']:,}  {r['sha']}  {r['fmt']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
