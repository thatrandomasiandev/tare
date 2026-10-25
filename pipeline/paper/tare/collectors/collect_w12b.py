#!/usr/bin/env python3
"""Collect W12b iSeqSearch measured.json (or report limitation)."""
from __future__ import annotations

import sys
from pathlib import Path

from common import REPO, load_json, rsync_from_carc, status_line, write_json

OUT = REPO / "pipeline/results/iseqsearch_timing/measured.json"
LIMITATION = REPO / "pipeline/results/iseqsearch_timing/LIMITATION.md"
REMOTE = "tare-w12b/pipeline/results/iseqsearch_timing/measured.json"


def main() -> int:
    if LIMITATION.is_file() and "second locked failure" in LIMITATION.read_text().lower():
        status_line("W12b", "FAILED", "stated limitation")
        return 1
    dest = REPO / "pipeline/results/iseqsearch_timing/_staging_measured.json"
    try:
        rsync_from_carc(REMOTE, dest)
    except SystemExit:
        status_line("W12b", "STILL RUNNING", "no measured.json")
        return 2
    payload = load_json(dest)
    write_json(OUT, payload)
    verdict = payload.get("verdict")
    if verdict != "COMPLETE":
        # Provenance kept; never fill ISeqSearchSpeedup (stated limitation).
        why = payload.get("why") or verdict
        controls = payload.get("controls") or {}
        lim = REPO / "pipeline/results/iseqsearch_timing/LIMITATION.md"
        if not lim.is_file():
            lim.write_text(
                "# W12b stated limitation\n\n"
                f"verdict={verdict}; why={why}; "
                f"tare_refused={controls.get('tare_refused')}. "
                "Second locked failure — no third attempt.\n"
            )
        status_line(
            "W12b",
            "FAILED",
            f"stated limitation verdict={verdict} why={why} "
            f"tare_refused={controls.get('tare_refused')}",
        )
        return 1
    status_line("W12b", "COLLECTED", str(OUT.relative_to(REPO)))
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
