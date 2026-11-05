<!-- Staged copy of the internal record WAVE-STATUS.md for the Third Edition pack. Internal host names and filesystem paths genericized to host classes / file names; content otherwise verbatim. Original retained in the internal program workdir. -->

# Edge fast-track wave — status (2026-10-27)

Tommy's order (13:28 CT): finish the pending Kickstarter device models as a
priority, contribute resources, get them onto hardware for testing.

## Inventory (factory registry, verified 2026-10-27)

Pending (queued, skeleton repos, NO weights), Kickstarter four:
- ThoxMini: ThoxEdge-0.8B (Qwen/Qwen3.5-0.8B), ThoxEdge-0.5B (Qwen/Qwen2.5-0.5B-Instruct)
- ThoxClip: ThoxFlux-350M (LiquidAI/LFM2.5-350M), ThoxNano-360M (HuggingFaceTB/SmolLM-360M)
- ThoxKey: ThoxNano-135M (HuggingFaceTB/SmolLM-135M)
- ThoxAir: no queued assistant model; Air ships thoxair-16m-role today and
  rides the 350M-class tier + mesh (gap noted to Tommy 2026-10-27).

Already published per device (role models): thoxkey-9m-role, thoxair-16m-role,
thoxclip-9m-role, thoxmini-125m-role; plus thoxmini-3b and lfm3-omni-2b (Mini).

Not trainable as-is (decisions, not runs): ThoxKey-TLM (no base; its own card
proposes retiring it in favor of ThoxKey-9M-role), ThoxMesh-Head-C6 (base is a
placeholder string), ThoxUSB-Edge (same base as ThoxEdge-0.8B; not a
Kickstarter-four device; ThoxUSB has no locked hardware spec).

## Runs

- Pilot (voice-command): job 6ae0eaed FAILED pre-training (HF Jobs inject no
  private-repo token). Fixed by passing HF_TOKEN as a job secret via
  launch_job.py on the Mac. Relaunch 6ae0edc23fb22a235dd30268 RUNNING 13:36 CT.
- Pathfinder (ThoxFlux-350M): job 6ae0edfa41e90535df7662cc, t4-small,
  SCHEDULING at 13:31 CT. Bundle: Thox-ai/thox-edge-sft (train_edge_sft.py,
  LoRA r32 on thox-factory-sft-v5 train.jsonl 205 rows, merged weights into
  the existing repos).
- Pathfinder FAILED 2026-10-27 13:34 CT (18:34Z, ERROR, exit 1, running 156s):
  `TypeError: SFTConfig.__init__() got an unexpected keyword argument
  'warmup_ratio'` at train_edge_sft.py:48. Root cause verified from wheels:
  transformers v5 (job installs >=5.20.2, resolved 5.21) removed
  `warmup_ratio`; replacement is `warmup_steps` (float in [0,1) = ratio).
  All other SFTConfig args checked valid in trl 1.16.0 / transformers 5.21.
  Thox-ai/ThoxFlux-350M unchanged (lastModified 2026-10-24, no
  training_summary.json; its safetensors/GGUF are the Oct 24 base repack).
- Fix applied 14:14 CT: train_edge_sft.py `warmup_ratio=0.05` ->
  `warmup_steps=0.05` locally, on the Mac (/tmp/lfm3-pilot), and uploaded to
  Thox-ai/thox-edge-sft, commit e4064570f4ddb38ed73987d85941f697bf96d508;
  verified by re-download.
- Pathfinder RELAUNCHED once (only the pathfinder): job
  6ae0f83e41e90535df76725b, t4-small, RUNNING at 14:15 CT (19:15Z,
  scheduling 13s). Follow-up check edge-wave-check-20261027-2 at ~14:42 CT.
  The other four were NOT launched; they stay gated on a completed
  pathfinder with training_summary.json.
- Queued behind pathfinder verification (check at 14:12 CT): ThoxEdge-0.8B
  (a10g-small), ThoxEdge-0.5B, ThoxNano-360M, ThoxNano-135M (t4-small).
- Pathfinder RELAUNCH FAILED (check edge-wave-check-20261027-2, 14:38 CT):
  job 6ae0f83e41e90535df76725b finished 2026-10-27T19:17:58Z, running 154s;
  hf inspect reports stage CANCELED, but the logs end in a traceback (treat
  as failed, not a clean cancel). Warmup fix HELD: SFTConfig constructed,
  train.jsonl read (205 rows), base weights loaded 148/148. Failure at
  train_edge_sft.py:53, SFTTrainer construction:
  `Dataset.from_list(rows)` -> datasets arrow_dataset.py:1279
  `AttributeError: 'list' object has no attribute 'get'`. Root cause: rows
  was a list of message-lists (`json.loads(l)["messages"]` per line);
  from_list needs a list of dicts. Identical bug to the one diagnosed in
  the LFM3 pilot check at 14:35 CT the same day.
- Thox-ai/ThoxFlux-350M UNCHANGED by the relaunch: sha
  b5e34a706adab7ed6fdba4de645c1b2e71f05a3d, lastModified 2026-10-24,
  no training_summary.json. The gate for the other four is NOT met.
- Fix VERIFIED LIVE in the dataset repo: Thox-ai/thox-edge-sft now at
  commit 360f543258fcd294f3b1ec25acb42b238f856409 (uploaded
  2026-10-27T19:37:29Z, minutes before this check, in the parallel
  pilot-fix work); train_edge_sft.py line 53 is now
  `Dataset.from_list([{"messages": m} for m in rows])`, matching the local
  and Mac (/tmp/lfm3-pilot) copies; verified by force re-download on the
  Mac during this check. No duplicate upload made.
- NO third relaunch launched by this check, and the other four were NOT
  launched. Reasons: step-3 caution after two consecutive pathfinder
  failures one bug at a time, plus the stage discrepancy (CANCELED vs a
  traceback exit). Next call is Sadie's in the main chat / Tommy's: a
  third pathfinder attempt can now run against dataset commit 360f5432.
  Finishing step (GGUF / cards / registry PR) cannot run — no trained
  weights exist yet.
- Transport note: this check first hit the known VM-replacement SSH
  failure (/root/.ssh was an empty 1970 dir again); fixed with the
  standing symlink repair (/root/.ssh -> (internal path)), after which
  `ssh mac-tommy true` exited 0 and the hf checks ran clean.

## Finishing path (after weights land)

the fleet Windows workstation: thoxllm-factory scripts/finish_edge_model.py per repo → Q4_K_M GGUF
back into the repo + firmware handoff; factuality gate; model cards rewritten
from skeleton to trained with real numbers (Tommy's 2026-10-27 card rule);
registry status updated via factory PR. Hardware: GGUF smoke on the fleet Windows workstation/Mac
llama.cpp immediately; Mini-tier models also qualify through the iOS catalog;
physical device flashing is a bench session with Tommy.
- Pathfinder #3 FAILED (check edge-wave-check-20261027-3, 19:22 CT):
  job 6ae0fd7a3fb22a235dd31c34, t4-small, created 2026-10-27T19:37:30Z,
  finished 19:40:26Z, stage ERROR exit 1, running 154s. Prior fixes HELD:
  warmup_steps accepted, dict-row dataset tokenized 205/205, base weights
  loaded 148/148, trainer.train() started. Failure on first backward step:
  trl/kernels/chunked_logprob.py _addmm_fp32 ->
  `RuntimeError: gemm input type at::BFloat16 and output type float is only
  supported for CUDA devices with compute capability 8.0 or higher`.
  Root cause: script used dtype=torch.bfloat16 + bf16=True on t4-small
  (Tesla T4, CC 7.5; bf16 gemm requires Ampere CC >=8.0). Our fault.
- Thox-ai/ThoxFlux-350M UNCHANGED by #3: sha
  b5e34a706adab7ed6fdba4de645c1b2e71f05a3d, lastModified 2026-10-24,
  no training_summary.json. Gate for the other four NOT met; they were
  NOT launched.
- Fix applied 19:23 CT: train_edge_sft.py dtype=torch.float16 and
  SFTConfig bf16=False, fp16=True (with explanatory comments), locally,
  on the Mac (/tmp/lfm3-pilot, py_compile OK), and uploaded to
  Thox-ai/thox-edge-sft, commit fd8b4a2cc812de80defe966a7a64f00d5eba6fb6;
  verified by force re-download on the Mac (fp16 present, bf16=True gone).
- Pathfinder RELAUNCHED once (only the pathfinder): job
  6ae140a541e90535df76cc68, t4-small, timeout 2h, SCHEDULING at
  19:24 CT (created 2026-10-28T00:24:05Z). Follow-up check
  edge-wave-check-20261027-4 at ~19:50 CT.
  Finishing step (GGUF / cards / registry PR) cannot run yet — no
  trained weights exist.
- Pathfinder #4 FAILED at PUBLISH, after training COMPLETED
  (check edge-wave-check-20261027-4, 19:50 CT): job
  6ae140a541e90535df76cc68, t4-small, created 2026-10-28T00:24:05Z,
  finished 00:30:34Z, stage ERROR exit 1, running 305s. The fp16 fix
  HELD end to end: dataset tokenized 205/205, base weights loaded
  148/148, training ran 78/78 steps in 20.01s, train_loss 3.463,
  logged loss fell 6.257 -> 2.544, mean_token_accuracy 0.6298,
  merged shards written. Failure at train_edge_sft.py:68:
  `api.upload_folder(merged_dir, repo_id=OUT, ...)` ->
  HFValidationError "Repo id must be in the form ... :
  '/tmp/edge/merged'". Root cause: huggingface_hub >=1.0 (verified
  1.8.0 on the Mac, 2.1.1 locally) made upload_folder keyword-only
  with signature (repo_id, folder_path, ...), so the positional
  merged_dir was read as repo_id. Same bug class as the LFM3 pilot
  launch #5 publish failure. Our fault. The #4 merged weights died
  with the job container; nothing was published.
- Thox-ai/ThoxFlux-350M UNCHANGED by #4: sha
  b5e34a706adab7ed6fdba4de645c1b2e71f05a3d, lastModified 2026-10-24,
  no training_summary.json. Gate for the other four NOT met; they
  were NOT launched.
- Fix applied 19:52 CT: upload_folder now called as
  `api.upload_folder(folder_path=merged_dir, repo_id=OUT, ...)`
  (upload_file was already all-keyword), locally, on the Mac
  (/tmp/lfm3-pilot, py_compile OK), and uploaded to
  Thox-ai/thox-edge-sft, commit
  172283bd01b678c401b813d6e27e89ef12ba7a27; verified by force
  re-download on the Mac (folder_path=merged_dir present,
  positional form gone, warmup_steps / dict-row / fp16 fixes all
  still present).
- Pathfinder RELAUNCHED once (only the pathfinder): job
  6ae1474d3fb22a235dd37b25, t4-small, timeout 2h, RUNNING at
  19:52 CT (created 2026-10-28T00:52:29Z, scheduling 13s).
  Follow-up check edge-wave-check-20261027-5 at 20:20 CT.
  Finishing step (GGUF / cards / registry PR) cannot run yet —
  no trained weights are published yet; training itself is now
  proven (loss 3.463 on #4), only the publish step was broken.
- Pathfinder #5 COMPLETED (check edge-wave-check-20261027-5, 20:20 CT):
  job 6ae1474d3fb22a235dd37b25, t4-small, created 2026-10-28T00:52:29Z,
  finished 00:56:07Z, stage COMPLETED, running 204s. The upload_folder
  keyword fix HELD end to end: dataset tokenized 205/205, base weights
  loaded 148/148, training ran 78/78 steps, train_loss 3.463, logged
  loss fell 6.257 -> 2.544, merged shards written, logs end with
  "pushed merged weights + summary to Thox-ai/ThoxFlux-350M".
- Thox-ai/ThoxFlux-350M VERIFIED PUBLISHED: new sha
  d0e42dd232c58b17451f911c166ee23c9af28339, lastModified
  2026-10-28T00:55:59Z (after the 19:52 CT launch; prior sha was the
  Oct 24 base repack b5e34a7). Repo now contains model.safetensors,
  config/tokenizer files, the pre-existing Q4_K_M GGUF, and
  training_summary.json: base LiquidAI/LFM2.5-350M, train_rows 205,
  epochs 3.0, lr 0.0001, lora_r 32, training_loss 3.463227467659192,
  method "LoRA SFT (TRL), merged", data
  Thox-ai/thox-factory-sft-v5/train.jsonl. Gate for the other four MET.
- Remaining four LAUNCHED in parallel from the Mac via launch_job.py
  (/tmp/lfm3-pilot, dataset Thox-ai/thox-edge-sft for all) at ~20:22 CT,
  verified by hf jobs inspect (labels/flavors/stages confirmed):
  - ThoxEdge-0.8B: job 6ae14e143fb22a235dd37ff4, a10g-small, timeout 2h,
    label edge-thoxedge-08b, run_thoxedge-08b.sh, RUNNING.
  - ThoxEdge-0.5B: job 6ae14e1f41e90535df76d4bb, t4-small, timeout 2h,
    label edge-thoxedge-05b, run_thoxedge-05b.sh, RUNNING.
  - ThoxNano-360M: job 6ae14e1f3fb22a235dd37ff8, t4-small, timeout 2h,
    label edge-thoxnano-360m, run_thoxnano-360m.sh, SCHEDULING.
  - ThoxNano-135M: job 6ae14e2041e90535df76d4bd, t4-small, timeout 2h,
    label edge-thoxnano-135m, run_thoxnano-135m.sh, SCHEDULING.
- Follow-up check edge-wave-check-20261027-6 created for
  2026-10-27 21:02 CT (~40 min after launch) to verify those four and
  report completion to Tommy in the main chat, including finishing step
  status (GGUF via thoxllm-factory scripts/finish_edge_model.py on
  the fleet Windows workstation — that script contains an embedded HF token fallback in
  source, to be flagged for scrubbing when the finisher runs, value
  never printed; model cards rewritten from skeleton to trained with
  real numbers per Tommy's model card rule; registry update PR).
  Finishing step has NOT run yet in this check; it is gated on all
  four verifying in check #6.
- SIDE-CHAT CROSS-CHECK (2026-10-27 ~21:25 CT, Tommy's "review other teams + pick up collaboratively" ask):
  independently verified via HF API — ThoxEdge-0.8B (sha 1ca557d, loss 1.454) and
  ThoxEdge-0.5B (sha 04e78ea, loss 1.680) COMPLETED + published with
  training_summary.json at 01:25Z. Both Nano jobs ERROR (exit 1). Full logs
  (via the jobs logs API, untruncated) show the identical root cause the
  check-#6 fix addresses: ValueError "tokenizer.chat_template is not set"
  at TRL dataset tokenization — SmolLM-135M/360M base tokenizers ship no
  chat template. Fix VERIFIED LIVE: dataset Thox-ai/thox-edge-sft
  train_edge_sft.py now carries the ChatML fallback and is byte-identical
  to the local copy. NO relaunch launched from the side chat (check #6 is
  in flight and owns the relaunch/finishing lane — duplicate jobs racing
  the same OUT repos would waste credits and could collide on upload).
  Also noted: published Edge/Flux model cards are now STALE — they still
  carry the 2026-10-23/24 status text ("no training log published") and
  the OLD safetensors SHA-256 table, and the in-repo GGUFs are still the
  base repacks, not the fine-tunes. Card rewrite + GGUF regeneration is
  the finishing step and must not be skipped.
- Check #6 (edge-wave-check-20261027-6, 21:02-21:28 CT): two of the
  four COMPLETED and verified published; the two Nano jobs FAILED on
  the chat-template bug, the script was fixed, and ONLY those two were
  relaunched once (this run owned the relaunch lane; the side-chat
  cross-check above launched none).
  - ThoxEdge-0.8B: job 6ae14e143fb22a235dd37ff4 COMPLETED (Jobs API).
    Repo verified: sha 1ca557d8c0c477cf357a744dfef3de16875d4ba1,
    lastModified 2026-10-28T01:25:18Z; commits de66e8ea "SFT on
    Thox-ai/thox-factory-sft-v5 (LoRA r32, 3.0 epochs, merged)"
    01:25:13Z + "Training summary" 01:25:18Z; model.safetensors
    1,504,827,288 B (new blob); training_summary.json: base
    Qwen/Qwen3.5-0.8B, train_rows 205, epochs 3.0, lr 0.0001,
    lora_r 32, training_loss 1.4541844832591522. Logs: loss
    3.051 -> 0.9518 over 7 logging points, "train done:
    1.4541844832591522", ends "pushed merged weights + summary to
    Thox-ai/ThoxEdge-0.8B". Note: first logged grad_norm was nan at
    epoch 0.38; subsequent points are finite and loss fell steadily.
  - ThoxEdge-0.5B: job 6ae14e1f41e90535df76d4bb COMPLETED (Jobs API).
    Repo verified: sha 04e78ea6999872198426c744f354065fbe0fb080,
    lastModified 2026-10-28T01:25:35Z; commits fb4fb121 (SFT)
    01:25:31Z + "Training summary" 01:25:35Z; model.safetensors
    988,097,536 B; training_summary.json: base
    Qwen/Qwen2.5-0.5B-Instruct, training_loss 1.6802658240000408
    (same 205 rows / 3 epochs / lr 1e-4 / r32). Logs: loss
    4.036 -> 1.099, ends "pushed merged weights + summary to
    Thox-ai/ThoxEdge-0.5B".
  - ThoxNano-360M: job 6ae14e1f3fb22a235dd37ff8 ERROR exit 1 (Jobs
    API: "Job failed with exit code: 1"). Started 01:23:29Z, died
    01:26:59Z at train_edge_sft.py:53 in SFTTrainer tokenization:
    `ValueError: Cannot use chat template functions because
    tokenizer.chat_template is not set and no template argument was
    passed!` (trl data_utils _tokenize -> apply_chat_template),
    0/205 rows tokenized, before training. Repo UNCHANGED: sha
    aacb034dbbadcb95501758988833b57537fda66b, lastModified
    2026-10-24T01:53:14Z, no training_summary.json.
  - ThoxNano-135M: job 6ae14e2041e90535df76d4bd ERROR exit 1,
    identical traceback (started 01:24:51Z, died 01:28:53Z). Repo
    UNCHANGED: sha 356921bbd501272dc565726b15c4994494bdcc75,
    lastModified 2026-10-24T01:53:12Z, no training_summary.json.
    Full failure logs saved:
    job-nano-360-135-failures-20261027-2102.txt
  - Root cause: SmolLM-360M/135M are base models; their tokenizers
    ship no chat_template. The three bases that passed (Qwen3.5-0.8B,
    Qwen2.5-0.5B-Instruct, LFM2.5-350M) all carry a native template.
    Our script's fault, same one-bug-at-a-time pattern as the
    pathfinder chain.
  - Fix applied ~21:15 CT: train_edge_sft.py sets a ChatML
    chat_template fallback ONLY when the loaded tokenizer has none.
    The template matches the OUT repos' own Modelfile inference
    contract exactly (<|im_start|>role\ncontent<|im_end|>\n, stop
    <|im_end|>); Jinja render validated locally (full + generation
    prompt forms). Updated locally, on the Mac (/tmp/lfm3-pilot),
    and uploaded to Thox-ai/thox-edge-sft, commit
    c250f9bb1b8e20b71f5c38c73ccfbcdac6a0303e (sha before 172283bd);
    verified by authenticated raw re-read: fallback present, and
    warmup_steps / dict-row / fp16 / upload_folder fixes all still
    present. (Parallel side-chat verification reached byte-identical
    independently.)
  - RELAUNCHED once each from the Mac via launch_job.py
    (/tmp/lfm3-pilot, dataset Thox-ai/thox-edge-sft), verified by
    Jobs API inspect at ~21:24 CT:
    - ThoxNano-360M: job 6ae15d7a41e90535df76ddfa, t4-small,
      timeout 2h, label edge-thoxnano-360m, run_thoxnano-360m.sh,
      RUNNING.
    - ThoxNano-135M: job 6ae15d7a41e90535df76ddfc, t4-small,
      timeout 2h, label edge-thoxnano-135m, run_thoxnano-135m.sh,
      SCHEDULING.
  - Follow-up check edge-wave-check-20261027-7 created for
    2026-10-27 21:53 CT covering ONLY the two relaunched jobs. Its
    body carries the rule: if a relaunch fails again, diagnose and
    report, no second relaunch in that check.
  - Finishing step (GGUF via finish_edge_model.py on the fleet Windows workstation,
    factuality gate, model-card rewrites with real numbers,
    registry PR) has NOT run: gated on all five verified; currently
    3 of 5 (Flux + both Edge). Side-chat note above adds: published
    cards are stale (2026-10-23/24 status text + old safetensors
    SHA table) and in-repo GGUFs are still base repacks, so the
    card rewrite + GGUF regeneration must not be skipped.
  - Transport note: the Mac hf CLI was unusable this whole check —
    its venv Python lives on /Volumes/VibeStore and died at startup
    with getpath InterruptedError (EINTR) on every attempt, and
    ~/.cache is a symlink onto the same volume. Workarounds used
    (documented in check #7's body): public repo API from the VM;
    Jobs API + SSE logs via Mac /opt/homebrew/bin/python3.12 with
    the token read in-process from ~/.zshrc (never printed);
    upload + launches via Mac /usr/bin/python3 (huggingface_hub
    1.8.0) with HF_TOKEN exported from ~/.zshrc in-shell. SSH itself
    stayed up after one early connection reset; no /root/.ssh repair
    was needed (symlink already correct).

- Check #7 (edge-wave-check-20261027-7, 21:53-22:00 CT): BOTH relaunched
  Nano jobs COMPLETED and verified published. All five edge models now
  have verified trained weights + training_summary.json.
  - ThoxNano-360M: job 6ae15d7a41e90535df76ddfa COMPLETED (Jobs API:
    created 2026-10-28T02:27:06Z, started 02:27:18Z, finished
    02:30:50Z, running 211s, t4-small). ChatML fallback HELD:
    205/205 tokenized, 78/78 steps, logs loss 4.473 -> 2.307,
    train_loss 3.1241229619735327, ends "pushed merged weights +
    summary to Thox-ai/ThoxNano-360M". Repo verified: SFT commit
    cc59bb2cd699 02:30:40Z + Training summary d3b4cad3237a 02:30:42Z;
    model.safetensors 723,674,624 B; training_summary.json: base
    HuggingFaceTB/SmolLM-360M, train_rows 205, epochs 3.0, lr 0.0001,
    lora_r 32, training_loss 3.1241229619735327.
  - ThoxNano-135M: job 6ae15d7a41e90535df76ddfc COMPLETED (created
    02:27:06Z, started 02:29:07Z, finished 02:32:20Z, running 192s,
    t4-small). Logs loss 4.715 -> 2.452, train_loss
    3.273088284027882, ends "pushed merged weights + summary to
    Thox-ai/ThoxNano-135M". Repo verified: SFT commit bc30e4f05370
    02:32:13Z + Training summary d3f76c2a546c 02:32:15Z;
    model.safetensors 269,060,280 B; training_summary.json: base
    HuggingFaceTB/SmolLM-135M, 205 rows / 3 epochs / lr 1e-4 / r32,
    training_loss 3.273088284027882.
  - ALL FIVE VERIFIED COMPLETE: ThoxFlux-350M loss 3.463 (sha
    d0e42dd2, 00:55:59Z), ThoxEdge-0.8B loss 1.4541844832591522,
    ThoxEdge-0.5B loss 1.6802658240000408, ThoxNano-360M loss
    3.1241229619735327, ThoxNano-135M loss 3.273088284027882.
  - PARALLEL-LANE CARD ACTIVITY during this check window (verified
    via commits API, not done by this check): at 02:41Z all repos
    received card commits — ThoxNano-360M HEAD 47a8c6971e76
    "docs(card): trained-card rewrite with edge-wave results; fix
    dead license badge" (its README now correctly states trained
    weights, job 6ae15d7a, loss 3.124, evaluation pending, and GGUF
    still the base repack / finishing not run); ThoxEdge-0.8B HEAD
    1e5ca19db2cb, ThoxEdge-0.5B HEAD f6e44a2e120a, ThoxNano-135M HEAD
    c86b9f92ed0f are badge-fix-only commits — those three cards plus
    ThoxFlux-350M still carry the stale 2026-10-23/24 status text
    and old safetensors SHA-256 tables.
  - FINISHING STEP HAS NOT RUN in this check and remains open:
    (1) GGUF Q4_K_M regeneration via thoxllm-factory
    scripts/finish_edge_model.py on the fleet Windows workstation — every in-repo GGUF
    is still the 2026-08-11 base repack, NOT the fine-tune;
    (2) factuality gate — not run on any trained weight;
    (3) model-card rewrites with real numbers for Flux / Edge-0.8B /
    Edge-0.5B / Nano-135M (Nano-360M done by the parallel lane);
    (4) registry update PR — none verified.
    Why not run here: finishing is a separate the fleet Windows workstation execution
    stream, and a parallel lane was actively pushing card commits
    at 02:41Z in this same window; this check did not race it.
    When the finisher runs, its embedded HF token fallback in
    source must be flagged for scrubbing (value never printed).
  - No follow-up runonce check created: no jobs remain running.

---

## FINISHING CLOSEOUT — 2026-10-28 (Workstream A, run record: RUN.md (Wave A finishing record))

The finishing step HAS RUN. Conversion + gate + smoke on the fleet Mac workstation; HF uploads + Ollama pushes from the fleet Windows workstation.

- (1) GGUF Q4_K_M REGENERATED from the trained safetensors for all five (manual llama.cpp pipeline; finish_edge_model.py is broken against current Ollama's safetensors-only create-time quantization). Uploaded to the HF repos, replacing the 2026-08-11 base repacks; Hub blob SHA-256 verified equal to the conversion records:
  - ThoxFlux-350M: 229,309,120 B, sha 7526e4014ff8ed4e6707459c6b90bd862c2339ea4bbf4fce8e629f09c087f3fa
  - ThoxEdge-0.8B: 529,289,280 B, sha 3b375f2971342c2cfeb9b5c97b68db8b35cb915d044555bb784dfde69b19310e
  - ThoxEdge-0.5B: 397,805,088 B, sha 2192b7b4f2d19c25cad7ff386a9403e853638af54d7bf43917e977d3b6069438
  - ThoxNano-360M: 270,590,080 B, sha 18cb1f5e83ecabe8dbdfe7bd535aeb3c653014396cc567938a8ce370fc3800a4
  - ThoxNano-135M: 105,453,664 B, sha aff370028ff25d5dbcf8080be5008fecf393c6b4a4f513df7299f2e07e9fe9ad
- (2) FACTUALITY GATE RUN on all five (49 questions, weights only): Edge-0.5B FAIL 21/49 (2.837/5), Edge-0.8B FAIL 19/49 (2.714/5), Flux-350M FAIL 4/49 (0.898/5), Nano-135M FAIL 2/49 (0.816/5), Nano-360M ERROR (gate aborted twice, model repetition loop, no score). Results are stated on every model card; serving-side grounding is required for facts.
- (3) MODEL CARDS: Flux / Edge-0.8B / Edge-0.5B / Nano-135M rewritten with real training numbers, gate results, and provenance; Nano-360M's card updated in place (GGUF + gate sections). Repo HEADs after the run: Flux ccb2de2f, Edge-0.8B db4403d7, Edge-0.5B 66efd2c6, Nano-360M e88857b1, Nano-135M 8774ebf8.
- OLLAMA: all five published to ollama.com/Thox-ai as :q4_k_m + :latest from the fleet Windows workstation; registry manifests verified, model-layer digests equal the GGUF SHA-256s above. ThoxEdge-0.8B published for the first time.
- SMOKE (the fleet Mac workstation, "What are you?"): Edge-0.8B, Flux-350M, Edge-0.5B answer with the THOX identity skin; Nano-360M echoes its system text; Nano-135M deflects with a question.
- TOKEN FLAG RESOLVED: finish_edge_model.py on current thoxllm-factory main (7149aa0) is already env-only; repo-wide credential-literal scan found zero matches. No scrub was needed and no scrub commit exists.
- (4) Registry update PR: NOT done in this run (outside the finishing brief's steps).
- the fleet Windows workstation triage: root / 20 GB free at start; journal vacuum + dangling image/builder prune reclaimed ~1.2 GB; volumes untouched; root still 98% used, flagged.
