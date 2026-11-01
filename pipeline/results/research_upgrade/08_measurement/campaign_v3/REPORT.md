# Measured campaign v3 — official analysis

**Status:** `COMPLETE_CORRECT_CAMPAIGN` (validate_campaign_runs.py + analysis.py)  
**Validated UTC:** 2026-11-01 (CARC evidence under `research_upgrade_measured_20261030_r3`)  
**Policy:** `policy_all_records_bounded_s299`  
**Candidate:** `11cdda0821614b8e6c89f2ca4b61b78a8e38c150`

## Headlines (locked estimators)

| Quantity | Value |
|---|---|
| Headline \(S_g\) (median over non-FLAGGED) | **3.4718** |
| 95% genome-cluster bootstrap CI | **[3.2979, 3.8084]** |
| \(n\) unflagged / flagged | **8 / 1** |
| Flagged genome | `GCF_049949335.1` (A_stock repeat max/min 1.555) |
| Sensitivity (all 9) \(S_g\) | 3.4432 |
| Cost of checking C/B (non-FLAGGED) | **1.5768** |
| C/B sensitivity (all 9) | 1.5812 |
| Compared C body lines (tbl+dom) | 466,725 |

STOP-2 flag budget: 1 ≤ 2; no reruns.

## Jobs

`13622799 13627956 13627957 13627958 13627959 13627960 13627961 13630225 13634326`

## Artifacts

- `analysis_campaign.json` — locked analysis.py output  
- `normalized_campaign.json` — raw-validated cells + provenance  
- `analysis_for_macros.json` — analysis + cells/decision_counts for `fill_macros_new.py`  
- `macros_filled.tex` — 63/63 macros (also copied to `pipeline/paper/tare/macros_filled.tex`)  
- `results/GCF_*.json` — per-genome `result.json` copies  

CARC collection: `/project2/biyik_1165/jjt_373/csci270-star/research_upgrade_measured_20261030_r3/evidence/collected_runs_20261101T033007Z`  
CARC official analysis: `.../evidence/official_analysis_20261101T0335Z`

## Paper wiring

`main.tex` inputs `macros_filled.tex` and fills `\cref{tab:config}` all-record row. Abstract still leads with historical Bernoulli/bounded numbers — Josh owns any abstract prose rewrite.
