# TARE lab UI: screens and CLI contract (draft, 2026-10-22)

Goal: a lab that annotates many genomes with HMMER + Pfam can move to a new Pfam release
without re-running everything, and can see why every genome was reused, re-run, or refused.

## Principles

1. **Thin layer.** The UI builds argv, calls `python3 -m acts run`, and reads what it writes.
   It never decides SHIP/REFUSE itself, so it can never disagree with the paper.
2. **Data stays where it is.** The UI points at paths on the lab's machine or cluster. No uploads.
3. **One workflow first.** v1 = `hmmscan` + Pfam, local runs and SLURM job scripts.
   Infernal + Rfam is the second preset; everything else waits.
4. **Explain every outcome.** A refusal with a plain reason builds trust; a silent full rerun does not.

## Screens

### 1. Projects (home)

```
┌ TARE ───────────────────────────────────────────────────────────────┐
│ Projects                                              [+ New project]│
│                                                                      │
│ Name               Tool + database        Genomes  Last release  Status │
│ Soil isolates      hmmscan · Pfam         212      38.0          ✔ up to date │
│ Gut MAGs batch 3   hmmscan · Pfam         1,048    37.4          ● 38.0 available │
│ Rfam pilot         cmscan · Rfam          40       15.0          ✖ 2 refused │
└──────────────────────────────────────────────────────────────────────┘
```

A project = a set of genomes + one fixed tool command + one cache. Changing the command
makes a new project (the cache namespace keys the argv and the program binary).

### 2. New project

```
┌ New project ─────────────────────────────────────────────────────────┐
│ Name            [ Gut MAGs batch 3                    ]              │
│ Genomes         [ /project/lab/mags/*.faa             ] [Browse] 1,048 found │
│ Tool preset     (•) HMMER hmmscan + Pfam   ( ) Infernal cmscan + Rfam │
│ Database        [ /db/pfam/37.4/Pfam-A.hmm            ]              │
│ Command         hmmscan --cut_ga --noali --cpu [4]                   │
│                   --tblout {output:tblout} --domtblout {output:domtblout} │
│                   -o /dev/null {reference} {input}        [Edit ▸]   │
│ Run on          (•) This machine   ( ) SLURM cluster → job script    │
│ Cache folder    [ /project/lab/tare-cache/gut-mags-3  ]              │
│                                                                      │
│ First run fills the cache: ≈1.3× the cost of a normal run, once.     │
│                                            [Cancel]  [Create + fill] │
└──────────────────────────────────────────────────────────────────────┘
```

### 3. Update preview (before anything runs)

```
┌ Update Gut MAGs batch 3: Pfam 37.4 → 38.0 ───────────────────────────┐
│ Database change          new 412 · changed 1,206 · removed 38 · same 21,104 │
│ Changed fraction         6.9%      Full-rerun threshold  80% (break-even) │
│ Plan                     replay changed families only (all 1,048 genomes) │
│ Expected                 ≈4× faster than a full rerun · output identical │
│ Check on every genome    audit of 299 records: misses a 1% error with p ≤ 0.05 │
│                                                                      │
│ ⓘ If the changed fraction were above 80%, TARE would run in full     │
│   instead; reuse would not pay off.                                  │
│                                [Cancel]  [Download job script]  [Run] │
└──────────────────────────────────────────────────────────────────────┘
```

### 4. Run monitor

```
┌ Running: 312 / 1,048 ───────────────────────────── elapsed 0:41:12 ─┐
│ ████████████░░░░░░░░░░░░░░░░░░░░░░░░  30%                           │
│ ✔ Exact 298   ↻ Full rerun 9   ✖ Refused 3   ! Failed 2   … Queued 736 │
│                                                                      │
│ Genome              Phase      Time    Outcome                       │
│ MAG_0312.faa        audit      0:14    …                             │
│ MAG_0311.faa        done       0:52    ✔ Exact                        │
│ MAG_0310.faa        done       3:40    ↻ Full rerun                   │
└──────────────────────────────────────────────────────────────────────┘
```

### 5. Results

```
┌ Results: Pfam 38.0 ────────────────────────── [Export tables] [Provenance] ┐
│ ✔ Exact 1,031   ↻ Full rerun 9   ✖ Refused 6   ! Failed 2                   │
│ Time 6.1 h vs ≈25.9 h full rerun (4.24×)                                   │
│                                                                            │
│ Filter: [All ▾]                                                            │
│ Genome         Outcome        Why                                          │
│ MAG_0001.faa   ✔ Exact        Replayed 1,618 families; audit 299/299 matched │
│ MAG_0310.faa   ↻ Full rerun   Changed fraction above threshold               │
│ MAG_0477.faa   ✖ Refused      Audit found a row that differs from a full run │
│ MAG_0902.faa   ! Failed       hmmscan exited with status 1 (see log)         │
└────────────────────────────────────────────────────────────────────────────┘
```

Every row opens screen 6.

### 6. Genome detail ("why")

```
┌ MAG_0477.faa ──────────────────────────────────────────────────────┐
│ ✖ Refused: a sampled check found a row that differs from a full run. │
│ Your output for this genome came from a full run instead, so it is   │
│ still correct. Nothing reused was shipped.                           │
│                                                                      │
│ Details (from decision.txt)                                          │
│   decision      REFUSE_AUDIT                                         │
│   why           domtblout: <raw reason text>                         │
│   audit         s = 299, ε = 0.05, κ = 0.01                          │
│   program       /usr/bin/hmmscan sha256:…                            │
│   files         tables/  decision.txt  log                [Open folder] │
└──────────────────────────────────────────────────────────────────────┘
```

## CLI contract

### What exists today (main at 3b8ad2a)

One call per genome:

```
python3 -m acts run --strategy reference \
  --pin "-Z {entry_count}" --verify audit \
  --prep "hmmpress -f {reference}" \
  --input GENOME.faa --reference Pfam-A.hmm \
  --cache CACHE/cache.jsonl -o OUT/GENOME \
  -- hmmscan --cut_ga --noali --cpu 4 \
     --tblout {output:tblout} --domtblout {output:domtblout} \
     -o /dev/null {reference} {input}
```

This is the exact headline command (`scripts/headline_carc_measured.py`). The audit defaults
to the bounded audit (s = 299); `--f-threshold` defaults to the cache's break-even, else 0.80.

Outputs:

| Path | Content |
|---|---|
| `OUT/GENOME/decision.txt` | `key: value` lines: `strategy`, `decision`, `why`, then extra keys (`program_binary`, audit fields, …) |
| `OUT/GENOME/tables/<name>` | the tool's output tables (`tblout`, `domtblout`) |
| `OUT/GENOME/tables/<name>.provenance.json` | which rows were reused or rescaled |
| stdout | `strategy:`, `decision:`, `why:` lines |

Exit codes: `0` = SHIP or FALLBACK (outputs are correct), `1` = any REFUSE, `2` = usage or run error.

Decision codes, and what the UI shows:

| Code | Badge | Plain-language line |
|---|---|---|
| `SHIP` | ✔ Exact | Reused unchanged results; checked against a full run on a sample. |
| `FALLBACK` | ↻ Full rerun | Too much changed for reuse to pay off, so the tool ran in full. |
| `REFUSE_AUDIT` | ✖ Refused | A sampled check found a difference, so nothing reused was shipped. |
| `REFUSE_MATCH` | ✖ Refused | Reused rows did not match the tool's own replay. |
| `REFUSE_PIN` | ✖ Refused | Some scores depend on database size and could not be pinned. |
| `REFUSE` | ✖ Refused | Show `why` as is. |
| exit 2 | ! Failed | The run itself failed; show the log. |

Rule: the UI keys on the **code**, never on parsing `why`. `why` is shown verbatim under Details.

Open question to check before shipping v1: after a REFUSE, does `OUT/tables/` hold a full-run
output, or nothing? Screen 6's text depends on the answer.

### What the UI needs added (small, in `pipeline/acts/`, each with tests)

1. **`OUT/result.json`** next to `decision.txt`: the same fields as JSON plus
   `schema_version`, `exit_code`, `wall_s` and per-phase times. Reading `key: value` text is fragile.
2. **`python3 -m acts plan`**: no tool run. Diffs the new reference against the cache's entry
   hashes and prints JSON: `{"new": n, "changed": n, "removed": n, "same": n,
   "changed_fraction": f, "threshold": t, "threshold_basis": "break-even|default",
   "action": "replay|full", "audit_s": 299}`. This drives screen 3.
3. **`--events OUT/events.jsonl`**: one line per phase change (`probe`, `fill`, `replay`,
   `audit`, `write`, `done`) with a timestamp. This drives screen 4. Until it exists, the UI
   can show "running" and switch to the outcome when `decision.txt` appears.
4. **`python3 -m acts slurm-script`** (or a UI-side template): one array job per project,
   one task per genome, same argv as above, results under one `OUT/` root.

The UI itself (any stack) only needs: build argv from the project, launch or emit a script,
poll `events.jsonl` / `result.json`, and render screens 1–6.
