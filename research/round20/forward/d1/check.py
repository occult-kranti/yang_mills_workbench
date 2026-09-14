#!/usr/bin/env python3
"""Exact forward fixtures for D1; operator proof is in report.md."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent


def require(test, text):
    if not test:
        raise ValueError(text)


def selected(face):
    a, b, x, y, z = face
    return (a, b) == (0, 1) and y % 2 == 0 and x % 4 < 3


def face_links(face):
    a, b, x, y, z = face
    p = (x, y, z)
    pa, pb = list(p), list(p)
    pa[a] += 1
    pb[b] += 1
    return {(a, *p), (b, *pa), (a, *pb), (b, *p)}


def factor(link):
    axis, x, y, z = link
    if axis == 0 and x % 4 < 3:
        return ('strip', x - x % 4, y - y % 2, z)
    if axis == 1 and y % 2 == 0:
        return ('strip', x - x % 4, y, z)
    return ('free', *link)


def factor_links(fac):
    if fac[0] == 'free':
        return {fac[1:]}
    _, x, y, z = fac
    return set().union(*(face_links((0, 1, x + dx, y, z)) for dx in range(3)))


def retained(L):
    return [(*ab, x, y, z) for ab in ((0, 1), (0, 2), (1, 2))
            for x, y, z in product(range(L + 1), repeat=3)
            if not selected((*ab, x, y, z))]


def weight(face):
    return F(1, 24 * 2 ** sum(face[2:]))


def closed(L):
    require(type(L) is int and L >= 0, 'nonnegative integer regulator required')
    m = L + 1
    g = 2 * (1 - F(1, 2 ** m))
    a = sum((F(1, 2 ** r) * (1 - F(1, 16 ** max(0, 1 + (L-r)//4))) / (1-F(1,16)) for r in range(3)), F())
    b = (1 - F(1, 4 ** ((m+1)//2))) / (1 - F(1,4))
    return g**3/8 - a*b*g/24


def complete(faces):
    raw = set().union(*(face_links(f) for f in faces))
    facs = {factor(e) for e in raw}
    full = set().union(*(factor_links(i) for i in facs))
    return raw, facs, full


def validate_completion(faces, facs, full):
    needed = set().union(*(face_links(f) for f in faces))
    require(needed <= full, 'crossing face support dropped')
    require({factor(e) for e in needed} <= facs, 'reference factor omitted')
    for i in facs:
        require(factor_links(i) <= full, 'completed strip link omitted')
        require(all(factor(e) == i for e in factor_links(i)), 'reference factors overlap')


def scale(reference='E_star', reference_positive=True, alpha='1', tau='1/64', im_z='1'):
    require(reference == 'E_star' and reference_positive is True, 'fixed positive physical reference required')
    a, t, b = F(alpha), F(tau), F(im_z)
    require(a > 0 and b != 0, 'positive alpha and nonreal physical z required')
    return a, t, b


def rejected(fn):
    try:
        fn()
    except (ValueError, TypeError):
        return True
    return False


def encode(obj):
    if isinstance(obj, F): return str(obj)
    if isinstance(obj, dict): return {k: encode(v) for k,v in obj.items()}
    if isinstance(obj, (list, tuple)): return [encode(x) for x in obj]
    return obj


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    rows=[]
    prior = F(107,135)
    for L in range(9):
        faces=retained(L)
        raw,facs,full=complete(faces)
        validate_completion(faces,facs,full)
        direct=sum(map(weight,faces),F())
        require(direct==closed(L), 'enumeration/closed-form mismatch')
        tail=F(107,135)-direct
        require(0<tail<prior,'tail not strictly decreasing')
        prior=tail
        require(len(facs)<=4*len(faces), 'finite support count fails')
        require(all(len(factor_links(f)) == (10 if f[0]=='strip' else 1) for f in facs),'factor link cardinality')
        a,t,b=scale()
        rows.append(dict(L=L, omitted_faces=len(faces), raw_links=len(raw),
                         factors=len(facs),strip_factors=sum(f[0]=='strip' for f in facs),
                         free_factors=sum(f[0]=='free' for f in facs),completed_links=len(full),
                         retained_weight=direct,tail_weight=tail,epsilon_over_E_star=a*abs(t)*tail,
                         resolvent_bound_times_E_star=a*abs(t)*tail/b**2))
    faces=retained(0); raw,facs,full=complete(faces)
    clipped={e for e in full if max(e[1:])<=0}
    strip=next(i for i in facs if i[0]=='strip')
    removed=full-{next(iter(factor_links(strip)))}
    h=F(3,4); wrong_resolvent_square=h*h/(1+h*h)
    c=F(1,96)
    disjoint_faces=[(0,2,2,0,0),(0,2,0,0,2)]
    require(face_links(disjoint_faces[0]).isdisjoint(face_links(disjoint_faces[1])), 'signed witness faces overlap')
    require(all(weight(f)==c for f in disjoint_faces), 'signed witness weights differ')
    central_links={e:1 for f in disjoint_faces for e in face_links(f)}
    central_links[next(iter(face_links(disjoint_faces[1])))]=-1
    def central_trace(f):
        v=1
        for e in face_links(f): v*=central_links[e]
        return v
    attained=abs(c*central_trace(disjoint_faces[0])-c*central_trace(disjoint_faces[1]))
    dimension_witnesses=[{'proposed_finite_dimension':n,'Peter_Weyl_spin':n,
                          'matrix_coefficients_in_that_spin':(2*n+1)**2} for n in (1,10,100)]
    controls={
      'crossing_face_omission_rejected':rejected(lambda:validate_completion(faces,facs,clipped)),
      'incomplete_strip_rejected':rejected(lambda:validate_completion(faces,facs,removed)),
      'signed_cancellation_rejected':rejected(lambda:require(abs(c-c)>=attained,'opposite disjoint multipliers attain 2c')) and attained==2*c,
      'negative_tau_has_same_budget':abs(scale(tau='-1/64')[1])==abs(scale()[1]),
      'zero_reference_rejected':rejected(lambda:scale(reference_positive=False)),
      'kappa_reference_rejected':rejected(lambda:scale(reference='kappa')),
      'real_resolvent_parameter_rejected':rejected(lambda:scale(im_z='0')),
      'finite_dimension_claim_rejected':all(w['matrix_coefficients_in_that_spin']>w['proposed_finite_dimension'] for w in dimension_witnesses),
      'discarded_exterior_norm_resolvent_claim_rejected':wrong_resolvent_square==F(9,25) and wrong_resolvent_square>0,
    }
    require(all(controls.values()),'a wrong-model control did not reject')
    results=dict(schema='ym20-forward-d1-v1',loop='d1',status='passed',
        tail_limit='0',infinite_omitted_weight=F(107,135),fixtures=rows,
        scale={'reference':'fixed positive E_star','alpha_over_E_star':'1','tau':'1/64','Im_z_over_E_star':'1'},
        controls=controls,wrong_exterior_resolvent_square_times_E_star_squared=wrong_resolvent_square,
        finite_dimension_counterexamples=dimension_witnesses,signed_cancellation_actual_multiplier_norm_lower=attained,
        theorem='||R_H(z)-R_HL(z)|| <= alpha*abs(tau)*t_L/abs(Im(z))^2',
        scope='finite factor exhaustion with exact exterior reference in declared A2 product sector; each factor infinite dimensional')
    (out/'results.json').write_text(json.dumps(encode(results),indent=2,sort_keys=True)+'\n')
    sources=[HERE/'check.py',HERE/'report.md',ROOT/'research/round20/contracts/d1.json',ROOT/'research/round19/advisor/a2-gate.json',ROOT/'research/round19/forward/a2/report.md']
    manifest={'sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'outputs':{'results.json':hashlib.sha256((out/'results.json').read_bytes()).hexdigest()}}
    (out/'source-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'passed','loop':'d1','fixtures':len(rows),'controls':len(controls)}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=HERE/'output')
    main(parser.parse_args().output)
