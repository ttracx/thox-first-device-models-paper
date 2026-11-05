<!-- Staged copy of the internal record RUN.md for the Third Edition pack. Internal host names and filesystem paths genericized to host classes / file names; content otherwise verbatim. Original retained in the internal program workdir. -->

# Wave B Overnight Training Track — RUN

Date: 2026-10-28 (overnight, Tommy's 02:21 CT order). Executor: Sadie
subagent track. Claim discipline: no accuracy claims without a run; every
gate result below is from an executed gate run.

## Track status summary

- Step 1 (ThoxClip-Qwen3-0.6B finishing): DONE. GGUF + gate result in
  card v3, HF commit `ede5f0d3d53f40768a176259575b098576eb10692a`,
  Ollama `thox-ai/thoxclip-qwen3-0.6b:q4_k_m` + `:latest` pushed.
- Step 2 (Wave B dataset): DONE, published (see below).
- Step 3 (six retrains): DONE (see training table).
- Step 4 (gates + publish rule): DONE for five models (four edge
  models republished on improvement; B5 skin placed in the device
  catalog). One open item: ThoxEdge-0.8B's Wave B gate must be re-run
  on the fleet Mac workstation when it recovers; its Wave B artifact is retained
  unpublished on the fleet Windows workstation and Wave A remains latest (details below).

## Step 2 — Wave B dataset (DONE, published)

- Corpus: `train_wave_b.jsonl`, 982 rows, dict-row contract
  (`messages`: system/user/assistant), SHA-256
  `9ddf814ddd6a5f057eab4842461bce24c7d2bc082ac1d26576b7cb6fcbfe50e8`.
- Composition: 838 newly authored rows + 144 v5 rows retained verbatim.
  49 v5 rows superseded by canonical rewrites of the same prompt during
  dedupe; 12 v5 rows excluded for asserting device chipset identities
  contradicting the THOX facts card / no-processor-invention directive
  (v5 indices 35, 44, 45, 46, 47, 48, 50, 56, 68, 70, 121, 150).
- Domains: company_facts 415, device_support 125, tool_routing 121,
  campaign 106, coding 85, persona 54, ops 33, safety 25, model_lineup 18.
- Sources: THOX facts card (`thoxllm-factory/facts/data/THOX_FACTS.md`);
  live thox.ai campaign oracle (kits $189/$419/$699 with limits
  150/100/50; Early Bird singles $79/$119/$239/$319; Super Early Bird
  through Nov 2, 2026 23:59 CT; delivery estimate Feb–Apr 2027; free
  standard shipping on eligible orders over $499); voice-command pilot
  routing contract; canonical THOX runbook answers. Recorded design
  decision: campaign figures taught only in campaign-framed questions;
  generic price questions train decline + pointer to www.thox.ai
  (matches the factuality gate). No processor/chipset specifics anywhere;
  dedicated processor-decline rows added.
- Validation: row-by-row structure check (roles, non-empty turns);
  trainer loader contract (`Dataset.from_list([{"messages": ...}])`)
  exercised by every Step 3 run.
- Published: `Thox-ai/thox-factory-sft-v5` (private), commit
  `71ab11b32971ef2828b57adad52ec8fe3d371fc5`. The repo's `train.jsonl`
  verified byte-identical to the local factory v5 copy (SHA-256
  `ac118a250bc989c9478ec7e4ebdcc706e12e489979b02e6bf1af8b831f8b2514`)
  before publishing; v5 file untouched. The repo previously had no
  README; a full dataset card was created (frontmatter + Wave B section).

## Step 1 — ThoxClip-Qwen3-0.6B finishing (DONE)

- Transfer chain verified by SHA-256 at every hop: VM publish dir →
  the fleet Windows workstation /mnt/v/wave-b/clip-publish/ → the fleet Mac workstation snapshots/
  (`model.safetensors` 1,192,135,096 B, `08dde03d…` = the published HF
  artifact).
- GGUF (the fleet Mac workstation manual pipeline): `ThoxClip-Qwen3-0.6B.Q4_K_M.gguf`,
  396,704,672 B, SHA-256
  `1e009136e1ed3bdfee1343a5309c7d5f36d75b517ad84d56233c9ffe5c248d96`.
- Factuality gate (the fleet Mac workstation, Ollama backend, weights only): **FAIL,
  22/49 passed, score 2.776/5, 14 hard failures.** By category: verified
  2/12 (2.5), unknown 11/26 (2.269), known_false 9/10 (4.7), pricing 0/1
  (0.0). Smoke ("What are you?") answers in THOX identity as the
  ThoxClip device assistant. Recorded verbatim in the model card.
- Card v3 (GGUF row, gate result, grounding-required limitation) and the
  GGUF published to Thox-ai/ThoxClip-Qwen3-0.6B, HF commit
  `ede5f0d3d53f40768a176259575b098576eb10692a` (GGUF hash re-verified
  from the repo after upload). Ollama
  `thox-ai/thoxclip-qwen3-0.6b:q4_k_m` + `:latest` pushed from
  the fleet Windows workstation; the model page is live on ollama.com (verified).

## Corpus correction (decision record, 2026-10-28 ~02:47 CT)

First gate-report inspection (Wave A Edge-0.5B verdicts) showed the
gate's known-false detectors hard-fail an answer that merely REPEATS a
fabricated name inside a denial (e.g. naming "Thox API" while rejecting
it). A scan of the built Wave B corpus found 10 rows (the part-4 frame
family for the two fabricated product names) repeating the fabrication
in the assistant turn. Fix applied before any retrain consumed the
corpus: those 10 answers rewritten to deny without naming the
fabrication; rescan = zero hits for every fabricated string (founder
names, firms, amounts, cities) in any assistant turn. The Edge-0.5B run
launched minutes earlier on the unpatched file was killed (~15 min in)
and relaunched on the corrected corpus so all six retrains share one
identical dataset. Corrected corpus SHA-256:
`6665a8cbd79197c61a9db8119b743faedc3e469407364bb553ec9478e90a5784`
(982 rows, unchanged count); republished to the dataset repo (HEAD
`e76e1b027cde01d47c0dffaa9fbbc15c2ba43f93`).

## Step 3 — Retrains (the fleet Windows workstation, local; HF Jobs token-blocked per
Workstream B). Recipe: `train_wave_b.py` (adapted from the proven
train_clip_cpu.py): LoRA r32 alpha 64, merged to bf16, LR 1e-4 cosine,
warmup_ratio 0.05, 3 epochs, max_length 1024, bs 8, CUDA fp32 + bf16
autocast on the RTX 4060 Ti (16.0 of 17.2 GB VRAM free at launch; the two
loopback llama-servers co-resident). Data: the Wave B corpus above for
every model.

All six retrains completed on the fleet Windows workstation (RTX 4060 Ti, CUDA fp32 + bf16
autocast), on the corrected corpus (SHA-256 `6665a8cb…`, 982 rows,
3 epochs, LR 1e-4 cosine, warmup_steps 0.05, LoRA r32 alpha 64 merged
to bf16). Final train losses (TRL train_loss; corpora differ between
waves, so Wave A losses are listed for provenance, not as a quality
comparison):

| Model | Base | Wave B loss | Wave A loss (205 rows) | Runtime |
|---|---|---:|---:|---:|
| ThoxEdge-0.5B | Qwen/Qwen2.5-0.5B-Instruct | 0.7093 | 1.680 | 102 s |
| ThoxEdge-0.8B | Qwen/Qwen3.5-0.8B | 0.5466 | 1.454 | 207 s |
| ThoxNano-360M | HuggingFaceTB/SmolLM-360M | 1.5150 | 3.124 | 113 s |
| ThoxFlux-350M | LiquidAI/LFM2.5-350M | 1.6682 | 3.463 | 49 s |
| ThoxNano-135M | HuggingFaceTB/SmolLM-135M | 1.6403 | 3.273 | 110 s |
| B5 skin | saidutta69/SmolLM2-1.7B-Instruct-heretic | 0.6348 | n/a (no prior train) | 253 s (bs 4) |

Trainer fixes required en route (recorded, all in `train_wave_b.py`):
(1) `warmup_ratio` is not accepted by this TRL SFTConfig; the proven
script's `warmup_steps=0.05` form is used. (2) SFTTrainer must receive
`processing_class=tok` (as the canonical trainer does) or it reloads a
fresh tokenizer and the ChatML fallback for the template-less SmolLM
bases is lost; Nano-360M/135M failed on this first. (3) Qwen3.5-0.8B's
Auto load pulls an image processor needing PIL/torchvision (absent);
the trainer falls back to the config's named text class
(`Qwen3_5ForCausalLM`, the Wave A artifact's architecture).

## Step 4 — Gates, GGUF, publish decisions

Wave A gate baselines (the fleet Mac workstation, weights only, 49 questions):
ThoxEdge-0.5B FAIL 21/49, 2.837/5 · ThoxEdge-0.8B FAIL 19/49, 2.714/5 ·
ThoxFlux-350M FAIL 4/49, 0.898/5 · ThoxNano-135M FAIL 2/49, 0.816/5 ·
ThoxNano-360M ERROR (gate aborted, repetition loop; no score) ·
B5 raw heretic: never numerically gated in Wave A (5-prompt smoke
failure on file in shortlist-builds-20261028/work/kh-internal-tiers.md);
a baseline gate on the raw catalog GGUF was run in this track before
the skin's gate (result below).

Publish rule (per the brief): republish HF + Ollama only if the Wave B
gate score improves on Wave A; regressions keep the Wave A artifact as
latest and are reported, not published.

Wave B gate results (the fleet Windows workstation, Ollama 0.40.11, weights only) and
publish decisions under the brief's rule (republish only on score
improvement). Every verdict remains FAIL under the gate policy (zero
hard failures allowed); scores are the comparison the rule specifies.

| Model | Wave A | Wave B | Decision |
|---|---|---|---|
| ThoxEdge-0.5B | FAIL 21/49, 2.837 | FAIL 47/49, **4.837** (verified 11/12, unknown 26/26, known_false 10/10, pricing 0/1; sole hard failure = the pricing question, answered without the required decline) | IMPROVED → republished HF + Ollama |
| ThoxEdge-0.8B | FAIL 19/49, 2.714 | INVALID measurement: 0/49 with every answer empty | HELD — not published; see note |
| ThoxFlux-350M | FAIL 4/49, 0.898 | FAIL 20/49, **2.49** (verified 3/12, unknown 9/26, known_false 8/10, pricing 0/1) | IMPROVED → republished HF + Ollama |
| ThoxNano-360M | ERROR (no score) | FAIL 23/49, **2.959** (verified 3/12, unknown 17/26, known_false 2/10, pricing 1/1) | IMPROVED (first completed gate) → republished HF + Ollama |
| ThoxNano-135M | FAIL 2/49, 0.816 | FAIL 23/49, **3.0** (verified 1/12, unknown 14/26, known_false 7/10, pricing 1/1) | IMPROVED → republished HF + Ollama |
| B5 skin | FAIL 7/49, 1.163 (raw base, baseline run in this track; by category verified 2/12, unknown 5/26, known_false 0/10, pricing 0/1) | FAIL 44/49, **4.653** (verified 9/12, unknown 26/26, known_false 8/10, pricing 1/1; sole hard failure = product-lineup question, fabricated names repeated inside the rejection) | IMPROVED → device-catalog placement (below) |

ThoxEdge-0.8B note: the 0/49 is a serving artifact, not a model
result. On the fleet Windows workstation's Ollama 0.40.11 the Qwen3.5 model returns its
answers in the `thinking` channel with empty `content` (verified by
direct /api/chat inspection: the correct answer "www.thox.ai" arrived
as thinking text); the gate reads content, so every answer scored as
empty. The same model answers correctly via /api/generate and its
smoke was clean THOX identity. The Wave B artifact (merged weights on
the fleet Windows workstation; GGUF 529,296,896 B, SHA-256
`183fb38e8c53999c3902371a456ab9e00e5ffc3251e316398b30d7beab77fe43`)
is retained unpublished; its gate should be re-run on the fleet Mac workstation
(Ollama 0.40.12, the Wave A host) when the fleet Mac workstation recovers. Under the
publish rule an invalid measurement cannot justify a republish, so
Wave A remains latest. This is the track's one open item.

B5 distribution decision (conservative, recorded): the skin improved
by +3.49 points, but B5's channel is the device catalog, not public
registries. The DEVICE-SHIP exception covers on-device delivery; a
public HF/Ollama posting of an uncensored model would be a public
distribution the exception does not name, and PUBLIC-HOSTED remains
held. The skinned GGUF was therefore placed in the the fleet Windows workstation device
catalog (`SmolLM2-1.7B-Instruct-heretic-waveb-Q4_K_M.gguf`,
1,055,609,344 B, SHA-256
`d406f8b193f84d94a17c5da5462ac92dcc3d30a1a9b021a6062607b8d429d028`),
with a full model card (`SmolLM2-1.7B-Instruct-heretic-waveb-CARD.md`,
including the failed-gate history of the raw artifact) and a local-only
Ollama tag `thox-device/smollm2-1.7b-heretic-waveb:q4` (never pushed).

Wave B GGUFs (Q4_K_M, manual llama.cpp pipeline, the fleet Windows workstation):
ThoxEdge-0.5B 397,807,488 B `6fb3222b996048fac6e4241274104382f30582b30bbddf47edcf9b56917d8598` ·
ThoxFlux-350M 229,314,592 B `8c9fa8f0a08e3b7904ece716b6716ca16f2330c13a5dbfa3870b034ac610ca7a` ·
ThoxNano-360M 270,590,336 B `b1c6dcc9c91a8664c420edcc9dbd9f47967f37b5abe193a2a4f5a37ecd904876` ·
ThoxNano-135M 105,453,888 B `7ae9664d5d27d82481d5bc16415cef2f4326f430f6fb33569b62927d87df8d66`

Smokes (the fleet Windows workstation, "What are you?", generate endpoint): Edge-0.5B,
Flux-350M, Edge-0.8B, B5 skin answer in THOX identity/house voice;
Nano-360M answers tersely on-identity ("A ThoxClip assistant.");
Nano-135M degenerates into token repetition on the bare generate
prompt (its chat-path gate answers were coherent; the 135M remains
the weakest artifact, as in Wave A).

Publish records (all hashes verified from the registries after
upload; the the fleet Windows workstation uplink dropped connections repeatedly during
the publish window — Xet CAS resets on HF, TCP resets and one HTTP
416 on Ollama — and every publish was retried to a verified landing):

- HF Thox-ai/ThoxEdge-0.5B: commit
  `75065d2f288c60bd37842808e3d47efb4131542d`; weights SHA-256
  `aa3b81fd4e8c92fbea25009c5488d96e5e6a743fb073c577604ffb3e2746c4d3`;
  GGUF + safetensors LFS hashes verified OK.
- HF Thox-ai/ThoxFlux-350M: commit
  `856bbdeadb909f6f8e1194ba90af671e6cd5052a`; weights SHA-256
  `c3d8a54d1353c759e247b639b180d1bea69f52f0d7aa071347e17f64eba7f52a`;
  verifies OK. (Card license remains the base model's LFM license,
  unchanged.)
- HF Thox-ai/ThoxNano-360M: commit
  `e2b539111be1cbc678b41c887c0f61d02b950626`; weights SHA-256
  `eda05372b511be9d809d7bc65dc93c847c6f1d28f598b7fc9abcfeaf32c1a758`;
  verifies OK.
- HF Thox-ai/ThoxNano-135M: commit
  `92cc969c2cad83daf7ea10e3d758c4675163b065`; weights SHA-256
  `b7bf1a3eeb35e5a40d27fb1b7ef895bbce53cc2fe6a990fb79ff1a72f38fdf79`;
  verifies OK.
- Each HF card gained a dated "Wave B retrain (2026-10-28)" section
  with the corpus hash, training loss, both gate scores, the FAIL
  verdict, and the new GGUF hash; Files-table GGUF rows refreshed
  where present.
- Ollama (pushed from the fleet Windows workstation, `:q4_k_m` and `:latest`):
  thoxedge-0.5b (remote tags verified on ollama.com, 398 MB, updated
  2026-10-28 ~04:43 CT), thoxflux-350m, thoxnano-360m, thoxnano-135m,
  thoxclip-qwen3-0.6b — all pushes completed; local digests:
  edge 0.5b fd49c8e609f8, flux 0e96518ae6cd, nano-360m 2bcc94dd771e,
  nano-135m 5b7295617731, clip f2a73b016d17.
- ThoxEdge-0.8B: NOT published (held, see the note above). the fleet Mac workstation was
  still SSH-unresponsive at 04:52 CT (~1.6 h into the tenant load
  storm); re-running its gate there is the track's single open item.

## Blockers and deviations

- **the fleet Mac workstation outage (deviation, recorded):** from ~03:15 CT, the fleet Mac workstation SSH
  became unresponsive (connection timeouts, then banner-exchange
  timeouts) in a tenant load storm on the shared the hosting provider host; it
  was still down at 03:40 CT. Step 1 (ThoxClip) was completed on the fleet Mac workstation
  before the outage. Step 4 finishes were moved to the fleet Windows workstation: identical
  gate code (copied from the canonical thoxllm-factory tree), identical
  49 questions, identical pack Modelfiles, same manual llama.cpp
  pipeline (the fleet Windows workstation checkout /mnt/v/ttracx-projects/llama.cpp). Only
  deltas: host, and Ollama 0.40.11 (the fleet Windows workstation) vs 0.40.12 (the fleet Mac workstation).
  Wave A baselines were measured on the fleet Mac workstation; the host delta is recorded
  with every Wave B score. Smoke tests for republished models ran on
  the fleet Windows workstation for the same reason. An earlier the fleet Mac workstation-side finish-all
  orchestrator died with the outage (its rsyncs returned 255); no
  partial the fleet Mac workstation artifacts were used.
- the fleet Windows workstation root disk is at 99% (13 GB free at last check); all work
  was kept on /mnt/v per instructions. Docker volumes untouched.
