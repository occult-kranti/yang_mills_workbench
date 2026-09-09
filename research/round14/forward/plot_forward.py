"""Generate the loop-1 scientific figure from saved CSV data."""
from pathlib import Path
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
with (HERE/"output/covariance_curves.csv").open() as f:
    rows=[{k:float(v) for k,v in r.items()} for r in csv.DictReader(f)]
eta=[r["eta"] for r in rows]
fig,ax=plt.subplots(figsize=(9,5.5),layout="constrained")
ax.plot(eta,[r["covariance_1_2"] for r in rows],color="#155e75",lw=2.3,
        label=r"$\kappa_1=1,\ \kappa_2=2$: reduced quadrature")
ax.plot(eta,[r["covariance_0_0"] for r in rows],color="#a85522",lw=2.3,
        label=r"$\kappa_1=\kappa_2=0$: exact family $u(\eta)/4$")
ax.plot(eta,[r["tangent_1_2"] for r in rows],color="#155e75",lw=1.2,ls="--",
        label=r"Origin tangent $\eta\,v(1)v(2)$ (local approximation)")
ax.axhline(0,color="#475569",lw=1,ls=":",label="Zero covariance: exact only at the undeformed baseline here")
ax.axvline(0,color="#94a3b8",lw=.7)
ax.set(xlabel=r"Mixed-loop coupling $\eta$",ylabel=r"Connected covariance $\langle xy\rangle-\langle x\rangle\langle y\rangle$",
       title="A declared mixed-loop term creates a measurable correlation")
ax.grid(alpha=.18);ax.legend(loc="upper left",fontsize=8.5)
fig.text(.01,-.01,"Finite Euclidean SU(2) measure. Lines are floating evaluations; this figure is not a mass-gap or interval certificate.",fontsize=8)
fig.savefig(HERE/"output/covariance.png",dpi=180,bbox_inches="tight")
fig.savefig(HERE/"output/covariance.svg",bbox_inches="tight")
