# QA report — First Device Models, Third Edition (staged pack)

Build date: 2026-11-04. Status: **STAGED ONLY** — no deposit, no
surface edits, no founder email, no social.

## Source reconstruction — fidelity PASS

No build tree survived for this paper; the Second Edition DOCX
(SHA-256 a3e24217…4672, byte-identical to the dataset copy) is the
only editable source. `reconstruct.py` rebuilt the Markdown source
from it; `fidelity_check.py` then compared the reconstruction against
the DOCX itself: **27/27 tables, 754/754 table cells identical,
400/400 paragraphs present** (`fidelity.json`). The legacy cover
lockup image extracted from the DOCX is not carried into the Template
v1.0 layout (the template cover is typographic); it remains in the
build record under `assets/`.

## Audit Major AB-1 — closure re-verified line-by-line: CLOSED

The 2026-10-30 Research Loop audit's single Major: the paper's "six
distinct failure classes" completeness claim was contradicted by a
seventh distinct failure in its own source S2 (the SmolLM
chat-template failure). The audit required five additions. Each was
re-verified against the v2.1 text for this edition (checker:
`verify_numbers.py` §5, all passing) — not assumed from the
disposition record:

| Audit requirement | Where it holds in the text | Verdict |
|---|---|---|
| Seventh class in §1's enumeration | §1 counts **eleven** distinct failure classes; the seventh named is "a tokenizer chat template contract" | CLOSED |
| Seventh class in §6.2's table | Class 7 row: both SmolLM follower jobs (6ae14e1f…, 6ae14e20…), the TRL ValueError, 0/205 rows tokenized, the ChatML fallback fix and its lesson; the table has exactly **11 rows** | CLOSED |
| §6.5 category analysis counts it | "The eleven failures fall into four structural categories"; the Data contracts analysis discusses the seventh failure and failure 9 explicitly | CLOSED |
| Relaunch jobs in §10.3 | Follower relaunch rows: 6ae15d7a41e90535df76ddfa (Nano-360M, completed, 211 s) and 6ae15d7a41e90535df76ddfc (Nano-135M, completed, 192 s) | CLOSED |
| Fix commit in §10.5 | "Edge ChatML chat template fallback…" — Thox-ai/thox-edge-sft commit c250f9bb1b8e20b71f5c38c73ccfbcdac6a0303e | CLOSED |

The paper's Document control also narrates the fix and its source.
One reading note: a Document-control sentence says the audit fix took
§§1/6.5 to "seven failure classes" — that sentence describes the
audit-fix step for the original two programs, in the same revision
that then extended the taxonomy to eleven with the Wave B/finishing
classes (8–11); the operative counts in §1 and §6.5 both read eleven
and agree. No residual inconsistency; no text change was needed or
made for AB-1 in this edition.

Spot checks of the other adjudicated items: AB-2 (§12 wording) —
§12 reads "On publication, this edition joins the Wave C paper in the
Hugging Face dataset…", publication-state as the disposition records:
HOLDS. AB-3 (§3.5 prices) — the $2.50/$1.00/$0.40 flavor rates are
framed in the paper as observed rates and are classed REPORTED in
summary.json, never MEASURED: HOLDS.

## Numbers verification — PASS 86/86

Independent checker (`verify_numbers.py`): the constant abstainer
re-derived from the supplement's per-question report (25/49, mean
3.531, 0 hard, splits); the pilot re-checked against the published
S6 artifact (35 train rows, 14 held out, name accuracy 1/14, exact
0.0); every Wave A figure matched against the S8 finishing record's
own table (totals, means, hard counts); every Wave B figure matched
against the S9 record (totals, means, splits, losses; Clip 22/49,
2.776, 14 hard); the invalid Edge-0.8B Wave B state confirmed in S9;
then every headline figure checked as printed in the shipped PDF and
HTML (all gate totals/means, splits, the five Wave A GGUF SHA-256s
and byte counts, corpus 205/838/144/982, flavor prices, pilot
0.7614 / 1/14 / 0/14, the AB-1 job ids and fix commit). **86/86
PASS** (`numbers-verification.json`).

Evidence gaps honored, not filled: Wave A/B per-question gate
outputs were not retained (§10.6) — summary.json carries totals,
splits, and means only; Wave A per-category splits were not retained
either and are recorded as null; Wave B hard-failure counts are
recorded only where S9 states them (Edge-0.5B: 1; Clip: 14).

## Blocker sweep — PASS, one item HELD by design

`sweep.json`, three tiers:

- **Tier 1 — internal identifiers (37 pack text files): 0 hits.**
  The paper text substitutions (34, asserted at build) genericize
  the two host names to host classes (including both Appendix C
  glossary headwords, where the hosting provider's name also
  appeared) and replace the §10.1 register's literal paths with
  source names. The staged evidence copies (S1/S2/S8/S9 records and
  four supplement text files) were genericized the same way; the
  already-public dataset originals are untouched — for those four
  supplement files the supplement MANIFEST's hashes describe the
  public originals, and the pack's own manifest hashes the staged
  copies. The scrub tooling itself enumerates the identifiers and is
  excluded from the public bundle.
- **Tier 2 — shipped paper HTML: 0 hits.**
- **Tier 3 — evidence content: 68 matches, all adjudicated:** 66 are
  regex quantifier braces in the supplement's gate source code; 2
  are the facts package's CONFIDENTIAL field values (gate data
  semantics, already public). None is a document placeholder or mark.
- **Byline: HELD.** The cover carries a marked placeholder drawn
  from the manifest's authorship record (Prepared by: Sadie Weaving,
  CAO; accountable human author: Tommy Xaypanya, CTO & Co-Founder;
  Craig Ross is not an author), and the second edition's authorship
  disclosure is retained verbatim in the front matter below it,
  pending Tommy's ruling. Not passed, not waived — held.

## Render QA — PASS

Playwright renders at 1280 px and a true 390 px (`render-metrics.json`,
screenshots + `contact-sheet.jpg`): no horizontal document scroll at
either width for paper or demo. One defect found and fixed: the
Appendix A per-run configuration table (942 px) overflowed the
desktop column — the template's block-scroller table rule applies
only at narrow widths by design, so the build's addendum extends the
same rule to wide screens (`@media screen and (min-width:821px)`);
print layout is unaffected. Demo interaction smoke test: the
abstainer's per-question grid renders all 49 cells and a click
returns the question's record; model cards lead with verified recall
and mark the Edge-0.8B Wave B state as an invalid measurement, not a
score. PDF: 41 pages, Letter; dark template cover by design, light
body with running header and tagline footer.

## Provenance of this build

- Source: the dataset's Second Edition DOCX/PDF, hash-verified
  against the pipeline manifest before reconstruction.
- Evidence: the public waves-ab-supplement (dataset), the pilot's
  published result artifacts, and the S8/S9 run records, staged as
  scrubbed copies in `exp/`.
- Nothing was deposited, pushed, or posted. Live surfaces are
  byte-unchanged by this build.

## Finalization addendum — 2026-11-04 (publication lane)

- **Byline: FINALIZED** under Tommy Xaypanya's ruling of 2026-11-04
  (keep the original authorship as published). The cover placeholder
  block is replaced by the final byline (prepared by Sadie Weaving;
  accountable human author Tommy Xaypanya, corresponding author); the
  cover pill reads "Public edition"; the Third Edition document-control
  block records the ruling. The second edition's authorship disclosure
  is retained verbatim in the front matter. Craig Ross is not an author.
- **Re-verification after finalization:** numbers 86/86 PASS; blocker
  sweep PASS (byline item finalized; tier 1: 0, tier 2: 0, tier 3: 68,
  all adjudicated); PDF 41 pp.
- **Final hashes (SHA-256):** PDF
  e27d90bfffb5b51fe19c4a76a3105aa67ae47f3767ef336796acfeffd089a4d7;
  HTML ed9c6ade385b4eeddeaa493118980edad51d624c6691afa1e11ccd0bcbba500c;
  demo 72a922da185c54c9ab45248c4270776ab8476e6da97b5b14f8f53d428e05782e
  (unchanged by finalization); summary.json
  6db452f29270486c272c92c5175d3883be8e0edc1e5228949dea0d9e54a9d812
  (unchanged). The artifact ZIP hash is recorded in the pack
  HANDOFF.md (the ZIP cannot hash itself).
