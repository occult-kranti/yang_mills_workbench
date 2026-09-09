"""Plot exact Taylor enclosure widths; endpoints stay in the certificate JSON."""
from pathlib import Path
import csv
from fractions import Fraction
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
with (HERE/"loop2_output/certificate_summary.csv").open() as f:
    rows=[r for r in csv.DictReader(f) if r["id"].startswith("central_N")]
degrees=[int(r["degree"]) for r in rows]
widths=[float(Fraction(r["width"])) for r in rows]
fig,ax=plt.subplots(figsize=(8.5,5),layout="constrained")
ax.semilogy(degrees,widths,"o-",color="#155e75",lw=2,ms=7,label="Exact covariance-enclosure width")
ax.axhline(1e-12,color="#a85522",ls="--",lw=1.5,label=r"Requested width $10^{-12}$")
ax.annotate("Degree 4: sign inconclusive",(degrees[0],widths[0]),xytext=(11,1e-1),
            arrowprops={"arrowstyle":"->","color":"#475569"},fontsize=9)
ax.annotate("Degree 24: target passed",(24,widths[4]),xytext=(8,1e-19),
            arrowprops={"arrowstyle":"->","color":"#475569"},fontsize=9)
ax.set(xlabel="Taylor degree N",ylabel="Exact upper endpoint minus lower endpoint",
       title=r"Certified refinement at $\kappa_1=\kappa_2=1,\ \eta=1/4$")
ax.set_xticks(degrees);ax.grid(alpha=.2);ax.legend(loc="upper right",fontsize=9)
fig.text(.01,-.01,"Widths are exact rational quantities displayed on a floating logarithmic axis. This is a finite Euclidean covariance certificate.",fontsize=8)
fig.savefig(HERE/"loop2_output/certificate_refinement.png",dpi=180,bbox_inches="tight")
fig.savefig(HERE/"loop2_output/certificate_refinement.svg",bbox_inches="tight")
