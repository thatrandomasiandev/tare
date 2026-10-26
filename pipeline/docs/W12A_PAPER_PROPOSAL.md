# W12a proposed paper sentences (for W4)

Branch `exp/w12a-expert-script`. Do **not** edit `pipeline/paper/tare/main.tex` here.
Hub (W4) integrates after verifying `% source:` keys against committed result files.

Protocol: `pipeline/docs/BASELINES_EXACT_PROTOCOL.md` (2026-10-19 pre-registration + 2026-10-25 TIMEOUT remainder addendum, sha `6933190`).
Merged file: `pipeline/results/baselines_exact/server.json` via `scripts/merge_w12a_server.py` (no re-timing; speed-score flags kept from each job).

## Disclosure (n genomes)

All five locked measured genomes are present. Under the pre-registration speed-score rule, **three** of five are speed-scored. File status is `inconclusive`; `locked_claim` is false; `walls_are_evidence` is false; `summary.not_the_locked_five` is true. Do not state a five-genome locked CARC claim.

Not speed-scored (TARE did not SHIP on every timed decision):

- `GCF_019969525.1` — duplicate row key `('WP_153681168.1', 'Cadherin_5', '2.2e-11')` (job `13347581`).
- `GCF_040271735.2` — duplicate row key `('WP_000726974.1', 'Gly-zipper_OmpA', '1.2e-06')` on untimed cache fill and all three timed TARE reps (job `13447212`).

Speed-scored: `GCF_018415995.1`, `GCF_037231045.1`, `GCF_055807995.1`.

## Proposed sentences

On the three genomes that met the pre-registered speed-score rule (every timed TARE decision SHIP, three positive walls per arm, stock-vs-stock body match, ≥1000 body lines), CARC exclusive EPYC 7542 timing gives median TARE speedup \(S_g^{\mathrm{tare}}=5.32\) (bootstrap 95% CI \([5.02, 5.35]\)) and median expert-script speedup \(S_g^{\mathrm{expert}}=5.96\) (CI \([5.55, 6.17]\)), with median ratio \(R_g=S_g^{\mathrm{tare}}/S_g^{\mathrm{expert}}=0.866\) (CI \([0.842, 0.959]\)); \(n=3\), bootstrap seed 20261249, not the locked five.

% source: pipeline/results/baselines_exact/server.json status = inconclusive
% source: pipeline/results/baselines_exact/server.json locked_claim = false
% source: pipeline/results/baselines_exact/server.json walls_are_evidence = false
% source: pipeline/results/baselines_exact/server.json genomes_speed_scored = 3
% source: pipeline/results/baselines_exact/server.json summary.n_scored = 3
% source: pipeline/results/baselines_exact/server.json summary.not_the_locked_five = true
% source: pipeline/results/baselines_exact/server.json summary.scored_genomes = ["GCF_018415995.1","GCF_037231045.1","GCF_055807995.1"]
% source: pipeline/results/baselines_exact/server.json summary.S_g_tare.median = 5.323566266485665
% source: pipeline/results/baselines_exact/server.json summary.S_g_tare.ci95 = [5.02079646876123, 5.3451058680848815]
% source: pipeline/results/baselines_exact/server.json summary.S_g_expert.median = 5.95976876651325
% source: pipeline/results/baselines_exact/server.json summary.S_g_expert.ci95 = [5.5514576356985135, 6.17426481667094]
% source: pipeline/results/baselines_exact/server.json summary.R_g.median = 0.8657072585634371
% source: pipeline/results/baselines_exact/server.json summary.R_g.ci95 = [0.8424481998315241, 0.9589492734759609]
% source: pipeline/results/baselines_exact/server.json merge.present_stems (n=5)

Two of the five locked genomes are not speed-scored because TARE REFUSEd on duplicate row keys (Cadherin_5 on `GCF_019969525.1`; Gly-zipper_OmpA on `GCF_040271735.2`), so this paper does not claim the pre-registered five-genome locked CARC result.

% source: pipeline/results/baselines_exact/server.json limitation
% source: pipeline/results/baselines_exact/server_partial_13347581.json proteomes[GCF_019969525.1].tare_ship = false
% source: pipeline/results/baselines_exact/server_remainder_g3.json proteomes[GCF_040271735.2].speed_scored = false
% source: pipeline/results/baselines_exact/server_remainder_g3.json untimed.cache_fill.decision = REFUSE

On each of the three speed-scored genomes, stock-vs-stock, TARE, and expert tbl/dom bodies are byte-identical under the pinned normalizer.

% source: pipeline/results/baselines_exact/server.json byte_identity.GCF_018415995.1
% source: pipeline/results/baselines_exact/server.json byte_identity.GCF_037231045.1
% source: pipeline/results/baselines_exact/server.json byte_identity.GCF_055807995.1

## Jobs (evidence chain)

| Piece | Job | Host | Role |
|---|---|---|---|
| Indices 0–2 | `13347581` TIMEOUT | b22-11 | `server_partial_13347581.json` |
| Index 3 | `13447212` COMPLETED | b22-21 | `server_remainder_g3.json` |
| Index 4 | `13447213` COMPLETED | b22-18 | `server_remainder_g4.json` |

Addendum for remainder: commit `6933190`. Do not touch SC job `13447796_1` or job `12864756`.
