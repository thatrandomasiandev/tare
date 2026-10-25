# Sunday paper report — 2026-10-26

**Owner:** W4 (PAPER). Hub may finalize narrative; numbers below are from W4 commits.
**Deadline:** 06:30 PT Mon 2026-10-26.

## Status (close)

- Commits (paper, on `main`): see `git log --oneline c760eff^..HEAD` (mock-review fixes + fold-ins).
- Gates: check_paper_sources **0 mismatches**; `main.pdf` **13 pp**, refs on p13; anonymity **OK**; `pytest pipeline/tests` **412 passed, 1 skipped** (earlier this session).
- Remaining PENDING macros: **none** (`macros_pending.tex` = headline filled only).
- arXiv: `./build_arxiv.sh` **succeeds**; `arxiv.pdf` written. Reading copy: `TARE-paper-current.pdf` rebuilt with `\def\arxivbuild{1}` (named authors + TARE).
- `main` pushed.

## Waiting on W1 / W2 / W3

| Stream | Folded? | State |
|--------|---------|-------|
| W1 Semgrep | Yes (determinism finding) | Measured FAIL stock-vs-stock at `-j 32` (745 vs 746). No speedup claimed. Resubmit at `-j 1` still on W1. |
| W2 shared-contract | Partial | `measured_N1.json` TIMEOUT after r=2; ρ_C 1.55 / 1.40 (mean 1.47). N∈{5,20} still open. |
| W3 W12a | Stated limitation | Expert-script = laptop-only in Discussion; server partial not a locked ratio. |

## Mock-review fixes landed

| # | Commit theme |
|---|--------------|
| 1 | Cite 3.49× with s=299 guarantee (intro + conclusion) |
| 2 | Semgrep demote → Beyond biology subsection with measured FAIL |
| 3/13 | Table 4 first-run≠update + n=4 INCR CI note |
| 4 | ExpertScriptRatio → laptop-only stated limitation (no PENDING) |
| 5 | Audit does-not-cover plainbox |
| 6 | Infernal reduced-check plainbox |
| 7 | Decision-procedure line in Related Work |
| 8 | Design cut + drop unused PENDING macros |
| 9 | Scale (PROJECTED, not measured) |
| 10 | Red-team attack table |
| 12 | Intro worked pin `-Z 30134` / 3719 candidates |
| 15 | Amdahl gap at fΔ named as heavier audit |

Also: W12b / WA2 stated limitations (no PENDING); `build_arxiv.sh` false-positive fix.

## Hub notes

- Do **not** commit Josh's `tools/carc-gpu-dashboard/` dirty files.
- Orchestrator may extend this report; keep `% source:` keys verified against JSON on `main`.
