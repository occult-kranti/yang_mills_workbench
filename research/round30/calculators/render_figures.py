#!/usr/bin/env python3
"""Plot admitted exact AT2 information; all shown spectra are abstract controls."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'research/round30/figures'


def main():
    gate = ROOT / 'research/round30/advisor/at2-gate.json'
    data = json.loads(gate.read_text())
    if data['verdict'] != 'accepted_within_scope':
        raise ValueError('AT2 admission required')
    OUT.mkdir(exist_ok=True)
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'pdf.fonttype': 42, 'svg.fonttype': 'none'})
    fig, axes = plt.subplots(2, 3, figsize=(11.4, 6.8), gridspec_kw={'height_ratios': [1, 1.15]})
    colors = ['#116b74', '#be6528', '#635b9e']
    measures = [([2, 4], [1/8, 1/8]), ([1, 3, 5], [1/32, 3/16, 1/32])]
    for j, (x, w) in enumerate(measures):
        marker, stems, baseline = axes[0, j].stem(x, w, basefmt=' ')
        plt.setp(stems, color=colors[j], linewidth=2)
        plt.setp(marker, color=colors[j], markersize=7)
        axes[0, j].set(xlim=(0, 6), ylim=(0, .21), xlabel=r'Energy $x=E/\alpha$',
                       ylabel='Atomic weight', title='Control ' + 'AB'[j] + ' - discrete')
    lo, hi = 3-np.sqrt(3), 3+np.sqrt(3)
    axes[0, 2].fill_between([lo, hi], [1/(8*np.sqrt(3))]*2, color=colors[2], alpha=.3)
    axes[0, 2].plot([lo, hi], [1/(8*np.sqrt(3))]*2, color=colors[2], lw=2)
    axes[0, 2].set(xlim=(0, 6), ylim=(0, .21), xlabel=r'Energy $x=E/\alpha$',
                   ylabel='Density (not atomic weight)', title='Control C - continuous')
    for ax in axes[1]: ax.remove()
    ax = fig.add_subplot(2, 1, 2)
    times = np.linspace(0, 4, 401)
    for j, (energies, weights) in enumerate(measures):
        corr = sum(w * np.exp(-e*times) for e, w in zip(energies, weights))
        ax.plot(times, corr, label='Control ' + 'AB'[j], color=colors[j], lw=2)
    corr = np.full_like(times, .25)
    nonzero = times > 0
    corr[nonzero] = (np.exp(-lo*times[nonzero])-np.exp(-hi*times[nonzero]))/(8*np.sqrt(3)*times[nonzero])
    ax.plot(times, corr, label='Control C', color=colors[2], lw=2, ls='--')
    ax.set(xlabel=r'Dimensionless Euclidean duration $s=\alpha t_E/\hbar$',
           ylabel=r'Correlation $C(s)$', ylim=(0, .26), xlim=(0,4))
    ax.legend(frameon=False, ncol=3)
    ax.grid(alpha=.15)
    fig.suptitle('Hruday / HNM moment-information controls', fontsize=15, fontweight='bold', y=.99)
    fig.text(.5, .935, 'All three share moments (1/4, 3/4, 5/2). These are abstract controls, not computed AQ spectra.',
             ha='center', fontsize=10)
    fig.subplots_adjust(top=.86, bottom=.11, hspace=.55, wspace=.38)
    base = OUT / 'hnm-spectral-certificates'
    fig.savefig(base.with_suffix('.pdf'), metadata={'Title': 'HNM spectral information controls', 'Author': 'Hruday N M (BUNZEEY)', 'CreationDate': None, 'ModDate': None})
    fig.savefig(base.with_suffix('.png'), dpi=180, metadata={'Software': 'HNM research workbench'})
    plt.close(fig)
    metadata = {'gate_sha256': hashlib.sha256(gate.read_bytes()).hexdigest(),
                'caption': 'Three positive spectral measures share the same zeroth, first and second moments but differ in atomic structure and Euclidean correlations. A and B are the exact discrete controls; C is the uniform density on [3-sqrt(3),3+sqrt(3)] with total mass1/4. Density and atomic-weight axes are distinguished. These are information-limit controls, not spectra computed for the AQ lattice Hamiltonian.',
                'curve_accuracy': 'Floating-point renderings of exact analytic formulas; the proof and rational inverse-moment enclosures are in AT2.',
                'source': 'research/round30/advisor/at2-gate.json'}
    (OUT / 'captions.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(json.dumps({'status': 'plotted', 'files': [str(base.with_suffix(s).relative_to(ROOT)) for s in ('.pdf','.png')]}))


if __name__ == '__main__': main()
