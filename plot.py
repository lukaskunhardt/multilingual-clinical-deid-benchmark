"""Draw character F1 against leak rate for every model in results.json (written by evaluate.py).

    python plot.py --results results.json --split test --out chart.png
"""
import argparse
import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# short names for the chart; models I trained are drawn in blue
NAMES = {
    "Horizon-pii-redactor-base": "Horizon pii-redactor-base",
    "Horizon-pii-redactor-small": "Horizon pii-redactor-small",
    "german-clinical-deid": "german-clinical-deid",
    "german-clinical-deid-base": "german-clinical-deid-base",
    "pii-filter-small": "pii-filter-small",
    "openai-privacy-filter_opf-viterbi": "openai/privacy-filter (opf)",
    "openai-privacy-filter_pipeline-packed": "openai/privacy-filter (pipeline)",
    "OpenMed-privacy-filter-multilingual-v2": "OpenMed multilingual-v2",
    "piiranha-v1": "piiranha-v1",
}
MINE = {"german-clinical-deid", "german-clinical-deid-base", "pii-filter-small"}
# label offsets in points, set by hand so that no label covers a point or another label
OFFSET = {
    "Horizon-pii-redactor-base": (12, 6, "left"),
    "german-clinical-deid": (-12, 14, "right"),
    "german-clinical-deid-base": (12, -16, "left"),
    "pii-filter-small": (0, 14, "center"),
    "openai-privacy-filter_opf-viterbi": (-12, 10, "right"),
    "Horizon-pii-redactor-small": (0, -24, "center"),
    "OpenMed-privacy-filter-multilingual-v2": (-12, 8, "right"),
    "piiranha-v1": (-8, 18, "right"),
    "openai-privacy-filter_pipeline-packed": (-12, -22, "right"),
}
BLUE, GREY = "#0072B2", "#6b6b6b"


def pareto(points):
    """Points no other point beats on both axes (lower leak rate, higher F1), sorted by leak rate."""
    front = [p for p in points if not any(q[0] <= p[0] and q[1] >= p[1] and q != p for q in points)]
    return sorted(front)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default="results.json")
    ap.add_argument("--split", default="test")
    ap.add_argument("--out", default="chart.png")
    a = ap.parse_args()
    res = json.load(open(a.results, encoding="utf-8"))
    rows = {m: (r[a.split]["leak_rate"], r[a.split]["char_f1"]) for m, r in res.items() if a.split in r}

    plt.rcParams.update({"font.size": 17, "axes.spines.top": False, "axes.spines.right": False})
    fig, ax = plt.subplots(figsize=(16, 10), dpi=100)
    # nobody reaches the top left corner: high F1 and few letters with a leak
    ax.text(0.0, 0.99, "\u2196 better", va="top", fontsize=17, color="#00684b")
    front = pareto(list(rows.values()))
    ax.step([p[0] for p in front], [p[1] for p in front], where="post", color="#999999", lw=2, ls="--", zorder=1)
    for m, (x, y) in rows.items():
        mine = m in MINE
        ax.scatter(x, y, s=170, color=BLUE if mine else GREY, marker="o" if mine else "s", edgecolor="white", lw=2, zorder=3)
        dx, dy, ha = OFFSET.get(m, (10, 6, "left"))
        ax.annotate(NAMES.get(m, m), (x, y), xytext=(dx, dy), textcoords="offset points", ha=ha, va="center",
                    fontsize=16, color="#1a1a1a")
    ax.set_xlim(-0.02, 1.05)
    ax.set_ylim(0.6, 1.0)
    ax.set_xlabel("Leak rate: share of letters with a missed name, ID, contact or street (lower is better)")
    ax.set_ylabel("Character F1 (higher is better)")
    ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    ax.grid(color="#e6e6e6", lw=1)
    ax.set_title("Nine de-identification models on the test split (1,980 letters, 22 languages)", fontsize=20, loc="left", pad=16)
    handles = [plt.Line2D([], [], marker="o", ls="", color=BLUE, ms=13, label="my models (none trained on this data)"),
               plt.Line2D([], [], marker="s", ls="", color=GREY, ms=13, label="other open models"),
               plt.Line2D([], [], ls="--", color="#999999", lw=2, label="best trade-off so far")]
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False, fontsize=16, bbox_to_anchor=(0.5, 0.0))
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(a.out, facecolor="white")
    print("wrote", a.out)


if __name__ == "__main__":
    main()
