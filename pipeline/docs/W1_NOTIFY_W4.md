# W1 → W4 notify (Semgrep Sunday final)

Branch: `exp/semgrep-domain`  
Worktree: `/Users/joshuaterranova/Desktop/CSCI270/ACTS-semgrep`

## Freeze checkpoint (2026-10-26 ~05:00 PT)

**13448662** still **RUNNING** on `b22-27` (started 04:25:51; ~34 min elapsed; TimeLimit 6h). **Not cancelled.**  
Partial: stock-vs-stock **PASS** (746=746 at `-j 16`); errors-dependence in progress. Timed chain not started.

**For 07:00 paper:** keep locked **fallback** (labeled pilot + G1 cost-shape + `-j`/timeout determinism). Fold measured into proposal **only if** 13448662 finishes before 07:00 and scores SHIP; otherwise measured = not completed.

## Commits

| SHA | What |
|---|---|
| `f69ccdf4db2e49925fd3a7224382eba85677dd9f` | Lock `-j 16` addendum + determinism JSON from 13447196 |
| `63d8f55e1fb6481b2c6a9905c59709f4df9184ff` | Same addendum: `r=2` for freeze/queue |
| `5739134f2a79cfe47ef2cddebe31c932e724d7d2` | `SEMGREP_PAPER_PROPOSAL.md` + initial `W1_NOTIFY_W4.md` |
| `26c262c` | Point notify at live measured **13448662** |

## Jobs

| Job | Role | Outcome |
|---|---|---|
| 13415937 | smoke | PASSED (SHIP) |
| 13415938 | measured (`-j 32`) | FAILED stock-vs-stock (745 vs 746; `identical-is-comparison` @ `0809.py:651`) |
| 13447196 | determinism sweep | COMPLETED; all `-j` 16/8/4/1 identical except `time`; lock **16** |
| **13448662** | measured (`-j 16`, `r=2`, exclusive EPYC 7542) | **RUNNING** past freeze — leave running; fold if done by 07:00 |
| 13448640 / 13448642 | prior measured submits | **cancelled** — do not collect |
| 12864756 | — | **never touched** |

## Paths for W4 / hub

- Proposal: `pipeline/docs/SEMGREP_PAPER_PROPOSAL.md`
- Addendum: `pipeline/docs/SEMGREP_PILOT.md` (§Addendum 2026-10-25)
- Determinism: `pipeline/results/nonbio/semgrep_determinism_13447196.json`
- j32 miss: `pipeline/results/nonbio/semgrep_j32_stock_diff.json`
- Failed measured: `pipeline/results/nonbio/semgrep_measured_13415938.json`
- Smoke: `pipeline/results/nonbio/semgrep_smoke_13415937.json`
- Cost-shape G1: `pipeline/results/nonbio/g1_laptop.json` (on `main`; `a_share=0.9756`)
- Measured scored JSON: **pending** — `pipeline/results/nonbio/semgrep_measured.json` only after 13448662 COMPLETED + score

## Fallback (locked)

Freeze: paper keeps pilot (labeled), cost-shape, determinism finding; measured = not completed unless folded before 07:00 from a finished SHIP result.
