"""Build the First Device Models THIRD EDITION paper in Template v1.0.

Source of content: src/whitepaper.md, reconstructed from the Second
Edition (hardened v2.1) DOCX — the only editable source of record —
with cell-level fidelity QA (wp/qa/fidelity_check.py: 27/27 tables,
754/754 cells, 400/400 paragraphs). This build re-lays that text into
Template v1.0, applies the Process section 4 security-sweep
genericizations (scrub.PAPER_SUBS, asserted: host classes; section
10.1 register paths replaced with source names), appends the Third
Edition document-control block, embeds the template's Inter +
JetBrains Mono @font-face block, and takes every stat-card number
from exp/results/summary.json. The paper has no abstract section; the
cover's status panel carries the paper's own second-edition status
statement verbatim.

Outputs: wp/paper.src.html (== shipped HTML), wp/cover.html,
wp/body.html (PDF renders; furniture added by pdf.cjs).
Byline finalized 2026-11-04 under Tommy Xaypanya's ruling (keep the
second edition's authorship as published); see wp/qa/QA-REPORT.md.
"""
from __future__ import annotations

import base64
import html as htmllib
import json
import re
import sys
from pathlib import Path

import markdown

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scrub import PAPER_SUBS, apply_subs  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SRC_MD = ROOT / "src" / "whitepaper.md"
ASSETS = ROOT / "assets"
TEMPLATE_DIR = Path.home() / "workspace/standards/THOX_Research_Paper_Template_v1.0"
S = json.loads((ROOT / "exp" / "results" / "summary.json").read_text(encoding="utf-8"))

VERSION = "v3.0"
DATE = "2026-11-04"
TITLE = "First Device Models, Trained In-House"
DEK = ("How THOX Built the Training Rails, Proved Them with a Voice Command "
       "Adapter, and Published ThoxFlux-350M on Kickstarter Launch Day")


def template_css() -> str:
    build_src = (TEMPLATE_DIR / "build.py").read_text(encoding="utf-8")
    css = build_src.split('CSS = """', 1)[1].split('"""', 1)[0]
    example = (TEMPLATE_DIR / "example" / "THOX_MeshStack_Research_Paper_v1.0.1.html").read_text(encoding="utf-8")
    faces = re.findall(r"@font-face\{[^}]*\}", example)
    assert len(faces) >= 20, f"expected the template font block, got {len(faces)} faces"
    css = css.replace("/*__FONTS__*/", "\n".join(faces))
    css = css.replace("/*__KATEX__*/", "")
    css += """
/* --- reissue addenda (First Device Models v3.0): blockquote, figures, author hold --- */
blockquote{border-left:3px solid var(--green);background:var(--pale);padding:8px 12px;margin:10px 0 12px;font-size:9.5pt;break-inside:avoid}
blockquote p{margin:0}
.figwrap img{width:100%;height:auto}
.authorhold{border:1.5px dashed var(--green);border-radius:6px;padding:10px 12px;margin:0 0 14px;font-size:8.6pt;color:#F3F4F6}
.authorhold .ah-t{font-family:'JetBrains Mono',monospace;font-size:8pt;letter-spacing:.08em;text-transform:uppercase;color:var(--green);margin-bottom:4px}
.authorhold p{margin:0 0 4px;font-size:8.6pt;line-height:1.45;color:#F3F4F6}
@media screen{pre{overflow-x:auto}}
@media screen and (min-width:821px){table{display:block;overflow-x:auto}}
@media screen and (max-width:760px){code{overflow-wrap:anywhere;word-break:break-word}p,li,td{overflow-wrap:break-word}a{overflow-wrap:anywhere}}
"""
    return css


def md2html(text: str) -> str:
    return markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])


def figures_to_datauri(fragment: str) -> str:
    def repl(m: re.Match) -> str:
        alt, src = m.group(1), m.group(2)
        path = ROOT / src
        b64 = base64.b64encode(path.read_bytes()).decode()
        num = re.match(r"Figure (\d+)", alt)
        label = f"Figure {num.group(1)}." if num else "Figure."
        caption = re.sub(r"^Figure \d+\s*—\s*", "", alt)
        return (f'<figure><div class="figwrap"><img alt="{htmllib.escape(alt)}" '
                f'src="data:image/png;base64,{b64}"></div>'
                f'<figcaption><b>{label}</b> {htmllib.escape(caption)}</figcaption></figure>')
    return re.sub(r'<p><img alt="([^"]*)" src="(assets/[^"]*)" /></p>', repl, fragment)


def split_chunks(md_text: str) -> list[tuple[str, str]]:
    parts = re.split(r"(?m)^(#[ ]+.*)$", md_text)
    chunks: list[tuple[str, str]] = []
    pre = parts[0]
    for i in range(1, len(parts), 2):
        chunks.append((parts[i].strip(), parts[i + 1]))
    return chunks


def main() -> None:
    raw = SRC_MD.read_text(encoding="utf-8")
    text, sub_log = apply_subs(raw, PAPER_SUBS)
    zero = [e for e in PAPER_SUBS if e[0] not in [x["pattern"] for x in sub_log]]
    if zero:
        raise SystemExit(f"security-sweep substitutions that did not fire: {zero}")
    (ROOT / "wp" / "qa").mkdir(parents=True, exist_ok=True)
    (ROOT / "wp" / "qa" / "paper-scrub-log.json").write_text(json.dumps(sub_log, indent=1), encoding="utf-8")

    # The source's provenance register splits its table with blank lines
    # between row groups; python-markdown ends a table at a blank line and
    # would print the later rows as raw pipe text. Rejoin row groups.
    _lines = text.split("\n")
    _joined: list[str] = []
    for _i, _ln in enumerate(_lines):
        if _ln.strip() == "" and _joined and _joined[-1].lstrip().startswith("|") \
                and _i + 1 < len(_lines) and _lines[_i + 1].lstrip().startswith("|") \
                and "---" not in _lines[_i + 1]:
            continue
        _joined.append(_ln)
    text = "\n".join(_joined)

    chunks = dict()
    order = []
    for head, body in split_chunks(text):
        chunks[head] = body
        order.append(head)

    def get(prefix: str) -> tuple[str, str]:
        for h in order:
            if h.startswith(prefix):
                return h, chunks[h]
        raise KeyError(prefix)

    # --- front matter (chunk 0 body: subtitle, then the front-matter block) ---
    front = chunks[order[0]]
    status_m = re.search(r"(Status as of October 30, 2026 \(second edition\):.*?)(?=\n# |\Z)", front, re.S)
    assert status_m, "second-edition status paragraph not found in front matter"
    status_html = md2html(status_m.group(1).strip())
    fm_lines = []
    for line in front.splitlines():
        if line.startswith("## "):
            continue
        if line.strip() in ("Technical Whitepaper", "THOX.ai", "Your AI. Your Data. Your Rules.™"):
            continue
        fm_lines.append(line)
    front_md = "\n".join(fm_lines)
    front_md = front_md.replace(status_m.group(1), "").strip()
    front_html = figures_to_datauri(md2html(front_md))

    # --- contents list generated from the section heads ---
    contents_items = [h[2:].strip() for h in order if h not in (order[0], "# Contents")]

    # --- Third Edition document-control block (appended to that chunk) ---
    docctl_head, docctl_body = get("# Document control")
    docctl_body += """

Version: 3.0 (third edition)

Date: November 4, 2026

Author: Sadie Weaving, Chief Agentic Officer, THOX.ai

What changed in the third edition: Process v1.0 reissue of the second edition (hardened paper-version 2.1). Layout moved to the THOX Research Paper Template v1.0; the source was reconstructed from the second edition's DOCX with table-level fidelity verification; the evidence was consolidated into a single summary (exp/results/summary.json in the artifact bundle) with the public waves-ab-supplement and staged run records; a companion GATE49 wave explorer demo was added. Public-edition security sweep: internal host names are replaced with host classes, and the section 10.1 register's filesystem paths are replaced with the register's source names. The Research Loop audit item AB-1 closure (the failure taxonomy) was re-verified line-by-line against source S2 for this edition and holds: sections 1, 6.2, and 6.5 count eleven distinct failure classes, the seventh being the tokenizer chat template contract from S2. No measured result was altered and no other text changed. Byline finalized under Tommy Xaypanya's ruling of November 4, 2026: the second edition's authorship stands as published (prepared by Sadie Weaving, Chief Agentic Officer; accountable human author Tommy Xaypanya, CTO & Co-Founder), and the second edition's authorship disclosure is retained verbatim in the front matter.
"""
    chunks[docctl_head] = docctl_body

    # --- body sections ---
    body_parts: list[str] = []
    body_parts.append('<div class="callout"><div class="ct">Process v1.0 reissue — Third Edition</div><div>'
                      'This is the Process v1.0 pack reissue (Third Edition, v3.0, 2026-11-04) of the '
                      'Second Edition (hardened paper-version 2.1, October 30, 2026). Content is '
                      'unchanged from the second edition except the changes recorded in the Document '
                      'control section: the Process section 4 security sweep (host classes; section 10.1 '
                      'source names) and this edition\'s own record. Every number traces to the pack\'s '
                      'single evidence source, exp/results/summary.json.</div></div>')
    body_parts.append(front_html)
    for head in order:
        if head in (order[0], "# Contents"):
            continue
        frag = figures_to_datauri(md2html(chunks[head].strip()))
        # Wide tables: the template CSS itself renders table as a block-level
        # horizontal scroller; no wrapper (a wrapper broke that behaviour).
        # '## x.y Title' renders as <h2>; demote to template h3 with number span.
        frag = re.sub(r"<h2>(\d+\.\d+)\s+([^<]*)</h2>", r'<h3><span class="num">\1</span> \2</h3>', frag)
        m = re.match(r"# (\d+)\.\s+(.*)", head)
        ma = re.match(r"# Appendix ([A-Z])\.\s+(.*)", head)
        if m:
            frag = (f'<h2 id="s{m.group(1)}"><span class="num">{m.group(1)}</span>'
                    f'{htmllib.escape(m.group(2))}</h2>\n' + frag)
        elif ma:
            frag = (f'<h2 id="app{ma.group(1)}"><span class="num">{ma.group(1)}</span>'
                    f'Appendix {ma.group(1)}. {htmllib.escape(ma.group(2))}</h2>\n' + frag)
        elif head == "# Document control":
            frag = '<h2 id="docctl"><span class="num">§</span>Document control</h2>\n' + frag
        body_parts.append(frag)
    body_html = "\n".join(body_parts)

    # --- stat cards from summary.json ---
    wb = S["wave_b"]["models"]["ThoxEdge-0.5B"]
    wa = S["wave_a"]["models"]["ThoxEdge-0.5B"]
    abst = S["constant_abstainer"]
    pilot = S["pilot_lfm3_voice"]["final_launch"]
    kpis = [
        (f'{wb["passed"]}/49 · verified {wb["splits"]["verified"][0]}/12',
         f'ThoxEdge-0.5B, Wave B gate (mean {wb["mean"]}/5) — Wave A was {wa["passed"]}/49; every verdict in both waves is FAIL under the zero-hard-failure policy', "Measured · GATE49"),
        (f'{abst["passed"]}/49',
         "Constant-abstainer floor — the prescribed decline responder through the same scorer; Wave totals are read against it", "Measured · GATE49 scorer"),
        ("982 rows",
         "Wave B corpus (838 newly authored + 144 retained after hygiene), replacing the 205-row Wave A corpus", "Calculated · construction record"),
        (f'{pilot["full_exact_matches"]} exact',
         f'Voice pilot held-out result: {pilot["function_names_correct"]} function names, {pilot["full_exact_matches"]} full exact matches of 14 — weak as performance, strong as pipeline evidence', "Measured · pilot artifact"),
    ]
    kpi_html = ('<div class="kpis">' + "".join(
        f'<div class="kpi"><div class="kv">{v}</div><div class="kl">{l}</div><div class="kt">{t}</div></div>'
        for v, l, t in kpis) + "</div>")

    contents_html = ('<div class="contents"><div class="ct">Contents</div><ol>' +
                     "".join(f"<li>{htmllib.escape(i)}</li>" for i in contents_items) + "</ol></div>")

    byline = """<p class="byline">THOX.ai Research · Prepared by: Sadie Weaving, Chief Agentic Officer, THOX.ai · Accountable human author: Tommy Xaypanya, CTO &amp; Co-Founder, THOX.ai (corresponding author) · ORCID 0009-0000-4425-9565</p>"""

    cover = f"""<section class="cover"><div class="cover-inner">
<div class="eyebrow"><span>THOX.AI RESEARCH · WHITEPAPER {VERSION.upper()} · THIRD EDITION · {DATE}</span><span class="pill">Public edition</span></div>
<h1>{htmllib.escape(TITLE)}</h1>
<p class="deck">{htmllib.escape(DEK)}</p>
{byline}
<div class="abstract"><div class="ct">Status of record (second edition)</div>{status_html}</div>
{kpi_html}
{contents_html}
<div class="cover-foot">Your AI. Your Data. Your Rules.™ · THOX.ai LLC · Process v1.0 reissue (Third Edition) of the Second Edition, hardened paper-version 2.1 (October 30, 2026). DOI: pending deposit — none issued. Evidence: exp/results/summary.json in the artifact bundle.</div>
</div></section>"""

    css = template_css()
    head = (f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            f'<title>{htmllib.escape(TITLE)} — THOX First Device Models Whitepaper {VERSION} (Third Edition)</title>\n'
            f'<meta name="description" content="THOX.ai Research whitepaper {VERSION}">\n'
            f'<style>{css}</style></head>\n')
    full = head + f'<body data-version="{VERSION}">\n{cover}\n<section class="paper-body">\n{body_html}\n</section>\n</body></html>'
    cover_doc = head + f'<body data-version="{VERSION}">\n{cover}\n</body></html>'
    body_doc = head + f'<body data-version="{VERSION}">\n<section class="paper-body">\n{body_html}\n</section>\n</body></html>'

    wp = ROOT / "wp"
    (wp / "paper.src.html").write_text(full, encoding="utf-8")
    (wp / "cover.html").write_text(cover_doc, encoding="utf-8")
    (wp / "body.html").write_text(body_doc, encoding="utf-8")
    print("wrote wp/paper.src.html", len(full), "bytes; substitutions:", sum(e["count"] for e in sub_log))


if __name__ == "__main__":
    main()
