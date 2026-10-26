# W2 → hub: post-freeze shared-contract update (status-file only)

**Ask hub:** append the block below to `pipeline/docs/prompts/2026-10-26_status.md`
on **main**. Do **not** fold N5/N10 ρ into `pipeline/paper/tare/main.tex` until
Josh approves. Paper remains **N1-only**.

**Branch:** `exp/shared-contract`  
**Artifact:** `pipeline/results/shared_contract/measured_post_freeze.json`  
**Policy:** `pipeline/docs/SHARED_CONTRACT_POST_FREEZE_2026-10-25.md`

---

## Paste for `2026-10-26_status.md`

### Shared contract — post-freeze lab score (not paper)

- Exclusive A-N5 (13447796) + A-rest (13447797) COMPLETED; equal-footing
  EPYC 7542. Defective 13447415 never scored.
- Arm C N5 **r0** job **13447416** COMPLETED PASS (07:05:20 wall).
  r1 **13447417** / r2 **13447418** still pending at score time; N10 C
  **13447419** RUNNING — left running, not cancelled.
- **ρ(5) lab (r=1 disclosed):** point **1.660**, genome-bootstrap 95% CI
  **[0.964, 3.166]** (seed 20261342), **q = 1.0**, exactness all body-identical
  to exclusive stock.
  `% source: pipeline/results/shared_contract/measured_post_freeze.json scores.5.rho.point_rho=1.659865177255842 scores.5.rho.ci95 scores.5.q_mean=1.0 scores.5.exactness_all_ok=true scores.5.rho_replicates.n=1`
- Per-genome C walls (r0): stored first **11468.5 s**, then reused
  **3723.7 / 3515.7 / 2890.6 / 3897.1 s**; T_A sum **15360.1 s**, T_C sum
  **25495.7 s**.
  `% source: pipeline/results/shared_contract/arm_c_postfreeze/arm_c_N5_r0_13447416.json batch`
- **ρ(1) unchanged** (paper): mean **1.474**, CI **[1.398, 1.549]**, r=2 TIMEOUT.
  `% source: pipeline/results/shared_contract/measured.json scores.1` / `measured_N1.json`
- **ρ(10):** not scored (C N10 incomplete).
- **Non-claim:** these N5 numbers are post-freeze lab / status only; not the
  07:00 paper fold-in.

---

## Job table at score time

| Job | Role | State |
|-----|------|-------|
| 13447796 | Exclusive A-N5 | COMPLETED 0–4 |
| 13447797 | Exclusive A-rest | COMPLETED 0–4 |
| 13447416 | C N5 r0 | COMPLETED PASS |
| 13447417 | C N5 r1 | PENDING (Priority) |
| 13447418 | C N5 r2 | PENDING (Dependency) |
| 13447419 | C N10 r0 | RUNNING |
| 13447415 | Excluded A | never score |

## Commits (fill after push)

- Post-freeze score commit: **`69070ce2acf8bfccc2ca9010d2a9f1900a3e858e`**
