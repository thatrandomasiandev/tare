#!/usr/bin/env python3
"""Collect W13 headline_bounded measured results (STILL RUNNING until array done)."""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

from common import REPO, die, load_json, rsync_from_carc, status_line, write_json

OUT = REPO / "pipeline/results/exact_replay/headline_bounded.json"
REMOTE_DIR = "headline_bounded/results"
N_TASKS = 9


def _score(measured: list[Path]) -> dict:
    """Score task JSONs with the locked headline_analysis scorer."""
    sys.path.insert(0, str(REPO / "pipeline" / "scripts"))
    from headline_analysis import load_records, summarize  # noqa: WPS433

    records = load_records(measured)
    summary = summarize(records)
    if summary.get("any_fail"):
        fails = [
            f"{r.get('proteome')}:{r.get('fail_reasons')}"
            for r in records
            if r.get("outcome") == "FAIL"
        ]
        die(f"W13 control FAIL: {fails}")
    if summary.get("n_speedups") != N_TASKS or summary.get("headline_median") is None:
        die(
            f"W13 incomplete score n_speedups={summary.get('n_speedups')} "
            f"median={summary.get('headline_median')}"
        )
    summary["test"] = "headline-bounded"
    summary["audit_mode"] = "bounded"
    summary["audit_s_target"] = 299
    summary["job_array"] = "13260162_[0-8]"
    summary["protocol"] = "pipeline/docs/EXACT_REPLAY_PROTOCOL.md"
    return summary


def main() -> int:
    staging = REPO / "pipeline/results/exact_replay/_w13_staging"
    staging.mkdir(parents=True, exist_ok=True)
    try:
        rsync_from_carc(f"{REMOTE_DIR}/", staging)
    except SystemExit:
        status_line("W13", "STILL RUNNING", "rsync/missing results")
        return 2
    files = sorted(staging.glob("headline_bounded_*.json"))
    # exclude pilot
    measured = [p for p in files if "pilot" not in p.name]
    if len(measured) < N_TASKS:
        status_line("W13", "STILL RUNNING", f"{len(measured)}/{N_TASKS} tasks")
        return 2
    for path in measured:
        row = load_json(path)
        if row.get("outcome") != "EXACT":
            die(f"{path.name} outcome={row.get('outcome')}")
    # Prefer a scored aggregate if present on CARC; else score locally.
    agg = staging / "headline_bounded.json"
    if agg.is_file():
        payload = load_json(agg)
        if payload.get("headline_median") is None:
            payload = _score(measured)
    else:
        payload = _score(measured)
    # Attach paired comparison to the prior Bernoulli headline when available.
    old_path = REPO / "pipeline/results/exact_replay/headline_carc.json"
    if old_path.is_file() and "paired_vs_bernoulli_headline" not in payload:
        old = json.loads(old_path.read_text())
        om = {
            g["proteome"]: g["S_g"]
            for g in (old.get("genomes") or [])
            if g.get("S_g") is not None
        }
        pairs = []
        for g in payload.get("genomes") or []:
            p = g.get("proteome")
            sb = g.get("S_g")
            so = om.get(p)
            pairs.append(
                {
                    "proteome": p,
                    "S_g_bounded": sb,
                    "S_g_original": so,
                    "ratio_bounded_over_original": (sb / so) if (sb and so) else None,
                }
            )
        ratios = [
            p["ratio_bounded_over_original"]
            for p in pairs
            if p.get("ratio_bounded_over_original") is not None
        ]
        payload["paired_vs_bernoulli_headline"] = {
            "original_source": "pipeline/results/exact_replay/headline_carc.json",
            "original_headline_median": old.get("headline_median"),
            "original_bootstrap_ci95": old.get("bootstrap_ci95"),
            "genomes": pairs,
        }
        if ratios:
            payload["paired_ratio_min"] = min(ratios)
            payload["paired_ratio_max"] = max(ratios)
            payload["paired_ratio_median"] = statistics.median(ratios)
    write_json(OUT, payload)
    status_line(
        "W13",
        "COLLECTED",
        f"{OUT.relative_to(REPO)} median={payload.get('headline_median'):.4f}",
    )
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
