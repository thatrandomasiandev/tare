# Monday finish report — 2026-10-26 (CUT ~23:45 PT)

## 1. Paper changes (section by section, commits)

| Section | Change | Commit |
|---------|--------|--------|
| Anticipated objections (W12a) | Lead with expert trade-off: ~87% of expert speedup ($R_g{=}0.866$), `-Z` expertise, 68/227223 DIAMOND drops, Cadherin_5 / Gly-zipper_OmpA REFUSE E-values; rescale kept; InterProScan dropped from this para (still in Related Work table) | `5558637` |
| Beyond biology (Semgrep) | CUT disclosure: 13448662 failed pre-timing gate; cleaned-ruleset measured rerun **in progress**; no Semgrep speedup claimed | CUT fold (`this report`) |
| Baselines / shared contract | CUT disclosure: keep N1-only ρ(1)=1.474; ρ(5)/ρ(10) omitted; equal-footing $N{=}5$ arm **still running** | CUT fold (`this report`) |

No Semgrep measured fold (M not done). No ρ(5) fold (C r2 still running).

## 2. S — Semgrep final attempt

| Job | Role | Outcome |
|-----|------|---------|
| 13464943 / 13464944 | P/R first submit | CANCELLED (~10m; serial cleanup too slow) |
| **13465006** | P pre-flight | **PASS** (P1–P8); committed `f68cb95` |
| **13465007** | R rehearsal | **REHEARSAL_PASS**; committed `f68cb95` |
| **13471102** | M measured | **still RUNNING** ~2h15 / 8h at CUT (b22-01); left running |

**Verdict:** still running (M). Paper: labeled pilot + measured in progress; **no speedup claimed**.

## 3. C — shared contract N5

| Job | State at CUT |
|-----|----------------|
| A-N5 13447796 / A-rest 13447797 | COMPLETED |
| C N5 r0 13447416 | COMPLETED PASS |
| C N5 r1 13447417 | COMPLETED (04:18:28) |
| C N5 r2 13447418 | **RUNNING** ~2h15 / 8h (b22-04) — left running |
| C N10 r0 13447419 | COMPLETED (08:57:03) — not folded (wait for full N5 score first) |

- Lab ρ(5) r=1 only (status): 1.660 [0.964, 3.166] — **not paper**
- **Paper:** N1-only ρ(1)=1.474 [1.398, 1.549]; ρ(5)/ρ(10) omitted; sentence that $N{=}5$ arm is still running
- **Repeats scored for paper ρ(5):** none (need r0–r2 all scored under addenda)

## 4. H — new Anticipated objections paragraph (quoted)

> An expert shell script (changed families with `-Z`, then each protein's candidates) is TARE without gate/check/audit. On three of five locked genomes meeting the pre-registered speed-score rule, exclusive-node EPYC 7542 timing gives median $S_g^{tare}=5.32$ (95% CI $[5.02, 5.35]$) and $S_g^{expert}=5.96$ (CI $[5.55, 6.17]$), so TARE reaches about 87% of that speedup ($R_g=0.866$, CI $[0.842, 0.959]$; $n{=}3$, seed 20261249)—`inconclusive`, not the locked five. The script needs per-tool expertise (HMMER E-values depend on database size, hence `-Z`) that TARE derives by probing, and silently drops 68 of 227,223 DIAMOND hits; two genomes REFUSEd on non-unique keys Cadherin_5 ($2.2\times10^{-11}$) and Gly-zipper_OmpA ($1.2\times10^{-6}$). Rescaling cached E-values matched only 58.0% of 44,132 HMMER hit lines (Wilson 95% CI 57.5--58.5%).

## 5. Gates at CUT

| Gate | Result |
|------|--------|
| `python3 -m artifact.check_paper_sources` | **0 mismatches** |
| `main.pdf` (OSDI/PARE) | **13 pp** |
| `arxiv.pdf` | **13 pp** |
| Anonymity | **OK** |
| `pytest -q tests` | **411 passed, 2 skipped** (exit 0; was 412/1 Sunday) |
| PENDING/TODO/?? in PDFs | **none** |

Paths:
- `pipeline/paper/tare/main.pdf`
- `pipeline/paper/tare/arxiv.pdf`
- `pipeline/paper/tare/TARE-paper-current.pdf`
- `/Users/joshuaterranova/Desktop/CSCI270/TARE-paper-changes-monday.pdf` (latexdiff vs `667ad04`, green adds, `--no-del`)

## 6. Jobs still running (leave alone; tomorrow)

| Job | Next |
|-----|------|
| **13471102** Semgrep M | Collect/score when COMPLETED; fold Beyond-biology only on PASS + verified JSON; else limitation |
| **13447418** C N5 r2 | When done, score all N5 r0–r2 under addenda; fold ρ(5) only if complete; N10 JSON already on CARC stage |

Never touch 12864756; never score 13447415.

## 7. Five lines for Prof. Zhang

1. Monday CUT: paper still headlines **4.24×** / **3.49×** on nine genomes, byte-identical.
2. Expert-script baseline rewritten to lead with the trade-off (~87% of expert speedup on three scored genomes; inconclusive).
3. Semgrep pre-flight and rehearsal passed; the exclusive measured run is still going—no Semgrep speedup in the paper.
4. Shared-contract paper stays at ρ(1)=1.47; the N=5 arm has two of three repeats done and one still running.
5. PDFs and a green latexdiff vs Saturday baseline are on disk; remaining jobs left running for Tuesday collection.
