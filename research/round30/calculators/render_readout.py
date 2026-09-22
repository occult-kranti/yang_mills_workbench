#!/usr/bin/env python3
"""Render reviewed rational AT3 intervals; this script does no new inference."""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]


def main():
    gate_path = ROOT / 'research/round30/advisor/at3-gate.json'
    gate = json.loads(gate_path.read_text())
    if gate['verdict'] != 'accepted_within_scope':
        raise ValueError('Reviewed AT3 admission required')
    source_name = 'research/round30/reverse/at3/output/results.json'
    source = ROOT / source_name
    if hashlib.sha256(source.read_bytes()).hexdigest() != gate['bindings'][source_name]:
        raise ValueError('Changed reviewed interval source')
    results = json.loads(source.read_text())
    fixtures = results['fixture_certificates']
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'pdf.fonttype': 42})
    fig, ax = plt.subplots(figsize=(10.8, 4.6))
    ticks, labels = [], []
    for base, name, color, truth in [(4, 'A', '#116b74', Fraction(3,32)),
                                    (1, 'B', '#be6528', Fraction(1,10))]:
        for offset, key, label in [(0, 'zero', 'zero sample error'),
                                   (-.75, 'envelope', 'all allowed errors')]:
            y = base + offset
            if key == 'envelope':
                endpoints = [fixtures[name]['minus']['interval_I'][0],
                             fixtures[name]['plus']['interval_I'][1]]
            else:
                endpoints = fixtures[name][key]['interval_I']
            lo, hi = map(lambda v: float(Fraction(v)), endpoints)
            ax.plot([lo, hi], [y, y], lw=7, color=color, alpha=.65,
                    solid_capstyle='butt')
            ax.scatter([float(truth)], [y], color='black', marker='|', s=150, zorder=3)
            ticks.append(y)
            labels.append(f'{name}: {label}')
    ax.set(yticks=ticks, yticklabels=labels, ylim=(-.4,5), xlim=(.0927,.1024),
           xlabel=r'Dimensionless inverse integral $I=\alpha R$')
    ax.grid(axis='x', alpha=.18)
    fig.suptitle('Hruday / HNM finite Euclidean readout', fontsize=15, fontweight='bold')
    fig.text(.5,.88, '4097 nodes · per-sample error ≤ 10⁻⁶ · each returned interval has width < 0.002',
             ha='center')
    fig.text(.5,.055, 'Abstract A/B controls only; no AQ samples computed. Black marks: exact known integrals.',
             ha='center', fontsize=9)
    fig.subplots_adjust(left=.24, bottom=.20, top=.82)
    out = ROOT / 'research/round30/figures'
    out.mkdir(exist_ok=True)
    base = out / 'hnm-euclidean-readout'
    fig.savefig(base.with_suffix('.pdf'), metadata={'Title': 'HNM Euclidean readout controls',
                'Author': 'Hruday N M (BUNZEEY)', 'CreationDate': None, 'ModDate': None})
    fig.savefig(base.with_suffix('.png'), dpi=180, metadata={'Software': 'HNM research workbench'})
    plt.close(fig)
    caption = {'caption': 'Certified inverse-integral intervals for the two abstract equal-moment controls A and B. The zero-error rows still include the protocol error allowances. The all-errors rows are envelopes of possible returned intervals: they include both the observed-sum shift and the sample allowance inside each certificate. Each individual returned interval has width below 0.002; its full varying-data envelope can be wider. The envelopes remain separated by more than 0.004293. Black marks show the known exact values 3/32 and 1/10. These are synthetic controls, not AQ measurements or computed AQ response values.',
               'curve_accuracy': 'Floating-point rendering of frozen exact rational endpoints; the source output supplies rigorous enclosures.',
               'source': source_name,
               'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
               'gate_sha256': hashlib.sha256(gate_path.read_bytes()).hexdigest()}
    (out / 'euclidean-caption.json').write_text(json.dumps(caption, indent=2) + '\n')
    print(json.dumps({'status': 'plotted', 'source': source_name}))


if __name__ == '__main__':
    main()
