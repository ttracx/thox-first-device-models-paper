# First Device Models, Trained In-House — Third Edition artifact bundle

Process v1.0 pack for the THOX first-device-models whitepaper,
finalized 2026-11-04. Byline finalized under Tommy Xaypanya's ruling
of 2026-11-04: the second edition's authorship stands as published
(Sadie Weaving, preparer; Tommy Xaypanya, accountable human author),
and the second edition's authorship disclosure is retained verbatim
in the paper's front matter. The DOI of record is issued by this
edition's Zenodo deposit and is recorded in `CITATION.cff`, the THOX
research-publishing pipeline manifest, and `HANDOFF.md`.

## Contents

- `dist/` — the shipped trio:
  - `THOX_First_Device_Models_Trained_In-House_Whitepaper_v3.0.pdf` — the paper (41 pp, Template v1.0).
  - `THOX_First_Device_Models_Trained_In-House_Whitepaper_v3.0.html` — single-file HTML edition.
  - `FirstDeviceModels_Demo_v3.0.html` — the GATE49 wave explorer (Wave A vs Wave B, verified recall primary), client-side on the evidence data.
- `src/` — the source of record and its reconstruction:
  - `fdm-v21.docx` / `fdm-v21.pdf` — the Second Edition (hardened paper-version 2.1, 2026-10-30) files as served in the Hugging Face whitepapers dataset (SHA-256 a3e24217…4672 / f10fe708…60b178). The DOCX is the only editable source that survives; no build tree existed.
  - `whitepaper.md` — the Markdown source reconstructed from the DOCX, verified cell-by-cell (27/27 tables, 754/754 cells, 400/400 paragraphs; `wp/qa/fidelity.json`).
  - `docx_tables.json`, `docx_paras.json` — the extraction record the fidelity QA runs against.
- `exp/` — the evidence bundle:
  - `exp/results/summary.json` — **the single evidence source** for every headline figure.
  - `exp/waves-ab-supplement/` — the paper's public supplement (GATE49 scorer + facts package, six serving Modelfiles, the constant-abstainer per-question record), staged from the dataset. Four text files (README, MANIFEST, VENDOR, the ThoxClip Modelfile) carried internal host names/paths and are genericized in the staged copies, as in the paper text; the public originals are untouched, so the supplement MANIFEST's hashes for those four files describe the public originals, not the staged copies (the pack's own MANIFEST.sha256.json hashes the staged copies).
  - `exp/records/` — staged copies of the internal run records the paper's register cites (S1 pilot record, S2 edge status record, S8 Wave A finishing record, S9 Wave B record), genericized the same way; originals retained internally.
  - `exp/pilot/` — the pilot's published result artifacts (S6).
- `wp/` — the build: `reconstruct.py` (DOCX → Markdown), `build.py`
  (Template v1.0 layout), `build_demo.py`, `consolidate_summary.py`,
  `pdf.cjs`, and `qa/` with the QA report, fidelity + numbers
  verification, blocker sweep, render metrics, screenshots, and the
  contact sheet. The identifier-scrub tooling and its raw logs are
  retained in the internal build tree only: they enumerate the
  internal identifiers they remove.

## Edition note

The Third Edition is a Process v1.0 reissue of the Second Edition
(hardened v2.1): content unchanged except the changes recorded in the
paper's Document control — Template v1.0 layout, host classes in place
of internal host names, the §10.1 register's filesystem paths replaced
with source names, and this edition's own record. The Research Loop
audit's Major (AB-1, failure-taxonomy completeness against source S2)
was re-verified line-by-line for this edition and holds; see
`wp/qa/QA-REPORT.md`. The Wave A/B per-question gate outputs were not
retained on the run hosts (§10.6); nothing in this pack reconstructs
them.

## Verification

- Reconstruction fidelity: PASS (`wp/qa/fidelity.json`).
- Numbers + AB-1 closure: **86/86 PASS** (`wp/qa/verify_numbers.py`,
  `wp/qa/numbers-verification.json`).
- Blocker sweep: PASS, byline item finalized
  (`wp/qa/sweep.json`, `wp/qa/QA-REPORT.md`).
