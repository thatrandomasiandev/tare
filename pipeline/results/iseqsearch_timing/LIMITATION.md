# W12b iSeqSearch timing — stated limitation (2026-10-24)

**Status:** second locked failure. No re-scoring. No third attempt.  
**Job:** `13347608` (confirm `13347607`).  
**Result file:** `pipeline/results/iseqsearch_timing/measured.json`  
**Verdict:** `FAIL_CONTROL` (`why`: a locked control failed).

## What the scorer vs TARE recorded

- Pre-registered control `controls.tare_refused` was **false** (scorer FAIL).
- In every timed TARE arm, the recorded decision was **`REFUSE`** with why  
  `out: row-key sets differ (...)`.
- `controls.tare_returned_stock` was **true** on every arm (stock-identical returned output).

Josh (2026-10-24): treat as a **stated limitation**. Leave `\ISeqSearchSpeedup` out of the paper. Keep the existing iSeqSearch **exactness** result (1.30% of shared lines byte-identical) unchanged.
