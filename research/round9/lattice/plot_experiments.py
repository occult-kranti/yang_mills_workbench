"""Plots from saved data only; no simulation or diagnostic thresholds are changed."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from su2_lattice import exact_one_plaquette

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'results'
FIG = ROOT/'figures'
FIG.mkdir(exist_ok=True)
data = json.loads((OUT/'all_diagnostics.json').read_text())
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
colors = {'cold':'#246a9d','hot':'#e08a29'}

fig, axes = plt.subplots(3, 1, figsize=(10,9), sharex=True, constrained_layout=True)
for ax, beta in zip(axes,[0.,.5,2.2]):
    for c in data['chains']:
        if c['beta'] != beta:
            continue
        raw = np.genfromtxt(OUT/c['raw_csv'],delimiter=',',names=True)
        # Nonoverlapping 32-sweep means are display bins, not the primary 64-sweep uncertainty.
        binned = raw['plaquette_mean'].reshape(-1,32).mean(axis=1)
        ax.plot(np.arange(32,2049,32)-15.5,binned,label=c['start'].capitalize(),color=colors[c['start']],lw=1.4)
    ax.set_ylabel('Mean plaquette')
    label = 'plaquette uncertainty INSUFFICIENT' if beta==2.2 else 'predeclared batching criteria met'
    ax.set_title(f'β={beta:g} · {label}',loc='left',fontweight='bold')
    ax.grid(alpha=.15)
axes[0].legend(frameon=False,ncol=2)
axes[-1].set_xlabel('Measured sweep after 512 warmup sweeps (32-sweep display bins)')
fig.suptitle('Actual 4D SU(2), 2×2×2×2 lattice · no mass estimate',fontsize=15,fontweight='bold')
fig.savefig(FIG/'lattice_chain_histories.png',dpi=170)
fig.savefig(FIG/'lattice_chain_histories.svg')
plt.close(fig)

fig, ax = plt.subplots(figsize=(9,5),constrained_layout=True)
labels=[]
for i,c in enumerate(c for c in data['chains'] if c['beta']>0):
    s=c['statistics']['ward']['64']
    ax.errorbar(i,s['mean'],yerr=s['se'],fmt='o',capsize=5,color=colors[c['start']],ms=7)
    labels.append(f"β={c['beta']:g}\n{c['start']}")
ax.axhline(0,color='#40464d',ls='--',lw=1)
ax.set_xticks(range(4),labels)
ax.set_ylabel('⟨β² |vec(UA)|² − 3β scalar(UA)⟩')
ax.set_title('Exact finite-lattice link identity: target zero',loc='left',fontweight='bold')
ax.text(.01,-.2,'Bars: one estimated SE from 64-sweep batches. Consistency is a limited sampler diagnostic.',transform=ax.transAxes,fontsize=10)
ax.grid(axis='y',alpha=.15)
fig.savefig(FIG/'link_identity_diagnostic.png',dpi=170,bbox_inches='tight')
fig.savefig(FIG/'link_identity_diagnostic.svg',bbox_inches='tight')
plt.close(fig)

fig, ax=plt.subplots(figsize=(9,5),constrained_layout=True)
grid=np.linspace(0,2.5,251)
ax.plot(grid,[exact_one_plaquette(x)['mean'] for x in grid],color='#246a9d',label='Exact one-matrix I₂(β)/I₁(β)')
for i,run in enumerate(data['one_plaquette']):
    s=run['checks']['mean']
    ax.errorbar(run['beta'],s['mean'],yerr=s['se'],fmt='o',ms=7,capsize=4,color='#e08a29',label='20,000 IID samples; one SE' if i==0 else None)
ax.set_xlabel('β')
ax.set_ylabel('Normalized trace mean')
ax.set_title('Independent one-matrix control · not the 4D lattice formula',loc='left',fontweight='bold')
ax.legend(frameon=False)
ax.grid(alpha=.15)
fig.savefig(FIG/'one_plaquette_control.png',dpi=170)
fig.savefig(FIG/'one_plaquette_control.svg')
plt.close(fig)
print('Rendered 3 scientific figures from saved results.')
