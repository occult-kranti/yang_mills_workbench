#!/usr/bin/env python3
"""Optional scientific figure from already verified CSV endpoints."""
import csv
from pathlib import Path
from fractions import Fraction
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"


def read(name):
    with (OUT / name).open(newline="") as stream:
        return list(csv.DictReader(stream))


def log_value(row):
    # Display transform only; certificate endpoint remains an exact rational.
    value = Fraction(row["bound_rational"])
    if value <= 0:
        raise ValueError("logarithmic plot requires a strictly positive recorded bound")
    return math.log10(value.numerator) - math.log10(value.denominator)


fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.7), constrained_layout=True)
rows = read("boundary_decay.csv")
axes[0].plot([int(row["radius"]) for row in rows], [log_value(row) for row in rows], color="#2467a5", lw=2.4)
axes[0].set_title("Distant boundaries at fixed drive budget")
axes[0].set_xlabel("Boundary distance R in plaquette steps")
axes[0].set_ylabel("log₁₀ certified observable-error upper bound")
axes[0].text(.04, .09, "3 spatial dimensions; |X| = 4; ‖A‖ = 1\nJ = 1/4; z = 8", transform=axes[0].transAxes, fontsize=9,
             bbox={"facecolor": "white", "alpha": .9, "edgecolor": "#d5dfe8"})
rows = read("scaling_cases.csv")
for case, label, color in (("fixed_time_and_coupling", "Fixed z = 8", "#2467a5"),
                           ("slow_time_growth", "Growing z = R/10", "#008378"),
                           ("time_or_coupling_growth", "Growing z = R", "#b45309")):
    selected = [row for row in rows if row["case"] == case]
    axes[1].plot([int(row["radius"]) for row in selected], [log_value(row) for row in selected],
                 "o-", color=color, label=label, lw=2, ms=4)
axes[1].set_title("Changing time or coupling changes the bound")
axes[1].set_xlabel("Boundary distance R in plaquette steps")
axes[1].set_ylabel("log₁₀ certified observable-error upper bound")
axes[1].legend(frameon=False, fontsize=9)
for ax in axes:
    ax.grid(alpha=.2)
    ax.spines[["top", "right"]].set_visible(False)
fig.suptitle("Locality certificate diagnostics — bounds, not simulated errors", fontsize=13)
fig.savefig(OUT / "locality_bounds.png", dpi=180)
fig.savefig(OUT / "locality_bounds.svg")
plt.close(fig)
print("Rendered locality_bounds.png and locality_bounds.svg from recorded rational endpoints.")
