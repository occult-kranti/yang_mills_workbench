#!/usr/bin/env python3
"""Draw frozen actual graph coordinates, gated for final manuscript use."""
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft",action="store_true")
    args = parser.parse_args()
    paths = {"forward":ROOT / "research/round28/forward/ah1/output/results.json",
             "reverse":ROOT / "research/round28/reverse/ah1/output/graph.json"}
    for side,path in paths.items():
        base = ROOT / f"research/round28/{side}/ah1"
        freeze = json.loads((base / "freeze.json").read_text())
        expected = (freeze["bindings"][str(path.relative_to(ROOT))] if side == "forward"
                    else freeze["files"][str(path.relative_to(base))])
        if sha(path) != expected:
            raise RuntimeError("Frozen graph source changed: " + side)
    gate_path = ROOT / "research/round28/advisor/ah1-gate.json"
    gate_hash = None
    if not args.draft:
        gate = json.loads(gate_path.read_text())
        if gate["loop"] != "ah1" or gate["verdict"] != "accepted_with_limits":
            raise RuntimeError("AH1 admission required")
        for path in paths.values():
            if gate["bindings"][str(path.relative_to(ROOT))] != sha(path):
                raise RuntimeError("Graph not bound by final admission")
        gate_hash = sha(gate_path)
    f = json.loads(paths["forward"].read_text())["graph"]
    r = json.loads(paths["reverse"].read_text())
    if f["vertices"] != r["vertices"] or f["internal_face_ids"] != r["internal_faces"]:
        raise RuntimeError("Graph coordinate comparison failed")
    if [(e["tail"],e["head"],e["axis"]) for e in f["edges"]] != [(e["tail_coordinate"],e["head_coordinate"],e["axis"]) for e in r["links"]]:
        raise RuntimeError("Independent link comparison failed")
    if [(p["tail"],p["axes"],p["word"]) for p in f["faces"]] != [(p["base"],p["axes"],p["word"]) for p in r["faces"]]:
        raise RuntimeError("Independent face comparison failed")
    if [len(r["vertices"]),len(r["links"]),len(r["faces"])] != [24,46,29]:
        raise RuntimeError("Unexpected graph")
    data = {"schema":"ym28-ah1-figure-v1","draft":args.draft,"gate_sha256":gate_hash,
            "sources":{str(p.relative_to(ROOT)):sha(p) for p in paths.values()},
            "counts":{"vertices":24,"links":46,"faces":29,"internal_faces":7},
            "internal_face_ids":r["internal_faces"],
            "scope":"Actual coordinate geometry only; no heat simulation or volume limit."}
    (HERE / "ah1-figure-data.json").write_text(json.dumps(data,indent=2)+"\n")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10})
    fig = plt.figure(figsize=(9.0,3.8))
    fig.subplots_adjust(left=.01,right=.985,bottom=.19,top=.87,wspace=.18)
    ax = fig.add_subplot(121,projection="3d",proj_type="ortho")
    plan = fig.add_subplot(122)
    colors = {(1,2):"#3478a2",(0,2):"#c47727"}
    for edge in r["links"]:
        a,b = edge["tail_coordinate"],edge["head_coordinate"]
        ax.plot(*zip(a,b),color="#59646c",linewidth=1.1,alpha=.85)
    ax.scatter(*zip(*r["vertices"]),s=13,color="#20384b",depthshade=False)
    polygons,polygon_colors = [],[]
    for i in r["internal_faces"]:
        face = r["faces"][i]
        a,b = face["axes"]
        corners = [list(face["base"]) for _ in range(4)]
        corners[1][a] += 1
        corners[2][a] += 1
        corners[2][b] += 1
        corners[3][b] += 1
        color = colors[tuple(face["axes"])]
        polygons.append(corners);polygon_colors.append(color)
        xs,ys = zip(*[(p[0],p[1]) for p in corners])
        plan.plot(xs,ys,color=color,linewidth=4,solid_capstyle="butt",zorder=3)
        cx=sum(xs)/4;cy=sum(ys)/4
        dx,dy = ((.08,0) if tuple(face["axes"]) == (1,2) else (0,.10))
        plan.text(cx+dx,cy+dy,str(i),color=color,ha="left" if dx else "center",va="center" if dx else "bottom",
                  bbox={"facecolor":"white","edgecolor":"none","pad":1},fontsize=10,zorder=5)
    ax.add_collection3d(Poly3DCollection(polygons,facecolors=polygon_colors,alpha=.22,edgecolors="none"))
    ax.set_box_aspect((3,2,1));ax.view_init(elev=23,azim=-58)
    ax.set(xlim=(-.1,3.1),ylim=(-.1,2.1),zlim=(-.05,1.05),xticks=range(4),yticks=range(3),zticks=[0,1])
    ax.set_xlabel("x",labelpad=-2);ax.set_ylabel("y",labelpad=-2);ax.set_zlabel("z",labelpad=-4)
    ax.tick_params(pad=0,labelsize=8)
    ax.grid(False)
    for axis in (ax.xaxis,ax.yaxis,ax.zaxis):
        axis.pane.fill=False
        axis.pane.set_edgecolor("white")
    ax.set_title("All links and internal faces",loc="left",weight="bold",pad=5)
    for xx in range(4):plan.plot([xx,xx],[0,2],color="#c9ced2",linewidth=.8,zorder=1)
    for yy in range(3):plan.plot([0,3],[yy,yy],color="#c9ced2",linewidth=.8,zorder=1)
    plan.scatter([x for x in range(4) for y in range(3)],[y for x in range(4) for y in range(3)],s=16,color="#20384b",zorder=4)
    plan.set(xlim=(-.16,3.16),ylim=(-.12,2.25),xticks=range(4),yticks=range(3),xlabel="x",ylabel="y")
    plan.set_aspect("equal");plan.spines[["top","right"]].set_visible(False)
    plan.set_title("Internal faces: xy plan view",loc="left",weight="bold",pad=10)
    legend = [Line2D([0],[0],color=colors[(1,2)],lw=3,label="4 yz faces"),
              Line2D([0],[0],color=colors[(0,2)],lw=3,label="3 xz faces")]
    fig.legend(handles=legend,loc="lower center",bbox_to_anchor=(.765,.012),ncol=2,frameon=False)
    path = HERE / "figures/ah1-complete-graph.png"
    path.parent.mkdir(exist_ok=True)
    fig.savefig(path,dpi=190,metadata={"Software":"Round28 exact-coordinate graph figure"})
    plt.close(fig)
    print(json.dumps({"figure":str(path.relative_to(ROOT)),"sha256":sha(path),"draft":args.draft}))


if __name__ == "__main__":
    main()
