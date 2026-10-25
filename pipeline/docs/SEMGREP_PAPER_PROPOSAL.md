# Semgrep paper proposal (≤0.4 column) — W1 Sunday final

Hub-only integrate into `pipeline/paper/tare/main.tex`. Experiment branch does not edit `main.tex`.

**Measured status (freeze 05:00 PT Mon 2026-10-26):** exclusive resubmit **13448662** (`-j 16`, `r=2`) was PENDING at submit with `sbatch --test-only` start ≈ **2026-10-26T22:09** PT — after freeze. Locked fallback: paper keeps **pilot (labeled)**, **cost-shape**, **determinism**; measured = **not completed**.

---

## Proposed sentences (with `% source:`)

Semgrep’s wall time is overwhelmingly rule-proportional: a laptop cost-shape fit gives \(T(f)=4.3+171.3\cdot f\) s with **97.6%** of full-scan cost in the rule term (`a_share=0.9756`).
% source: pipeline/results/nonbio/g1_laptop.json (semgrep.fit.a_share, a_s, c_s); pipeline/docs/SEMGREP_G2_DESIGN.md

On a laptop pilot (labeled, not CARC measured), after locking `--timeout 0`, release-pair updates **SHIP** with output equal to stock except the declared volatile JSON field `time`; default timeouts had previously produced rule×file `Timeout` rows in top-level `errors` (C4).
% source: pipeline/results/nonbio/semgrep_pilot.json (w2_overnight); pipeline/docs/SEMGREP_PILOT.md §Addendum 2026-10-24 (W2 overnight)

CARC smoke **13415937** (100-file subset) also **SHIP**ped stock-identical except `time` under the Apptainer wrapper for `semgrep/semgrep:1.182.1` (`sha256:451b3d875c00dac7ed5db5293e584a07de11449a409c10b3c2d2652f429630b6`).
% source: pipeline/results/nonbio/semgrep_smoke_13415937.json; pipeline/docs/SEMGREP_PILOT.md §Addendum 2026-10-24 (container)

Stock-vs-stock is the gate that catches Semgrep nondeterminism: measured **13415938** failed at `-j 32` (745 vs 746 findings); the sole differing finding was `identical-is-comparison` on `0809.py:651`.
% source: pipeline/results/nonbio/semgrep_j32_stock_diff.json; pipeline/results/nonbio/semgrep_measured_13415938.json

Determinism sweep **13447196** then showed all three stock runs identical except `time` at each of `-j ∈ {16,8,4,1}` (746 findings); the largest stable parallelism locked for resubmit is **`-j 16`**.
% source: pipeline/results/nonbio/semgrep_determinism_13447196.json; pipeline/docs/SEMGREP_PILOT.md §Addendum 2026-10-25

**Measured per-step speedups with CIs:** not available by freeze (job **13448662** not completed). Do not invent walls; if 13448662 finishes later, replace this clause from `pipeline/results/nonbio/semgrep_measured.json` only after hub verification.

---

## Non-claims

- No measured exclusive-node speedup claim until `semgrep_measured.json` exists with status SHIP.
- Smoke walls (subset, non-exclusive) are not speed evidence.
- G1 cost-shape is laptop shape only (`laptop_wall_is_speed_evidence: false` in g1 JSON).
