# Public supplement — "First Device Models, Trained In-House" (second edition, hardening revision 2.1)

This supplement is the public reproduction package for the whitepaper. It is
hosted with the paper in the Hugging Face dataset `Thox-ai/thox-whitepapers`.
It contains the evaluation instrument exactly as scored, the serving
Modelfiles the gate runs used, and one complete per-question gate output
produced for the hardening revision. See `MANIFEST.md` for the file list with
SHA-256 hashes and provenance.

## Contents

- `gate49/` — the GATE49 factuality gate bundle: the scorer
  (`factuality_gate49.py`), the `facts` package that generates the 49
  questions from the THOX facts card and checks answers (detectors, decline
  markers, aggregation, gate policy), the facts card itself
  (`facts/data/thox_facts.json`, version 1.1.0, with its `SOURCE.json`
  provenance and the human-readable `THOX_FACTS.md`), and `VENDOR.md`, the
  vendoring record that traces every file to `ttracx/thoxllm-factory`
  (`scripts/factuality_gate.py` and the `facts/` package) and verifies the
  generated question split (verified 12 / unknown 26 / known_false 10 /
  pricing 1) is the same split the Waves A/B runs report. The Wave A and
  Wave B gates ran the factory original of this code; the vendored copy
  differs from the original by one path block only (see `VENDOR.md` §3).
- `modelfiles/` — the serving Modelfiles the gate runs ran under, one per
  model. The five edge Modelfiles are the finishing pack Modelfiles as
  published in each model repository on Hugging Face (retrieved from the
  repositories at their current HEAD, which the Wave B commits did not
  change). The ThoxClip-Qwen3-0.6B Modelfile is the Wave B finishing
  Modelfile from the program workdir; that model's repository does not
  carry a Modelfile file. Each Modelfile's SYSTEM text is a one-line
  identity prompt; none of them contains any fact the gate scores.
- `gate-outputs/constant-abstainer/` — a complete per-question gate output
  produced for the hardening revision (2026-10-30): a constant-abstainer
  transcript (every question answered with the facts card's prescribed
  decline form) scored offline by the bundled scorer in `--transcript`
  mode. Result: 25/49 passed, 0 hard failures, score 3.531/5, verdict PASS.
  This is the instrument's abstention floor, reported in Section 11.4 of
  the paper. Files: `transcript.json` (the answers), `answers.json`,
  `factuality-report.json` (per-question verdicts), `factuality-report.md`.

## What is not in this supplement, and why

- **Per-question gate outputs for the Wave A and Wave B model runs.** Those
  gate runs executed on fleet hosts (the fleet Mac workstation for Wave A and the ThoxClip
  finishing; the fleet Windows workstation for Wave B) and their per-question outputs were not
  retained in the program records available to this paper; the run records
  preserve the aggregate tables, category splits, and hard-failure counts
  the paper reports. The constant-abstainer output above is included so a
  reader can inspect the scorer's per-question verdict format end to end.
- **The training corpora.** `train.jsonl` (205 rows) and `train_wave_b.jsonl`
  (982 rows) stay in the private dataset repository
  `Thox-ai/thox-factory-sft-v5`. They contain pre-release campaign material
  (campaign figures and launch framing written before the campaign closed),
  and THOX does not publish pre-release campaign material. Corpus
  composition, hashes, and hygiene operations are fully described in
  Sections 11.1 and 11.2 of the paper so the construction can be audited
  against the recorded hashes by anyone with repository access.
- **Job logs and the pilot seed repository.** Hugging Face job logs live
  with the job records under the `Thox-ai` namespace; the pilot's dataset
  repository `Thox-ai/lfm3-omni-voice-seed` is private for the same
  pre-release reason. The pilot's published `results.json` (per-row held
  out predictions) is in its public model repository,
  `Thox-ai/lfm3-omni-voice-lora-pilot`.
