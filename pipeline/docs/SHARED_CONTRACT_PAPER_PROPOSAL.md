# Shared-contract paper proposal (W2) — Sunday freeze fold-in

**Status:** Honest fold-in after freeze **05:00 PT 2026-10-26**. Hub (W3)
integrates; this file does **not** edit `pipeline/paper/tare/main.tex`.

**Sources of truth:**
- `pipeline/results/shared_contract/measured.json` (`outcome=PARTIAL_FREEZE`)
- `pipeline/results/shared_contract/measured_N1.json`
- `pipeline/results/shared_contract/exclusive_arm_a_13447796/`
- `pipeline/docs/SUNDAY_FALLBACK_RULES_2026-10-25.md`
- `pipeline/docs/SHARED_CONTRACT_MEASURED_ADDENDUM_2026-10-25b.md`

## Freeze / fallback (disclosed)

| Item | At freeze | Scored into headline ρ? |
|------|-----------|-------------------------|
| N=1 (job 13383296) | COMPLETED r=2 TIMEOUT | **Yes** |
| Exclusive arm A N5 (13447796 tasks 0–4) | COMPLETED (5/5 genomes) | Walls recorded; **no ρ** (no C) |
| Arm C N5 (13447416–18) | 0 COMPLETED repeats (PENDING) | **No** |
| Exclusive A-rest (13447797) | PENDING | **No** |
| Arm C N10 (13447419) | PENDING | **No** |
| Defective non-exclusive A (13447415) | EXCLUDED / quarantined | **Never** |

Fallback applied: report **N1 only** for ρ; omit ρ(5) and ρ(10); exclusive
A-N5 walls kept for provenance and equal-footing readiness.

## Proposed paper sentences (every number has `% source:`)

### ρ(N)

1. On the locked measured draw (seed 20261341), shared-contract arm C vs stock
   arm A at **N=1** yields mean **ρ(1) = 1.474** with 95% bootstrap CI
   **[1.398, 1.549]** (seed 20261342, r=2 completed after TIMEOUT; do not
   impute a third replicate).
   `% source: pipeline/results/shared_contract/measured.json scores.1.rho.mean=1.473889341472594 scores.1.rho.ci95=[1.3983988740523141,1.5493798088928736] scores.1.rho.seed=20261342 n1.report_r=2 n1.outcome=TIMEOUT`

2. **ρ(5)** and **ρ(10)** are **not reported** at Sunday freeze: arm C had
   zero COMPLETED repeats by 05:00 PT, so equal-footing ρ = T_C/T_A cannot be
   formed. Exclusive arm-A stock for the N=5 prefix finished (array 13447796)
   and is held for a post-freeze C completion; it is not a headline ρ.
   `% source: pipeline/results/shared_contract/measured.json outcome=PARTIAL_FREEZE fallback_applied.rho_omitted_for=["5","10"] fallback_applied.n5_repeats_completed=0 freeze.jobs.arm_C_N5.completed_repeats=0 freeze.jobs.exclusive_A_N5.state`

3. Equal-footing exclusive arm-A walls for draws[0..4] (sum **15360.1 s**):
   GCF_002357915.1 **2309.4 s**; GCF_002953435.1 **3566.1 s**;
   GCF_010365405.1 **2295.6 s**; GCF_017900975.1 **3205.1 s**;
   GCF_019375055.2 **3984.0 s** (job 13447796, `--exclusive --mem=0
   --constraint=epyc-7542`).
   `% source: pipeline/results/shared_contract/measured.json exclusive_arm_a_n5_completed freeze.jobs.exclusive_A_N5.walls_s freeze.jobs.exclusive_A_N5.sum_wall_s=15360.079279713798`

### Reuse fraction q

4. At N=1, reuse fraction **q is undefined** (no genomes after the first to
   reuse a stored contract); measured batches record `q=null`.
   `% source: pipeline/results/shared_contract/measured_N1.json scores.1.q_mean=null scores.1.q_values=[]`

5. Laptop P2d realistic pilot (shape only, not CARC headline): after the first
   genome, **q = 1.0** (4/4 `contract_store: reused`) with CONFIRM_N=10.
   `% source: pipeline/results/shared_contract/p2d_realistic.json summary.q=1.0 summary.reused=4 confirm_n=10`

6. CARC measured **q(N=5)** / **q(N=10)** are **unavailable** at freeze (no
   arm-C completes). Do not substitute laptop q into CARC ρ claims.
   `% source: pipeline/results/shared_contract/measured.json fallback_applied.equal_footing_C_for_n5=false`

### Verification cost

7. On N=1 CARC measured, arm-C first-genome path stores the contract
   (`contract_store: stored`); `contract_confirm_wall_s` is null on both
   completed replicates (confirm wall is recorded on reuse, not on store).
   `% source: pipeline/results/shared_contract/measured_N1.json scores.1.confirm_wall_s_mean=null batches[*].arm_c[0].contract_store=stored batches[*].arm_c[0].contract_confirm_wall_s=null`

8. P2d laptop reuse confirms cost shape: mean confirm wall **≈15.5 s** on
   reused genomes (pilot scale; not CARC measured).
   `% source: pipeline/results/shared_contract/p2d_realistic.json cost_model.V / summary confirm walls ~15.5s`

### Shared vs per-genome; CONFIRM_N=10 safety

9. Shared contract store is **one store per (N, replicate) batch** across
   genomes; **per-genome pin check, neighbor/random pads (IC2), bounded
   audit, and per-genome row cache remain per genome** and are never shared
   across accessions. Default path without `--contract-store` stays (GATE R).
   `% source: pipeline/docs/SHARED_CONTRACT_MEASURED.md §What stays per genome; pipeline/results/shared_contract/p2d_gate_r.json`

10. **CONFIRM_N = 10** is the smallest n with all-available-genome
    self-consistency on full Pfam **and** poisoned-store fail **and**
    wrong-member fail (P2d recalibration). Production accept still uses
    full-table `verify_stored_fit`; reduced-n confirm is a cheap filter, not
    the sole safety gate.
    `% source: pipeline/results/shared_contract/p2d_confirm_n.json chosen=10 rule`

11. Safety claim for the paper: shared-contract reuse is kept safe because
    (a) each genome still runs its own pin check / IC2 / bounded audit, and
    (b) CONFIRM_N=10 caught poison and wrong-member in calibration while
    full-table verify remains the accept path — so a bad shared contract
    cannot silently ship.
    `% source: pipeline/results/shared_contract/p2d_confirm_n.json results[0].poison_caught=true results[0].wrong_member_caught=true; docs/SHARED_CONTRACT_MEASURED.md`

### Exactness (body-identical to stock)

12. For every completed N=1 arm-B and arm-C replicate (r=0,1), tbl and domtbl
    bodies are **byte-identical** to the paired stock arm-A bodies; all
    decisions SHIP.
    `% source: pipeline/results/shared_contract/measured_N1.json scores.1.exactness.all_body_identical_to_stock=true scores.1.exactness.all_ship=true`

13. No N≥5 arm-C exactness rows exist at freeze; do not claim multi-genome
    exactness from exclusive A stock alone.
    `% source: pipeline/results/shared_contract/measured.json fallback_applied.n5_repeats_completed=0`

### Arm B (first-run overhead)

14. Arm B (TARE without `--contract-store`) was measured on N=1 only: mean
    ρ_B/A = **1.731** (values 1.617, 1.844). Omitted for N≥5 per 2026-10-25
    addendum; first-run overhead bounded by N1 arm B + headline.
    `% source: pipeline/results/shared_contract/measured_N1.json arm_B_cost_measured.mean_rho_B_over_A=1.7305492771915243; measured.json arm_B_policy`

## Non-claims

- Do not claim CARC ρ(5), ρ(10), or CARC q(N>1) from this freeze fold-in.
- Do not use any 13447415 wall or quarantined `excluded_13447415/` artifact.
- Do not treat exclusive A-N5 walls as a speedup without matched exclusive C.
- Laptop P2d q and confirm walls are **pilot / shape**, not MEASURED CARC
  headline numbers.

## Hub integration notes

- Label every shipped number MEASURED vs PROJECTED/pilot.
- Prefer sentences 1, 9–12 for the shared-contract paragraph; put freeze
  disclosure (2, 6, 13) in a footnote or results caveat.
- Leave jobs 13447416–19 and 13447797 running for post-freeze collection;
  any later ρ must be a new dated addendum + re-score, not a silent edit.
