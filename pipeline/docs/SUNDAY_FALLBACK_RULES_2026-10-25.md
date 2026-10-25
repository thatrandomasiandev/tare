# Sunday freeze / fallback rules — 2026-10-25

**Status:** PRE-REGISTERED. Committed before any new measured data from the
2026-10-25b exclusive arm-A re-run, Semgrep measured re-submit, or W12a
remainder collection is scored into paper numbers.

**Freeze time:** **05:00 PT Monday 2026-10-26.**

Whatever has **COMPLETED** by freeze is scored. Anything still running is
reported as not finished; its partial JSON is **not** used for headline
numbers.

## Shared contract

- **07:00 PT Monday deliverable:** paper uses **N1 only** (r=2 TIMEOUT,
  disclosed). Exclusive arm A jobs stay queued (do not cancel).
- **After 07:00:** when exclusive arm A and N5 arm C repeats complete,
  collect/score under the existing measured addenda and record a
  post-freeze update in `pipeline/docs/prompts/2026-10-26_status.md`.
  Fold into `main.tex` **only after Josh approves**.
- If fewer than 3 N5 repeats finish by that post-freeze collection: report
  the completed repeats (r = 1 or 2, disclosed).
- If N10 does not finish: report N5 (and N1) only in the post-freeze note.
- ρ needs exclusive arm A for the same genomes; else report the reuse
  fraction q and exactness only (no ρ). Arm-C mode does not record
  same-node timed stock (verified 2026-10-25 ~15:03 PT).
- Job array 13447415 and its quarantined artifacts are never scored
  (addendum 2026-10-25b).

## Semgrep

- If the measured run does not finish: the paper keeps the pilot (labeled
  pilot), the cost-shape result, and the determinism finding, and states the
  measured run as in progress / not completed.

## W12a

- Report the genomes completed (3, 4, or 5), disclosed.

## Paper

- No PENDING marker may remain after freeze fold-in.
- Every number that ships carries a `% source:` key to a committed file.
- MEASURED vs PROJECTED labeled.
