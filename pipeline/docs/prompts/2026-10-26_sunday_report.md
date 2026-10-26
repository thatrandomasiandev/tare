# Sunday final report — 2026-10-26

**Written:** ~06:00 PT Monday (ahead of 06:30 slot; content frozen).  
**Paper tip at report:** `667ad04` (arXiv stamp). Hard deliverable window through 07:00 PT.  
**Fallback rules:** `pipeline/docs/SUNDAY_FALLBACK_RULES_2026-10-25.md` (applied at freeze ~04:55).

---

## 1. Per-workstream status

### W1 Semgrep (`exp/semgrep-domain`)

| Item | Value |
|------|-------|
| Status | **Fallback locked in paper** |
| Measured job | **13448662** RUNNING since 04:25:51 on b22-27 (6h limit); **not cancelled** |
| Prior jobs | 13447196 COMPLETED (determinism); 13415937 smoke PASS; 13415938 j32 FAIL; 13448640/13448642 cancelled |
| Never touch | **12864756** |
| Addenda / docs | `SEMGREP_PILOT.md`, `SEMGREP_PAPER_PROPOSAL.md`, `W1_NOTIFY_W4.md` |
| Result files | `semgrep_pilot.json`, `g1_laptop.json`, `semgrep_determinism_13447196.json`, `semgrep_j32_stock_diff.json`, smoke JSON |
| Paper | Labeled pilot; G1 cost-shape \(T(f)=4.3+171.3\cdot f\), 97.6% rule share; j32 nondeterminism lesson; `-j 16` lock; **measured not completed**; **no Semgrep speedup** |

### W2 Shared contract (`exp/shared-contract`)

| Item | Value |
|------|-------|
| Status | **N1-only in paper** (`PARTIAL_FREEZE`) |
| Measured merge | `pipeline/results/shared_contract/measured.json` |
| N1 source | `measured_N1.json` (job **13383296** TIMEOUT r=2/3) |
| Exclusive A-N5 | **13447796** tasks 0–4 **COMPLETED** (walls committed; **no ρ**) |
| Exclusive A-rest | **13447797** PENDING (~left running) |
| Arm C N5 | **13447416–18** PENDING |
| Arm C N10 | **13447419** PENDING |
| Excluded | **13447415** never scored |
| Notify / proposal | `W2_NOTIFY_W4.md`, `SHARED_CONTRACT_PAPER_PROPOSAL.md` (tip ~`8db7498` / pin `05a3d89`) |
| Paper ρ(1) | mean **1.474**, 95% CI **[1.398, 1.549]**, bootstrap seed **20261342**, r=2 TIMEOUT; exact SHIP |
| Not in paper | ρ(5), ρ(10), CARC q(N>1) — Josh lock until he OK |

### W3 W12a expert baseline (`exp/w12a-expert-script`)

| Item | Value |
|------|-------|
| Status | **Folded — 3/5 inconclusive** |
| Jobs | **13347581** TIMEOUT partial; rem **13447212** g3 + **13447213** g4 COMPLETED |
| Merge | `pipeline/results/baselines_exact/server.json` |
| Notify / proposal | `W3_NOTIFY_W4.md`, `W12A_PAPER_PROPOSAL.md` (`896c53e`) |
| Speed-scored | 3/5: `GCF_018415995.1`, `GCF_037231045.1`, `GCF_055807995.1` |
| Not scored | 2/5 REFUSE duplicate-key (`GCF_019969525.1`, `GCF_040271735.2`) |
| MEASURED | \(S_g^{\mathrm{tare}}=5.32\) [5.02, 5.35]; \(S_g^{\mathrm{expert}}=5.96\) [5.55, 6.17]; \(R_g=0.866\) [0.842, 0.959]; seed 20261249 |
| Flags | `status=inconclusive`, `locked_claim=false`, `not_the_locked_five=true` |

### W4 Paper (main)

| Milestone | Result |
|-----------|--------|
| Coherence | earlier (`1633ddc`) |
| W1 fold | ~15:39 Sun (Semgrep fallback text) |
| W3 fold | ~00:17–00:25 Mon (W12a 3/5) |
| Freeze | ~04:55 (`abdc436`) |
| W2 N1 fold | ~05:03–05:05 (`5a948f3`) |
| arXiv | ~05:55–05:56 (`667ad04`) |
| This report | `2026-10-26_sunday_report.md` |

---

## 2. What changed in the paper (exact)

1. **Beyond biology (Semgrep):** labeled pilot; cost-shape G1; stock-vs-stock j32 miss; determinism → `-j 16`; measured job cited as not completed; no speedup.
2. **Baselines / shared contract:** N1 measured ρ(1)=1.474 CI [1.398, 1.549] with `PARTIAL_FREEZE` disclosure; ρ(5)/ρ(10) omitted.
3. **Anticipated objections (W12a):** exclusive-node EPYC expert vs TARE on 3/5 speed-scored genomes; inconclusive / not locked five.
4. **Headlines unchanged:** 4.24× Bernoulli (CI 4.17–4.68) and 3.49× bounded s=299 (CI 3.32–4.10); nine genomes; byte-identical.

---

## 3. Gates (final recheck at report write)

| Gate | Result |
|------|--------|
| `python3 -m artifact.check_paper_sources` | **0 mismatches** (77 source comments) |
| `main.pdf` (OSDI / PARE) | **13 pp**; References start **p12** |
| Anonymity scan | **OK** |
| `pytest -q tests` | **412 passed, 1 skipped** |
| PENDING in PDF | **none** |
| `arxiv.pdf` | **13 pp** via `build_arxiv.sh` (TARE + `author_local.tex`) |
| `TARE-paper-current.pdf` | copied from `arxiv.pdf` (local; gitignored) |
| latexdiff vs `862b6dc` | `/Users/joshuaterranova/Desktop/CSCI270/TARE-paper-changes-since-sat.pdf` (green adds, `--no-del`) |

---

## 4. Jobs still running (leave alone)

| Job | Role | Action |
|-----|------|--------|
| **13448662** | Semgrep measured | Leave RUNNING; fold only if completes + verified JSON before/at post-07:00 hub decision |
| **13447797** | SC exclusive A-rest | Leave queued |
| **13447416–19** | SC arm C | Leave queued |
| **12864756** | — | **Never touch** |

Post-07:00: when A-rest/C complete, score under addenda → **status file only**; **no `main.tex` N5/N10 ρ** until Josh approves.

---

## 5. FOR JOSH (decisions only)

1. **Approve N5/N10 ρ paper fold?** After A-rest + C finish and W2 scores — yes/no (default: status-only).
2. **Semgrep measured 13448662:** when it finishes, fold into Beyond-biology or keep fallback forever for this arXiv cut?
3. **arXiv upload:** use local `pipeline/paper/tare/arxiv.pdf` (13 pp) when ready.

---

## 6. Five-line plain-English summary

1. Headlines stay **4.24×** and **3.49×** on nine genomes, byte-identical.  
2. Semgrep is in the paper as a labeled pilot + cost shape + determinism lesson; the big measured run is still going and is not claimed.  
3. Shared-contract speedup is **N=1 only** (ρ≈1.47); bigger-N results wait for your OK.  
4. Expert-script bake-off finished on **3 of 5** genomes (honest inconclusive), not a locked five-genome win.  
5. arXiv PDF and a green change-marked PDF are on disk; remaining cluster jobs were left running on purpose.
