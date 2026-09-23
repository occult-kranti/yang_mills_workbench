#!/usr/bin/env python3
"""Round32 presentation figures for the Yang-Mills workbench.

Every figure produced here is a schematic illustration of a Round32 setup
(geometry, kernel comparison, or a planning-notes error budget). NONE of
these figures carries admission weight and none computes, replays, or
certifies any admitted result: they are drawn directly from fixed integer
geometry and from decimal previews already written into the Round32
advisor/skeptic record. See research/round32/figures/README.md for the
source of every number and every geometric fact.

Determinism contract:
  - No network access, no external data files.
  - Only matplotlib and the standard library are imported.
  - `random.seed` is fixed even though no stochastic element is used, in
    case a later edit introduces one (defensive, not decorative).
  - `svg.hashsalt` is fixed so SVG clip-path/id hashes do not depend on
    Python object identity (matplotlib hashes content, not id(), once a
    salt string is set: backend_svg.RendererSVG._make_id).
  - `metadata={'Date': None}` is passed to every savefig call (PNG and
    SVG) so no build timestamp is embedded.
  - Font family is pinned to the bundled DejaVu Sans so text metrics do
    not depend on what is installed on the host.
  - Every PNG written under research/round32/figures/ is byte-copied
    (not re-rendered) into dist/, so the two copies are identical by
    construction and re-running the script twice can be checked with
    sha256 alone.

Run:  python3 -B research/round32/figures/make_figures.py
"""
from __future__ import annotations

import hashlib
import math
import random
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
from mpl_toolkits.mplot3d import Axes3D  # noqa: E402,F401  (registers 3d projection)
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection  # noqa: E402

random.seed(20260923)  # defensive; no stochastic element is used below

ROOT = Path(__file__).resolve().parents[3]
FIG_DIR = Path(__file__).resolve().parent
DIST_DIR = ROOT / "dist"

# ---------------------------------------------------------------------------
# Palette (dataviz skill reference palette, light mode; see references/palette.md)
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

STATUS_CRITICAL = "#d03b3b"

PRESENTATION_NOTE = "Presentation only; no admission weight."

plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans"],
        "font.size": 10,
        "svg.hashsalt": "ym-round32-figures-2026-09-23",
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


def footer(fig, extra: str) -> None:
    fig.text(
        0.5,
        0.014,
        f"{PRESENTATION_NOTE} {extra}",
        ha="center",
        va="bottom",
        fontsize=7.6,
        color=INK2,
    )


def style_3d_axes(ax) -> None:
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((1, 1, 1, 0))
        axis.pane.set_edgecolor(GRID)
        axis.line.set_color(BASE)
    ax.tick_params(colors=INK2, labelsize=7.5)


# ---------------------------------------------------------------------------
# Figure 1: one coarse factor's tail block
# ---------------------------------------------------------------------------
def fig1_coarse_factor():
    fig = plt.figure(figsize=(8.6, 6.6))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_proj_type("ortho")
    style_3d_axes(ax)

    verts = [(r, q, 0) for r in range(4) for q in range(2)]

    base_segs, sel_segs = [], []
    for (r, q, z) in verts:
        sel_x = r in (0, 1, 2)  # x-links of the selected strip: r=0,1,2, both q
        (sel_segs if sel_x else base_segs).append(((r, q, z), (r + 1, q, z)))
        sel_y = q == 0  # y-links of the selected strip: q=0, all r
        (sel_segs if sel_y else base_segs).append(((r, q, z), (r, q + 1, z)))
        base_segs.append(((r, q, z), (r, q, z + 1)))  # z-link: never selected-strip

    faces = []
    for r in (0, 1, 2):
        faces.append([(r, 0, 0), (r + 1, 0, 0), (r + 1, 1, 0), (r, 1, 0)])

    ax.add_collection3d(Line3DCollection(base_segs, colors=MUTED, linewidths=1.3, zorder=1))
    ax.add_collection3d(
        Poly3DCollection(faces, facecolor=C_AQUA, edgecolor=C_AQUA, alpha=0.32, linewidths=1.0, zorder=2)
    )
    ax.add_collection3d(Line3DCollection(sel_segs, colors=C_BLUE, linewidths=2.8, zorder=3))

    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    zs = [v[2] for v in verts]
    ax.scatter(xs, ys, zs, color=INK, s=34, depthshade=False, zorder=5)

    ax.set_xlim(0, 4)
    ax.set_ylim(0, 2.4)
    ax.set_zlim(0, 1.6)
    ax.set_box_aspect((4, 2.4, 1.6))
    ax.set_xlabel("x offset r  (0..3)")
    ax.set_ylabel("y offset q  (0,1)")
    ax.set_zlabel("z (out of block)")
    ax.set_xticks(range(5))
    ax.set_yticks(range(3))
    ax.set_zticks(range(2))
    ax.view_init(elev=20, azim=-55)

    handles = [
        Line2D([0], [0], color=INK, marker="o", linestyle="None", markersize=6, label="tail vertex (8)"),
        Line2D([0], [0], color=MUTED, linewidth=2.2, label="other owned link (14 of 24)"),
        Line2D([0], [0], color=C_BLUE, linewidth=3.2, label="selected-strip link (10 of 24)"),
        Patch(facecolor=C_AQUA, edgecolor=C_AQUA, alpha=0.32, label="selected xy face (3, shaded)"),
    ]
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.0, 0.98), fontsize=8.3)

    fig.suptitle(
        f"Round32 coarse factor: 4×2×1 tail block — {PRESENTATION_NOTE}",
        fontsize=11,
        color=INK,
        y=0.985,
    )
    ax.set_title(
        "8 tail vertices × 3 owned links = 24; ten selected-strip links; three selected xy faces at r=0,1,2",
        fontsize=9.2,
        color=INK2,
        pad=2,
    )
    footer(
        fig,
        "Geometry: research/round21/forward/i1/report.md §1–2; "
        "block T_b={(4b_x+r,2b_y+q,b_z)}, r=0..3, q=0,1.",
    )
    fig.subplots_adjust(top=0.90, bottom=0.10)
    return fig


# ---------------------------------------------------------------------------
# Figure 2: the Wilson-loop cover and its seven incident anchor stars
# ---------------------------------------------------------------------------
def cube_faces(center, half=0.5):
    cx, cy, cz = center
    d = half
    p = {}
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                p[(sx, sy, sz)] = (cx + sx * d, cy + sy * d, cz + sz * d)
    return [
        [p[(-1, -1, -1)], p[(1, -1, -1)], p[(1, 1, -1)], p[(-1, 1, -1)]],
        [p[(-1, -1, 1)], p[(1, -1, 1)], p[(1, 1, 1)], p[(-1, 1, 1)]],
        [p[(-1, -1, -1)], p[(-1, 1, -1)], p[(-1, 1, 1)], p[(-1, -1, 1)]],
        [p[(1, -1, -1)], p[(1, 1, -1)], p[(1, 1, 1)], p[(1, -1, 1)]],
        [p[(-1, -1, -1)], p[(1, -1, -1)], p[(1, -1, 1)], p[(-1, -1, 1)]],
        [p[(-1, 1, -1)], p[(1, 1, -1)], p[(1, 1, 1)], p[(-1, 1, 1)]],
    ]


def tetra_faces(center, half=0.30):
    cx, cy, cz = center
    d = half
    v = [
        (cx + d, cy + d, cz + d),
        (cx + d, cy - d, cz - d),
        (cx - d, cy + d, cz - d),
        (cx - d, cy - d, cz + d),
    ]
    return [
        [v[0], v[1], v[2]],
        [v[0], v[1], v[3]],
        [v[0], v[2], v[3]],
        [v[1], v[2], v[3]],
    ]


def fig2_wilson_cover_stars():
    fig = plt.figure(figsize=(9.0, 7.2))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_proj_type("ortho")
    style_3d_axes(ax)

    cover = [(0, 0, 0), (0, 0, 1)]  # R = {0, e_z}
    anchors = [
        ("0", (0, 0, 0)),
        ("−e_x", (-1, 0, 0)),
        ("−e_y", (0, -1, 0)),
        ("−e_z", (0, 0, -1)),
        ("e_z", (0, 0, 1)),
        ("e_z−e_x", (-1, 0, 1)),
        ("e_z−e_y", (0, -1, 1)),
    ]
    label_box = dict(boxstyle="round,pad=0.12", facecolor=SURFACE, edgecolor="none", alpha=0.78)

    for c in cover:
        ax.add_collection3d(
            Poly3DCollection(cube_faces(c, 0.42), facecolor=C_BLUE, edgecolor=C_BLUE, alpha=0.10, linewidths=0.8)
        )

    for name, c in anchors:
        ax.add_collection3d(
            Poly3DCollection(
                tetra_faces(c, 0.26), facecolor=C_MAGENTA, edgecolor=C_MAGENTA, alpha=0.32, linewidths=0.7
            )
        )
        ax.text(c[0], c[1] + 0.46, c[2], name, fontsize=7.6, color=INK2, ha="center", bbox=label_box, zorder=8)

    w = [(-0.16, -0.05, -0.16), (0.16, -0.05, -0.16), (0.16, -0.05, 0.16), (-0.16, -0.05, 0.16)]
    loop = w + [w[0]]
    ax.plot(
        [q[0] for q in loop],
        [q[1] for q in loop],
        [q[2] for q in loop],
        color=C_ORANGE,
        linewidth=4.2,
        solid_capstyle="round",
        zorder=9,
    )
    ax.text2D(
        0.02,
        0.03,
        "W = ½Tr[U(0,x)·U(e_x,z)·U(e_z,x)⁻¹·U(0,z)⁻¹]  (four thick links at the fine origin)",
        transform=ax.transAxes,
        fontsize=8.2,
        color=C_ORANGE,
        ha="left",
        va="bottom",
    )

    ax.set_xlim(-1.8, 1.8)
    ax.set_ylim(-1.8, 1.8)
    ax.set_zlim(-1.8, 1.8)
    ax.set_box_aspect((1, 1, 1))
    ax.set_xlabel("coarse x (b_x)")
    ax.set_ylabel("coarse y (b_y)")
    ax.set_zlabel("coarse z (b_z)")
    ax.view_init(elev=15, azim=-40)

    handles = [
        Patch(facecolor=C_BLUE, edgecolor=C_BLUE, alpha=0.30, label="cover factor R = {0, e_z}  (2)"),
        Line2D([0], [0], color=C_ORANGE, linewidth=3.5, label="Wilson loop W links (4, thick)"),
        Patch(facecolor=C_MAGENTA, edgecolor=C_MAGENTA, alpha=0.45, label="incident anchor star b+S  (7)"),
    ]
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.0, 0.98), fontsize=8.3)

    fig.suptitle(
        f"Round32 Wilson-loop cover and incident stars — {PRESENTATION_NOTE}", fontsize=10.6, color=INK, y=0.985
    )
    ax.set_title(
        "R−S = {0, −e_x, −e_y, −e_z, e_z, e_z−e_x, e_z−e_y}  (seven anchors, S={0,e_x,e_y,e_z})",
        fontsize=8.6,
        color=INK2,
        pad=2,
    )
    footer(
        fig,
        "Coarse-block positions are schematic, not fine-lattice scale. "
        "Geometry: research/round32/skeptic/triage.md (a).",
    )
    fig.subplots_adjust(top=0.90, bottom=0.10)
    return fig


# ---------------------------------------------------------------------------
# Figure 3: window kernel vs Poisson kernel
# ---------------------------------------------------------------------------
def fig3_window_vs_poisson():
    s = 1.0
    n = 400
    thetas = [10 ** (-2 + 4 * i / (n - 1)) for i in range(n)]

    poisson = [s / (math.pi * (s * s + t * t)) for t in thetas]
    window = [(4 * s ** 3 / math.pi) * (s * s + t * t) ** -2 for t in thetas]
    poisson_m1 = [t * p for t, p in zip(thetas, poisson)]
    window_m1 = [t * w for t, w in zip(thetas, window)]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.4, 5.0))

    ax1.loglog(thetas, poisson, color=C_BLUE, linewidth=2.0, label="Poisson: s/(π(s²+θ²))")
    ax1.loglog(thetas, window, color=C_ORANGE, linewidth=2.0, label="window: |ĝ(θ)| = (4s³/π)(s²+θ²)⁻²")
    ax1.set_xlabel("θ  (Euclidean frequency, s=1)")
    ax1.set_ylabel("kernel value")
    ax1.set_title("(a) kernel modulus", fontsize=10, color=INK2)
    ax1.legend(fontsize=8, loc="lower left")
    ax1.grid(True, which="both", color=GRID, linewidth=0.6, alpha=0.8)

    ax2.loglog(thetas, poisson_m1, color=C_BLUE, linewidth=2.0, label="θ·Poisson  (tail ~ 1/θ)")
    ax2.loglog(thetas, window_m1, color=C_ORANGE, linewidth=2.0, label="θ·window  (tail ~ θ⁻³)")
    ax2.set_xlabel("θ")
    ax2.set_ylabel("|θ|·kernel")
    ax2.set_title("(b) first-moment integrand", fontsize=10, color=INK2)
    ax2.legend(fontsize=8, loc="lower left")
    ax2.grid(True, which="both", color=GRID, linewidth=0.6, alpha=0.8)
    note_box = dict(boxstyle="round,pad=0.22", facecolor=SURFACE, edgecolor="none", alpha=0.82)
    ax2.text(
        0.97, 0.16, "Poisson: ∫|θ|·kernel dθ diverges (log)",
        transform=ax2.transAxes, ha="right", va="bottom", fontsize=7.8, color=C_BLUE, bbox=note_box,
    )
    ax2.text(
        0.97, 0.05, "window: M₀ = 2, M₁ = 4s/π  (both finite)",
        transform=ax2.transAxes, ha="right", va="bottom", fontsize=7.8, color=C_ORANGE, bbox=note_box,
    )

    fig.suptitle(
        f"Round32 window kernel vs Poisson kernel at s=1 — {PRESENTATION_NOTE}", fontsize=11, color=INK, y=0.99
    )
    footer(
        fig,
        "g(x)=e⁻ˢˣ (x≥0), eˢˣ(1−2sx+2s²x²) (x<0); "
        "constants from research/round32/advisor/deliberation-2.md.",
    )
    fig.subplots_adjust(top=0.84, bottom=0.20, wspace=0.28)
    return fig


# ---------------------------------------------------------------------------
# Figure 4: error-budget comparison (planning-notes preview)
# ---------------------------------------------------------------------------
def fig4_error_budget():
    budgets = [
        (
            "AT4 Poisson, L=1×10⁴",
            [
                ("state", 8.08e-4, C_BLUE),
                ("centering", 6.5e-7, C_YELLOW),
                ("dynamics", 7.2e-7, C_ORANGE),
                ("tail", 3.2e-5, C_AQUA),
            ],
            None,
        ),
        (
            "optimized Poisson floor",
            [("dynamics (bulk)", 1.187e-6, C_ORANGE), ("tail", 7.8e-8, C_AQUA)],
            "state → 0 (suppressed to isolate the dynamics+tail floor)",
        ),
        (
            "window + crude tier, D=2.37×10⁻⁵",
            [("state (2D)", 4.74e-5, C_BLUE), ("dynamics", 1.56e-7, C_ORANGE)],
            None,
        ),
        (
            "window + exact tier, D≈1.4×10⁻⁸",
            [("state (2D)", 2.8e-8, C_BLUE), ("dynamics", 1.56e-7, C_ORANGE)],
            None,
        ),
    ]

    fig, ax = plt.subplots(figsize=(11.4, 5.8))
    n = len(budgets)
    ys = list(range(n - 1, -1, -1))
    cat_offset = {0: -0.20, 1: -0.07, 2: 0.07, 3: 0.20}
    trans = ax.get_yaxis_transform()

    for (name, comps, note), y in zip(budgets, ys):
        total = sum(v for _, v, _ in comps)
        ax.hlines(y, 1e-9, 3e-3, color=GRID, linewidth=0.8, zorder=1)
        for i, (label, value, color) in enumerate(comps):
            ax.plot(
                value, y + cat_offset.get(i, 0), "o", color=color, markersize=8,
                markeredgecolor=SURFACE, markeredgewidth=0.6, zorder=3,
            )
        ax.plot(total, y, "D", color=INK, markersize=8, markeredgecolor=SURFACE, markeredgewidth=0.6, zorder=4)
        ax.text(
            1.02, y, f"total ≈ {total:.2e}", transform=trans, fontsize=8.4, color=INK2,
            va="center", ha="left", clip_on=False,
        )
        if note:
            ax.text(0.01, y - 0.30, note, transform=trans, fontsize=7.2, color=MUTED, va="center", style="italic")

    ax.axvline(1e-6, color=STATUS_CRITICAL, linestyle="--", linewidth=1.3, zorder=2)
    ax.text(1e-6, n - 0.32, "target 1×10⁻⁶", color=STATUS_CRITICAL, fontsize=8.2, ha="center", va="bottom")

    ax.set_xscale("log")
    ax.set_xlim(1e-9, 3e-3)
    ax.set_ylim(-0.70, n - 0.25)
    ax.set_yticks(ys)
    ax.set_yticklabels([b[0] for b in budgets], fontsize=9)
    ax.set_xlabel("error magnitude (dimensionless, log scale)")
    ax.tick_params(axis="y", length=0)
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    ax.grid(axis="x", which="major", color=GRID, linewidth=0.6, alpha=0.8)

    handles = [
        Line2D([0], [0], marker="o", color=C_BLUE, linestyle="None", markersize=7, label="state"),
        Line2D([0], [0], marker="o", color=C_YELLOW, linestyle="None", markersize=7, label="centering"),
        Line2D([0], [0], marker="o", color=C_ORANGE, linestyle="None", markersize=7, label="dynamics"),
        Line2D([0], [0], marker="o", color=C_AQUA, linestyle="None", markersize=7, label="tail"),
        Line2D([0], [0], marker="D", color=INK, linestyle="None", markersize=7, label="total"),
    ]
    ax.legend(handles=handles, loc="upper center", ncol=5, fontsize=8, bbox_to_anchor=(0.5, -0.14))

    fig.suptitle(
        f"Round32 error-budget previews at τ=1×10⁻⁸, s=1 — {PRESENTATION_NOTE}",
        fontsize=10.8,
        color=INK,
        y=0.98,
    )
    footer(
        fig,
        "Values are previews from the planning notes, not certified results. "
        "Source: round32/advisor/deliberation-2.md, skeptic/triage.md (c)2.",
    )
    fig.subplots_adjust(left=0.26, right=0.78, top=0.88, bottom=0.24)
    return fig


# ---------------------------------------------------------------------------
# Figure 5: the link-flip set E on a 2x2x2 fine block
# ---------------------------------------------------------------------------
def fig5_link_flip_set():
    fig = plt.figure(figsize=(8.6, 7.2))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_proj_type("ortho")
    style_3d_axes(ax)

    def in_e(axis, p):
        px, py, pz = p
        if axis == "x":
            return py % 2 == 0
        if axis == "y":
            return pz % 2 == 0
        return px % 2 == 0  # axis == "z"

    e_segs, not_e_segs = [], []
    for px in (0, 1):
        for py in (0, 1):
            for pz in (0, 1):
                p = (px, py, pz)
                if px == 0:
                    seg = (p, (px + 1, py, pz))
                    (e_segs if in_e("x", p) else not_e_segs).append(seg)
                if py == 0:
                    seg = (p, (px, py + 1, pz))
                    (e_segs if in_e("y", p) else not_e_segs).append(seg)
                if pz == 0:
                    seg = (p, (px, py, pz + 1))
                    (e_segs if in_e("z", p) else not_e_segs).append(seg)

    ax.add_collection3d(
        Line3DCollection(not_e_segs, colors=MUTED, linewidths=1.6, linestyles=(0, (4, 2)), zorder=1)
    )
    ax.add_collection3d(Line3DCollection(e_segs, colors=C_BLUE, linewidths=3.0, zorder=2))

    verts = [(px, py, pz) for px in (0, 1) for py in (0, 1) for pz in (0, 1)]
    ax.scatter(*zip(*verts), color=INK, s=28, depthshade=False, zorder=5)

    faces = [
        ("xy (z=0)", [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], C_AQUA, (0.5, 0.5, -0.16)),
        ("xz (y=0)", [(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)], C_YELLOW, (0.5, -0.22, 0.5)),
        ("yz (x=0)", [(0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)], C_MAGENTA, (-0.24, 0.5, 0.5)),
    ]
    for label, poly, color, tpos in faces:
        ax.add_collection3d(Poly3DCollection([poly], facecolor=color, edgecolor=color, alpha=0.30, linewidths=1.4, zorder=3))
        ax.text(*tpos, f"{label}\nE-count = 3 (odd)", fontsize=7.4, color=INK2, ha="center")

    ax.set_xlim(-0.3, 1.3)
    ax.set_ylim(-0.3, 1.3)
    ax.set_zlim(-0.3, 1.3)
    ax.set_box_aspect((1, 1, 1))
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.view_init(elev=26, azim=-115)

    handles = [
        Line2D([0], [0], color=C_BLUE, linewidth=3, label="link in E (6 of 12)"),
        Line2D([0], [0], color=MUTED, linewidth=2, linestyle=(0, (4, 2)), label="link not in E (6 of 12)"),
    ]
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.0, 0.98), fontsize=8.3)

    fig.suptitle(
        f"Round32 link-flip set E on a 2×2×2 fine block — {PRESENTATION_NOTE}",
        fontsize=10.4,
        color=INK,
        y=0.985,
    )
    ax.set_title(
        "E = {(p,x): p_y even} ∪ {(p,y): p_z even} ∪ {(p,z): p_x even}; "
        "every plaquette meets E an odd number of times",
        fontsize=8.4,
        color=INK2,
        pad=2,
    )
    footer(
        fig,
        "Sign-flip control: H(τ) and H(−τ) unitarily equivalent. "
        "Source: research/round32/advisor/deliberation-2.md.",
    )
    fig.subplots_adjust(top=0.88, bottom=0.10)
    return fig


# ---------------------------------------------------------------------------
# Figure 6: the Round11 two-plaquette graph
# ---------------------------------------------------------------------------
def fig6_two_plaquette_graph():
    fig, ax = plt.subplots(figsize=(7.8, 5.4))

    verts = {"TL": (0, 1), "TM": (1, 1), "TR": (2, 1), "BL": (0, 0), "BM": (1, 0), "BR": (2, 0)}
    links = [
        ("h1", "TL", "TM", False),
        ("h2", "TM", "TR", False),
        ("h3", "BL", "BM", False),
        ("h4", "BM", "BR", False),
        ("vL", "TL", "BL", False),
        ("vM", "TM", "BM", True),
        ("vR", "TR", "BR", False),
    ]

    for name, a, b, shared in links:
        (x0, y0), (x1, y1) = verts[a], verts[b]
        color = C_ORANGE if shared else C_BLUE
        lw = 4.4 if shared else 2.4
        ax.plot([x0, x1], [y0, y1], color=color, linewidth=lw, solid_capstyle="round", zorder=2)
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        dx = x1 - x0
        ox, oy = (0.15, 0.0) if dx == 0 else (0.0, 0.12)
        ax.text(mx + ox, my + oy, name, fontsize=10.5, color=color, ha="center", va="center", fontweight="bold")

    for name, (x, y) in verts.items():
        ax.plot(x, y, "o", color=INK, markersize=11, markeredgecolor=SURFACE, markeredgewidth=1.2, zorder=3)
        voy = 0.15 if y == 1 else -0.17
        ax.text(x, y + voy, name, fontsize=10, color=INK, ha="center", va="center")

    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.55, 1.55)
    ax.set_aspect("equal")
    ax.axis("off")

    handles = [
        Line2D([0], [0], color=C_BLUE, linewidth=2.6, label="link (6)"),
        Line2D([0], [0], color=C_ORANGE, linewidth=4.4, label="shared link vM (1)"),
        Line2D([0], [0], marker="o", color=INK, linestyle="None", markersize=8, label="vertex (6)"),
    ]
    ax.legend(handles=handles, loc="lower center", ncol=3, fontsize=8.6, bbox_to_anchor=(0.5, -0.08))

    fig.suptitle("Round32 reference: the Round11 two-plaquette graph", fontsize=11.5, color=INK, y=0.97)
    ax.set_title("a different finite model (AZ2), not the Z³ AQ family", fontsize=9.6, color=INK2, pad=10)
    footer(fig, "Seven links, six vertices, two squares sharing vM. Source: round11/advisor/advisor.md §1.")
    fig.subplots_adjust(top=0.84, bottom=0.18)
    return fig


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
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    builders = [
        ("r32-coarse-factor", fig1_coarse_factor),
        ("r32-wilson-cover-stars", fig2_wilson_cover_stars),
        ("r32-window-vs-poisson", fig3_window_vs_poisson),
        ("r32-error-budget", fig4_error_budget),
        ("r32-link-flip-set", fig5_link_flip_set),
        ("r32-two-plaquette-graph", fig6_two_plaquette_graph),
    ]

    written = []
    for name, builder in builders:
        fig = builder()
        written.extend(save_all(fig, name))

    for path in written:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f"{digest}  {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
