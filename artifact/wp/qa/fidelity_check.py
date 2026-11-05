"""DOCX fidelity QA for the reconstructed First Device Models source.

Table fidelity: every table cell in the DOCX is compared, cell by
cell, against the reconstructed Markdown tables (formatting markers
and pipe escapes normalized away). Paragraph fidelity: every
non-empty DOCX paragraph's text must appear in the reconstructed
document's normalized text. Exit 0 only on a clean pass. Writes
wp/qa/fidelity.json.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"


def norm(s: str) -> str:
    s = s.replace("\\|", "|")
    s = re.sub(r"\*\*\*|\*\*|\*", "", s)
    s = s.replace("`", "")
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def md_tables(md: str) -> list[list[list[str]]]:
    tables, cur = [], []
    for line in md.split("\n"):
        if line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{3,}:?", c or "---") for c in cells):
                continue
            cur.append(cells)
        else:
            if cur:
                tables.append(cur)
                cur = []
    if cur:
        tables.append(cur)
    return tables


def main() -> None:
    md = (SRC / "whitepaper.md").read_text(encoding="utf-8")
    docx_tables = json.loads((SRC / "docx_tables.json").read_text(encoding="utf-8"))
    paras = json.loads((SRC / "docx_paras.json").read_text(encoding="utf-8"))

    mt = md_tables(md)
    table_result = {"docx_tables": len(docx_tables), "md_tables": len(mt),
                    "cells_compared": 0, "cell_mismatches": []}
    # Match tables by order; a DOCX table and an md table correspond 1:1
    # (the extractor emits them in body order).
    for ti, (dt, rt) in enumerate(zip(docx_tables, mt)):
        if len(dt) != len(rt):
            table_result["cell_mismatches"].append(
                {"table": ti, "issue": f"row count docx {len(dt)} vs md {len(rt)}"})
        for ri, (drow, rrow) in enumerate(zip(dt, rt)):
            for ci, (dc, rc) in enumerate(zip(drow, rrow)):
                table_result["cells_compared"] += 1
                if norm(dc) != norm(rc):
                    table_result["cell_mismatches"].append(
                        {"table": ti, "row": ri, "col": ci,
                         "docx": norm(dc)[:120], "md": norm(rc)[:120]})

    whole = norm(md)
    para_result = {"paras": 0, "missing": []}
    for p in paras:
        t = norm(p["text"])
        if not t:
            continue
        para_result["paras"] += 1
        if t not in whole:
            para_result["missing"].append({"style": p["style"], "text": t[:120]})

    ok = (len(docx_tables) == len(mt) and not table_result["cell_mismatches"]
          and not para_result["missing"])
    out = {"table_fidelity": table_result, "paragraph_fidelity": para_result,
           "verdict": "PASS" if ok else "FAIL"}
    (ROOT / "wp" / "qa" / "fidelity.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"fidelity: {out['verdict']} | tables {len(docx_tables)} vs {len(mt)} | cells {table_result['cells_compared']} compared, {len(table_result['cell_mismatches'])} mismatches | paras {para_result['paras']}, missing {len(para_result['missing'])}")
    for m in table_result["cell_mismatches"][:6]:
        print("CELL:", m)
    for m in para_result["missing"][:6]:
        print("PARA:", m)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
