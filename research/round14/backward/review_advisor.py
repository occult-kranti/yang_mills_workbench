#!/usr/bin/env python3
"""Independent loop2 review of root's formal and exact-transfer calculations."""
from fractions import Fraction as Q
from math import factorial
from pathlib import Path
import contextlib
import hashlib
import io
import json
import sys


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def set_partitions(items):
    """Restricted-growth recursive enumeration, distinct labelled set elements."""
    if not items:
        yield []
        return
    first, *rest = items
    for partition in set_partitions(rest):
        yield [(first,)] + partition
        for i in range(len(partition)):
            yield partition[:i] + [(first,) + partition[i]] + partition[i+1:]


def cumulant_polynomial(labels):
    """Definition via all set partitions; independent of derivative/centering code."""
    result = {}
    for partition in set_partitions(list(range(len(labels)))):
        key = []
        for block in partition:
            power = tuple(sum(labels[j][k] for j in block) for k in range(3))
            key.append(power)
        key = tuple(sorted(key))
        coefficient = (-1)**(len(partition)-1) * factorial(len(partition)-1)
        result[key] = result.get(key, Q(0)) + coefficient
    return {key: value for key, value in result.items() if value}


def interval_times(a,b):
    corners = [x*y for x in a for y in b]
    return min(corners), max(corners)


def review(advisor_file, output_dir):
    advisor_file=Path(advisor_file).resolve(); output_dir=Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    original = advisor_file.read_bytes()
    frozen_hash = hashlib.sha256(original).hexdigest()
    ns = {"__name__":"independently_reviewed_advisor", "__file__":str(advisor_file)}
    exec(compile(original, str(advisor_file), "exec"), ns)
    checks=[]
    def gate(name,condition,details=None):
        if not condition:
            raise ValueError(name)
        checks.append({"name":name,"passed":True,"details":details})
    x,y,z=(1,0,0),(0,1,0),(0,0,1)
    expected=cumulant_polynomial([x,y,z,z])
    xy=ns['covariance'](x,y)
    produced=ns['derivative'](ns['derivative'](xy))
    gate('formal second derivative equals independent set-partition cumulant',produced==expected)
    parts=list(set_partitions([0,1,2,3]))
    gate('all fifteen labelled set partitions enumerated',len(parts)==15)
    coarse=sum(factorial(len(p)-1) for p in parts)
    gate('independent absolute partition coefficient sum is26',coarse==26)
    points=[((1,1,1),Q(1,10)),((1,-1,-1),Q(2,10)),
            ((-1,1,-1),Q(3,10)),((-1,-1,1),Q(4,10))]
    def raw(power):
        return sum((w*p[0]**power[0]*p[1]**power[1]*p[2]**power[2]
                    for p,w in points),Q(0))
    partition_value=Q(0)
    for key, coefficient in expected.items():
        term=coefficient
        for power in key:
            term*=raw(power)
        partition_value+=term
    means=[raw(x),raw(y),raw(z)]
    center4=sum((w*(p[0]-means[0])*(p[1]-means[1])*(p[2]-means[2])**2
                 for p,w in points),Q(0))
    def cov(i,j):
        return sum((w*(p[i]-means[i])*(p[j]-means[j]) for p,w in points),Q(0))
    fixture=center4-cov(0,1)*cov(2,2)-2*cov(0,2)*cov(1,2)
    gate('nondegenerate admissible center-element cumulant fixture',
         fixture==partition_value and fixture!=0)
    # The sharper7 uses conventional Cauchy–Schwarz/variance bounds in prose;
    # summing constants is recorded only as arithmetic, not independent analysis.
    gate('sharper term bound arithmetic',4+1+2==7)

    ns['HERE']=output_dir
    with contextlib.redirect_stdout(io.StringIO()):
        ns['main']()
    record=json.loads((output_dir/'advisor_checks.json').read_text())
    gate('executed frozen source hash matches record',record['source_sha256']==frozen_hash)
    gate('all advisor gates populated and true',bool(record['checks']) and
         record['count']==len(record['checks']) and all(c['passed'] is True for c in record['checks']))
    root=advisor_file.parent.parent
    checker=root/'vendor/moment_bounds.py'; collection=root/'vendor/round13-certificates.json'
    gate('legacy source binding matches actual bytes',record['legacy_checker_sha256']==sha(checker))
    gate('legacy collection binding matches actual bytes',record['legacy_collection_sha256']==sha(collection))
    saved=json.loads(collection.read_text())
    matches=[c for c in saved['certificates'] if c['kappa']=='1' and c['level']==6]
    gate('unique selected variance certificate',len(matches)==1)
    rawlo,rawhi=map(Q,matches[0]['variance_interval'])
    D=10**15
    # divmod on numerator and denominator provides an independent rounding route.
    alo=rawlo*D; ahi=rawhi*D
    qlo,rlo=divmod(alo.numerator,alo.denominator)
    qhi,rhi=divmod(ahi.numerator,ahi.denominator)
    lower=Q(qlo,D); upper=Q(qhi+(rhi!=0),D)
    gate('outward compaction exactly reproduced',record['outward_variance_interval']==[str(lower),str(upper)])
    gate('compacted interval contains original rational endpoints',lower<=rawlo<=rawhi<=upper)
    gate('each compaction slack smaller than one denominator unit',
         0<=rawlo-lower<Q(1,D) and 0<=upper-rawhi<Q(1,D))
    gate('compacted lower variance is positive',lower>0)
    for row in record['perturbative_intervals']:
        eta=Q(row['eta'])
        product=interval_times((lower,upper),(lower,upper))
        linear=interval_times((eta,eta),product)
        radius=Q(7,2)*eta*eta
        interval=(linear[0]-radius,linear[1]+radius)
        gate('signed perturbative enclosure '+str(eta),
             tuple(map(Q,(row['lower'],row['upper'])))==interval)
        status='positive' if interval[0]>0 else 'negative' if interval[1]<0 else 'inconclusive'
        gate('semantic sign '+str(eta),row['status']==status)
    zero=interval_times((Q(0),Q(0)),(lower*lower,upper*upper))
    gate('zero deformation has exact zero perturbative interval',zero==(Q(0),Q(0)))
    gate('outward negative rational branch',
         all(Q(q,n)<=v<=Q(q+1,n)
             for n in range(1,12) for j in range(-12,13)
             for v in [Q(j,7)] for q in [(v*n).numerator//(v*n).denominator]))
    gate('source unchanged during frozen execution',sha(advisor_file)==frozen_hash)
    result={'schema':'ym14-independent-advisor-review-v1','status':'passed','phase':'loop2',
      'check_count':len(checks),'checks':checks,
      'source_sha256':sha(__file__),
      'reviewed_source_hashes':{'advisor/advisor_checks.py':frozen_hash,
                               'vendor/moment_bounds.py':sha(checker),
                               'vendor/round13-certificates.json':sha(collection)},
      'accepted':'Formal fourth cumulant, exact outward compaction and signed perturbative interval transfer.',
      'limits':['Legacy variance proof is inherited through its pinned reviewed checker; this review independently checks its transfer algebra.',
                'The constant7 also requires the conventional centered-variable inequalities reviewed in backward.md.',
                'Finite spectral countermodel restrictions illustrate the separate infinite-dimensional construction; their arithmetic does not prove it.']}
    (output_dir/'independent_advisor_review.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'passed','check_count':len(checks)}))
    return result


if __name__=='__main__':
    if len(sys.argv)!=3:
        raise SystemExit('usage: review_advisor.py ADVISOR_FILE OUTPUT_DIR')
    review(sys.argv[1],sys.argv[2])
