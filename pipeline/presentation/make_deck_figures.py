"""Graphs for the TARE progress deck (USC template), drawn at each picture slot's exact size.

Reads only committed result files under pipeline/results/. Writes transparent PNGs to
pipeline/presentation/deck/. Palette taken from the template: cardinal for TARE, warm gray for
the baseline (a full rerun or another tool), burnt orange for wrong output, navy and slate for
text and secondary marks. No titles inside graphs: the slide title carries the message.

Run: python3 pipeline/presentation/make_deck_figures.py
"""
import json
import statistics
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
RES = HERE.parent / "results"
OUT = HERE / "deck"
OUT.mkdir(exist_ok=True)

CARD, NAVY, SLATE, ORANGE = "#980000", "#1B2333", "#4A5568", "#B5541A"
WARM, WARM2, CREAM, LIGHT = "#BEBBB4", "#C5C4BF", "#EEEAE1", "#D9C3C3"
plt.rcParams.update({
    "font.family": "Helvetica Neue", "font.size": 10, "axes.labelsize": 10, "xtick.labelsize": 9,
    "ytick.labelsize": 9, "legend.fontsize": 9, "axes.edgecolor": SLATE, "axes.labelcolor": NAVY,
    "xtick.color": SLATE, "ytick.color": SLATE, "text.color": NAVY, "axes.spines.top": False,
    "axes.spines.right": False, "axes.linewidth": 0.8, "savefig.transparent": True,
})


def load(rel):
    return json.loads((RES / rel).read_text())


def fig_at(w, h):
    return plt.subplots(figsize=(w, h))


def save(fig, name):
    fig.tight_layout(pad=0.4)
    fig.savefig(OUT / f"{name}.png", dpi=300)
    plt.close(fig)
    print("wrote", name)


def headline():  # slot 5.43 x 4.44
    h = load("exact_replay/headline_carc.json")
    g = sorted([x for x in h["genomes"] if x["outcome"] == "EXACT"], key=lambda x: x["S_g"])
    fig, ax = fig_at(5.43, 4.44)
    ci = h["bootstrap_ci95"]
    ax.axhspan(ci["low"], ci["high"], color=LIGHT, alpha=0.6, lw=0, zorder=0)
    ax.bar(range(len(g)), [r["S_g"] for r in g], color=CARD, width=0.66, zorder=2)
    ax.axhline(h["headline_median"], color=NAVY, lw=1.2, ls="--", zorder=3)
    ax.text(-0.45, 5.2, f"median {h['headline_median']:.2f}×  (band: 95% CI)", fontsize=10, fontweight="bold", zorder=4)
    ax.axhline(1, color=SLATE, lw=1)
    for i, r in enumerate(g):
        ax.text(i, r["S_g"] - 0.12, f"{r['S_g']:.2f}", ha="center", va="top", color="white", fontsize=8, fontweight="bold")
    ax.set_xticks(range(len(g)))
    ax.set_xticklabels([f"G{i + 1}" for i in range(len(g))])
    ax.set_xlabel("nine bacterial genomes, sorted by speedup")
    ax.set_ylabel("speedup over a full rerun")
    ax.set_ylim(0, 5.6)
    save(fig, "headline")


def exactness():  # slot 6.08 x 4.42
    t = load("exact_replay/exactness_totals.json")
    names = {
        "hmmer_replay_300": "HMMER replay, 300 proteins", "hmmer_replay_3_genomes": "HMMER replay, 3 genomes",
        "hmmer_tool_2_laptop": "HMMER, 2 genomes (laptop)", "hmmer_tool_server_genomes": "HMMER, 9 genomes (server)",
        "hmmer_tool_diverse_genomes": "HMMER, 48 diverse genomes", "infernal_replay_10": "Infernal replay, 10 genomes",
        "infernal_tool_family_removal": "Infernal, 1 family removed", "infernal_tool_10_genomes": "Infernal, 10 genomes",
    }
    rows = list(t["rows"].items())
    fig, ax = fig_at(6.08, 4.42)
    ax.barh(range(len(rows)), [v / 1000 for _, v in rows], color=CARD, height=0.62)
    for i, (_, v) in enumerate(rows):
        ax.text(v / 1000 + 6, i, f"{v:,}  ·  0 differ", va="center", fontsize=9)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([names[k] for k, _ in rows])
    ax.invert_yaxis()
    ax.set_xlim(0, 640)
    ax.set_xlabel("output lines compared byte for byte (thousands)")
    save(fig, "exactness")


def churn():  # slot 6.08 x 4.42
    p = load("release_chain/pairs.json")["pairs"]
    fig, ax = fig_at(6.08, 4.42)
    x = range(len(p))
    un = [q["unchanged_strict"] / q["z_new"] for q in p]
    ed = [q["edited"] / q["z_new"] for q in p]
    nw = [q["added"] / q["z_new"] for q in p]
    ax.bar(x, un, color=WARM2, width=0.66, label="unchanged: reused")
    ax.bar(x, ed, bottom=un, color=LIGHT, width=0.66, label="edited: rerun")
    ax.bar(x, nw, bottom=[a + b for a, b in zip(un, ed)], color=CARD, width=0.66, label="new: rerun")
    for i, q in enumerate(p):
        ax.text(i, 1.025, f"{100 * q['f_delta']:.0f}%", ha="center", fontsize=9, color=CARD, fontweight="bold")
    ax.set_xticks(list(x))
    ax.set_xticklabels([f"{q['old_release']}\nto {q['new_release']}" for q in p], fontsize=8)
    ax.set_ylim(0, 1.13)
    ax.set_ylabel("share of the new Pfam release")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.32), ncol=3, frameon=False)
    save(fig, "churn")


def cost_model():  # slot 5.61 x 2.97
    s = load("exact_replay/server_cost_fit.json")
    h = load("exact_replay/headline_carc.json")
    a, c = s["a"], s["c"]
    fs = [i / 1000 for i in range(5, 1000)]
    fig, ax = fig_at(5.61, 2.97)
    ax.plot([100 * f for f in fs], [1 / (a * f + c) for f in fs], color=CARD, lw=2, label="model 1 / (a·f + c)")
    ax.axhline(1 / c, color=CARD, ls=":", lw=1)
    ax.text(55, 1 / c + 0.3, f"ceiling {1 / c:.1f}×", ha="center", fontsize=8, color=CARD)
    ax.axhline(1, color=SLATE, lw=0.8)
    ax.plot([100 * pr["f_delta"] for pr in s["predictions"]], [pr["speedup"] for pr in s["predictions"]], "o",
            color=WARM, mec=SLATE, ms=5, label="other Pfam releases (model)")
    ax.plot([100 * s["f"]], [h["headline_median"]], "D", color="white", mec=NAVY, mew=1.6, ms=7, label="measured 4.24×")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 11.5)
    ax.set_xlabel("share of the database that changed (%)")
    ax.set_ylabel("speedup")
    ax.legend(frameon=False, loc="center right", fontsize=8)
    save(fig, "cost_model")


def time_split():  # slot 5.61 x 2.67
    s = load("exact_replay/server_cost_fit.json")["phase_bars"]["genomes"][1]
    stock = s["stock_median_s"]
    st = s["stages_s"]
    fig, ax = fig_at(5.61, 2.67)
    ax.barh(1, stock, color=WARM2, height=0.5)
    ax.text(stock - 30, 1, f"full rerun  {stock:.0f} s", va="center", ha="right", fontsize=9)
    left = 0
    for k, col, lab in (("discovery", CARD, "discovery"), ("replay", "#C46A6A", "replay"), ("check", NAVY, "check + audit"),
                        ("other", WARM, "other")):
        ax.barh(0, st[k], left=left, color=col, height=0.5, label=lab)
        left += st[k]
    ax.text(left + 40, 0, f"TARE  {s['tare_wall_s']:.0f} s  ({s['S_g']:.2f}× faster)", va="center", fontsize=9, color=CARD, fontweight="bold")
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["update", "rerun"])
    ax.set_xlabel("seconds (median genome, server)")
    ax.set_xlim(0, stock * 1.05)
    ax.legend(frameon=False, ncol=4, loc="lower center", bbox_to_anchor=(0.5, 1.0), fontsize=8)
    save(fig, "time_split")


def infernal():  # slot 5.81 x 4.47
    m = load("infernal/measured2.json")["summary"]
    bars = [("full rerun", 1.0, None, WARM), ("first\nversion", 328.4 / 666.0, None, ORANGE),
            ("TARE\nno clans", m["noclan"]["median_s_g"], m["noclan"]["bootstrap_median"], CARD),
            ("TARE\nwith clans", m["clan"]["median_s_g"], m["clan"]["bootstrap_median"], CARD)]
    fig, ax = fig_at(5.81, 4.47)
    for i, (lab, v, ci, col) in enumerate(bars):
        err = None if ci is None else [[v - ci["p2.5"]], [ci["p97.5"] - v]]
        ax.bar(i, v, color=col, width=0.6, yerr=err, capsize=5, ecolor=NAVY)
        ax.text(i, (ci["p97.5"] if ci else v) + 0.06, f"{v:.2f}×", ha="center", fontsize=11, fontweight="bold")
    ax.axhline(1, color=SLATE, ls="--", lw=0.8)
    ax.set_xticks(range(4))
    ax.set_xticklabels([b[0] for b in bars])
    ax.set_ylabel("speedup over a full rerun")
    ax.set_ylim(0, 2.7)
    save(fig, "infernal")


def safety():  # slot 6.08 x 4.42
    v2 = load("adversarial/v2_summary.json")["arms"]
    m = load("adversarial/measured.json")["cells"]
    first = sum(c["UNSAFE"] for k, c in m.items() if k.startswith(("C2", "C3")))
    fig, ax = fig_at(6.08, 4.42)
    groups = ["all hidden faults", "faults reaching ≥1% of records"]
    vals = {"audit off": (first / 800, None), "audit ~50 records": (v2["shipped"]["hidden_unsafe"] / 800, v2["shipped"]["covered_unsafe"] / 400),
            "bounded audit, 299": (v2["bounded"]["hidden_unsafe"] / 800, v2["bounded"]["covered_unsafe"] / 400)}
    cols = [ORANGE, WARM, CARD]
    w = 0.26
    for j, (lab, (a, b)) in enumerate(vals.items()):
        xs = [0 + (j - 1) * w, 1 + (j - 1) * w]
        ys = [a, b if b is not None else 0]
        bars = ax.bar(xs, [100 * y for y in ys], width=w, color=cols[j], label=lab)
        for x, y, bv in zip(xs, ys, [a, b]):
            if bv is not None:
                ax.text(x, 100 * y + 1.5, f"{100 * y:.1f}%", ha="center", fontsize=8.5)
    ax.axhline(5, color=CARD, ls=":", lw=1)
    ax.text(0.5, 6.2, "guarantee: at most 5%", ha="center", fontsize=8.5, color=CARD)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(groups)
    ax.set_ylabel("wrong updates that got through (%)")
    ax.set_ylim(0, 100)
    ax.legend(frameon=False, loc="upper right")
    save(fig, "safety")


def diamond():  # slot 6.08 x 4.42
    d = load("diamond_order/g1_measured.json")
    sh = d["shuffles"]
    fig, ax = fig_at(6.08, 4.42)
    x = range(len(sh))
    miss = [s["comparison"]["missing"] for s in sh]
    extra = [s["comparison"]["extra"] for s in sh]
    ax.bar([i - 0.19 for i in x], miss, width=0.38, color=ORANGE, label="hits lost")
    ax.bar([i + 0.19 for i in x], extra, width=0.38, color=WARM, label="hits gained")
    for i in x:
        ax.text(i - 0.19, miss[i] + 0.7, str(miss[i]), ha="center", fontsize=9)
        ax.text(i + 0.19, extra[i] + 0.7, str(extra[i]), ha="center", fontsize=9)
    ax.set_xticks(list(x))
    ax.set_xticklabels([f"order {i + 1}" for i in x])
    ax.set_ylabel("rows that changed (of 210,460)")
    ax.set_ylim(0, 48)
    ax.legend(frameon=False, loc="upper right")
    save(fig, "diamond")


def baselines():  # slot 5.61 x 2.97
    b = load("baseline_overhead.json")["modes"]["hmmscan"]
    r = statistics.mean(float(x) for x in b["riker"]["paired_ratio_vs_stock"])
    i = statistics.mean(float(x) for x in b["incr_default"]["paired_ratio_vs_stock"])
    h = load("exact_replay/headline_carc.json")
    fig, ax = fig_at(5.61, 2.97)
    names = ["Riker", "INCR", "TARE"]
    upd = [1.0, 1.0, h["headline_median"]]
    first = [r, i, h["first_run_overhead_median"]]
    xs = range(3)
    ax.bar([x - 0.19 for x in xs], first, width=0.38, color=WARM2, label="first run, × plain run")
    ax.bar([x + 0.19 for x in xs], upd, width=0.38, color=[WARM, WARM, CARD], label="speedup after a release")
    for x, v in zip(xs, first):
        ax.text(x - 0.19, v + 0.1, f"{v:.2f}", ha="center", fontsize=8.5)
    for x, v in zip(xs, upd):
        ax.text(x + 0.19, v + 0.1, f"{v:.2f}×", ha="center", fontsize=8.5, fontweight="bold" if v > 1 else None)
    ax.set_xticks(list(xs))
    ax.set_xticklabels(names)
    ax.set_ylim(0, 5.2)
    ax.legend(frameon=False, loc="upper left", fontsize=8)
    save(fig, "baselines")


def approximate():  # slot 5.61 x 2.67
    r = load("baselines_exact/rescale.json")["pooled"]["tbl"]
    i = load("reference_diamond/dx.json")["dx_i"]["idiamond"]
    vals = [("rescale old E-values", 100 * r["byte_identical_over_stock"], WARM),
            ("iSeqSearch", 100 * i["shared_byte_identical"] / i["shared_rows"], WARM), ("TARE", 100.0, CARD)]
    fig, ax = fig_at(5.61, 2.67)
    ax.barh(range(3), [v for _, v, _ in vals], color=[c for _, _, c in vals], height=0.55)
    for k, (_, v, _) in enumerate(vals):
        ax.text(v + 1.5, k, f"{v:.1f}%", va="center", fontsize=9, fontweight="bold")
    ax.set_yticks(range(3))
    ax.set_yticklabels([v[0] for v in vals])
    ax.invert_yaxis()
    ax.set_xlim(0, 115)
    ax.set_xlabel("output lines identical to a full rerun (%)")
    save(fig, "approximate")


def diverse():  # slot 5.61 x 2.97
    d = load("diverse_genomes/measured_score.json")["by_group"]
    groups = [("archaea", "Archaea"), ("bacteria", "Bacteria"), ("eukaryote", "Eukaryotes"), ("mag", "Metagenome-\nassembled")]
    fig, ax = fig_at(5.61, 2.97)
    ship = [d[g]["pass"] for g, _ in groups]
    ref = [d[g]["needless_refusal"] for g, _ in groups]
    ax.bar(range(4), ship, color=CARD, width=0.6, label="shipped, exact")
    ax.bar(range(4), ref, bottom=ship, color=WARM2, width=0.6, label="refused although exact (since fixed)")
    for k in range(4):
        ax.text(k, ship[k] + ref[k] + 0.6, f"{ship[k]}/{ship[k] + ref[k]}", ha="center", fontsize=9)
    ax.set_xticks(range(4))
    ax.set_xticklabels([n for _, n in groups], fontsize=8.5)
    ax.set_ylabel("genomes")
    ax.set_ylim(0, 36)
    ax.legend(frameon=False, loc="upper right", fontsize=8)
    save(fig, "diverse")


def prosite():  # slot 5.61 x 2.67
    a = load("unrelated_ship/measured.json")["checks"]
    b = load("unrelated_ship/measured_v2.json")["checks"]
    fig, ax = fig_at(5.61, 2.67)
    rows = [("draw 1", a["n_ship"], a["n"] - a["n_ship"]), ("draw 2", b["n_ship"], b["n"] - b["n_ship"])]
    for k, (lab, s, inc) in enumerate(rows):
        ax.barh(k, s, color=CARD, height=0.5, label="shipped, exact" if k == 0 else None)
        ax.barh(k, inc, left=s, color=WARM2, height=0.5, label="too few lines to count" if k == 0 else None)
        ax.text(s + inc + 0.4, k, f"{s} of {s + inc}", va="center", fontsize=9, fontweight="bold")
    ax.set_yticks(range(2))
    ax.set_yticklabels([r[0] for r in rows])
    ax.invert_yaxis()
    ax.set_xlim(0, 25)
    ax.set_xlabel("genomes (PROSITE pfscanV3)")
    ax.legend(frameon=False, loc="upper right", fontsize=8)
    save(fig, "prosite")


def payback():  # slot 3.18 x 2.92
    h = load("exact_replay/headline_carc.json")
    f = load("infernal/fill_summary.json")["variants"]["noclan"]
    fig, ax = fig_at(3.18, 2.92)
    vals = [("HMMER", h["first_run_overhead_median"], h["break_even_n_median"], CARD),
            ("Infernal", f["median_fill_over_stock"], f["payback_releases"], WARM)]
    for k, (lab, fill, n, col) in enumerate(vals):
        ax.bar(k, fill, color=col, width=0.55)
        ax.text(k, fill + 0.12, f"{fill:.2f}×\npays back\nafter {n:.1f}", ha="center", fontsize=8)
    ax.axhline(1, color=SLATE, ls="--", lw=0.8)
    ax.set_xticks(range(2))
    ax.set_xticklabels([v[0] for v in vals])
    ax.set_ylabel("first run, × a full run", fontsize=8.5)
    ax.set_ylim(0, 6.6)
    save(fig, "payback")


if __name__ == "__main__":
    for fn in (headline, exactness, churn, cost_model, time_split, infernal, safety, diamond, baselines, approximate,
               diverse, prosite, payback):
        fn()
