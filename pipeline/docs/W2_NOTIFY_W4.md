# W2 → W4 notify (shared contract, Sunday freeze)

**From:** W2 shared-contract (`exp/shared-contract`)  
**To:** W4 (paper / hub consumers of shared-contract numbers)  
**Freeze:** 05:00 PT 2026-10-26  
**Branch tip at notify:** see `git rev-parse HEAD` after the commit that adds this file.

## Paths

| Artifact | Path |
|----------|------|
| Measured merge | `pipeline/results/shared_contract/measured.json` |
| N1 source | `pipeline/results/shared_contract/measured_N1.json` |
| Exclusive A-N5 walls | `pipeline/results/shared_contract/exclusive_arm_a_13447796/` |
| Paper sentences | `pipeline/docs/SHARED_CONTRACT_PAPER_PROPOSAL.md` |
| Equal-footing addendum | `pipeline/docs/SHARED_CONTRACT_MEASURED_ADDENDUM_2026-10-25b.md` |
| Fallback rules | `pipeline/docs/SUNDAY_FALLBACK_RULES_2026-10-25.md` |
| CONFIRM_N evidence | `pipeline/results/shared_contract/p2d_confirm_n.json` |

## Outcome at freeze

- `measured.json` **`outcome=PARTIAL_FREEZE`**
- Headline ρ available for **N=1 only** (mean 1.474, CI [1.398, 1.549], seed 20261342, r=2 TIMEOUT)
- Exclusive A-N5 (13447796) **COMPLETED** 5/5; walls committed under `exclusive_arm_a_13447796/`
- Arm C N5/N10 and A-rest: **not COMPLETED** by freeze → **no ρ(5), no ρ(10), no CARC q(N>1)**
- 13447415 remains EXCLUDED (never score)

## Job IDs (CARC)

| Role | Job | Freeze state |
|------|-----|--------------|
| Exclusive A-N5 | 13447796 | COMPLETED 0–4 |
| Exclusive A-rest | 13447797 | PENDING |
| C N5 r0/r1/r2 | 13447416 / 13447417 / 13447418 | PENDING |
| C N10 r0 | 13447419 | PENDING (Dependency) |
| Excluded A | 13447415 | CANCELLED / quarantined |

## SHAs to pin

- Pre-register / exclusive A submit: `33a95592e1005ca5a5d9730ed03c575b1030be09`
- This notify commit: `8db74987b8f56d17f39eea75fbd39e251b37bfc1` (notify pin `05a3d895c0b9a31aa198d57703e56b0e56b6b4b2`)

## Ask of W4

Use only `measured.json` + `SHARED_CONTRACT_PAPER_PROPOSAL.md` for shared-contract
claims. Do not invent ρ(5)/ρ(10). Leave live C/A-rest jobs alone unless hub
schedules a post-freeze addendum.
