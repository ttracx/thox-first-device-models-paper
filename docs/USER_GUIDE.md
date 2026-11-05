# User Guide — First Device Models, Trained In-House (paper repository)

## What this repository is

This is the publication record for the THOX.ai Research whitepaper
**"First Device Models, Trained In-House", Third Edition (v3.0)
(public edition)**, DOI
[10.5281/zenodo.23969824](https://doi.org/10.5281/zenodo.23969824).
Prepared by Sadie Weaving (THOX.ai); accountable human author: Tommy
Xaypanya (THOX.ai, corresponding author). It holds the paper, its
interactive GATE49 wave explorer demo, and the evidence files every
printed number traces to. It does not hold the models; the Waves A/B
models live in their own model repositories.

The Third Edition is a Process v1.0 reissue of the Second Edition
(hardened paper-version 2.1, 2026-10-30): Template v1.0 layout, the
source reconstructed from the second edition's DOCX with
table-level fidelity verification, evidence consolidated into one
source, and internal host identifiers genericized. The changes are
recorded in the paper's Document control. No measured result was
altered.

## Who it is for

- Readers evaluating THOX's first in-house training program.
- Reviewers who want to check a claim in the paper against its
  evidence file.
- THOX engineers tracing a gate verdict or a taxonomy item to its
  record.

## Reading the paper

Open `paper/THOX_First_Device_Models_Trained_In-House_Whitepaper_v3.0.pdf`,
or the identical-content single-file HTML edition
`paper/THOX_First_Device_Models_Trained_In-House_Whitepaper_v3.0.html`.
The paper reports the training rails, the voice-command pilot, and
the two edge waves; §8.3 explains why verified recall (of 12) is the
primary figure beside each 49-question total, and §10 is the
provenance register.

## Checking a number

Every headline figure traces to `artifact/exp/results/summary.json`,
the pack's single evidence source. The QA record of the independent
re-verification (86/86 PASS for this edition) and of the source
reconstruction fidelity (27/27 tables, 754/754 cells, 400/400
paragraphs) is in `artifact/wp/qa/`.

## Running the demo

Open `paper/FirstDeviceModels_Demo_v3.0.html` in any browser. It is
the GATE49 wave explorer (Wave A vs Wave B, verified recall
primary), rendered entirely client-side from the evidence data
embedded in it; no network is needed.

## Citing the paper

Use `CITATION.cff` or `paper.bib` at the repository root. The DOI of
record is 10.5281/zenodo.23969824.
