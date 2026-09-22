#!/usr/bin/env python3
"""Render exact admitted coefficients; floating point is used only for display."""
from fractions import Fraction
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(item):
    if "exact" in item:
        return Fraction(item["exact"])
    return Fraction(item["numerator"],item["denominator"])


def main():
    gate_path = ROOT / "research/round28/advisor/ag3-gate.json"
    gate = json.loads(gate_path.read_text())
    if gate["verdict"] != "accepted_with_limits" or gate["loop"] != "ag3":
        raise RuntimeError("AG3 admission required")
    paths = {side:ROOT / f"research/round28/{side}/ag3/output/results.json"
             for side in ("forward","reverse")}
    evidence = {}
    for side,path in paths.items():
        if sha(path) != gate["bindings"][str(path.relative_to(ROOT))]:
            raise RuntimeError("Changed admitted figure source")
        evidence[side] = json.loads(path.read_text())["endpoints"]
    forward,reverse = evidence["forward"],evidence["reverse"]
    rows = []
    for interval in ("main","narrow"):
        active = q(forward[interval]["ratio"])
        if active != q(reverse[interval]["ratio"]):
            raise RuntimeError("Independent exact coefficient mismatch")
        passive = q(forward[interval]["passive_embedding_ratio"])
        rows.append({"interval":interval,"active_ceiling":str(active),
                     "passive_ceiling":str(passive),
                     "actual_input":"r=||B||_2",
                     "actual_lower_weight_comparison_proved":False})
    data = {"schema":"ym28-addendum-figure-data-v1","gate_sha256":sha(gate_path),
            "sources":{str(p.relative_to(ROOT)):sha(p) for p in paths.values()},
            "ag3":rows,"scope":"Sufficient bounds across support weights; neither actual norms nor theorem completion."}
    (HERE / "figure-data.json").write_text(json.dumps(data,indent=2)+"\n")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,
                         "axes.spines.top":False,"axes.spines.right":False})
    fig,ax = plt.subplots(figsize=(7.8,3.25),layout="constrained")
    values = [Fraction(rows[0]["active_ceiling"]),Fraction(rows[0]["passive_ceiling"]),
              Fraction(rows[1]["active_ceiling"])]
    labels = ["Main active step\nM ≤ 0.001","Passive reweighting\nminimum support 4",
              "Narrow active step\nM ≤ 0.0001"]
    ax.bar(range(3),list(map(float,values)),width=.56,color=["#275b84","#84898d","#337b64"],zorder=3)
    for i,value in enumerate(values):
        ax.text(i,float(value)+.035,f"{float(value):.6f}",ha="center",va="bottom",
                bbox={"facecolor":"white","edgecolor":"none","pad":1.5})
    ax.set_xticks(range(3),labels)
    ax.set_ylim(0,1)
    ax.set_ylabel("Upper coefficient multiplying r")
    ax.set_title("AG3: active and passive upper certificates",loc="left",weight="bold",pad=14)
    ax.grid(axis="y",color="#e4e7e9",zorder=0)
    ax.tick_params(axis="x",length=0,pad=9)
    ax.set_axisbelow(True)
    (HERE / "figures").mkdir(exist_ok=True)
    path = HERE / "figures/ag3-passive-comparison.png"
    fig.savefig(path,dpi=180,metadata={"Software":"Round28 exact admitted-data figure"})
    plt.close(fig)
    print(json.dumps({"figure":str(path.relative_to(ROOT)),"sha256":sha(path)}))


if __name__ == "__main__":
    main()
