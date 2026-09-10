"""Exact S3 joint-Gram recurrence for the declared four-face observable."""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import hashlib
import itertools
import json
import math

SOURCE_BYTES = Path(__file__).read_bytes()
SOURCE_SHA = hashlib.sha256(SOURCE_BYTES).hexdigest()
DIMENSION = 4
TAYLOR_DEGREE = 6
MAX_MOMENT_DEGREE = 14
_DECLARED = json.dumps([DIMENSION, TAYLOR_DEGREE, MAX_MOMENT_DEGREE, SOURCE_SHA], separators=(',', ':'))


def unchanged():
    if Path(__file__).read_bytes() != SOURCE_BYTES:
        raise ValueError('loaded Gram source changed')
    if json.dumps([DIMENSION, TAYLOR_DEGREE, MAX_MOMENT_DEGREE, SOURCE_SHA], separators=(',', ':')) != _DECLARED:
        raise ValueError('declared dimension or degree changed')


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)


def rational(value):
    if type(value) is not str or len(value) > 1000:
        raise ValueError('canonical rational string required')
    try:
        q = F(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError('invalid rational') from exc
    if str(q) != value:
        raise ValueError('noncanonical rational')
    return q


def _matrix(value, rows, columns):
    if type(value) not in (list, tuple) or len(value) != rows:
        raise ValueError('incorrect matrix row count')
    if any(type(row) not in (list, tuple) or len(row) != columns for row in value):
        raise ValueError('incorrect nested matrix type or width')
    return tuple(tuple(rational(x) for x in row) for row in value)


def _coefficients(value):
    if type(value) not in (list, tuple) or len(value) != 4:
        raise ValueError('exactly four individual coefficients required')
    return tuple(rational(x) for x in value)


def _psd_rank(matrix):
    """Full rational semidefinite Schur elimination, permitting null pivots."""
    work = [list(row) for row in matrix]
    rank = 0
    while work:
        if any(work[i][i] < 0 for i in range(len(work))):
            raise ValueError('Gram is not positive semidefinite')
        pivot = next((i for i in range(len(work)) if work[i][i] > 0), None)
        if pivot is None:
            if any(x != 0 for row in work for x in row):
                raise ValueError('zero-diagonal block has nonzero off-diagonal entries')
            return rank
        p = work[pivot][pivot]
        rest = [i for i in range(len(work)) if i != pivot]
        work = [[work[i][j]-work[i][pivot]*work[pivot][j]/p for j in rest] for i in rest]
        rank += 1
    return rank


def validate(gram, kappa):
    """Validate the whole declared family before invoking any cached moment."""
    unchanged()
    g = _matrix(gram, 5, 5)
    k = _coefficients(kappa)
    if any(g[i][j] != g[j][i] for i in range(5) for j in range(5)):
        raise ValueError('Gram must be symmetric')
    rank = _psd_rank(g)
    if rank > 4:
        raise ValueError('Gram rank exceeds ambient dimension four')
    if any(g[i][i] != 1 for i in range(1, 5)):
        raise ValueError('all four observable directions must be unit vectors')
    if any(g[0][i] != sum((k[j]*g[j+1][i] for j in range(4)), F(0)) for i in range(1, 5)):
        raise ValueError('action-direction cross constraints fail')
    if g[0][0] != sum((k[i]*k[j]*g[i+1][j+1] for i in range(4) for j in range(4)), F(0)):
        raise ValueError('action norm constraint fails')
    return g, k, rank


def vector_data(directions, kappa, action=None):
    unchanged()
    a = _matrix(directions, 4, 4)
    k = _coefficients(kappa)
    b = tuple(sum((k[i]*a[i][j] for i in range(4)), F(0)) for j in range(4))
    if action is not None:
        if type(action) not in (list, tuple) or len(action) != 4 or tuple(rational(x) for x in action) != b:
            raise ValueError('supplied action vector differs from the declared linear combination')
    vectors = (b,)+a
    g = tuple(tuple(sum((x*y for x, y in zip(u, v)), F(0)) for v in vectors) for u in vectors)
    strings = [[str(x) for x in row] for row in g]
    _, _, rank = validate(strings, list(map(str, k)))
    return {'vectors': [list(map(str, row)) for row in vectors], 'gram': strings, 'rank': rank,
            'kappa': list(map(str, k)), 'vector_order': ['b', 'a1', 'a2', 'a3', 'a4']}


def _exponents(value):
    if type(value) not in (list, tuple) or len(value) != 5 or any(type(x) is not int or x < 0 for x in value):
        raise ValueError('five nonnegative exact integer exponents required')
    if sum(value) > MAX_MOMENT_DEGREE:
        raise ValueError('moment degree exceeds the declared diagnostic budget')
    return tuple(value)


@lru_cache(maxsize=32768)
def _moment(g, exponents):
    total = sum(exponents)
    if total == 0:
        return F(1)
    if total % 2:
        return F(0)
    i = next(i for i, k in enumerate(exponents) if k > 0)
    value = F(0)
    for j in range(5):
        multiplicity = exponents[j]-int(i == j)
        # A zero multiplicity must be skipped before building lower powers.
        if multiplicity == 0:
            continue
        lowered = list(exponents)
        lowered[i] -= 1
        lowered[j] -= 1
        if any(x < 0 for x in lowered):
            raise RuntimeError('recurrence generated a negative exponent')
        value += multiplicity*g[i][j]*_moment(g, tuple(lowered))
    return value/(DIMENSION+total-2)


def moment(gram, kappa, exponents):
    g, _, _ = validate(gram, kappa)
    e = _exponents(exponents)
    return _moment(g, e)


def coefficients(gram, kappa):
    g, _, _ = validate(gram, kappa)
    numerator, partition = [], []
    for n in range(TAYLOR_DEGREE+1):
        z = _moment(g, (n, 0, 0, 0, 0))/math.factorial(n)
        value = F(0)
        for chosen in itertools.product((0, 1), repeat=4):
            m = sum(chosen)
            e = (n,)+tuple(2*x for x in chosen)
            value += F(4**m*(-1)**(4-m), 81)*_moment(g, e)
        numerator.append(value/math.factorial(n))
        partition.append(z)
    # Immutable values protect cached arithmetic from caller mutation.
    return tuple(numerator), tuple(partition)


def primitive_moments(gram, kappa):
    g, _, _ = validate(gram, kappa)
    return [{'degree': n, 'subset_mask': mask,
             'exponents': [n]+[2*((mask >> i) & 1) for i in range(4)],
             'moment': str(_moment(g, (n,)+tuple(2*((mask >> i) & 1) for i in range(4))))}
            for n in range(TAYLOR_DEGREE+1) for mask in range(16)]


def certify(directions, kappa, action=None):
    data = vector_data(directions, kappa, action)
    num, den = coefficients(data['gram'], data['kappa'])
    return {'schema': 'ym18-c1-certificate-v1', 'source_sha256': SOURCE_SHA,
            **data, 'dimension': 4, 'formal_parameter': 't; not physical time', 'degree': 6,
            'observable': 'product_i(4(q dot a_i)^2-1)/81',
            'action': 'q dot b with b=sum_i kappa_i a_i',
            'numerator_coefficients': list(map(str, num)), 'partition_coefficients': list(map(str, den)),
            'primitive_moments': primitive_moments(data['gram'], data['kappa']),
            'coefficient_convention': '[t^n] includes 1/n! for exp(t q dot b)',
            'scope': 'exact degree-zero-through-six diagnostics; no tail certificate or surrounding-link integration',
            'admissibility': 'symmetric PSD rank<=4, unit directions, full action cross and norm constraints'}


def verify(certificate):
    if type(certificate) is not dict:
        raise ValueError('certificate object required')
    try:
        v = certificate['vectors']
        if type(v) is not list or len(v) != 5:
            raise ValueError('complete five-vector data required')
        expected = certify(v[1:], certificate['kappa'], v[0])
    except KeyError as exc:
        raise ValueError('incomplete certificate') from exc
    if canonical(certificate) != canonical(expected):
        raise ValueError('certificate differs from complete source-bound replay')
    return True


def transform(directions, orthogonal):
    unchanged()
    a = _matrix(directions, 4, 4)
    h = _matrix(orthogonal, 4, 4)
    if any(sum((h[i][k]*h[j][k] for k in range(4)), F(0)) != int(i == j) for i in range(4) for j in range(4)):
        raise ValueError('common transformation must be orthogonal')
    return [[str(sum((row[k]*h[j][k] for k in range(4)), F(0))) for j in range(4)] for row in a]


def fixture_inputs():
    tetra = [['1/2']+list(map(str, signs)) for signs in
             [(F(1, 2), F(1, 2), F(1, 2)), (F(1, 2), F(-1, 2), F(-1, 2)),
              (F(-1, 2), F(1, 2), F(-1, 2)), (F(-1, 2), F(-1, 2), F(1, 2))]]
    commuting = [['1', '0', '0', '0'], ['1', '0', '0', '0'], ['0', '1', '0', '0'], ['0', '-1', '0', '0']]
    hadamard = [[str(F(x, 2)) for x in row] for row in [(1, 1, 1, 1), (1, -1, 1, -1), (1, 1, -1, -1), (1, -1, -1, 1)]]
    reflection = [[str(-1 if i == j == 0 else int(i == j)) for j in range(4)] for i in range(4)]
    common = ['1/16']*4
    return [
        ('tetra_common', tetra, common), ('commuting_common', commuting, common),
        ('tetra_hadamard', transform(tetra, hadamard), common),
        ('commuting_hadamard', transform(commuting, hadamard), common),
        ('tetra_reflected', transform(tetra, reflection), common),
        ('commuting_reflected', transform(commuting, reflection), common),
        ('rank1_equal', [['1', '0', '0', '0'] for _ in range(4)], common),
        ('rank2', [['1', '0', '0', '0'], ['0', '1', '0', '0'], ['3/5', '4/5', '0', '0'], ['-4/5', '3/5', '0', '0']], common),
        ('tetra_zero_kappa', tetra, ['0']*4),
        ('tetra_signed_kappa', tetra, ['1/16', '-1/32', '1/8', '-3/64']),
        ('commuting_zero_b_nonzero_kappa', commuting, ['1/16', '-1/16', '1/16', '1/16']),
    ]


def collection():
    unchanged()
    return {'schema': 'ym18-c1-collection-v1', 'source_sha256': SOURCE_SHA,
            'dimension': 4, 'degree': 6, 'vector_order': ['b', 'a1', 'a2', 'a3', 'a4'],
            'fixtures': [{'id': name, 'certificate': certify(a, k)} for name, a, k in fixture_inputs()],
            'historical_convention': {
                'round17': 'trace directions were conjugate boundary quaternions (h0,-h1,-h2,-h3)',
                'current': 'base fixtures use the listed h coordinates as direction vectors',
                'common_reflection_to_round17': [['1', '0', '0', '0'], ['0', '-1', '0', '0'], ['0', '0', '-1', '0'], ['0', '0', '0', '-1']],
                'effect': 'transform every action and observable direction together; complete Gram unchanged; common scalar-axis action unchanged'},
            'isometry_scope': 'full untruncated central integrals of the declared dot-product observable/action family; no transformation of surrounding-link measure',
            'coefficient_scope': 'formal Taylor coefficients only; t is not physical time and no finite-t error bound is claimed'}


def verify_collection(value):
    if type(value) is not dict or canonical(value) != canonical(collection()):
        raise ValueError('missing or changed frozen C1 evidence')
    return True
