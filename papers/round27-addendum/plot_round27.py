#!/usr/bin/env python3
"""Display frozen exact evidence. Floats are used only after decisions are checked."""
from fractions import Fraction
from pathlib import Path
import json
import hashlib
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DIST = ROOT / "dist"


def main():
    source = ROOT / "research/round27/forward/ai2/output/results.json"
    gate_path = ROOT / "research/round27/advisor/ai2-gate.json"
    gate = json.loads(gate_path.read_text())
    if "accepted" not in gate.get("verdict", ""):
        raise RuntimeError("AI2 final accepted-with-limits gate is required")
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    if gate.get("bindings", {}).get(str(source.relative_to(ROOT))) != source_hash:
        raise RuntimeError("AI2 output is not bound by its final gate")
    data = json.loads(source.read_text())
    f = Fraction
    ratios, decisions = {}, []
    for row in data["rows"]:
        for probe in ("4", "5"):
            record = row["scalar_discrimination"][probe]
            # Derive distance from the stored exact margin and sum of radii.
            margin = f(record["signed_margin"])
            disk_sum = f(record["disk_sum"])
            ratio = (margin + disk_sum) / disk_sum
            if margin + disk_sum != f(record["imaginary_center_distance"]):
                raise RuntimeError("Stored distance/margin/radius identity failed")
            if (margin > 0) != record["disjoint"]:
                raise RuntimeError("Exact margin and recorded decision disagree")
            ratios[(probe, row["power"], row["k"])] = ratio
            decisions.append({"probe": probe, "power": row["power"],
                              "k": row["k"], "separation_ratio": str(ratio),
                              "disjoint": margin > 0})
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(1, 2, figsize=(10.7, 3.6), layout="constrained")
    for ax, probe in zip(axes, ("4", "5")):
        arr = np.array([[math.log10(float(ratios[(probe,p,k)]))
                         for k in (3,4,5)] for p in (12,18,24)])
        im = ax.imshow(arr, cmap="RdBu", norm=TwoSlopeNorm(vmin=-15, vcenter=0, vmax=1), aspect="auto")
        ax.set_xticks(range(3), ["3", "4", "5"])
        ax.set_yticks(range(3), [r"$10^{-12}$", r"$10^{-18}$", r"$10^{-24}$"])
        ax.set_xlabel("Collar depth k")
        ax.set_ylabel("Profile difference u")
        ax.set_title(fr"Probe $B_{probe}$")
        for i,p in enumerate((12,18,24)):
            for j,k in enumerate((3,4,5)):
                val = float(ratios[(probe,p,k)])
                txt = f"{val:.2g}"
                if val > 1: txt += "\nseparated"
                ax.text(j, i, txt, ha="center", va="center", fontsize=10,
                        color="white" if arr[i,j] < -8 or arr[i,j] > .3 else "black")
    cb = fig.colorbar(im, ax=axes, shrink=.88, pad=.035)
    cb.set_label(r"$\log_{10}$(separation / sum of radii)")
    output = DIST / "ym-round27-discrimination.png"
    fig.savefig(output, dpi=180, facecolor="white")
    plt.close(fig)
    provenance = {
        "schema": "ym27-addendum-figure-v1",
        "source": str(source.relative_to(ROOT)),
        "source_sha256": source_hash,
        "gate": str(gate_path.relative_to(ROOT)),
        "gate_sha256": hashlib.sha256(gate_path.read_bytes()).hexdigest(),
        "plot": str(output.relative_to(ROOT)),
        "decisions": decisions,
        "scope": "Exact rational decisions; floating-point rendering only. No simulation or new proof."
    }
    agate_path = ROOT / "research/round27/advisor/ag1-gate.json"
    agate = json.loads(agate_path.read_text())
    if "accepted" not in agate.get("verdict", ""):
        raise RuntimeError("AG1 final accepted-with-limits gate is required")
    agpaths = [ROOT / f"research/round27/{side}/ag1/output/results.json"
               for side in ("forward", "reverse")]
    agpaths.append(ROOT / "research/round27/skeptic/ag1-independent.json")
    agdata = []
    for p in agpaths:
        if agate.get("bindings", {}).get(str(p.relative_to(ROOT))) != hashlib.sha256(p.read_bytes()).hexdigest():
            raise RuntimeError("AG1 source is not bound by its final gate: " + str(p))
        agdata.append(json.loads(p.read_text()))
    vals = [f(agdata[0]["narrow"]["new_mixing_over_actual_A2_upper"]),
            f(agdata[1]["narrow"]["narrow_selected_contraction_ratio"]),
            f(next(b for b in agdata[2]["budgets"] if f(b["M"]) == f(1,10000))["selected_source_contraction_upper"])]
    if not (0 < vals[0] < f(2,3) and 0 < vals[1] < 1 and 0 < vals[2] < f(605,1000)):
        raise RuntimeError("Recorded AG1 headline thresholds do not match exact evidence")
    fig, ax = plt.subplots(figsize=(9.2, 3.05), layout="constrained")
    ax.barh([2,1,0], [float(v) for v in vals], height=.52,
            color=["#36668b", "#82909c", "#35765d"])
    ax.set_yticks([2,1,0], ["Forward rooted count", "Reverse word count", "Skeptic integrated tail"])
    ax.set_xlim(0,1.08)
    ax.set_xlabel("Upper bound on new mixing norm / actual input norm")
    ax.set_title(r"One selected-source step, $0<M\leq10^{-4}$")
    ax.axvline(2/3, color="#333333", linestyle="--", linewidth=1)
    ax.axvline(1, color="#555555", linestyle=":", linewidth=1)
    for y,v in zip([2,1,0],vals):
        ax.text(float(v)-.018,y,f"{float(v):.6f}",va="center",ha="right",fontsize=10,color="white")
    ax.text(2/3,2.40,"2/3",ha="center",fontsize=9,bbox={"facecolor":"white","edgecolor":"none","pad":1})
    ax.text(1,2.40,"1",ha="center",fontsize=9,bbox={"facecolor":"white","edgecolor":"none","pad":1})
    ax.set_ylim(-.55,2.68)
    agoutput = DIST / "ym-round27-contraction-bounds.png"
    fig.savefig(agoutput,dpi=180,facecolor="white")
    plt.close(fig)
    provenance["ag1"] = {"gate":str(agate_path.relative_to(ROOT)),
        "gate_sha256":hashlib.sha256(agate_path.read_bytes()).hexdigest(),
        "sources":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in agpaths},
        "upper_bounds":[str(v) for v in vals],"plot":str(agoutput.relative_to(ROOT)),
        "scope":"Three sufficient bounds on the new selected mixing family; no exact contraction factor or repeated iteration."}
    (HERE / "figure-data.json").write_text(json.dumps(provenance, indent=2) + "\n")
    print(output)
    print(agoutput)


if __name__ == "__main__":
    main()
