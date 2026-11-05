"""Build the First Device Models Third Edition companion demo:
a GATE49 wave explorer (Wave A vs Wave B, verified recall primary).

Single self-contained HTML. Data comes from exp/results/summary.json
plus the one per-question record that survives — the constant
abstainer's report in the public supplement. The Wave A/B model runs'
per-question outputs were not retained (paper section 10.6); the demo
shows totals, splits, and means for them and says so, rather than
reconstructing grids that do not exist.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S = json.loads((ROOT / "exp" / "results" / "summary.json").read_text(encoding="utf-8"))
ABST = json.loads((ROOT / "exp" / "waves-ab-supplement" / "gate-outputs" / "constant-abstainer" / "factuality-report.json").read_text(encoding="utf-8"))


def main() -> None:
    data = {
        "wave_a": S["wave_a"]["models"], "wave_b": S["wave_b"]["models"],
        "losses": S["wave_b"]["losses"], "wilson": S["wilson_95"],
        "abstainer": {"passed": S["constant_abstainer"]["passed"], "mean": S["constant_abstainer"]["mean"],
                      "hard": S["constant_abstainer"]["hard_failures"], "splits": S["constant_abstainer"]["splits"],
                      "verdicts": [{"id": v["id"], "cat": v["category"], "passed": bool(v["passed"]),
                                    "score": v["score"], "hard": bool(v["hard_failure"])} for v in ABST["verdicts"]]},
        "pilot": S["pilot_lfm3_voice"],
    }
    demo = HTML.replace("/*__DATA__*/", json.dumps(data))
    out = ROOT / "dist" / "FirstDeviceModels_Demo_v3.0.html"
    out.write_text(demo, encoding="utf-8")
    print("wrote", out, len(demo), "bytes")


HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GATE49 Wave Explorer — First Device Models (THOX Whitepaper, Third Edition)</title>
<meta name="description" content="Interactive explorer for the First Device Models whitepaper: Wave A vs Wave B GATE49 results with verified recall primary, the constant-abstainer floor with its preserved per-question record, and the voice pilot result. Rendered client-side from the paper's evidence bundle (summary.json).">
<style>
:root{--bg:#FFFFFF;--fg:#111827;--muted:#6B7280;--rule:#E5E7EB;--card:#F9FAFB;--green:#047C3D;--green-ink:#047C3D;--pale:#E6F4EC;--bad:#B91C1C;--amber:#B45309;--mono:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,monospace;--sans:Inter,system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0B0F14;--fg:#F3F4F6;--muted:#9CA3AF;--rule:#1F2937;--card:#111827;--green:#05A451;--green-ink:#05A451;--pale:#0F2A1B;--bad:#F87171;--amber:#FBBF24}}
:root[data-theme="dark"]{--bg:#0B0F14;--fg:#F3F4F6;--muted:#9CA3AF;--rule:#1F2937;--card:#111827;--green:#05A451;--green-ink:#05A451;--pale:#0F2A1B;--bad:#F87171;--amber:#FBBF24}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--sans);line-height:1.5;font-size:15px}
.wrap{max-width:960px;margin:0 auto;padding:24px 16px 48px}
header{border-bottom:2px solid var(--green);padding-bottom:10px;margin-bottom:18px}
.eyebrow{font-family:var(--mono);font-size:11px;color:var(--green);text-transform:uppercase;letter-spacing:.08em}
h1{font-size:24px;margin:6px 0 4px;line-height:1.2}
h2{font-size:18px;margin:26px 0 8px;border-bottom:1px solid var(--rule);padding-bottom:4px}
p{margin:0 0 10px}
.note{font-size:13px;color:var(--muted)}
.card{background:var(--card);border:1px solid var(--rule);border-radius:8px;padding:14px;margin:10px 0}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin:10px 0}
.kpi{border:1px solid var(--rule);border-top:3px solid var(--green);border-radius:6px;padding:10px;background:var(--card)}
.kv{font-family:var(--mono);font-size:22px;font-weight:700;color:var(--green-ink)}
.kl{font-size:12px;color:var(--muted);margin-top:3px}
.kt{font-family:var(--mono);font-size:10px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-top:6px}
.mgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:10px;margin:10px 0}
.mcard{border:1px solid var(--rule);border-radius:8px;padding:12px;background:var(--card)}
.mcard h3{margin:0 0 6px;font-size:15px}
.vr{font-family:var(--mono);font-size:26px;font-weight:700;color:var(--green-ink)}
.bar{height:8px;background:var(--rule);border-radius:4px;overflow:hidden;margin:5px 0}
.bar>i{display:block;height:100%;background:var(--green)}
.bar.b>i{background:#9CA3AF}
.rm{font-size:12px;color:var(--muted)}
.catbar{display:flex;height:10px;border-radius:4px;overflow:hidden;margin:4px 0;border:1px solid var(--rule)}
.catbar>i{display:block;height:100%}
.qgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(30px,1fr));gap:4px;margin:10px 0}
.q{aspect-ratio:1;border-radius:4px;border:1px solid var(--rule);font-family:var(--mono);font-size:9px;display:flex;align-items:center;justify-content:center;cursor:pointer;color:var(--fg);background:var(--card);padding:0}
.q.pass{background:var(--pale);border-color:var(--green)}
.q.hard{background:#FEE2E2;border-color:var(--bad);color:var(--bad);font-weight:700}
.q.fail{background:var(--card);color:var(--muted)}
.out{font-family:var(--mono);font-size:12.5px;white-space:pre-wrap;word-break:break-word;background:var(--bg);border:1px solid var(--rule);border-radius:6px;padding:10px;margin:8px 0 0;overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:13px;margin:8px 0}
th,td{text-align:left;padding:5px 6px;border-bottom:1px solid var(--rule)}
th{color:var(--muted);font-weight:600}
footer{margin-top:30px;font-size:12px;color:var(--muted);border-top:1px solid var(--rule);padding-top:10px}
.theme{float:right;font-size:12px;background:transparent;color:var(--muted);border:1px solid var(--rule);padding:4px 8px;margin:0;cursor:pointer}
.invalid{color:var(--bad);font-weight:600}
</style>
</head>
<body>
<div class="wrap">
<header>
  <button class="theme" id="themeBtn" type="button">Theme: auto</button>
  <div class="eyebrow">THOX.ai Research &middot; companion demo to the Third Edition</div>
  <h1>GATE49 wave explorer: the first device models, Wave A vs Wave B</h1>
  <p class="note">Every number is rendered in your browser from the paper's evidence bundle (<b>exp/results/summary.json</b>). GATE49 is the fleet's 49-question factuality gate (verified 12 / unknown 26 / known_false 10 / pricing 1). Because 37 of its 49 items are refusal-rewarded by design, the paper's primary factuality figure is <b>verified recall (of 12)</b>; the 49-question total measures abstention discipline plus verified recall. <b>Every verdict in both waves is FAIL</b> under the gate's zero-hard-failure policy — the totals are scores, not passes. Wave A ran on a 205-row corpus, weights only; Wave B on a 982-row corpus, under changed conditions the paper tables in full (section 11.4), so A→B is an observed delta, not an ablation. No model in these waves has been qualified on physical device hardware.</p>
</header>

<h2>The headline comparison</h2>
<div class="kpis" id="kpis"></div>

<h2>Model by model</h2>
<div class="mgrid" id="models"></div>

<h2>The floor: the constant abstainer, per question</h2>
<p class="note">A responder that declines every question in the facts card's prescribed form scores 25/49 with zero hard failures — the floor every total is read against. This run's per-question report is the one complete per-question record preserved from these waves (public supplement); the Wave A/B model runs' per-question outputs were not retained on the run hosts (paper section 10.6) and are not reconstructed here or anywhere.</p>
<div class="card" id="abstCard"></div>

<h2>Program 1: the voice command pilot</h2>
<div class="card" id="pilot"></div>

<footer>
Evidence classes: gate results and the abstainer run are MEASURED (run records S8/S9 and the supplement report); Wilson intervals in the paper are CALCULATED; the section 3.5 flavor prices are REPORTED (HF Jobs public price list). Demo data: exp/results/summary.json in the artifact bundle for "First Device Models, Trained In-House" (Third Edition).<br>
Your AI. Your Data. Your Rules.&trade; &middot; THOX.ai LLC
</footer>
</div>
<script type="application/json" id="data">/*__DATA__*/</script>
<script>
const D = JSON.parse(document.getElementById('data').textContent);
const CATCOLORS = {verified:'#047C3D', unknown:'#6B7280', known_false:'#B91C1C', pricing:'#B45309'};
const $ = s => document.querySelector(s);
const MODELS = ['ThoxEdge-0.5B','ThoxEdge-0.8B','ThoxFlux-350M','ThoxNano-360M','ThoxNano-135M','ThoxClip-Qwen3-0.6B'];

$('#kpis').innerHTML = [
  ['47/49 · 11/12', 'ThoxEdge-0.5B Wave B total and verified recall (Wave A: 21/49) — the wave\'s best, still FAIL on one hard failure', 'Measured · GATE49'],
  ['25/49', 'Constant-abstainer floor: declining everything passes half the gate with zero hard failures', 'Measured · scorer run'],
  ['205 → 982 rows', 'Corpus growth Wave A to Wave B (838 newly authored + 144 retained after hygiene)', 'Calculated · construction record'],
  ['0/14 exact', 'Voice pilot held-out: 1/14 function names, 0/14 full exact matches — the pilot proved the rails, not the adapter', 'Measured · pilot artifact'],
].map(([v,l,t]) => `<div class="kpi"><div class="kv">${v}</div><div class="kl">${l}</div><div class="kt">${t}</div></div>`).join('');

function splitLine(splits) {
  if (!splits) return 'category splits not retained in the finishing record';
  return Object.entries(splits).map(([c,[p,t]]) => `${c} ${p}/${t}`).join(' · ');
}
function catBar(splits) {
  if (!splits) return '';
  const tot = Object.values(splits).reduce((a,[p,t]) => a + t, 0);
  return '<div class="catbar">' + Object.entries(splits).map(([c,[p,t]]) =>
    `<i style="width:${t/tot*100}%;background:${CATCOLORS[c]};opacity:${t ? (0.35 + 0.65*(p/t)) : 0.2}" title="${c}: ${p}/${t}"></i>`).join('') + '</div>';
}
function waveBlock(label, r, other) {
  if (!r) return '';
  if (r.verdict === 'ERROR') return `<div class="rm">${label}</div><div class="invalid">Gate ERROR — repetition loop, no score</div>`;
  if (r.verdict === 'INVALID MEASUREMENT') return `<div class="rm">${label}</div><div class="invalid">Invalid measurement — every answer empty (serving artifact); artifact held, never validly measured</div>`;
  const vr = r.splits ? `<div class="vr">${r.splits.verified[0]}/12 <span style="font-size:13px">verified recall</span></div>` : '';
  return `<div class="rm">${label} — total</div>
    <div class="bar${other?' b':''}"><i style="width:${r.passed/49*100}%"></i></div>
    <div><b>${r.passed}/49</b> · mean ${r.mean}/5${r.hard_failures != null ? ` · hard ${r.hard_failures}` : ''} · ${r.verdict}</div>
    ${vr}${catBar(r.splits)}<div class="rm">${splitLine(r.splits)}</div>`;
}
$('#models').innerHTML = MODELS.filter(m => D.wave_a[m] || D.wave_b[m]).map(m => {
  const a = D.wave_a[m], b = D.wave_b[m];
  const loss = D.losses[m] ? `<div class="rm">Wave B training loss ${D.losses[m]}</div>` : '';
  const dec = b && b.decision ? `<p class="rm" style="margin-top:6px"><b>Decision:</b> ${b.decision}</p>` : '';
  return `<div class="mcard"><h3>${m}</h3>${waveBlock('Wave A (205 rows)', a, true)}${waveBlock('Wave B (982 rows)', b, false)}${loss}${dec}</div>`;
}).join('');

const A = D.abstainer;
$('#abstCard').innerHTML = `<div class="vr">${A.passed}/49</div>
  <div>mean ${A.mean}/5 · hard failures ${A.hard} · verdict in report: PASS (as a responder; it is a floor, not a model)</div>
  ${catBar(Object.fromEntries(Object.entries(A.splits).map(([k,v]) => [k, v])))}
  <div class="rm">${splitLine(A.splits)}</div>
  <div class="qgrid">${A.verdicts.map((v,i) => `<button type="button" class="q ${v.passed?'pass':(v.hard?'hard':'fail')}" data-q="${i}" title="${v.id}">${i+1}</button>`).join('')}</div>
  <div class="out" id="qOut">Select a question cell for its record.</div>`;
$('#abstCard').querySelectorAll('.q').forEach(btn => btn.addEventListener('click', () => {
  const v = A.verdicts[+btn.dataset.q];
  $('#qOut').textContent = `${v.id}\ncategory: ${v.cat} · score: ${v.score}/5 · passed: ${v.passed} · hard failure: ${v.hard}`;
}));

const P = D.pilot;
$('#pilot').innerHTML = `<p><b>Base:</b> ${P.base}. <b>Seed:</b> ${P.seed.train_rows} train rows; held out ${P.seed.heldout_rows} (${P.seed.heldout_split}). <b>Launches:</b> ${P.launches_total}; the sixth completed and published to <span style="font-family:var(--mono)">${P.published_repo}</span>.</p>
<p><b>Held-out result:</b> function names correct ${P.final_launch.function_names_correct} · full exact matches ${P.final_launch.full_exact_matches} · train loss ${P.final_launch.train_loss} · JSON parse rate ${P.final_launch.json_parse_rate}.</p>
<p class="note">${P.reading}</p>`;

const themeBtn = $('#themeBtn');
const themes = ['auto','light','dark']; let ti = 0;
themeBtn.addEventListener('click', () => {
  ti = (ti + 1) % 3; const t = themes[ti];
  themeBtn.textContent = 'Theme: ' + t;
  if (t === 'auto') document.documentElement.removeAttribute('data-theme');
  else document.documentElement.setAttribute('data-theme', t);
});
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
