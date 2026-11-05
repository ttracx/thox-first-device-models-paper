# Supplement manifest

Generated 2026-10-30 for the hardening revision (edition 2.1) of "First Device Models, Trained In-House". SHA-256 over file bytes.

| File | Bytes | SHA-256 |
|---|---:|---|
| `README.md` | 4029 | `c6e2b2fae0dbf20a399bda9712a8d32513932e3cc11caad8b8f5d8afb911880e` |
| `gate-outputs/constant-abstainer/answers.json` | 7209 | `3fc83256ed21ab2d7c5bee6074bd5f1d27e2a0fbf1889f23f75efa5b766a3c44` |
| `gate-outputs/constant-abstainer/factuality-report.json` | 19388 | `2b3ea527d9eb7defa004867914ce1c7e547c5c9a9913f8bd58acca6287838f46` |
| `gate-outputs/constant-abstainer/factuality-report.md` | 7195 | `00778cd1fcc469c56601d91b09021dac5c146891f9b38994710c954018f076b1` |
| `gate-outputs/constant-abstainer/transcript.json` | 7000 | `d9ec18a30f0282bb34d722817d7971151c52a05e6cd0c70f123927b660dc707f` |
| `gate49/VENDOR.md` | 9320 | `9e112ead6e3f5a8176eab262b655646680bcca35872161e317b7970edd3738ae` |
| `gate49/facts/__init__.py` | 2221 | `db0c5fdc0de38256a806bfd72f2ddfb11bb71988451fcaac293bcf717efc2dd6` |
| `gate49/facts/checker.py` | 13211 | `5bf88203a29bcd6b8f7670a6b282e5b0ecae7b163e25f929f22dc1cae116371d` |
| `gate49/facts/data/SOURCE.json` | 898 | `a1802fc8e4a07bb4c2a98e3bdb9543ff5b6643a9ab83ba96ccacca291ecf3b96` |
| `gate49/facts/data/THOX_FACTS.md` | 11643 | `2f5c2c68f7f4feda2a57fc1b2e78f3deb5b3aa68d23194332641a5fd0e93942a` |
| `gate49/facts/data/thox_facts.json` | 13586 | `635d81ba119089328aca60bab11b5285347f0a73fa81cda686ff5328a8a163c9` |
| `gate49/facts/dataset.py` | 23554 | `cf68d8a53be4db89ac097fbf06531e67e6a236c181f9cac2ba28b7c9385eb8dc` |
| `gate49/facts/errors.py` | 694 | `24b191feb5e5b0e05af29cd81267445e2ff16bfdc656f0682f32b51e3e12d988` |
| `gate49/facts/loader.py` | 11923 | `6803d6d65b6e00fe6add25507e0c1f05b8f7f953e7faac3a364d7dd070b3d9c5` |
| `gate49/facts/prompt.py` | 6175 | `7dfc447f49def61d3018f4c4d861391076cdd6129013b6ac5a113a5ed87ed477` |
| `gate49/facts/questions.py` | 41819 | `ee60ada3025ae79682a19801c67cab6d076376b6c7657871964977de8386a79a` |
| `gate49/facts/sync.py` | 11380 | `02302d15e598f7841b1fb9dc3423d2e64d76ab0aa989d6599c006d59e87e6203` |
| `gate49/factuality_gate49.py` | 14737 | `d980d460e0a152a4880ec5d86eae3c2dcbfee27a3bcde1ab2d02a59489d96815` |
| `gate49/grounding_system.txt` | 5032 | `fcd659858230c02b98be2396ea1f1edcc70fd4d04619ce8b6a75f85095c81862` |
| `gate49/probe_flagship.py` | 10954 | `632ad1fde6b422c9b8f2aaf21272b4ac8226e28b9e837f02afc30d134ce1e30d` |
| `gate49/run_gate49_job.py` | 13110 | `2f8990b191b5e7e20da2ff5a8850e1a6cd3af4b0ed8f1802dcd416b54daf8433` |
| `modelfiles/ThoxClip-Qwen3-0.6B.Modelfile` | 942 | `0b76e974370a7ff43b61c47d72b1863ea88da0a7cdc9e7ffebc5b39e71c00d62` |
| `modelfiles/ThoxEdge-0.5B.Modelfile` | 886 | `05b6db92cc0ad4cb34ae8cfec161b45dd2935ec8e226a50429f7eb8aeae9e071` |
| `modelfiles/ThoxEdge-0.8B.Modelfile` | 885 | `c7cac93fd8138a2b0d506e4de8a043842b3597162e9fe72fe6d9d41b3ef13499` |
| `modelfiles/ThoxFlux-350M.Modelfile` | 1133 | `64822ed10d1157cef2bb92dcb11f17630754a3a3f44171d55fac278ffbb71438` |
| `modelfiles/ThoxNano-135M.Modelfile` | 795 | `2d5037e6b5b54568cba8cf8636fe778767f5e12bfd0bc4ab783568d673793696` |
| `modelfiles/ThoxNano-360M.Modelfile` | 796 | `8ade1c900d338fa2c04a25045747772f7ef89c85074c25d4b3d0623f629a07e3` |

Provenance notes:

- `gate49/` files are byte copies of the control-plane vendored bundle (`(internal control-plane workdir)`), whose own `VENDOR.md` traces them to `ttracx/thoxllm-factory` and to the two control-plane repositories (commits `8b46f482facf4a22902f6cddfbba125b1c1a12d8` and `064f5729818f0a9680de86108c528d62aa69f34b`).
- `modelfiles/Thox*.Modelfile` for the five edge models were retrieved 2026-10-30 from `https://huggingface.co/Thox-ai/<repo>/resolve/main/Modelfile` (repository HEAD; the Modelfile in each repo was last changed by its finishing commit and was not touched by the Wave B republish commits).
- `modelfiles/ThoxClip-Qwen3-0.6B.Modelfile` is the Wave B finishing Modelfile from the program workdir (`the Wave B program record's Modelfile.thoxclip-qwen3-0.6b`).
- `gate-outputs/constant-abstainer/` was produced 2026-10-30 by running the bundled scorer in offline transcript mode; the run is described in the supplement README and in Section 11.4 of the paper.
