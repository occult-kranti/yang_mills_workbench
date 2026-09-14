#!/usr/bin/env python3
"""Independent O1 rational, geometry and inference challenges; no producer imports."""
from fractions import Fraction as F
from pathlib import Path
from math import factorial
import argparse
import hashlib
import itertools
import json


def need(condition, message):
    if condition is not True:
        raise RuntimeError(message)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    out = p.parse_args().output
    need(not out.exists(), 'fresh output required')
    for component in (out.absolute(), *out.absolute().parents):
        need(not component.is_symlink(), 'symlink rejected')
    S = frozenset(((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)))
    def plus(a, b): return tuple(x+y for x, y in zip(a, b))
    def minus(a, b): return tuple(x-y for x, y in zip(a, b))
    def star(a): return frozenset(plus(a, b) for b in S)
    offsets = {minus(a, b) for a in S for b in S}
    need(len(offsets) == 13, 'star overlap')
    # Enumerate relative histories with ordered anchor tuples, not only unions.
    words = [(((0, 0, 0),), S)]
    word_rows = []
    for n in range(3):
        need(len(words) <= 13**n*factorial(n), 'ordered word count')
        weighted = sum(len(Y)*2**len(Y)*2**n for _, Y in words)
        upper = 16*(4+3*n)*208**n*factorial(n)
        need(weighted <= upper, 'root translation and support weight')
        need(all(len(Y) <= 4+3*n for _, Y in words), 'support growth')
        word_rows.append({'order': n, 'relative_histories': len(words),
                          'site_rooted_weight': weighted, 'reverse_upper': upper})
        if n < 2:
            next_words = []
            for history, Y in words:
                candidates = {minus(y, s) for y in Y for s in S}
                need(len(candidates) <= 13*(n+1), 'per insertion bound')
                next_words.extend((history+(a,), Y | star(a)) for a in candidates)
            words = next_words
    need(word_rows[1]['site_rooted_weight'] > 16*208, 'root multiplicity deletion must fail')
    full = set(itertools.product(range(4), repeat=3))
    retained = [a for a in full if star(a) <= full]
    need(max(sum(x in star(a) for a in retained) for x in full) == 4, 'diagonal overlap')
    first, second = star((1, 0, 0)), star((2, 0, 0))
    need(not bool(S & second) and bool((S | first) & second), 'base-only overlap misses word')
    need(len(S | first | second) == 10, 'generated support chain')

    Cf, Cr = F(25460736, 25), F(1970176, 5)
    tf, tr = F(5, 1536), F(5, 1664)
    need(Cf == 64*14*F(37, 5)*F(768, 5), 'forward constant')
    need(Cr == 16*20*F(37, 5)*F(832, 5), 'reverse constant')
    need(F(768, 5)*tf == F(1, 2) and F(832, 5)*tr == F(1, 2), 'closed endpoints')
    need(tr < tf and Cr < Cf, 'common conservative certificate')
    # The all-interval inequalities have exact factorizations/derivatives.
    for k in range(101):
        r = F(k, 200)
        need(14*r*(1-r)**3-(1-(1-r)**3)
             == r*(1-2*r)*(7*r*r-17*r+11), 'forward factorization')
        need(7*r*r-17*r+11 >= F(17, 4), 'positive last factor')
        need((7-4*r)/(1-r)**2 <= 20, 'reverse bound')
        need((10-4*r)/(1-r)**3 > 0, 'reverse monotonic derivative')

    # A new one-qubit fixture: h=diag(0,1), phi=tau/2 * [[0,1],[1,1]],
    # S=tau/2 * [[0,-1],[1,0]]. It obeys the norm upper assumptions;
    # it does not have or claim the physical SU(2) Haar variance.
    # Exact transformed offdiagonal is [tau*cos(tau)-(1+tau/2)*sin(tau)]/2.
    # cos(tau)<=1 and sin(tau)>=tau-tau^3/6 give the rational upper bound.
    t = F(1, 100)
    mixing_upper = -t*t/4+t**3/12+t**4/24
    vacuum_upper = -t*t/4+t**3/8+t**4/12
    need(mixing_upper < 0 and vacuum_upper < 0, 'scalar-centering counterexample')
    # Subtracting R00 changes no offdiagonal entry. For psi=Omega+z*e1,
    # the residual form has a nonzero linear term while <psi,h psi>=z^2.
    eps, volume = F(1, 1000), 2000
    need(2*eps < 1 and volume*eps > 1, 'local/global norm substitution')
    payload = {
        'schema': 'ym22-skeptic-independent-check-v1', 'loop': 'o1', 'passed': True,
        'driver_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'producer_imports': False, 'finite_checks_prove_unbounded_domain': False,
        'word_rows': word_rows,
        'rejected_inferences': ['missing site-root multiplicity', 'base-only overlap',
            'unchanging four-site support', 'diagonal overlap one',
            'scalar shift removes all vacuum mixing', 'local norm equals global norm'],
        'scalar_centering_fixture': {'scope': 'one-qubit lemma control, not SU2',
            'tau': str(t), 'vacuum_mean_upper': str(vacuum_upper),
            'centered_offdiagonal_upper': str(mixing_upper)},
        'common_certificate': {'tau0': str(tr), 'C': str(Cf), 'gap_threshold': False},
        'research_loops_added': 0
    }
    out.write_text(json.dumps(payload, sort_keys=True, indent=2)+'\n')
    print(json.dumps({'loop': 'o1', 'passed': True, 'checks': 'independent rational and geometry'}))


if __name__ == '__main__':
    main()
