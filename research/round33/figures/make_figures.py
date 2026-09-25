#!/usr/bin/env python3
"""Round33 presentation figures for the Yang-Mills workbench.

Every figure produced here is a schematic illustration of a Round33
experiment setup or of recorded, already-admitted values. NONE of these
figures carries admission weight and none computes, replays or certifies an
admitted result. Every plotted or printed number is read from a file bound by
the corresponding Round33 gate (producer output/results.json, skeptic review
JSON, producer report.md or the gate itself); nothing numeric is typed here.
Where two bound records state the same value (forward/reverse producers,
skeptic review, gate text) the script requires them to agree and stops
otherwise. See research/round33/figures/README.md for the source of every
number.

The only computation is a float preview of the BB2 item-5 bracket, evaluated
in log10 space from the recorded exact constants and the recorded bracket
formula, used to draw a curve. The script requires that this preview
reproduces the recorded first exceedance of 2 and the recorded N=5 and N=10
bracket previews; the curve is labelled a preview, not a certificate.

Outputs: five PNG (200 dpi) + SVG pairs under research/round33/figures/, a
byte copy of each PNG in dist/ (the path research/round33/advisor/figures.json
names), and research/round33/advisor/figures.json itself, whose captions are
assembled from the same record values.

Determinism contract (as in research/round32/figures/make_figures.py):
  - No network access; only matplotlib and the standard library.
  - `svg.hashsalt` fixed; `metadata={'Date': None}` on every savefig.
  - Font family pinned to the bundled DejaVu Sans; SVG text as paths.
  - `random.seed` fixed defensively (no stochastic element is used).
  - PNGs in dist/ are byte copies, not second renders.

Run:  python3 -B research/round33/figures/make_figures.py
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import re
import shutil
import textwrap
from fractions import Fraction
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Patch, Rectangle  # noqa: E402
from matplotlib.ticker import FuncFormatter, MultipleLocator  # noqa: E402
from mpl_toolkits.mplot3d import Axes3D  # noqa: E402,F401  (registers 3d projection)
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # noqa: E402

random.seed(20260925)  # defensive; no stochastic element is used below

ROOT = Path(__file__).resolve().parents[3]
FIG_DIR = Path(__file__).resolve().parent
DIST_DIR = ROOT / "dist"
R33 = "research/round33"
SCRIPT = R33 + "/figures/make_figures.py"
FIGURES_JSON = ROOT / R33 / "advisor" / "figures.json"

# ---------------------------------------------------------------------------
# Palette (dataviz reference palette, light mode; validated with
# validate_palette.js: all checks pass, contrast WARN -> every mark carries a
# visible text label). Status colours are used only with an icon and a label.
# ---------------------------------------------------------------------------
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BASE = "#c3c2b7"

C_BLUE = "#2a78d6"      # categorical slot 1
C_ORANGE = "#eb6834"    # categorical slot 2
C_AQUA = "#1baf7a"      # categorical slot 3
C_YELLOW = "#eda100"    # categorical slot 4
C_MAGENTA = "#e87ba4"   # categorical slot 5

STATUS_GOOD = "#0ca30c"
STATUS_WARNING = "#fab219"
STATUS_CRITICAL = "#d03b3b"

PRESENTATION_NOTE = "Presentation only; no admission weight."

plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans"],
        "mathtext.fontset": "dejavusans",
        "font.size": 10,
        "svg.hashsalt": "ym-round33-figures-2026-09-25",
        "svg.fonttype": "path",
        "figure.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "axes.edgecolor": BASE,
        "axes.labelcolor": INK2,
        "text.color": INK,
        "xtick.color": INK2,
        "ytick.color": INK2,
        "legend.frameon": False,
    }
)


# ---------------------------------------------------------------------------
# Record access. Every file read here is bound by the named loop's gate.
# ---------------------------------------------------------------------------
def require(ok: bool, message: str) -> None:
    if not ok:
        raise SystemExit("make_figures: " + message)


_GATES: dict[str, dict] = {}


def gate(loop: str) -> dict:
    if loop not in _GATES:
        _GATES[loop] = json.loads((ROOT / R33 / "advisor" / f"{loop}-gate.json").read_text(encoding="utf-8"))
    return _GATES[loop]


def bound(loop: str, rel: str) -> Path:
    """Return a path only if the loop's gate binds it with the current bytes."""
    g = gate(loop)
    require(rel in g["bindings"], f"{rel} is not bound by the {loop} gate")
    path = ROOT / rel
    require(hashlib.sha256(path.read_bytes()).hexdigest() == g["bindings"][rel],
            f"{rel} differs from the bytes bound by the {loop} gate")
    return path


def record(loop: str, rel: str) -> dict:
    return json.loads(bound(loop, rel).read_text(encoding="utf-8"))


def gate_text(loop: str) -> str:
    g = gate(loop)
    return " ".join([g["accepted"], g.get("decision", ""), " ".join(g.get("limitations", []))])


def in_gate(loop: str, *fragments: str) -> None:
    text = gate_text(loop)
    for fragment in fragments:
        require(fragment in text, f"{fragment!r} does not appear in the {loop} gate text")


def check_by_id(result: dict, check_id: str) -> dict:
    rows = [row for row in result["checks"] if row.get("id") == check_id]
    require(len(rows) == 1 and rows[0].get("passed") is True, f"check {check_id} missing or not passed")
    return rows[0]


def log10_frac(x: Fraction) -> float:
    require(x > 0, "log of a nonpositive value")
    return math.log10(x.numerator) - math.log10(x.denominator)


def log10_sum(*logs: float) -> float:
    top = max(logs)
    return top + math.log10(sum(10 ** (v - top) for v in logs))


def sci(preview: str, digits: int = 4) -> str:
    """Format a recorded decimal preview string (never a computed value)."""
    mantissa, exponent = f"{float(preview):.{digits}e}".split("e")
    return f"{mantissa}×10{superscript(int(exponent))}"


_SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def superscript(n: int) -> str:
    return str(n).translate(_SUP)


def footer(fig, extra: str) -> None:
    text = textwrap.fill(f"{PRESENTATION_NOTE} {extra}", width=int(fig.get_figwidth() * 15.5))
    fig.text(0.5, 0.01, text, ha="center", va="bottom", fontsize=7.6, color=INK2, linespacing=1.4)


def style_3d_axes(ax) -> None:
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((1, 1, 1, 0))
        axis.pane.set_edgecolor(GRID)
        axis.line.set_color(BASE)
    ax.tick_params(colors=INK2, labelsize=7.5)


def clean_axes(ax, keep=("bottom", "left")) -> None:
    for side in ("top", "right", "bottom", "left"):
        ax.spines[side].set_visible(side in keep)
        if side in keep:
            ax.spines[side].set_color(BASE)


# ---------------------------------------------------------------------------
# Figure 1: boundary sources of the BA1/BB1 comparisons on Lambda_N
# ---------------------------------------------------------------------------
def fig1_boundary_sources():
    ba1_path = R33 + "/forward/ba1/output/results.json"
    ba2_path = R33 + "/forward/ba2/output/results.json"
    ba1 = record("ba1", ba1_path)
    ba2 = record("ba2", ba2_path)
    sources = check_by_id(ba1, "boundary_sources_enumerated")
    distances = check_by_id(ba1, "boundary_distance_exact")["distances"]
    comparisons = ba1["headline"]["comparisons"]
    extra = ba2["headline"]["extra_faces"]
    formula = extra["count"]
    in_gate("ba2", formula + " extra faces")
    rows = sources["sources"]
    sizes = sorted(rows, key=int)
    for n in sizes:
        row = rows[n]
        require(row["F1_vs_F2_extra_faces"] == row["F1_vs_F2_formula_28N_5N_plus_1"] == extra["N" + n],
                "extra-face enumeration disagrees between BA1 and BA2 at N=" + n)
    nested_f1 = comparisons["F1 on Lambda_N versus F1 on Lambda_{N+1}"]
    nested_f2 = comparisons["F2 on Lambda_N versus F2 on Lambda_{N+1}"]
    same_n = comparisons["F1 versus F2 on the same Lambda_N"]
    require(nested_f1["source_set"] == nested_f2["source_set"], "nested source sets differ")

    demo = "3"  # display choice: the middle recorded box size
    require(demo in distances and demo in rows, "demo box size not recorded")
    n = int(demo)
    dist = distances[demo]
    # Geometric sanity of the drawing against the recorded distances (l-infinity).
    require(max(0, abs(n - 1)) == dist["layer_e_z"] and n == dist["layer_0"], "layer distances")
    require(max(0, abs(n + 1 - 1)) == dist["shell_e_z"] and n + 1 == dist["shell_0"], "shell distances")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.6, 6.2), gridspec_kw={"width_ratios": [1.0, 1.15]})

    # (a) x-z slice (y=0) of the coarse lattice for the demo box.
    cats = {"interior": [], "layer": [], "shell": []}
    for x in range(-(n + 1), n + 2):
        for z in range(-(n + 1), n + 2):
            m = max(abs(x), abs(z))
            if (x, z) in ((0, 0), (0, 1)):
                continue
            cats["interior" if m < n else "layer" if m == n else "shell"].append((x, z))
    ax1.add_patch(Rectangle((-n - 0.5, -n - 0.5), 2 * n + 1, 2 * n + 1, fill=False, edgecolor=BASE, linewidth=1.0))
    ax1.scatter(*zip(*cats["interior"]), s=26, color=BASE, zorder=2)
    ax1.scatter(*zip(*cats["layer"]), s=58, color=C_ORANGE, edgecolor=SURFACE, linewidth=1.2, zorder=3)
    ax1.scatter(*zip(*cats["shell"]), s=58, color=C_BLUE, edgecolor=SURFACE, linewidth=1.2, zorder=3)
    ax1.scatter([0, 0], [0, 1], s=120, marker="s", color=INK, edgecolor=SURFACE, linewidth=1.4, zorder=4)
    box = dict(boxstyle="round,pad=0.18", facecolor=SURFACE, edgecolor="none", alpha=0.9)
    ax1.text(-0.28, 0.0, "0", fontsize=9, color=INK, va="center", ha="right", bbox=box, zorder=6)
    ax1.text(-0.28, 1.0, "e_z", fontsize=9, color=INK, va="center", ha="right", bbox=box, zorder=6)
    ax1.annotate("", xy=(0.2, n), xytext=(0.2, 1), zorder=5,
                 arrowprops=dict(arrowstyle="<->", color=C_ORANGE, lw=1.6, shrinkA=5, shrinkB=5))
    ax1.annotate("", xy=(0.42, n + 1), xytext=(0.42, 1), zorder=5,
                 arrowprops=dict(arrowstyle="<->", color=C_BLUE, lw=1.6, shrinkA=5, shrinkB=5))
    ax1.text(0.58, n - 0.5, f"to (0,0,N): d∞ = N−1 = {dist['layer_e_z']}", fontsize=8.2, color=INK,
             ha="left", va="center", bbox=box, zorder=6)
    ax1.text(0.58, n + 0.5, f"to (0,0,N+1): d∞ = N = {dist['shell_e_z']}", fontsize=8.2, color=INK,
             ha="left", va="center", bbox=box, zorder=6)
    ax1.set_xlim(-n - 1.7, n + 1.7)
    ax1.set_ylim(-n - 1.7, n + 2.1)
    ax1.set_aspect("equal")
    ax1.set_xticks(range(-n - 1, n + 2))
    ax1.set_yticks(range(-n - 1, n + 2))
    ax1.set_xlabel("coarse x  (slice y = 0)")
    ax1.set_ylabel("coarse z")
    ax1.tick_params(labelsize=7.8, length=0)
    clean_axes(ax1, keep=())
    ax1.set_title(f"(a) Λ_N = [−N,N]³ at N = {n}: where the new terms sit", fontsize=10, color=INK2, loc="left")
    ax1.legend(
        handles=[
            Line2D([0], [0], marker="s", color=INK, linestyle="None", markersize=8, label="cover R = {0, e_z}"),
            Line2D([0], [0], marker="o", color=C_BLUE, linestyle="None", markersize=8,
                   label="shell Λ_{N+1}∖Λ_N: nested comparisons"),
            Line2D([0], [0], marker="o", color=C_ORANGE, linestyle="None", markersize=8,
                   label="outer layer max|b_i| = N: F1 vs F2"),
            Line2D([0], [0], marker="o", color=BASE, linestyle="None", markersize=6, label="interior of Λ_N"),
        ],
        loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2, fontsize=8.0,
    )

    # (b) enumerated source terms, all in face units.
    series = [
        ("F1_nested_new_faces", "F1: Λ_N vs Λ_{N+1}  (new whole stars, as faces)", C_BLUE),
        ("F2_nested_new_faces", "F2: Λ_N vs Λ_{N+1}  (new faces)", C_AQUA),
        ("F1_vs_F2_extra_faces", f"F1 vs F2 on the same Λ_N  (extra faces, {formula})", C_ORANGE),
    ]
    height = 0.26
    ymax = 0
    yticks, ylabels = [], []
    for gi, size in enumerate(sizes):
        base_y = (len(sizes) - 1 - gi) * 1.2
        yticks.append(base_y)
        ylabels.append(f"N = {size}")
        row = rows[size]
        for si, (key, _, color) in enumerate(series):
            y = base_y + (1 - si) * (height + 0.04)
            value = row[key]
            ax2.barh(y, value, height=height, color=color, edgecolor=SURFACE, linewidth=0)
            note = f"{value}"
            if key == "F1_nested_new_faces":
                note += f"  ({row['F1_nested_new_stars']} new stars)"
            ax2.text(value + 150, y, note, va="center", ha="left", fontsize=8.0, color=INK)
            ymax = max(ymax, value)
    ax2.set_yticks(yticks)
    ax2.set_yticklabels(ylabels, fontsize=9)
    ax2.tick_params(axis="y", length=0)
    ax2.set_xlim(0, ymax * 1.38)
    ax2.set_xlabel("number of source terms (faces), exact enumeration")
    ax2.grid(axis="x", color=GRID, linewidth=0.6)
    ax2.set_axisbelow(True)
    clean_axes(ax2, keep=("bottom",))
    ax2.set_title("(b) enumerated boundary sources per comparison", fontsize=10, color=INK2, loc="left")
    ax2.legend(handles=[Patch(facecolor=c, label=lab) for _, lab, c in series],
               loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=1, fontsize=8.0)
    ax2.text(
        0.99, 0.02,
        f"nested: every new term meets the shell (d∞ ≥ N from e_z)\n"
        f"same N: every extra face lies in the outer layer (d∞ ≥ N−1 from e_z)",
        transform=ax2.transAxes, ha="right", va="bottom", fontsize=7.8, color=INK2,
        bbox=dict(boxstyle="round,pad=0.3", facecolor=SURFACE, edgecolor=GRID),
    )

    fig.suptitle(f"Round33 BA1/BB1 boundary sources on Λ_N — {PRESENTATION_NOTE}", fontsize=11, color=INK, y=0.985)
    footer(fig, f"Counts and distances: {ba1_path} (checks boundary_sources_enumerated, boundary_distance_exact); "
                f"{formula}: {ba2_path}.")
    fig.subplots_adjust(left=0.05, right=0.97, top=0.9, bottom=0.27, wspace=0.18)

    caption = (
        f"{PRESENTATION_NOTE} (a) An x–z slice (y=0) of the centered coarse cube Λ_N at N={n} with the cover "
        f"R={{0,e_z}}, the outer layer max|b_i|=N (source set of the F1-versus-F2 comparison: "
        f"{same_n['new_terms']}) and the shell Λ_(N+1)∖Λ_N (source set of both nested comparisons); the recorded "
        f"l-infinity distances from e_z are N−1={dist['layer_e_z']} to the layer and N={dist['shell_e_z']} to the shell. "
        f"(b) Exact enumerations for N=" + ", ".join(sizes) + ": F1 nested new faces "
        + ", ".join(str(rows[s]['F1_nested_new_faces']) for s in sizes)
        + " (" + ", ".join(str(rows[s]['F1_nested_new_stars']) for s in sizes) + " new stars), F2 nested new faces "
        + ", ".join(str(rows[s]['F2_nested_new_faces']) for s in sizes) + ", F1-versus-F2 extra faces "
        + ", ".join(str(rows[s]['F1_vs_F2_extra_faces']) for s in sizes) + f" = {formula}."
    )
    return fig, {"title": "Boundary sources of the BA1/BB1 comparisons on Λ_N", "caption": caption}


# ---------------------------------------------------------------------------
# Figure 2: admitted rate curves and the BB2 item-5 bracket against N
# ---------------------------------------------------------------------------
def fig2_rate_curves():
    bb1_path = R33 + "/skeptic/bb1.json"
    bb2_path = R33 + "/skeptic/bb2.json"
    bb1 = record("bb1", bb1_path)["recommended_bound"]
    bb2 = record("bb2", bb2_path)["recommended_bound"]
    bb2_fwd = record("bb2", R33 + "/forward/bb2/output/results.json")["headline"]

    C = Fraction(bb1["C"]["value"])
    q = Fraction(bb1["C"]["q"])
    Cp = Fraction(bb2["C_prime"]["value"])
    cps = Fraction(bb2["c_site_prime"]["value"])
    Cdyn = Fraction(bb2["C_dyn"]["value"])
    require(Fraction(bb2["q"]) == q, "BB1 and BB2 q differ")
    require(Fraction(bb2_fwd["C_prime"]["value"]) == Cp and Fraction(bb2_fwd["c_site_prime"]["value"]) == cps
            and Fraction(bb2_fwd["C_dyn"]["value"]) == Cdyn, "BB2 review and forward constants differ")
    in_gate("bb1", "C=" + bb1["C"]["value"], "q=" + bb1["C"]["q"])
    in_gate("bb2", "C'=" + bb2["C_prime"]["value"], "c'_site=" + bb2["c_site_prime"]["value"],
            "C_dyn=" + bb2["C_dyn"]["value"])
    item5 = bb2["item5"]
    lo, hi = map(int, re.fullmatch(r"(\d+)<=N<=(\d+)", item5["certified_rate_range"]).groups())
    vacuous = int(item5["vacuous_from"])
    below = int(item5["below_2_through"])
    require(below + 1 == vacuous, "recorded below-2 range and vacuous start disagree")
    in_gate("bb2", item5["certified_rate_range"], f"N={vacuous}", f"N={below}")
    require(item5["bracket"] == "C_dyn/(r_N-1) + c'_site |Lambda_{r_N}| e^{|Lambda_{r_N}|/10^8} q^(N-r_N) + 2C' q^(N-1)",
            "recorded bracket formula changed; update the preview below")
    in_gate("bb2", "r_N=floor((N-1)/2)")

    lq, lC, lCp, lcps, lCdyn = map(log10_frac, (q, C, Cp, cps, Cdyn))
    log10e = math.log10(math.e)

    def r_N(N):  # frozen rule quoted from the gate: r_N = floor((N-1)/2)
        return (N - 1) // 2

    def bracket_terms(N):
        r = r_N(N)
        lam = (2 * r + 1) ** 3  # |Lambda_r| for the centered cube [-r, r]^3
        dyn = lCdyn - math.log10(r - 1)
        region = lcps + math.log10(lam) + (lam / 10 ** 8) * log10e + (N - r) * lq
        rterm = math.log10(2) + lCp + (N - 1) * lq
        return dyn, region, rterm

    def bracket(N):
        return log10_sum(*bracket_terms(N))

    n_max = 20000
    log2 = math.log10(2)
    first = next(N for N in range(lo, n_max + 1) if bracket(N) >= log2)
    require(first == vacuous, f"preview first exceedance {first} differs from the recorded {vacuous}")
    require(all(bracket(N) >= log2 for N in range(vacuous, n_max + 1)), "preview bracket dips below 2 past the record")
    for N, key in ((5, "bracket_N5_preview"), (10, "bracket_N10_preview")):
        require(abs(10 ** bracket(N) / float(item5[key]) - 1) < 1e-5, "preview bracket disagrees at N=%d" % N)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.8, 6.0), gridspec_kw={"width_ratios": [1.45, 1.0]})
    y_lo, y_hi = -32, 6

    Ns = list(range(2, n_max + 1))
    ax1.plot(Ns, [lC + (N - 1) * lq for N in Ns], color=C_BLUE, linewidth=2.0)
    ax1.plot(Ns, [lCp + (N - 1) * lq for N in Ns], color=C_ORANGE, linewidth=2.0)
    Nb = list(range(lo, n_max + 1))
    ax1.plot(Nb, [bracket(N) for N in Nb], color=INK, linewidth=2.0)
    ax1.axvspan(lo, hi, color=C_AQUA, alpha=0.10, linewidth=0)
    ax1.axvspan(vacuous, n_max, color=STATUS_CRITICAL, alpha=0.10, linewidth=0)
    ax1.axhline(log2, color=INK2, linewidth=0.9)
    ax1.text(2.1, log2 + 0.5, "2 (the trivial bound; the bracket is vacuous at or above it)", fontsize=7.8, color=INK2)
    ax1.set_xscale("log")
    ax1.set_xlim(2, n_max)
    ax1.set_ylim(y_lo, y_hi)
    ax1.yaxis.set_major_locator(MultipleLocator(4))
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda v, _: "$10^{%d}$" % v))
    ax1.set_xlabel("box size N (coarse steps, fixed spacing; log scale)")
    ax1.set_ylabel("bound (log scale)")
    ax1.grid(True, which="major", color=GRID, linewidth=0.6)
    clean_axes(ax1)
    label_box = dict(boxstyle="round,pad=0.15", facecolor=SURFACE, edgecolor="none", alpha=0.9)
    for level, const, text in ((-22.0, lCp, f"C′ q^(N−1), C′={bb2['C_prime']['value']}  (BB2)"),
                               (-27.0, lC, f"C q^(N−1), C≈{sci(bb1['C']['preview'])}  (BB1)")):
        n_at = 1 + (level - const) / lq  # where the curve crosses this level
        ax1.annotate(text, xy=(n_at * 1.04, level), xytext=(n_at * 1.9, level), fontsize=8.0, color=INK,
                     va="center", bbox=label_box, arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
    ax1.text(40, bracket(40) + 1.0, "BB2 item-5 bracket (float preview)", fontsize=8.2, color=INK, bbox=label_box)
    ax1.text(math.sqrt(lo * hi) * 0.6, y_lo + 1.3, f"certified rate range {lo} ≤ N ≤ {hi}", fontsize=8.2,
             color=INK, ha="center", bbox=label_box)
    ax1.text(n_max * 0.93, y_lo + 5.0, f"vacuous\nfrom\nN = {vacuous}", fontsize=8.0, color=INK, ha="right",
             bbox=label_box)
    ax1.set_title(f"(a) admitted rates at q = {bb1['C']['q']} and the item-5 bracket", fontsize=10, color=INK2,
                  loc="left")
    ax1.legend(
        handles=[
            Line2D([0], [0], color=C_BLUE, linewidth=2.2, label="C q^(N−1): F1/F2 densities on R (BB1)"),
            Line2D([0], [0], color=C_ORANGE, linewidth=2.2, label="C′ q^(N−1): whole-sequence Cauchy bound (BB2)"),
            Line2D([0], [0], color=INK, linewidth=2.2, label="item-5 bracket, correlation functions (BB2)"),
            Patch(facecolor=C_AQUA, alpha=0.25, label=f"certified O(1/N) range {lo} ≤ N ≤ {hi}"),
            Patch(facecolor=STATUS_CRITICAL, alpha=0.25, label=f"bracket ≥ 2 (vacuous) from N = {vacuous}"),
            Patch(facecolor=STATUS_WARNING, alpha=0.3, label=f"{hi + 1} ≤ N ≤ {below}: below 2, no rate (in b)"),
        ],
        loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=2, fontsize=7.9,
    )

    # (b) zoom on the end of the certified range and the first exceedance.
    z_lo, z_hi = vacuous - 31, vacuous + 12
    Nz = list(range(z_lo, z_hi + 1))
    require(z_lo > hi, "zoom window must lie past the certified range")
    ax2.axvspan(z_lo - 1, vacuous - 0.5, color=STATUS_WARNING, alpha=0.12, linewidth=0)
    ax2.axvspan(vacuous - 0.5, z_hi + 1, color=STATUS_CRITICAL, alpha=0.10, linewidth=0)
    ax2.plot(Nz, [bracket_terms(N)[1] for N in Nz], color=C_AQUA, linewidth=1.6)
    ax2.plot(Nz, [bracket(N) for N in Nz], "o", color=INK, markersize=2.6)
    ax2.axhline(log2, color=INK2, linewidth=0.9)
    ax2.axvline(vacuous, color=INK2, linewidth=0.9)
    ax2.set_xlim(z_lo - 1, z_hi + 1)
    ax2.xaxis.set_major_locator(MultipleLocator(10))
    ax2.set_ylim(-18, 14)
    ax2.yaxis.set_major_locator(MultipleLocator(4))
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda v, _: "$10^{%d}$" % v))
    ax2.set_xlabel("box size N (linear)")
    ax2.grid(True, which="major", color=GRID, linewidth=0.6)
    clean_axes(ax2)
    ax2.text(vacuous - 1.5, 9.5, f"first N with\nbracket ≥ 2:\nN = {vacuous}", fontsize=8.0, color=INK, ha="right",
             bbox=label_box)
    ax2.text(z_lo, -16.3, f"{hi + 1} ≤ N ≤ {below}: below 2, no rate", fontsize=7.8, color=INK, bbox=label_box)
    ax2.text(z_hi, 9.5, "vacuous", fontsize=7.8, color=INK, ha="right", bbox=label_box)
    ax2.set_title("(b) zoom: parity sawtooth of r_N = ⌊(N−1)/2⌋", fontsize=10, color=INK2, loc="left")
    ax2.legend(
        handles=[
            Line2D([0], [0], marker="o", color=INK, linestyle="None", markersize=4, label="item-5 bracket at integer N"),
            Line2D([0], [0], color=C_AQUA, linewidth=1.8, label="region term c′_site|Λ_r|e^{|Λ_r|/10⁸}q^(N−r)"),
        ],
        loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=1, fontsize=7.9,
    )

    fig.suptitle(f"Round33 rates in N and the BB2 item-5 bracket — {PRESENTATION_NOTE}", fontsize=11, color=INK,
                 y=0.985)
    footer(fig, f"Constants and ranges: {bb1_path}, {bb2_path} (recommended_bound). "
                "Curves are float previews in log space, not certificates.")
    fig.subplots_adjust(left=0.07, right=0.98, top=0.9, bottom=0.27, wspace=0.16)

    caption = (
        f"{PRESENTATION_NOTE} (a) Against the box size N (log scale): the BB1 locality rate C q^(N−1) "
        f"(C≈{sci(bb1['C']['preview'])}, q={bb1['C']['q']}), the BB2 whole-sequence bound C′ q^(N−1) "
        f"(C′={bb2['C_prime']['value']}) and the BB2 item-5 bracket {item5['bracket']} with "
        f"C_dyn={bb2['C_dyn']['value']} and c′_site={bb2['c_site_prime']['value']}, drawn as a log-space float "
        f"preview of the recorded constants. The certified O(1/N) range {lo}≤N≤{hi} is shaded; the bracket stays "
        f"below 2 through N={below} and is at least 2 (vacuous) from N={vacuous}, where the preview reproduces "
        f"the recorded first exceedance. (b) Zoom on {z_lo}≤N≤{z_hi}: the region term overtakes the dynamics term "
        f"and alternates with the parity of N through r_N=⌊(N−1)/2⌋."
    )
    return fig, {"title": "Rates in N and the BB2 item-5 bracket", "caption": caption}


# ---------------------------------------------------------------------------
# Figure 3: BD1 gauge-group transfer ledger
# ---------------------------------------------------------------------------
def fig3_gauge_group_ledger():
    fwd_path = R33 + "/forward/bd1/output/results.json"
    rev_path = R33 + "/reverse/bd1/output/results.json"
    fwd = record("bd1", fwd_path)
    rev = record("bd1", rev_path)
    groups_text = re.search(r"for G in \{([^}]*)\}", gate("bd1")["accepted"]).group(1)
    groups = [g.strip() for g in groups_text.split(",")]
    ledger = {(row["group"], row["equation"]): row for row in fwd["transfer_ledger"]}
    moments = fwd["headline"]["moment_table"]

    rows = []
    for g in groups:
        flip = ledger[(g, "flip_lemma")]
        parity = ledger[(g, "parity_theorem")]
        first = ledger[(g, "first_order_coefficient")]["value"]
        require(rev["first_order_coefficients"][g]["value"] == first, "first-order coefficient disagrees " + g)
        require(rev["moment_table"][g]["E[W^3]"]["value"] == parity["E_W3"] == moments[g]["3"], "E[W^3] disagrees " + g)
        require(rev["moment_table"][g]["E[W^2]"]["value"] == moments[g]["2"], "E[W^2] disagrees " + g)
        centre = rev["centre"][g]
        require(centre["central_minus_one"] == (flip["status"] == "transfer_to_named_model"), "centre/flip " + g)
        rows.append({
            "group": g, "element": centre["element"], "E2": moments[g]["2"], "E3": parity["E_W3"], "first": first,
            "flip": flip, "parity": parity,
        })
    in_gate("bd1", "(" + ", ".join(r["first"] for r in rows[:-1]) + " and " + rows[-1]["first"] + " in that order)")

    def element_text(e):
        return "none" if e is None else e.split(" (")[0]

    def status_cell(row):
        if row["status"] == "transfer_to_named_model":
            return ("✓", STATUS_GOOD, "transfers", "")
        require(row["status"] == "obstruction_recorded", "unexpected ledger status " + row["status"])
        cx = row["counterexample"]
        if row["equation"] == "flip_lemma":
            detail = f"order-{cx['order']} coefficient of ω(W): {cx['value']}"
        else:
            detail = f"dω(W²)/dτ at first order: {cx['value']}"
        return ("✕", STATUS_CRITICAL, "obstruction recorded", detail)

    headers = ["Group", "central element\nacting as −1", "E[W²]", "E[W³]", "ω(W)/τ at\nfirst order",
               "link-flip lemma", "first-order parity (E[W³]=0)"]
    widths = [0.07, 0.13, 0.065, 0.065, 0.11, 0.28, 0.28]
    xs = [0.0]
    for w in widths[:-1]:
        xs.append(xs[-1] + w)

    fig, ax = plt.subplots(figsize=(13.2, 6.4))
    ax.set_xlim(0, 1)
    n_rows = len(rows)
    ax.set_ylim(-0.4, n_rows + 1.1)
    ax.axis("off")
    top = n_rows + 0.55
    for x, head in zip(xs, headers):
        ax.text(x + 0.008, top, head, fontsize=8.8, color=INK2, va="center", ha="left", fontweight="bold")
    ax.plot([0, 1], [n_rows + 0.05, n_rows + 0.05], color=BASE, linewidth=1.0)
    for i, row in enumerate(rows):
        y = n_rows - 0.5 - i
        if i % 2 == 0:
            ax.add_patch(Rectangle((0, y - 0.5), 1, 1, facecolor="#f3f2ee", edgecolor="none", zorder=0))
        ax.text(xs[0] + 0.008, y, row["group"], fontsize=10, color=INK, va="center", fontweight="bold")
        ax.text(xs[1] + 0.008, y, element_text(row["element"]), fontsize=9, color=INK, va="center")
        ax.text(xs[2] + 0.008, y, row["E2"], fontsize=9, color=INK, va="center", family="DejaVu Sans Mono")
        ax.text(xs[3] + 0.008, y, row["E3"], fontsize=9, color=INK, va="center", family="DejaVu Sans Mono")
        ax.text(xs[4] + 0.008, y, row["first"], fontsize=9.5, color=INK, va="center", family="DejaVu Sans Mono")
        for col, entry in ((5, row["flip"]), (6, row["parity"])):
            icon, color, label, detail = status_cell(entry)
            ax.text(xs[col] + 0.008, y + (0.16 if detail else 0), icon, fontsize=11, color=color, va="center",
                    fontweight="bold")
            ax.text(xs[col] + 0.03, y + (0.16 if detail else 0), label, fontsize=9, color=INK, va="center")
            if detail:
                ax.text(xs[col] + 0.03, y - 0.2, detail, fontsize=7.9, color=INK2, va="center",
                        family="DejaVu Sans Mono")
    ax.plot([0, 1], [-0.02, -0.02], color=BASE, linewidth=1.0)
    ax.text(0.0, -0.22, textwrap.fill(
            "Flip lemma: transfers exactly when a central element acts as −1 on the Wilson representation. "
            "First-order parity: transfers exactly when E[W³]=0. Coefficients agree between the characters "
            "route (forward) and Weyl integration (reverse).", width=200),
            fontsize=7.9, color=INK2, va="top")

    fig.suptitle(f"Round33 BD1 transfer ledger across gauge groups — {PRESENTATION_NOTE}", fontsize=11, color=INK,
                 y=0.975)
    footer(fig, f"Values: {fwd_path} (transfer_ledger, headline.moment_table), cross-checked against {rev_path}. "
                "One-plaquette graphs and group box models only.")
    fig.subplots_adjust(left=0.03, right=0.985, top=0.9, bottom=0.1)

    transfers = [r["group"] for r in rows if r["flip"]["status"] == "transfer_to_named_model"]
    parity_ok = [r["group"] for r in rows if r["parity"]["status"] == "transfer_to_named_model"]
    caption = (
        f"{PRESENTATION_NOTE} For G in {{{groups_text}}}: the central element acting as −1 on the Wilson "
        f"representation (if any), the Haar moments E[W²] and E[W³], the exact first-order coefficient of ω(W)/τ ("
        + ", ".join(f"{r['group']} {r['first']}" for r in rows)
        + f"), and the ledger status of the link-flip lemma (transfers: {', '.join(transfers)}) and of the "
        f"first-order parity theorem (transfers: {', '.join(parity_ok)}); every obstruction cell shows its exact "
        f"nonzero coefficient. Statements about one-plaquette finite graphs and group box models, not AM2 or "
        f"continuum statements for other groups."
    )
    return fig, {"title": "BD1 transfer ledger across gauge groups", "caption": caption}


# ---------------------------------------------------------------------------
# Figure 4: route A versus route B incidence on R
# ---------------------------------------------------------------------------
def cube_faces(center, half=0.5):
    cx, cy, cz = center
    p = {(sx, sy, sz): (cx + sx * half, cy + sy * half, cz + sz * half)
         for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)}
    return [
        [p[(-1, -1, -1)], p[(1, -1, -1)], p[(1, 1, -1)], p[(-1, 1, -1)]],
        [p[(-1, -1, 1)], p[(1, -1, 1)], p[(1, 1, 1)], p[(-1, 1, 1)]],
        [p[(-1, -1, -1)], p[(-1, 1, -1)], p[(-1, 1, 1)], p[(-1, -1, 1)]],
        [p[(1, -1, -1)], p[(1, 1, -1)], p[(1, 1, 1)], p[(1, -1, 1)]],
        [p[(-1, -1, -1)], p[(1, -1, -1)], p[(1, -1, 1)], p[(-1, -1, 1)]],
        [p[(-1, 1, -1)], p[(1, 1, -1)], p[(1, 1, 1)], p[(-1, 1, 1)]],
    ]


def tetra_faces(center, half=0.26):
    cx, cy, cz = center
    v = [(cx + half, cy + half, cz + half), (cx + half, cy - half, cz - half),
         (cx - half, cy + half, cz - half), (cx - half, cy - half, cz + half)]
    return [[v[0], v[1], v[2]], [v[0], v[1], v[3]], [v[0], v[2], v[3]], [v[1], v[2], v[3]]]


def coord_label(a):
    names = []
    for value, axis in zip(a, ("e_x", "e_y", "e_z")):
        if value == 1:
            names.append(("+" if names else "") + axis)
        elif value == -1:
            names.append("−" + axis)
    return "".join(names) or "0"


def fig4_route_incidence():
    path = R33 + "/forward/bc2/output/results.json"
    bc2 = record("bc2", path)
    inc = check_by_id(bc2, "route_b_incidence_on_R")
    marg = check_by_id(bc2, "route_b_first_order_R_marginal")["record"]
    size = sorted(k for k in inc if re.fullmatch(r"N\d+", k))[0]
    table = inc[size]
    stars = [row for row in table["table"] if row["group"] == "star"]
    singles = [row for row in table["table"] if row["group"] == "single"]
    require(len(stars) == table["stars"] and len(singles) == table["singles"], "incidence counts")
    require(sum(r["meeting_R"] for r in stars + singles) == table["meeting_R"], "meeting_R total")
    require(sum(r["inside_R"] for r in stars + singles) == table["inside_R"] == marg["faces_moving_rho_R_at_first_order"],
            "inside_R total")
    route_a_inside = sum(r["inside_R"] for r in stars)
    require(route_a_inside == marg["omitted_with_owner_set_R"] == table["omitted_inside_R"], "route-A inside count")
    require(sum(r["inside_R"] for r in singles) == marg["selected_single_sites"] == table["selected_inside_R"],
            "selected inside count")
    route_a_meeting = sum(r["meeting_R"] for r in stars)
    cover = [tuple(r["anchor"]) for r in singles]
    require(bc2["cover"] == "R={0,e_z}" and sorted(cover) == [(0, 0, 0), (0, 0, 1)], "cover R")
    in_gate("bc2", "cover R={0,e_z}", "21 omitted faces", "3 selected faces")

    fig = plt.figure(figsize=(13.4, 6.6))
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    ax.set_proj_type("ortho")
    style_3d_axes(ax)
    for c in cover:
        ax.add_collection3d(Poly3DCollection(cube_faces(c, 0.42), facecolor=C_BLUE, edgecolor=C_BLUE, alpha=0.08,
                                             linewidths=0.8))
    label_box = dict(boxstyle="round,pad=0.12", facecolor=SURFACE, edgecolor="none", alpha=0.8)
    for row in stars:
        a = tuple(row["anchor"])
        ax.add_collection3d(Poly3DCollection(tetra_faces(a, 0.24), facecolor=C_MAGENTA, edgecolor=C_MAGENTA,
                                             alpha=0.35, linewidths=0.7))
        ax.text(a[0] - 0.05, a[1] - 0.05, a[2] + 0.36, coord_label(a), fontsize=7.4, color=INK2, ha="center",
                bbox=label_box, zorder=8)
    for row in singles:
        a = tuple(row["anchor"])
        ax.scatter([a[0] + 0.3], [a[1] + 0.3], [a[2]], marker="D", s=70, color=C_AQUA, edgecolor=SURFACE,
                   linewidth=1.2, depthshade=False, zorder=9)
    ax.set_xlim(-1.6, 1.2)
    ax.set_ylim(-1.6, 1.2)
    ax.set_zlim(-1.6, 1.8)
    ax.set_box_aspect((1, 1, 1.2))
    ax.set_xlabel("coarse x")
    ax.set_ylabel("coarse y")
    ax.set_zlabel("coarse z")
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax.set_zticks([-1, 0, 1])
    ax.view_init(elev=16, azim=-50)
    ax.legend(
        handles=[
            Patch(facecolor=C_BLUE, alpha=0.3, label=f"cover R = {{0, e_z}}  ({len(cover)} factors)"),
            Patch(facecolor=C_MAGENTA, alpha=0.5, label=f"whole star meeting R  ({len(stars)}; routes A and B)"),
            Line2D([0], [0], marker="D", color=C_AQUA, linestyle="None", markersize=7,
                   label=f"single-factor group {{b}}, b ∈ R  ({len(singles)}; route B only)"),
        ],
        loc="upper left", bbox_to_anchor=(-0.02, 1.0), fontsize=8.0,
    )
    ax.set_title("(a) groups meeting the cover R", fontsize=10, color=INK2, loc="left", pad=2)

    ax2 = fig.add_subplot(1, 2, 2)
    order = sorted(stars, key=lambda r: (r["meeting_R"], r["anchor"])) + singles
    labels = [("star at " if r["group"] == "star" else "single group at ") + coord_label(r["anchor"]) for r in order]
    height = 0.36
    for i, row in enumerate(order):
        y = len(order) - 1 - i
        ax2.barh(y + height / 2 + 0.02, row["meeting_R"], height=height, color=C_BLUE, linewidth=0)
        ax2.barh(y - height / 2 - 0.02, row["inside_R"], height=height, color=C_ORANGE, linewidth=0)
        ax2.text(row["meeting_R"] + 0.3, y + height / 2 + 0.02, str(row["meeting_R"]), va="center", fontsize=8,
                 color=INK)
        ax2.text(row["inside_R"] + 0.3, y - height / 2 - 0.02, str(row["inside_R"]), va="center", fontsize=8,
                 color=INK)
    ax2.axhline(len(singles) - 0.5, color=INK2, linewidth=0.9)
    ax2.text(23.5, len(singles) - 0.42, "route B only ↓", fontsize=8, color=INK2, ha="right", va="bottom")
    ax2.set_yticks(range(len(order)))
    ax2.set_yticklabels(list(reversed(labels)), fontsize=8.4)
    ax2.tick_params(axis="y", length=0)
    ax2.set_xlim(0, 24)
    ax2.set_xlabel(f"faces per group (enumerated at {size[0]} = {size[1:]})")
    ax2.grid(axis="x", color=GRID, linewidth=0.6)
    ax2.set_axisbelow(True)
    clean_axes(ax2, keep=("bottom",))
    ax2.legend(handles=[Patch(facecolor=C_BLUE, label="faces meeting R"),
                        Patch(facecolor=C_ORANGE, label="faces inside R (move ρ_R at first order)")],
               loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2, fontsize=8.0)
    ax2.set_title("(b) incidence per group", fontsize=10, color=INK2, loc="left")
    ax2.text(
        0.98, 0.985,
        f"route A: {len(stars)} stars, {route_a_meeting} faces meet R, {route_a_inside} inside\n"
        f"route B: {len(stars)} stars + {len(singles)} single groups,\n"
        f"   {table['meeting_R']} faces meet R, {table['inside_R']} inside "
        f"({table['omitted_inside_R']} omitted + {table['selected_inside_R']} selected)",
        transform=ax2.transAxes, ha="right", va="top", fontsize=8.2, color=INK,
        bbox=dict(boxstyle="round,pad=0.4", facecolor=SURFACE, edgecolor=GRID),
    )

    fig.suptitle(f"Round33 BC2 route A versus route B incidence on R — {PRESENTATION_NOTE}", fontsize=11, color=INK,
                 y=0.975)
    footer(fig, f"Counts: {path} (checks route_b_incidence_on_R, route_b_first_order_R_marginal). "
                "Coarse positions schematic.")
    fig.subplots_adjust(left=0.02, right=0.97, top=0.9, bottom=0.17, wspace=0.25)

    caption = (
        f"{PRESENTATION_NOTE} (a) The cover R={{0,e_z}} with the {len(stars)} whole stars that meet it (anchors "
        + ", ".join(coord_label(r["anchor"]) for r in stars)
        + f") and, in route B only, the {len(singles)} single-factor groups at the two factors of R. (b) Faces "
        f"meeting R and faces inside R per group, enumerated at {size[0]}={size[1:]}: route A (zero-selected family, "
        f"no single-factor groups) has {route_a_meeting} faces meeting R and {route_a_inside} inside; route B "
        f"(uniform model) has {table['meeting_R']} meeting and {table['inside_R']} inside "
        f"({table['omitted_inside_R']} omitted faces with owner set R plus {table['selected_inside_R']} selected "
        f"faces), the {table['inside_R']} faces that move ρ_R at first order."
    )
    return fig, {"title": "Route A versus route B incidence on R", "caption": caption}


# ---------------------------------------------------------------------------
# Figure 5: the two-plaquette graph with independent couplings and the 1x2 loop
# ---------------------------------------------------------------------------


def monomial(m: int, n: int) -> str:
    def power(var, k):
        if k == 0:
            return ""
        return var + ("" if k == 1 else superscript(k))
    return power("l₁", m) + power("l₂", n)


def polynomial(table: dict) -> str:
    terms = sorted(((int(k.split(",")[0]), int(k.split(",")[1]), v) for k, v in table.items()),
                   key=lambda t: (t[0] + t[1], -t[0]))
    out = ""
    for m, n, value in terms:
        frac = Fraction(value)
        require(frac != 0, "zero entry in a nonzero table")
        sign = "−" if frac < 0 else "+"
        body = f"{abs(frac.numerator)}/{frac.denominator}" if frac.denominator != 1 else str(abs(frac.numerator))
        out += (("−" if sign == "−" else "") if not out else f" {sign} ") + f"{body}·{monomial(m, n)}"
    return out


def fig5_two_plaquette():
    res_path = R33 + "/forward/bd2/output/results.json"
    rep_path = R33 + "/forward/bd2/report.md"
    head = record("bd2", res_path)["headline"]
    report = bound("bd2", rep_path).read_text(encoding="utf-8")
    link_text = re.search(r"links (h1 \(.*?\))\. Round11", report).group(1)
    links = re.findall(r"(\w+) \((\w+)→(\w+)\)", link_text)
    squares = {
        name: re.findall(r"(h\d|v[LMR])", body)
        for body, name in re.findall(r"`[UV] = ([^`]+)` \((square \d)\)", report)
    }
    require(len(links) == 7 and len(squares) == 2, "graph not parsed from the BD2 report")
    shared = sorted(set(squares["square 1"]) & set(squares["square 2"]))
    require(len(shared) == 1, "the two squares must share exactly one link")
    shared = shared[0]
    tables = head["coefficient_tables_nonzero"]
    parities = head["parities"]
    require(head["z_sign_certified_all_grid_points"] is True, "z sign record")
    in_gate("bd2", "<z> = 7 l1 l2/216", "D=6 and D=8")

    col = {"L": 0, "M": 1, "R": 2}
    pos = {v: (col[v[1]], 1 if v[0] == "T" else 0) for _, a, b in links for v in (a, b)}

    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(13.0, 5.6), gridspec_kw={"width_ratios": [1.0, 1.25]})
    face_color = {"square 1": C_BLUE, "square 2": C_AQUA}
    for sq, lk in squares.items():
        xs_ = [pos[v][0] for name, a, b in links if name in lk for v in (a, b)]
        x0 = min(xs_)
        ax.add_patch(Rectangle((x0, 0), 1, 1, facecolor=face_color[sq], alpha=0.12, edgecolor="none", zorder=0))
    ax.add_patch(FancyBboxPatch((-0.14, -0.14), 2.28, 1.28, boxstyle="round,pad=0,rounding_size=0.08",
                                fill=False, edgecolor=C_MAGENTA, linewidth=2.2, zorder=1))
    for name, a, b in links:
        (x0, y0), (x1, y1) = pos[a], pos[b]
        is_shared = name == shared
        ax.plot([x0, x1], [y0, y1], color=C_ORANGE if is_shared else INK2, linewidth=4.0 if is_shared else 2.0,
                solid_capstyle="round", zorder=2)
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        vertical = x0 == x1
        right_edge = vertical and x0 == max(x for x, _ in pos.values())
        ox, oy = ((-0.08 if right_edge else 0.08), 0.0) if vertical else (0.0, 0.08)
        ax.text(mx + ox, my + oy, name, fontsize=9.5, color=INK,
                ha=("right" if right_edge else "left") if vertical else "center", va="center", zorder=4)
    for v, (x, y) in pos.items():
        ax.plot(x, y, "o", color=INK, markersize=8, markeredgecolor=SURFACE, markeredgewidth=1.2, zorder=3)
        ax.text(x, y + (0.25 if y == 1 else -0.27), v, fontsize=8.6, color=INK2, ha="center", va="center")
    ax.text(0.5, 0.5, "face 1\n−l₁ W₁", fontsize=10, color=INK, ha="center", va="center")
    ax.text(1.5, 0.5, "face 2\n−l₂ W₂", fontsize=10, color=INK, ha="center", va="center")
    ax.set_xlim(-0.45, 2.45)
    ax.set_ylim(-0.6, 1.6)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.legend(
        handles=[
            Patch(facecolor=C_BLUE, alpha=0.3, label="face 1, coupling l₁"),
            Patch(facecolor=C_AQUA, alpha=0.3, label="face 2, coupling l₂"),
            Line2D([0], [0], color=C_ORANGE, linewidth=4, label=f"shared link {shared}: C_shared"),
            Line2D([0], [0], color=C_MAGENTA, linewidth=2.2, label=f"1×2 loop z = ½Tr(UV) ({shared} cancels)"),
        ],
        loc="upper center", bbox_to_anchor=(0.5, 0.02), ncol=2, fontsize=8.0,
    )
    ax.set_title("(a) H_FG(l₁,l₂) = K − l₁W₁ − l₂W₂ on the Round11 graph", fontsize=10, color=INK2, loc="left")

    ax2.axis("off")
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_title("(b) exact coefficients through total order 4", fontsize=10, color=INK2, loc="left")
    entries = [("⟨W₁⟩", "W_1", C_BLUE), ("⟨z⟩", "z", C_MAGENTA), ("⟨C_shared⟩", "C_shared", C_ORANGE)]
    y = 0.9
    for label, key, color in entries:
        ax2.add_patch(Rectangle((0.0, y - 0.035), 0.012, 0.07, color=color, transform=ax2.transAxes))
        ax2.text(0.03, y, f"{label} = {polynomial(tables[key])}", fontsize=9.6, color=INK, va="center",
                 family="DejaVu Sans")
        ax2.text(0.03, y - 0.075, parities[key], fontsize=8.4, color=INK2, va="center")
        y -= 0.22
    ax2.text(0.0, y + 0.04,
             head["coefficient_index"] + ".\n"
             f"At l₁ = l₂ = l: ⟨z⟩ = {head['second_order_at_l1_eq_l2']['z']}·l² + …, "
             f"⟨C_shared⟩ = {head['second_order_at_l1_eq_l2']['C_shared']}·l² + …;\n"
             "the sign of ⟨z⟩ is certified positive at every recorded grid point.",
             fontsize=8.2, color=INK2, va="top")

    fig.suptitle(f"Round33 BD2 two-plaquette graph with independent couplings — {PRESENTATION_NOTE}", fontsize=11,
                 color=INK, y=0.975)
    footer(fig, f"Graph: {rep_path}; coefficients: {res_path} (headline). A finite graph, not the Z³ family.")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.88, bottom=0.12, wspace=0.08)

    caption = (
        f"{PRESENTATION_NOTE} (a) The Round11 open two-square patch ({len(pos)} vertices, {len(links)} links) with "
        f"independent couplings l₁ on face 1 and l₂ on face 2, the shared link {shared} (whose Casimir is C_shared) "
        f"and the 1×2 loop z around both faces. (b) The recorded exact coefficients: ⟨W₁⟩ = "
        f"{polynomial(tables['W_1'])}; ⟨z⟩ = {polynomial(tables['z'])}; ⟨C_shared⟩ = "
        f"{polynomial(tables['C_shared'])}; {head['coefficient_index']}. A finite graph, not the Z³ family."
    )
    return fig, {"title": "Two-plaquette graph with independent couplings and the 1×2 loop", "caption": caption}


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def save_all(fig, name: str):
    png_path = FIG_DIR / f"{name}.png"
    svg_path = FIG_DIR / f"{name}.svg"
    fig.savefig(png_path, format="png", dpi=200, facecolor=SURFACE, metadata={"Date": None})
    fig.savefig(svg_path, format="svg", facecolor=SURFACE, metadata={"Date": None})
    dist_path = DIST_DIR / f"{name}.png"
    shutil.copyfile(png_path, dist_path)
    plt.close(fig)
    return png_path, svg_path, dist_path


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    require(DIST_DIR.is_dir(), "dist/ is missing")

    builders = [
        ("r33-boundary-sources", fig1_boundary_sources),
        ("r33-rate-curves", fig2_rate_curves),
        ("r33-gauge-group-ledger", fig3_gauge_group_ledger),
        ("r33-route-incidence", fig4_route_incidence),
        ("r33-two-plaquette-couplings", fig5_two_plaquette),
    ]

    written, entries = [], []
    for name, builder in builders:
        fig, meta = builder()
        written.extend(save_all(fig, name))
        require(meta["caption"].startswith(PRESENTATION_NOTE), "caption must begin with the presentation note")
        entries.append({"path": f"{name}.png", "title": meta["title"], "caption": meta["caption"],
                        "source_path": SCRIPT})

    FIGURES_JSON.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    written.append(FIGURES_JSON)
    for path in written:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f"{digest}  {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
