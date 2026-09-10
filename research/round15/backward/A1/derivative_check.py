"""Independent raw-moment product rule versus centered-moment expansion."""
from itertools import combinations
import json


def add(poly, factors, value):
    key = tuple(sorted(factors))
    poly[key] = poly.get(key, 0) + value
    if poly[key] == 0:
        del poly[key]


def differentiate_covariance():
    out = {}
    # D mu_ab0 = mu_ab1 - mu_ab0 mu_001; explicit product rule.
    add(out, [(1,1,1)], 1)
    add(out, [(1,1,0),(0,0,1)], -1)
    add(out, [(1,0,1),(0,1,0)], -1)
    add(out, [(1,0,0),(0,0,1),(0,1,0)], 1)
    add(out, [(1,0,0),(0,1,1)], -1)
    add(out, [(1,0,0),(0,1,0),(0,0,1)], 1)
    return out


def expand_centered():
    out = {}
    labels = tuple(range(3))
    unit = [(1,0,0),(0,1,0),(0,0,1)]
    for size in range(4):
        for selected in combinations(labels, size):
            factors = [unit[i] for i in selected]
            remainder = tuple(int(i not in selected) for i in labels)
            if any(remainder):
                factors.append(remainder)
            add(out, factors, (-1)**size)
    return out


def run():
    differentiated = differentiate_covariance()
    centered = expand_centered()
    if differentiated != centered:
        raise ValueError('independent derivative/centered expansion mismatch')
    omitted = dict(centered)
    del omitted[((0,0,1),(0,1,0),(1,0,0))]
    if differentiated == omitted:
        raise ValueError('omitted normalization derivative was not detected')
    wrong = dict(centered)
    wrong[((0,0,1),(0,1,0),(1,0,0))] = 1
    if differentiated == wrong:
        raise ValueError('wrong centered-product multiplicity was not detected')
    return {'status':'passed','checks':3,
            'identity':"C_prime = E[(x-Ex)(y-Ey)(z-Ez)]",
            'analytic_bound':'2 from bounded dz, Cauchy-Schwarz and variances<=1',
            'terms':[{'moments':[list(v) for v in key],'coefficient':value}
                     for key,value in sorted(differentiated.items())]}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
