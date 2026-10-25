# TARE progress report, Wednesday Oct 21 to Saturday Oct 24, 2026

Built from the commit history and the committed result files. **Measured** = a committed result from a real run;
**projected** = computed from a stated formula; **pilot** = a laptop run used only to decide what to run next.

## Where the paper stood on Wednesday, and where it stands now

| | Wednesday Oct 21 | Saturday Oct 24 |
|---|---|---|
| Headline | 4.24× (server, nine genomes) with the original sampled audit | **Both, in the abstract:** 4.24× with the sampled audit (CI 4.17–4.68) and **3.49× under the bounded-audit default** (CI 3.32–4.10), same nine genomes, every update byte-identical |
| Release chain | Pilot only | **Measured** across five Pfam releases: 2 of 3 genomes exact at every step, 1.66× and 1.71× total savings |
| Comparison with other caching tools | Table 4 mixed laptop and server numbers (unfair) | **Matched Table 4**, one server and one workload: INCR 1.50×, ProcessCache 14.49×, TARE 4.20× (first run), Riker blocked |
| Formal content | Rules scattered through the design section | **One formal model:** five coupling classes, an exactness proposition, the audit bound, the cost model |
| Generality | Biology only (HMMER, Infernal) | **Semgrep (code security) works in pilot**; measured run in progress |
| First-run cost | Not addressed | **Shared contract** built and fixed: 100% reuse in pilot, projected 1.85× for 20 genomes (from 4.20×); measured run in progress |
| Impact | None | **Projected:** 143 vs 34 core-years per Pfam release across 544,814 RefSeq bacterial genomes (ranges 105–324 vs 22–78) |
| Related work across fields | None | Cross-field paragraph: search engines, proteomics, astronomy |
| Submission readiness | One consolidated draft | Finalize command, PENDING guards, 12 pages, anonymity scan, artifact, "PARE" for OSDI and "TARE" with names for arXiv |

## Decisions, why, and impact on the paper

| Date | Decision | Why | Impact on the paper |
|---|---|---|---|
| 10-21 | Build slide-ready graphs and a 19-slide progress deck (plus a reusable 50-slide template) | Progress update for Professor Zhang | None directly; presentation material |
| 10-22 | **Submission-ready structure:** one-command finalize, placeholders that fail the checks, 12-page cut, anonymity scan, anonymous artifact, checklist | So the only thing left at the end is waiting for results | The paper cannot be submitted with a placeholder, a name or an over-length body |
| 10-22 | **arXiv as "TARE" with names; OSDI as "PARE", anonymous** | OSDI allows arXiv only if the system name differs | Two builds from one source |
| 10-22 | Share a stamped draft with Professor Zhang and an outside PhD student | Early outside reads | Feedback pending |
| 10-23 | **Show the method outside biology.** Considered ClamAV, measured both, **chose Semgrep** | "General technique, not a HMMER trick" is the biggest gap for a systems venue; ClamAV's exactness can't be tested without malware | Semgrep becomes the generality evidence (measured run in progress) |
| 10-23 | **Measure before building:** cost-shape test (Semgrep 97.6% rule-proportional, ClamAV 85.7%) | Amdahl first; my ClamAV prediction was wrong and the test caught it | The cost model predicts which tools benefit |
| 10-23 | Literature sweep across fields | Check novelty; find the same problem elsewhere | Novelty holds; cross-field paragraph added |
| 10-23 | **Replace the unfair Table 4** with matched numbers | The old table mixed machines and workloads | TARE's first run (4.20×) is honestly higher than INCR's (1.50×) on a small input; the paper explains why |
| 10-23 | Collect W8 and fix the collectors (a dropped trailing slash meant finished results never registered) | Without the fix, W8 and W13 would have read "still running" forever | Measured release chain in the paper |
| 10-23 | Build the **shared contract** to cut the first-run cost | Turn a reviewer's attack into a design contribution | Pending its measured run |
| 10-23 | Write the **formal core** | What reviewers remember; it fixed 8 imprecisions | New section, page-neutral |
| 10-23 | Measure **impact at scale** from NCBI's RefSeq list | Make the importance obvious to non-experts | Projected core-years with ranges |
| 10-23 | **No AI attribution** in commits or prompts | Josh's decision | Process only |
| 10-24 | Shared-contract no-go **diagnosed as a verification bug**; fixed: 100% reuse, projected 1.85× for 20 genomes | Every genome inferred the same contract that was being rejected | Pending its measured run |
| 10-24 | Semgrep refusals diagnosed: **timeouts** (nondeterministic, so refusing was correct) plus **a TARE bug**; after fixes, updates ship exact | Correct refusal, then a real fix | Pending its measured run (container, since CARC's Linux is too old) |
| 10-24 | Move queued jobs to **`biyik_1173`** (PI approved) | Queue waits went from days to hours | Speeds up everything remaining; disclosed as an addendum |
| 10-24 | **W13: 3.49× under the bounded audit; state both speedups in the abstract** | 4.24× is the faster mode; 3.49× carries the safety guarantee | The abstract says what each number buys |
| 10-24 | W12b recorded as a **limitation** after its second locked failure | No third redesign | The stronger iSeqSearch exactness result stays |
| 10-24 | **One place for the paper:** the main ACTS folder on `main`; ACTS-hub removed | Two locations caused confusion | Process only |

## Negative and honest results added since Wednesday

- TARE's first run costs 4.20× on a small input vs INCR's 1.50× (fix pending).
- The bounded audit costs about 18% of the speedup (3.49× vs 4.24×).
- Pfam 38.0 (93% changed) costs more than a full rerun without the fallback; one genome refused at its first run in the release chain.
- W12b timing comparison is a stated limitation.
- The scale projection's model error (26%) is shown as a range.

## Open items and timeline

| Item | Status | Expected |
|---|---|---|
| W12a expert-script baseline | Running on CARC | Sunday morning |
| Shared contract measured run (1, 5, 20 genomes) | 1-genome batch running | Sunday to Monday |
| Semgrep measured run (container) | Image and smoke test in progress | Sunday to Monday |
| Fold in, coherence pass, outside reads | After the results | Monday to Tuesday |
| arXiv (TARE, with names) | After the above | About Oct 27–28 |
| OSDI '27 (PARE, anonymous) | Abstract Dec 1, paper Dec 8 | About a month of buffer |
