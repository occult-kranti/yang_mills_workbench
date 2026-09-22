#!/usr/bin/env python3
"""Plot reviewed synthetic readout intervals; floating geometry is illustrative."""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
R = ROOT / 'research/round30'


def main():
    gate_path = R / 'advisor/at3-gate.json'
    gate = json.loads(gate_path.read_text())
    if gate['verdict'] != 'accepted_within_scope':
        raise ValueError('The accepted AT3 review is required')
    result_path = R / 'forward/at3/output/results.json'
    if hashlib.sha256(result_path.read_bytes()).hexdigest() != gate['bindings'][str(result_path.relative_to(ROOT))]:
        raise ValueError('Changed reviewed result')
    result = json.loads(result_path.read_text())
    f = lambda x: float(Fraction(x))
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'axes.spines.top': False, 'axes.spines.right': False})
    fig, (left, right) = plt.subplots(1, 2, figsize=(11.8, 5),
                                     gridspec_kw={'width_ratios': [1.8, 1]})
    colors = {'A': '#146982', 'B': '#a4521b'}
    ticks, labels = [], []
    for name, base in [('A', 4), ('B', 0)]:
        for offset, sign in enumerate((-1, 0, 1)):
            row = result['fixture_outputs'][name][str(sign)]
            y = base + offset
            low, high = f(row['lower']), f(row['upper'])
            left.plot([low, high], [y, y], color=colors[name], lw=5, solid_capstyle='butt')
            left.plot([low, high], [y, y], '|', color=colors[name], markersize=11)
            ticks.append(y)
            labels.append(f'{name}: all errors ' + ('−ε' if sign < 0 else '+ε' if sign else '0'))
        left.axvline(f(result['fixture_exact_I'][name]), color=colors[name], linestyle=':', alpha=.7)
    left.set_yticks(ticks, labels)
    left.set_xlabel(r'Certified dimensionless inverse form $I=\alpha R$')
    left.set_title('All permitted error vectors lie between the extremes', fontsize=11, pad=16)
    left.grid(axis='x', alpha=.15)
    left.set_ylim(-.7, 6.7)
    left.text(.5, -.22, 'Dotted lines: known exact benchmark values\nA = 3/32; B = 1/10',
              transform=left.transAxes, ha='center', fontsize=9, color='#44515c')
    b = result['budgets']
    vals = [f(b['tail_upper']), 2*f(b['sample_error']), f(b['quadrature'])]
    right.barh([2, 1, 0], vals, color=['#445f7b', '#b58139', '#70a8ab'])
    right.set_yticks([2, 1, 0], ['Tail bound', 'Two noise allowances', 'Quadrature'])
    right.set_xlim(0, .00165)
    for y, value in zip([2, 1, 0], vals):
        right.text(value + .00003, y, f'{value:.7f}', va='center', fontsize=9)
    right.set_xlabel('Contribution to returned interval width')
    right.set_title('Certified width < 0.001701', fontsize=11, pad=16)
    right.ticklabel_format(axis='x', style='sci', scilimits=(-3, -3))
    right.text(.5, -.22, 'Target: 0.002\nAdditional arithmetic width < 10⁻²⁴',
               transform=right.transAxes, ha='center', fontsize=9, color='#44515c')
    fig.suptitle('Hruday / HNM finite Euclidean readout certificate', fontsize=17, y=.98)
    fig.text(.5, .90, 'Synthetic benchmarks only · 4,097 samples · no AQ correlator data',
             ha='center', fontsize=11, color='#44515c')
    fig.subplots_adjust(left=.12, right=.97, top=.78, bottom=.25, wspace=.62)
    out = R / 'figures'
    out.mkdir(exist_ok=True)
    fig.savefig(out / 'hnm-euclidean-readout.pdf', metadata={'CreationDate': None, 'ModDate': None})
    fig.savefig(out / 'hnm-euclidean-readout.png', dpi=170)
    plt.close(fig)
    caption = {
        'gate': str(gate_path.relative_to(ROOT)),
        'gate_sha256': hashlib.sha256(gate_path.read_bytes()).hexdigest(),
        'source': str(result_path.relative_to(ROOT)),
        'source_sha256': hashlib.sha256(result_path.read_bytes()).hexdigest(),
        'caption': 'AT3 certified readout intervals for the abstract equal-moment fixtures A and B. Each row includes quadrature, tail, deterministic sample and outward arithmetic errors. Constant-sign errors bound every permitted sample-error vector. Dotted lines show the known exact fixture values. The width target is met and the complete A/B error envelopes are disjoint. No actual AQ correlation samples or AQ response value are supplied.',
        'plot_accuracy': 'Plot coordinates are floating renderings of reviewed exact rational enclosures; numerical claims come from the bound source JSON, not pixel geometry.',
        'scope': 'Synthetic benchmark and conditional evaluator, not a proposed experimental apparatus or measurement.'
    }
    (out / 'euclidean-caption.json').write_text(json.dumps(caption, indent=2) + '\n')


if __name__ == '__main__':
    main()
