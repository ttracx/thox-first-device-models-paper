<!-- Staged copy of the internal record RUN.md for the Third Edition pack. Internal host names and filesystem paths genericized to host classes / file names; content otherwise verbatim. Original retained in the internal program workdir. -->

# Edge finishing run — 2026-10-28 (Workstream A)

Order: Tommy, 2026-10-27 ~23:46 CT — finish the five trained THOX edge models end to end (GGUF regen, factuality gate, model cards, Ollama publishing, smoke tests). Host directive 23:51 CT: conversion + smoke + eval on the fleet Mac workstation (Sadie's Mac); the fleet Windows workstation keeps disk triage + Ollama pushes (namespace key stays on the fleet Windows workstation; no keys copied between hosts).

Hosts: the fleet Mac workstation (the hosting provider M4, macOS 26.7) = snapshot staging, llama.cpp GGUF conversion, factuality gate, smoke tests. the fleet Windows workstation = disk triage, HF snapshot download, HF uploads (GGUF + Modelfile + cards), GGUF pull from the fleet Mac workstation, Ollama create/push. VM = orchestration only.

## 1. the fleet Windows workstation disk triage

Root `/` was 20 GB free (99% used) at start (brief said 23 GB; already tighter). Actions, regenerable material only: systemd journal vacuum freed 744.8 MB; dangling Docker image prune + builder prune reclaimed ~0.5 GB total. Root ended at 21 GB free (98%). Docker volumes (~86 GB flagged reclaimable) deliberately NOT touched (not provably regenerable). `/mnt/v` has 117 GB free; all finishing work on the fleet Windows workstation was placed under `/mnt/v/edge-finishing/` regardless. Root remains tight; a deeper cleanup needs a founder decision on volumes/caches, not done here.

## 2. Token scrub — verified unnecessary on current factory main

Cloned `ttracx/thoxllm-factory` to the fleet Windows workstation (`/mnt/v/edge-finishing/factory`, HEAD = merge 7149aa0, PR #78). Finding: `scripts/finish_edge_model.py` on current main is ALREADY env-only (`token = os.environ.get("HF_TOKEN")`, exits if unset). A repo-wide scan for credential literals (hf_/ghp_/sk- patterns) found ZERO matches in any file. The embedded-token fallback flagged in the fleet record is not present in current main, so there was nothing to scrub and no scrub commit exists. (A non-secret path string `V:\AI\huggingface\token` appears in compute/deploy.py comments; it is a file path, not a credential.)

## 3. GGUF regeneration — finisher broken, manual llama.cpp path used

`finish_edge_model.py` is broken against current Ollama: it quantizes with `ollama create -q q4_K_M` from a GGUF, and current Ollama refuses ("create-time quantization is only supported for safetensors imports"). Per the brief's fallback, conversion was done manually with llama.cpp on the fleet Mac workstation:

- Snapshots of all five trained repos downloaded on the fleet Windows workstation (`/mnt/v/edge-finishing/snapshots/`) and pushed to the fleet Mac workstation over the tailnet (the fleet Windows workstation-initiated rsync; the fleet Mac workstation's userspace tailscaled has no outbound tailnet routing). Safetensors byte sizes on the fleet Mac workstation matched WAVE-STATUS exactly.
- the fleet Mac workstation env: brew Python 3.15 venv (`venv`) with torch 2.14.1 CPU, transformers 5.21.0, gguf; llama.cpp cloned + built (`llama-quantize` OK; `llama-cli` build failed — Ollama app used for smoke instead). `convert_hf_to_gguf.py` → f16 GGUF → `llama-quantize q4_K_M`.
- Blocker found and fixed mid-run: `sentencepiece` would not install on Python 3.15 at first (source wheel build); a retry completed (0.2.2) and the three affected models (SmolLM ×2, Qwen2.5) converted. Qwen3.5 and LFM2.5 conversions did not need it.

Results (SHA-256 verified identical on the fleet Mac workstation, the fleet Windows workstation, and the HF blob store after upload):

| Model | New GGUF size | New GGUF SHA-256 | Old repack size (2026-08-11) |
|---|---:|---|---:|
| ThoxFlux-350M | 229,309,120 B | `7526e4014ff8ed4e6707459c6b90bd862c2339ea4bbf4fce8e629f09c087f3fa` | 229,308,960 B |
| ThoxEdge-0.8B | 529,289,280 B | `3b375f2971342c2cfeb9b5c97b68db8b35cb915d044555bb784dfde69b19310e` | 529,288,992 B |
| ThoxEdge-0.5B | 397,805,088 B | `2192b7b4f2d19c25cad7ff386a9403e853638af54d7bf43917e977d3b6069438` | 397,804,768 B |
| ThoxNano-360M | 270,590,080 B | `18cb1f5e83ecabe8dbdfe7bd535aeb3c653014396cc567938a8ce370fc3800a4` | 270,589,984 B |
| ThoxNano-135M | 105,453,664 B | `aff370028ff25d5dbcf8080be5008fecf393c6b4a4f513df7299f2e07e9fe9ad` | 105,453,568 B |

Note: new sizes differ from the old repacks by only ~100–320 B (GGUF metadata; tensor shapes are identical by construction). The meaningful difference is the weights: provenance is the conversion chain from the verified trained safetensors plus the behavioral smoke/gate results below — a base repack does not produce THOX identity answers.

Upload friction: the first two GGUFs uploaded cleanly via Xet. The remaining three hit a degraded route to `cas-server.xethub.hf.co` from the fleet Windows workstation (~00:30–01:20 CT): one Xet attempt stalled at ~60% for 25+ minutes in retry loops, and a classic-LFS attempt (HF_HUB_DISABLE_XET=1) died on a server disconnect. After a pause, a fresh upload run completed all three. All five repos also received the cleaned pack Modelfile.

## 4. Factuality gate (thoxllm-factory `scripts/factuality_gate.py`, the fleet Mac workstation, Ollama backend, weights only, no grounding)

49 canonical-fact questions per model, temperature 0. Exit 0 = pass, 1 = fail, 2 = could not run.

| Model | Result | Detail |
|---|---|---|
| ThoxEdge-0.5B | FAIL | 21/49 passed, 11 hard failures, score 2.837/5 (best of the wave) |
| ThoxEdge-0.8B | FAIL | 19/49 passed, 11 hard failures, score 2.714/5 |
| ThoxFlux-350M | FAIL | 4/49 passed, 33 hard failures, score 0.898/5 |
| ThoxNano-135M | FAIL | 2/49 passed, 32 hard failures, score 0.816/5 |
| ThoxNano-360M | ERROR (rc=2) | Gate could not complete: inference aborted twice with "prediction aborted, token repeat limit reached" — the model loops on at least one gate question. No score. |

Consistent with the 205-row identity-skin corpus: the fine-tunes do not hold canonical THOX facts from the weights. Per the brief, failed gates do not block publishing; every card states its result verbatim, and deployed surfaces must use serving-side grounding. (This deviates from PUSH-CHECKLIST.md's "gate passed" precondition; the brief's explicit instruction governed. Flagged for the parent.)

## 5. Model cards

Rewritten under the THOX model card rule and uploaded from the fleet Windows workstation (README.md per repo; repo HEAD after this run in parentheses):

- ThoxFlux-350M (ccb2de2f) — license: other / LFM Open License v1.0 with the under-$10M commercial ceiling stated on the card; gate FAIL 0.898/5 stated.
- ThoxEdge-0.8B (db4403d7) — apache-2.0, working `license-apache--2.0-blue.svg` badge; gate FAIL 2.714/5 stated. First complete card for this model (previous card had a wrong safetensors size and pre-training status text).
- ThoxEdge-0.5B (66efd2c6) — apache-2.0; gate FAIL 2.837/5 stated.
- ThoxNano-135M (8774ebf8) — apache-2.0; gate FAIL 0.816/5 and the weak smoke result stated.
- ThoxNano-360M (e88857b1) — the 2026-10-27 card was kept and surgically updated (GGUF now trained, gate ERROR + smoke recorded), not rewritten.

All cards carry: summary, intended use, out of scope, training data + procedure (thox-factory-sft-v5, 205 rows, LoRA r32 merged, lr 1e-4, 3 epochs, exact final losses + HF Jobs IDs), evaluation = gate result + "broader evaluation pending", limitations, files table with trained safetensors + new GGUF SHA-256, provenance.

## 6. Ollama publishing (the fleet Windows workstation, per PUSH-CHECKLIST.md)

- Probe: `thox-ai/publish-probe:tmp` create OK locally; its push errored with HTTP 416 RANGE_INVALID on the blob (the probe reused the Nano-135M GGUF blob) and left NO manifest in the registry (verified MANIFEST_UNKNOWN afterward — nothing to clean up). Namespace ownership is instead proven by the five successful authenticated pushes under `thox-ai/*` with the the fleet Windows workstation key.
- Flux Modelfile template re-verified against the trained repo's `tokenizer_config.json` before pushing (LFM2 tokenizer_config carries only `add_prefix_space`; the ChatML template stands, same as the repo's own Modelfile template).
- All five created, smoke-run locally on the fleet Windows workstation, pushed as `:q4_k_m` and `:latest`. One repair: thoxnano-135m's `:q4_k_m` manifest was missing after the first pass (same 416 sequence); a re-push fixed it.
- Ground-truth verification via registry.ollama.ai: for all five models, BOTH `:q4_k_m` and `:latest` manifests exist and their model-layer digests equal the new trained GGUF SHA-256s (aff37002…, 18cb1f5e…, 2192b7b4…, 3b375f29…, 7526e401…). ThoxEdge-0.8B's library page is new (first publish).

## 7. Smoke tests (the fleet Mac workstation, Ollama, pack Modelfiles, prompt "What are you?")

- ThoxEdge-0.8B: "I am a THOX assistant. I run on ThoxMini. I am trained on the THOX docs and the THOX spec. I am not a person. I am not a corporation."
- ThoxFlux-350M: "I am a THOX device assistant running on ThoxClip-class hardware."
- ThoxEdge-0.5B: "A THOX device. I do not communicate over the air; my firmware routes all messages to me."
- ThoxNano-360M: echoes its THOX/ThoxClip system text with some garbled tokens (identity present, template leakage).
- ThoxNano-135M: replied "What's the name of your device?" — deflection, weakest of the five.

No accuracy claims beyond the gate + smoke results above.

## the fleet Mac workstation friction (fleet record)

- No sudo (shared managed box); everything user-local. `brew install python@3.12` via the user-local HEAD brew silently did not land; Python 3.15 venv used instead, which cost time on `sentencepiece` (source build, eventually succeeded).
- llama.cpp `llama-cli` target failed to build (tools/cli Error 2); `llama-quantize` and the conversion script worked. Ollama app (0.40.12, `~/Applications`) covered smoke/gate serving on port 11435.
- Direct VM→the fleet Mac workstation SSH through the egress proxy resets frequently; `ssh -J knighthub` was the reliable route. All bulk transfers were the fleet Windows workstation-initiated over the tailnet (fast); the fleet Mac workstation cannot initiate tailnet transfers (userspace tailscaled, no outbound routing).
- The `the workspace volume` volume shows 2.3 Ti free; the tight disk figure (~42 GB) is the root volume. Keep edge work under `the workspace volume`.
- the fleet Mac workstation has no HF token and none was copied to it; all authenticated HF operations ran from the fleet Windows workstation.

## Deviations from the brief/checklist, stated plainly

1. `finish_edge_model.py` unused for conversion (broken Ollama quantize path); manual llama.cpp pipeline used per the brief's fallback. The finisher's f16-conversion stage did run once on the fleet Windows workstation for Nano-135M before the failure point; the shipped GGUFs all come from the the fleet Mac workstation pipeline.
2. Smoke tests ran on the fleet Mac workstation (host directive) rather than the fleet Windows workstation as the original step 6 said; the fleet Windows workstation also ran local smokes during the push flow.
3. PUSH-CHECKLIST "factuality gate passed" precondition not met by any model; publishing proceeded under the brief's explicit rule (fail does not block; card states the result).
4. WAVE-STATUS step (4), a factory registry update PR, was not part of this brief's steps and was not done.
