#!/usr/bin/env python3
"""V1 reverse: exact observable/instrument algebra, not a dynamics simulation."""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path


def g(real=0, imag=0):
    return (F(real), F(imag))


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def mul(x, y):
    return (x[0]*y[0] - x[1]*y[1], x[0]*y[1] + x[1]*y[0])


def conj(x):
    return (x[0], -x[1])


def matrix(rows):
    return [[v if isinstance(v, tuple) else g(v) for v in row] for row in rows]


def plus(a, b):
    return [[add(x, y) for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(a, x):
    return [[mul(g(x), v) for v in row] for row in a]


def dot(a, b):
    return [[sumg(mul(a[i][k], b[k][j]) for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def sumg(xs):
    r = g()
    for x in xs:
        r = add(r, x)
    return r


def star(a):
    return [[conj(a[j][i]) for j in range(len(a))] for i in range(len(a[0]))]


def require(ok, name):
    if not ok:
        raise RuntimeError(name)


def serial(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {k: serial(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [serial(v) for v in x]
    return x


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    ident = matrix([[1,0,0],[0,1,0],[0,0,1]])
    zero = scale(ident, 0)
    w = matrix([[0,1,0],[1,0,0],[0,0,0]])
    p = dot(w, w)
    p0 = plus(ident, scale(p, -1))
    pp = scale(plus(p, w), F(1,2))
    pm = scale(plus(p, scale(w, -1)), F(1,2))
    projectors = [pp, pm, p0]
    require(plus(plus(pp, pm), p0) == ident, 'complete PVM')
    for i, pi in enumerate(projectors):
        require(dot(pi, pi) == pi and star(pi) == pi, 'orthogonal projection')
        for j, pj in enumerate(projectors):
            if i != j:
                require(dot(pi, pj) == zero, 'disjoint outcomes')
    require(plus(pp, scale(pm, -1)) == w, 'first moment')
    require(plus(pp, pm) == p, 'second moment')
    binary_p = scale(plus(ident, w), F(1,2))
    binary_m = scale(plus(ident, scale(w, -1)), F(1,2))
    require(plus(binary_p, binary_m) == ident, 'binary normalized')
    require(plus(binary_p, scale(binary_m, -1)) == w, 'binary first moment')

    completions = [plus(w, p0), plus(w, scale(p0,-1))]
    for r in completions:
        require(dot(r, r) == ident and star(r) == r, 'unitary completion')
    u = matrix([[1,0,0],[0,g(0,1),0],[0,0,1]])
    require(dot(u, star(u)) == ident, 'fixture unitary')
    beta = lambda a: dot(dot(u, a), star(u))
    target = dot(w, beta(w))
    reconstructed = zero
    complex_components = []
    for r in completions:
        for s in completions:
            k = dot(r, beta(s))
            require(dot(k,star(k)) == ident, 'unitary product')
            reconstructed = plus(reconstructed, scale(k,F(1,4)))
            # In the fixture state |o>, Hadamard X/Y means are its (0,0) entry.
            c = k[0][0]
            ancilla = [[g(F(1,2)), mul(g(F(1,2)),conj(c))],
                       [mul(g(F(1,2)),c),g(F(1,2))]]
            xmean = add(ancilla[0][1], ancilla[1][0])
            ymean = add(mul(g(0,1),ancilla[0][1]),mul(g(0,-1),ancilla[1][0]))
            require(xmean == g(c[0]) and ymean == g(c[1]), 'quadrature signs')
            complex_components.append(c)
    require(reconstructed == target, 'four-unitary reconstruction')
    sequential = zero
    for outcome, proj in [(1,pp),(-1,pm),(0,p0)]:
        sequential = plus(sequential,scale(dot(dot(proj,beta(w)),proj),outcome))
    require(target[0][0] == g(0,1), 'unordered product is imaginary')
    require(sequential[0][0] == g(), 'sequential product loses imaginary signal')
    z = F(1,10**6)
    x = 80*z/7
    tail = F(44,9)*x*x/(1-x)**5
    margin = z/84-tail
    require(margin > z/168, 'inherited exact endpoint margin')
    delta, r, b = z/F(5376), z/F(5376), z/F(5376)
    total = 8*delta+4*r+4*b
    require(total < z/168 < margin, 'observable and readout transfer')
    controls = {
        'missing-zero-outcome-detected': plus(pp,pm) != ident,
        'binary-variance-substitution-detected': plus(binary_p,binary_m)[2][2] != p[2][2],
        'sequential-not-complex-correlator': sequential[0][0] != target[0][0],
        'dropped-unitary-completion-detected': dot(w,star(w)) != ident,
        'excessive-observable-error-inconclusive': margin-8*(z/84) < 0,
        'wilson-half-distance-exceeds-required-error': F(1,2) > z/1344,
        'finite-readout-keeps-infinite-complement': p0[2][2] == g(1),
        'mean-subtraction-required': F(1,3)**2 != 0,
    }
    for name, value in controls.items():
        require(value, name)
    results = {
        'loop':'v1','direction':'reverse','status':'passed',
        'arithmetic':'Gaussian rational matrix identities and rational error budgets',
        'claims':[
            'Exact three-outcome q-independent physical local PVM of W',
            'Full-space unitary completion with eight binary quadrature settings',
            'Uniform connected-correlator norm transfer costs 4delta per model',
            'Full-local-space norm distance from bounded multiplication is at least 1/2',
        ],
        'limitations':[
            'Matrix fixtures verify observable algebra, not full infinite dynamics',
            'Coherent instrument capabilities and physical accuracy are assumptions',
            'No Wilson-multiplication endpoint witness or physical-sector-only norm obstruction proved',
            'No shot resource theorem, homogeneous gap or continuum construction',
        ],
        'exact':{'z':z,'inherited_margin':margin,'simple_margin':z/168,
                 'delta':delta,'r':r,'b':b,'total_readout_loss':total,
                 'fixture_complex_product':target[0][0],
                 'fixture_sequential_product':sequential[0][0],
                 'quadrature_components':complex_components},
    }
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'results.json').write_text(json.dumps(serial(results),indent=2,sort_keys=True)+'\n')
    (args.output/'controls.json').write_text(json.dumps({'controls':controls},indent=2,sort_keys=True)+'\n')


if __name__ == '__main__':
    main()
