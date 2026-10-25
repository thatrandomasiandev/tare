# TARE progress report, Friday Oct 16 to Saturday Oct 24, 2026

Built from the commit history and the committed result files. **Measured** means a committed result from a real run;
**projected** means computed from a stated formula; **pilot** means a laptop or pre-measurement run used only to
decide what to run.

## Where the paper stood, and where it stands

| | Oct 16 | Oct 24 |
|---|---|---|
| Headline | Laptop and pilot numbers, no server headline | **Measured on a dedicated server:** 4.24× with the sampled audit (CI 4.17–4.68) and 3.49× under the bounded-audit default (CI 3.32–4.10), nine genomes, every update byte-identical |
| Exactness | Partial | **715,704 output lines** from HMMER and Infernal, zero differing |
| Safety | A sampled check without a stated bound | **A proven bound:** a hidden dependency affecting at least 1% of records ships with probability at most 5% (299 sampled records), backed by an adversarial study |
| Generality | HMMER, with Infernal in progress | HMMER and Infernal measured; DIAMOND and BLAST+ correctly refused; PROSITE inconclusive for power; **Semgrep (code security) working in pilot, measured run in progress** |
| Formal content | Rules scattered through the design section | **One formal model:** five coupling classes, an exactness proposition, the audit bound, the cost model |
| Comparisons | Mixed laptop and server numbers | **Matched Table 4** on one server and one workload |
| Impact | None | **Projected:** 143 vs 34 core-years per Pfam release across 544,814 RefSeq bacterial genomes |
| State | Two competing paper drafts | One paper, submission-ready structure, 12 pages, anonymous OSDI build plus a named arXiv build |

## Decisions, why, and impact on the paper

| Date | Decision | Why | Impact on the paper |
|---|---|---|---|
| 10-17 | Call the system **TARE**; tie every number in the paper to a result file, with a checker that verifies each value | One name; reviewers and readers can trace every claim, and the checker catches stale numbers | Every number is sourced; the checker has run clean at every step since |
| 10-17 | Key the cache on the program binary's content | A silently updated tool binary must never reuse old results | Removes a safety hole a reviewer would find |
| 10-17 | Pre-register the server headline before measuring | Test-design standard: decide the rules before seeing results | The headline is defensible as pre-registered |
| 10-17 | Fill the Infernal results (exact on ten genomes, about 2.1×) | A second biology tool family | Generality within biology |
| 10-18 | Run a full round of pre-registered experiments: diverse genomes, DIAMOND input order, BLAST+ pin, an adversarial grid, release chain, PROSITE (unrelated program), expert-script and rescaler baselines | Answer every reviewer question with data, including the ones that could hurt | Most of the evaluation section comes from this round |
| 10-19 | **Headline on the server: 4.24× over nine genomes**; one genome refused at its first run | First server-grade, pre-registered speedup | The paper's central number |
| 10-19 | Report diverse genomes honestly: 48 of 53 shipped exact, **0 unsafe**, 5 needless refusals (later fixed) | Shows behavior on unfamiliar genomes, including where it is conservative | Safety evidence on varied input |
| 10-19 | The adversarial grid showed the original check missed hidden dependencies; **make the bounded audit (299 records) the default** | A stated probability bound beats an unquantified check | Adds the safety guarantee, at the cost of speed (see 10-24) |
| 10-19 | Add the **break-even fallback**: run the tool in full when too much of the database changed | Some releases (Pfam 37.4 to 38.0, 93% changed) cannot pay off | The release-chain story ("38.0 is what the fallback is for") |
| 10-19 | BLAST+ does not ship; DIAMOND refuses because its filter reads neighboring entries | Report refusals as results, not hide them | Honest scope: the paper says which tools TARE refuses and why |
| 10-19 | **One paper:** archive the first paper and the CLAM draft | Two drafts were diverging | Single source of truth |
| 10-20 | Fold round-2 results in; pre-register the W13 re-time under the bounded audit | The headline must be measured with the default users get | Set up the 3.49× measurement |
| 10-20 | PROSITE fresh draw: 18 of 20 exact, **inconclusive for power**; no third redesign | Two locked attempts, so the rule says report and stop | A stated limitation, not a claim |
| 10-22 | Submission-ready structure: one-command finalize, PENDING guards, 12-page cut, anonymity scan, artifact export, anonymous name "PARE" for OSDI and "TARE" for arXiv | OSDI is double-blind; arXiv is allowed if the names differ | The paper cannot be submitted with a placeholder or a name in it |
| 10-23 | **Show the method outside biology.** Considered ClamAV; measured both; **chose Semgrep** | "General technique, not a HMMER trick" is the biggest gap for a systems venue. ClamAV's cost fits, but exactness cannot be tested without malware | Semgrep becomes the generality evidence (measured run in progress) |
| 10-23 | **Measure before building:** cost-shape test (Semgrep 97.6% rule-proportional, ClamAV 85.7%) | Amdahl first; my ClamAV prediction was wrong and the test caught it | The cost model predicts which tools benefit |
| 10-23 | Literature sweep across fields (Google Scholar Labs) | Check novelty and find the same problem elsewhere | Novelty holds; adds the cross-field paragraph (IR, proteomics, astronomy) |
| 10-23 | **Replace the unfair Table 4** with matched numbers from one server and one workload | The old table mixed laptop and server numbers | TARE's first run (4.20×) is honestly higher than INCR's (1.50×) on small inputs; the paper explains why |
| 10-23 | Build the **shared contract** to fix that first-run cost | Turn a reviewer's attack into a design contribution | Pending its measured run |
| 10-23 | Write the **formal core** | What reviewers remember; it fixed 8 imprecisions | New section; it replaced, not added, pages |
| 10-23 | Measure **impact at scale** from NCBI's RefSeq list | Make the importance obvious to non-experts | Projected 143 vs 34 core-years per release, with ranges |
| 10-23 | **No AI attribution** in commits or prompts | Josh's decision | Process only |
| 10-24 | Shared-contract no-go **diagnosed as a verification bug**, not a flaw in the idea; fixed: 100% reuse, projected 1.85× for 20 genomes | Every genome independently inferred the same contract that was being rejected | Pending its measured run |
| 10-24 | Semgrep refusals diagnosed: **timeouts** (nondeterministic, so refusing was correct) plus **a TARE bug**; after locking timeouts off and fixing the bug, updates ship exact | Correct refusal, then a real fix | Pending its measured run (container, since CARC's Linux is too old) |
| 10-24 | Move queued jobs to **`biyik_1173`** (PI approved) | Queue waits went from days to hours | Speeds up everything remaining; disclosed as an addendum |
| 10-24 | **W13: 3.49× under the bounded audit; state both speedups in the abstract** | 4.24× is the faster mode; 3.49× carries the safety guarantee; both are honest | The abstract tells readers exactly what each number buys |
| 10-24 | W12b (iSeqSearch timing) recorded as a **limitation** after its second locked failure | No third redesign | The stronger iSeqSearch exactness result (1.30% of lines identical) stays |
| 10-24 | **One place for the paper:** the main ACTS folder on `main` | Two locations caused confusion | Process only |

## Negative and honest results kept in the paper

- DIAMOND refuses (its filter reads neighboring entries); BLAST+ does not ship.
- TARE's first run costs 4.20× on a small input vs INCR's 1.50× (fix pending).
- Pfam 38.0 (93% changed) costs more than a full rerun without the fallback.
- The bounded audit costs about 18% of the speedup (3.49× vs 4.24×).
- PROSITE inconclusive for power; W12b timing comparison is a stated limitation.
- The scale projection's model error (26%) is reported as a range, not hidden.

## Open items and timeline

| Item | Status | Expected |
|---|---|---|
| W12a expert-script baseline | Running on CARC | Sunday morning |
| Shared contract measured run (1, 5, 20 genomes) | 1-genome batch running; others follow | Sunday to Monday |
| Semgrep measured run (container) | Image and smoke test in progress | Sunday to Monday |
| Fold both into the paper; coherence pass; outside reads | After the results | Monday to Tuesday |
| arXiv (named, TARE) | After the above | About Tuesday to Wednesday, Oct 27–28 |
| OSDI '27 (anonymous, PARE) | Abstract Dec 1, paper Dec 8 | About a month of buffer |
