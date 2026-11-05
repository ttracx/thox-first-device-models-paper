"""Reconstruct a Markdown build source from the First Device Models
Second Edition (v2.1) DOCX — the only editable source of record
(SHA-256 a3e24217...4672, verified against the pipeline manifest).

Walks the document body in order (paragraphs and tables interleaved),
maps Word styles to Markdown, preserves bold/italic/monospace runs,
extracts embedded images to ../assets/, and writes:
  ../src/whitepaper.md      the reconstructed source
  ../src/docx_tables.json   every DOCX table's cells, verbatim (fidelity QA input)
  ../src/docx_paras.json    every paragraph's style + text (fidelity QA input)
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import docx
from docx.document import Document as DocObj
from docx.table import Table
from docx.text.paragraph import Paragraph

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
ASSETS = ROOT / "assets"


def iter_block_items(parent: DocObj):
    for child in parent.element.body.iterchildren():
        if child.tag.endswith("}p"):
            yield Paragraph(child, parent)
        elif child.tag.endswith("}tbl"):
            yield Table(child, parent)


def run_md(run) -> str:
    t = run.text
    if not t:
        return ""
    font = run.font
    mono = font.name and ("mono" in font.name.lower() or "courier" in font.name.lower()
                          or "consol" in font.name.lower())
    if mono:
        return f"`{t}`" if "`" not in t else t
    if font.bold and font.italic:
        return f"***{t}***"
    if font.bold:
        return f"**{t}**"
    if font.italic:
        return f"*{t}*"
    return t


def para_md(p: Paragraph) -> str:
    return "".join(run_md(r) for r in p.runs) or p.text


def cell_text(cell) -> str:
    parts = []
    for p in cell.paragraphs:
        parts.append("".join(run_md(r) for r in p.runs) or p.text)
    return " <br> ".join(x for x in parts if x != "")


def main() -> None:
    d = docx.Document(str(SRC / "fdm-v21.docx"))
    # images
    img_map: dict[str, str] = {}
    ASSETS.mkdir(exist_ok=True)
    for rel in d.part.rels.values():
        if "image" in rel.reltype:
            blob = rel.target_part.blob
            ext = Path(rel.target_part.partname).suffix or ".png"
            name = f"img{len(img_map) + 1}{ext}"
            (ASSETS / name).write_bytes(blob)
            img_map[rel.rId] = name

    md: list[str] = []
    tables: list[list[list[str]]] = []
    paras: list[dict] = []
    for block in iter_block_items(d):
        if isinstance(block, Paragraph):
            style = (block.style.name or "Normal") if block.style else "Normal"
            text = para_md(block)
            paras.append({"style": style, "text": block.text})
            if not block.text.strip():
                continue
            # inline image?
            blips = block._p.findall(".//{http://schemas.openxmlformats.org/drawingml/2006/main}blip")
            img_lines = []
            for b in blips:
                rid = b.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed")
                if rid in img_map:
                    img_lines.append(f"![Figure](assets/{img_map[rid]})")
            if style.startswith("Title"):
                md.append(f"# {block.text.strip()}")
            elif style == "Heading 1":
                md.append(f"# {block.text.strip()}")
            elif style == "Heading 2":
                md.append(f"## {block.text.strip()}")
            elif style == "Heading 3":
                md.append(f"### {block.text.strip()}")
            elif style == "Heading 4":
                md.append(f"#### {block.text.strip()}")
            elif "List Bullet" in style:
                md.append(f"- {text.strip()}")
            elif "List Number" in style:
                md.append(f"1. {text.strip()}")
            elif style in ("Caption",):
                md.append(f"*{text.strip()}*")
            else:
                md.append(text.strip())
            md.extend(img_lines)
            md.append("")
        else:
            rows = [[cell_text(c) for c in row.cells] for row in block.rows]
            tables.append(rows)
            if not rows:
                continue
            ncol = max(len(r) for r in rows)
            def esc(s: str) -> str:
                return s.replace("|", "\\|")
            md.append("| " + " | ".join(esc(c) for c in rows[0]) + " |")
            md.append("|" + "---|" * ncol)
            for r in rows[1:]:
                r = r + [""] * (ncol - len(r))
                md.append("| " + " | ".join(esc(c) for c in r) + " |")
            md.append("")
    out = "\n".join(md)
    out = re.sub(r"\n{3,}", "\n\n", out)
    (SRC / "whitepaper.md").write_text(out, encoding="utf-8")
    (SRC / "docx_tables.json").write_text(json.dumps(tables, indent=1), encoding="utf-8")
    (SRC / "docx_paras.json").write_text(json.dumps(paras, indent=1), encoding="utf-8")
    print(f"whitepaper.md {len(out)} chars | tables {len(tables)} | paras {len(paras)} | images {sorted(img_map.values())}")


if __name__ == "__main__":
    main()
