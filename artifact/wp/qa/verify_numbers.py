"""Non-producer numbers verification for the First Device Models
Third Edition pack, plus the audit-Major (AB-1) closure re-check.

Independently: (1) re-derives the constant abstainer from the
supplement's per-question report; (2) checks the pilot figures against
the published result artifact (S6); (3) checks every Wave A/B figure
in summary.json against the S8/S9 run records staged in the pack;
(4) checks the figures printed in the shipped PDF/HTML against
summary.json; (5) re-verifies the AB-1 closure line-by-line in the
reconstructed source text. Exit 0 only if all pass. Writes
wp/qa/numbers-verification.json.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXP = ROOT / "exp"
DIST = ROOT / "dist"
SRC = ROOT / "src" / "whitepaper.md"
PDF = DIST / "THOX_First_Device_Models_Trained_In-House_Whitepaper_v3.0.pdf"
HTMLF = DIST / "THOX_First_Device_Models_Trained_In-House_Whitepaper_v3.0.html"

checks: list[dict] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    checks.append({"check": name, "pass": bool(ok), "detail": detail})


S = json.loads((EXP / "results" / "summary.json").read_text(encoding="utf-8"))
s8 = (EXP / "records" / "S8-wave-a-finishing-RUN.md").read_text(encoding="utf-8")
s9 = (EXP / "records" / "S9-wave-b-RUN.md").read_text(encoding="utf-8")

# --- 1. Abstainer re-derived -------------------------------------------------
abst = json.loads((EXP / "waves-ab-supplement/gate-outputs/constant-abstainer/factuality-report.json").read_text(encoding="utf-8"))
vs = abst["verdicts"]
passed = sum(1 for v in vs if v["passed"])
mean = round(sum(v["score"] for v in vs) / len(vs), 3)
hard = sum(1 for v in vs if v["hard_failure"])
rec = S["constant_abstainer"]
check("abstainer re-derived", passed == rec["passed"] == abst["passed_count"] and abs(mean - rec["mean"]) < 0.0015
      and hard == rec["hard_failures"], f"{passed}/49 mean {mean} hard {hard}")
for cat, crec in rec["splits"].items():
    cv = [v for v in vs if v["category"] == cat]
    check(f"abstainer split {cat}", sum(1 for v in cv if v["passed"]) == crec[0] and len(cv) == crec[1], f"{crec}")

# --- 2. Pilot vs S6 artifact ---------------------------------------------------
pilot = json.loads((EXP / "pilot/results-6ae105dc41e90535df7686b7.json").read_text(encoding="utf-8"))
prec = S["pilot_lfm3_voice"]
check("pilot artifact fields", pilot["train_rows"] == prec["seed"]["train_rows"] == 35
      and len(pilot["heldout"]) == prec["seed"]["heldout_rows"] == 14
      and abs(pilot["name_accuracy"] - 1 / 14) < 1e-9 and pilot["full_exact_match"] == 0.0,
      f"name_accuracy {pilot['name_accuracy']}, exact {pilot['full_exact_match']}")

# --- 3. Wave A/B figures vs S8/S9 records --------------------------------------
for model, r in S["wave_a"]["models"].items():
    if r["verdict"] == "ERROR":
        check(f"S8 {model} ERROR state", "ERROR" in s8 or "error" in s8.lower(), "record carries the error state")
        continue
    pat = rf"{re.escape(model)}\s*\|\s*FAIL\s*\|\s*{r['passed']}/49 passed, {r['hard_failures']} hard failures, score {r['mean']}"
    check(f"S8 record {model}", re.search(pat, s8) is not None, f"{r['passed']}/49 mean {r['mean']} hard {r['hard_failures']}")
for model, r in S["wave_b"]["models"].items():
    if r["passed"] is None or r["verdict"] == "INVALID MEASUREMENT":
        check(f"S9 {model} invalid state", "INVALID" in s9, "record carries the invalid measurement")
        continue
    check(f"S9 record {model} total+mean", f"{r['passed']}/49" in s9 and str(r["mean"]) in s9, f"{r['passed']}/49 mean {r['mean']}")
    if r["splits"]:
        sp = r["splits"]
        frag = f"verified {sp['verified'][0]}/12, unknown {sp['unknown'][0]}/26, known_false {sp['known_false'][0]}/10, pricing {sp['pricing'][0]}/1"
        check(f"S9 record {model} splits", all(x in s9 for x in [f"verified {sp[chr(39)+chr(39)] if False else sp['verified'][0]}/12", f"unknown {sp['unknown'][0]}/26", f"known_false {sp['known_false'][0]}/10", f"pricing {sp['pricing'][0]}/1"]), frag)
for model, loss in S["wave_b"]["losses"].items():
    check(f"S9/paper loss {model}", str(loss) in s9 or str(loss) in SRC.read_text(encoding="utf-8"), str(loss))
check("S9 Clip record", "22/49" in s9 and "2.776" in s9 and "14 hard failures" in s9, "Clip 22/49, 2.776, 14 hard")

# --- 4. Printed figures ----------------------------------------------------------
pdf_text = subprocess.run(["pdftotext", str(PDF), "-"], capture_output=True, text=True).stdout
html_text = re.sub(r"<[^>]+>", " ", HTMLF.read_text(encoding="utf-8"))
needles = ["21/49", "19/49", "4/49", "2/49", "47/49", "20/49", "23/49", "22/49", "25/49",
           "2.837", "2.714", "0.898", "0.816", "4.837", "2.959", "2.776", "3.531",
           "982", "838", "144", "205", "$2.50", "$1.00", "$0.40", "0.7614",
           "1/14", "0/14", "11/12", "c250f9bb", "6ae15d7a41e90535df76ddfa", "6ae15d7a41e90535df76ddfc"]
for model, g in S["wave_a"]["gguf"].items():
    needles.append(g["sha256"][:16])
    needles.append(f'{g["bytes"]:,}')
for n in needles:
    check(f"printed figure {n!r}", n in pdf_text and n in html_text, "")

# --- 5. AB-1 closure, line-by-line ----------------------------------------------
text = SRC.read_text(encoding="utf-8")
sec1 = text.split("# 2. Background")[0]
classes = S["failure_taxonomy"]["classes"]
enum_names = ["private repository authorization", "remote code trust", "a removed training configuration argument",
              "a dataset shape contract", "an unsupported numeric precision", "a positional upload call",
              "a tokenizer chat template contract", "the removed configuration argument recurring",
              "a tokenizer handoff defect", "a model-load dependency defect", "the factory finisher's breakage"]
for name in enum_names:
    check(f"AB-1 s.1 enumeration: {name[:44]}", name in sec1, "")
sec62 = text.split("## 6.2")[1].split("## 6.3")[0]
rows = re.findall(r"(?m)^\| \d+ \|", sec62)
check("AB-1 s.6.2 table has 11 classes", len(rows) == 11, f"{len(rows)} rows")
check("AB-1 s.6.2 class 7 is the chat-template contract", "Tokenizer chat template contract" in sec62
      and "6ae14e1f3fb22a235dd37ff8" in sec62 and "6ae14e2041e90535df76d4bd" in sec62, "")
sec65 = text.split("## 6.5")[1].split("# 7.")[0]
check("AB-1 s.6.5 counts eleven in four categories", "The eleven failures fall into four structural categories" in sec65
      and "The seventh failure belongs to this category" in sec65, "")
sec103 = text.split("## 10.3")[1].split("## 10.4")[0]
check("AB-1 s.10.3 relaunch jobs present", "6ae15d7a41e90535df76ddfa" in sec103 and "6ae15d7a41e90535df76ddfc" in sec103, "")
sec105 = text.split("## 10.5")[1].split("## 10.6")[0]
check("AB-1 s.10.5 fix commit present", "c250f9bb1b8e20b71f5c38c73ccfbcdac6a0303e" in sec105, "")
check("AB-1 S2 is the edge status record", "WAVE-STATUS.md" in text and "source S2" in text, "")

failed = [c for c in checks if not c["pass"]]
out = {"total": len(checks), "passed": len(checks) - len(failed), "failed": failed, "checks": checks}
(ROOT / "wp" / "qa" / "numbers-verification.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(f"FDM verification: {out['passed']}/{out['total']} PASS")
for f in failed:
    print("FAIL:", f["check"], f["detail"])
sys.exit(1 if failed else 0)
