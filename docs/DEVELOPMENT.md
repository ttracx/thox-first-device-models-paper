# Development — First Device Models whitepaper repository

## Repository conventions

- This repository is a **publication record**, not a working tree.
  The paper is never edited silently: a new edition is a new version
  in `paper/`, a new GitHub release, and a new version on Zenodo,
  following the THOX Research Paper Process v1.0.
- Canonical bytes: the files in `paper/` and `artifact/` are the
  exact bytes of the edition of record. Their SHA-256 hashes are in
  the root README and in `artifact/MANIFEST.sha256.json`. Any change
  to a shipped file is a new edition, never a fix-up commit.
- The byline follows the paper's front matter. Do not restyle the
  authorship or the front-matter authorship disclosure; both are
  part of the published record.

## Rebuilding the paper

The build tree is preserved in `artifact/wp/`:

- `wp/reconstruct.py` — reconstructs `src/whitepaper.md` from the
  second edition's DOCX (the only editable source of record).
- `wp/build.py` — lays the source into the THOX Research Paper
  Template v1.0 (cover, stat cards taken from
  `exp/results/summary.json`, body), appends the Third Edition
  document-control block, and writes `wp/paper.src.html` (== the
  shipped HTML edition), `wp/cover.html`, and `wp/body.html`.
- `wp/build_demo.py` — builds the GATE49 wave explorer demo.
- `wp/pdf.cjs` — renders the PDF (cover + body) with headless
  Chromium and merges with `pdfunite`. Do not reintroduce an
  `emulateMedia({colorScheme})` call: on this Chromium build it
  flips the print layout to screen metrics (see the QA report).
- `wp/consolidate_summary.py` — rebuilds `exp/results/summary.json`
  from the supplement and the staged run records.

## Verification before any new edition

- `wp/qa/fidelity_check.py` — DOCX reconstruction fidelity (Third
  Edition: 27/27 tables, 754/754 cells, 400/400 paragraphs).
- `wp/qa/verify_numbers.py` — re-derives every headline figure and
  re-checks the Research Loop audit item AB-1 line-by-line (Third
  Edition: 86/86 PASS).
- `wp/qa/sweep.py` (internal build tree only; the tool enumerates the
  identifiers it checks for) — the Process §4 blocker sweep (Third
  Edition: PASS; tier 1 0, tier 2 0, tier 3 68 adjudicated).
- Render QA at desktop and 390 px widths before calling an edition
  done; metrics are recorded in `wp/qa/`.

## Releases

Each edition gets a formal GitHub release whose assets are the
paper PDF, the HTML edition, the demo, and the artifact ZIP,
byte-identical to the pack of record.
