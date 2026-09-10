"""Check the actual two-link geometry, exact moments and complete interval ladder."""
import argparse
import copy
import csv
import hashlib
import json
import math
from fractions import Fraction as F
from pathlib import Path
import joint


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    source, out = Path(__file__).resolve().parent, Path(args.output).resolve()
    if out == source or out in source.parents:
        raise ValueError('output cannot overwrite source directory or an ancestor')
    out.mkdir(parents=True, exist_ok=True)
    checks = []

    def check(name, condition):
        if not condition:
            raise RuntimeError(name)
        checks.append(name)

    def reject(name, call):
        try:
            call()
        except (ValueError, TypeError, KeyError):
            checks.append('reject: '+name)
            return
        raise RuntimeError('invalid accepted: '+name)

    evidence = joint.collection()
    check('complete source-bound graph moment fixture and tail inventory replays', joint.verify_collection(evidence))
    geometry = evidence['geometry']
    check('actual four-cube graph has18vertices33links20faces', geometry['counts'] == [18, 33, 20])
    check('six affected faces retain exactly three U-only two V-only and one shared weight',
          {key:len(value) for key,value in geometry['categories'].items()} == {'constant':14,'x':3,'y':2,'w':1}
          and len(geometry['affected_faces']) == 6)
    faces = {f['id']:f for f in evidence['graph']['faces']}
    u, v = evidence['graph']['variable_links']['U'], evidence['graph']['variable_links']['V']
    utouch = {f['id'] for f in faces.values() if any(t['edge'] == u for t in f['word'])}
    vtouch = {f['id'] for f in faces.values() if any(t['edge'] == v for t in f['word'])}
    check('actual U and V incidence has four and three faces with one shared intersection',
          len(utouch) == 4 and len(vtouch) == 3 and len(utouch & vtouch) == 1
          and utouch | vtouch == set(geometry['affected_faces']))
    shared = geometry['categories']['w'][0]
    reduced = [term for term in faces[shared]['word'] if term['edge'] in (u,v)]
    check('actual shared oriented word reduces pointwise to U Vdagger', reduced == [{'edge':u,'sign':1},{'edge':v,'sign':-1}])
    check('noncommuting rational links satisfy all twenty actual word reductions',
          geometry['pointwise_noncommuting_fixture']['noncommuting']
          and all(row['actual_trace'] == row['reduced_trace'] for row in geometry['pointwise_noncommuting_fixture']['faces']))
    q = joint.quaternion(['3/5','4/5','0','0'])
    check('wrong dagger is discriminated pointwise by an exact rational fixture',
          joint.multiply(q,joint.conjugate(q))[0] == 1 and joint.multiply(q,q)[0] == F(-7,25))
    U = joint.quaternion(['3/5','4/5','0','0'])
    V = joint.quaternion(['5/13','0','12/13','0'])
    check('consistent dagger substitution preserves y and exchanges the two shared trace conventions',
          joint.conjugate(V)[0] == V[0] and joint.conjugate(joint.conjugate(V)) == V
          and joint.multiply(U,joint.conjugate(joint.conjugate(V)))[0] == joint.multiply(U,V)[0])
    inventory = evidence['joint_moments']
    check('complete969-moment superset includes every triple through totaldegree16',
          len(inventory) == math.comb(19,3) == 969
          and len({tuple(row['exponents']) for row in inventory}) == 969
          and all(sum(row['exponents']) <= 16 for row in inventory))
    check('correlated character convolution gives the exact mixed moments',
          joint.moment([1,1,1]) == F(1,16) and joint.moment([2,2,2]) == F(1,48))
    check('three independent traces and a deleted dimension divisor are rejected by distinct exact moments',
          F(1,16) != 0 and F(1,16) != F(1,8))
    check('one-trace semicircle second and fourth moments reject uniform scalar sampling',
          joint.moment([0,2,0]) == F(1,4) and joint.moment([0,4,0]) == F(1,8) and F(1,4) != F(1,3))
    arrays = {x['V_only_coefficient']:x for x in evidence['coefficient_arrays']}
    check('all numerator quadratic coefficients retain both V-only weights',
          [arrays[d]['numerator'][2] for d in (2,1,0)] == ['5/648','1/324','1/648'])
    check('full correlated cubic coefficients independently support non-even coupling dependence',
          arrays[2]['partition'][3] == '3/8' and arrays[2]['numerator'][3] == '1/54')
    check('only the action with both V-only weights deleted has the separate evenness diagnostic',
          all(arrays[0][name][degree] == '0' for name in ('numerator','partition') for degree in (1,3,5,7))
          and arrays[1]['numerator'][3] == '1/108')
    check('zero-action two-link mean and frozen-V mean are different exact integrals',
          arrays[2]['numerator'][0] == '0' and evidence['frozen_V_zero_kappa_mean'] == '1/27')
    # Low-order hypothesis audit uses full character moments, not hardcoded output coefficients.
    A = {2*i:F(math.comb(3,i)*4**i*(-1)**(3-i)) for i in range(4)}
    op = joint.polynomial()
    ex = lambda extra: sum((weight*joint.moment([i+extra[0],j+extra[1],k+extra[2]])
                            for (i,j,k),weight in op.items()), F(0))
    check('quadratic diagnostic retains exact A and mixed-square moment derivations',
          sum((c*joint.moment([p,0,0]) for p,c in A.items()), F(0)) == 1
          and ex([0,0,2]) == ex([0,2,0]) == F(1,324)
          and ex([2,0,0]) == ex([1,1,0]) == ex([1,0,1]) == ex([0,1,1]) == 0)
    refinements = evidence['refinements']
    check('complete fixed0,2,4,6,8 ladder retains all four insufficient widths',
          [c['degree'] for c in refinements] == [0,2,4,6,8]
          and [c['status'] for c in refinements] == ['insufficient-width']*4+['target-met'])
    check('positive-but-insufficient levels4and6 remain distinct from unresolved signs at0and2',
          [c['sign_status'] for c in refinements] == ['unresolved','unresolved','positive','positive','positive'])
    cases = {f['id']:f['certificate'] for f in evidence['fixtures']}
    check('all nine signed zero and omission fixtures are retained',len(cases) == 9)
    for c in refinements+list(cases.values()):
        joint.verify(c)
        low,high = map(F,(c['expectation_interval']['lower'],c['expectation_interval']['upper']))
        if low > high or F(c['partition_interval']['lower']) < 1:
            raise RuntimeError('normalization is not safely positive')
        if F(c['tail']) < 0:
            raise RuntimeError('negative tail')
    check('every complete numerator and Jensen-bounded denominator passes signed interval division',True)
    check('all nine final expectations meet the exact requested interval width',
          all(F(c['expectation_interval']['width']) <= joint.TARGET for c in cases.values()))
    check('all zero-action fixtures collapse to exact zero with no remainder',
          all(cases['d'+str(d)+'_zero']['expectation_interval'] == {'lower':'0','upper':'0','width':'0'}
              and cases['d'+str(d)+'_zero']['tail'] == '0' for d in (2,1,0)))
    check('full signed couplings have rigorously disjoint expectation intervals',
          F(cases['d2_negative']['expectation_interval']['upper']) < F(cases['d2_positive']['expectation_interval']['lower']))
    check('deleting one or both V-only weights gives disjoint normalized results',
          F(cases['d0_positive']['expectation_interval']['upper']) < F(cases['d1_positive']['expectation_interval']['lower'])
          and F(cases['d1_positive']['expectation_interval']['upper']) < F(cases['d2_positive']['expectation_interval']['lower']))
    check('the valid d0 sign exception preserves the whole interval exactly',
          cases['d0_positive']['expectation_interval'] == cases['d0_negative']['expectation_interval'])
    directions = {'-1':['-1','0','0','0'],'0':['0','1','0','0'],'3/5':['3/5','4/5','0','0'],'1':['1','0','0','0']}
    for row in evidence['central_Gram_family']:
        V = joint.quaternion(directions[row['y']])
        e = (F(1),F(0),F(0),F(0))
        k = F(row['kappa'])
        b = tuple(k*(3*e[i]+V[i]) for i in range(4))
        vectors = [b,e,e,e,V]
        expected = [[str(sum((x*y for x,y in zip(p,q)),F(0))) for q in vectors] for p in vectors]
        if row['gram'] != expected or F(row['direction_span_minor']) < 0:
            raise RuntimeError('complete conditional Gram connection failed')
    check('actual G(y) matches all five direction/action vectors including rank-deficient endpoints',
          [row['rank'] for row in evidence['central_Gram_family']] == [1,2,2,1])
    check('conditional partition cannot be silently discarded from the outer measure',
          F(joint.gram_family('1')['gram'][0][0]) != F(joint.gram_family('-1')['gram'][0][0]))
    check('signed interval division retains all four endpoint corners',
          joint.divide(joint.interval(F(-2),F(1)),joint.interval(F(1),F(3))) == joint.interval(F(-2),F(1)))
    bad = copy.deepcopy(evidence['graph']);bad['faces'].pop()
    reject('wrong face union from a deleted actual face',lambda:joint.validate_graph(bad))
    bad = copy.deepcopy(evidence['graph']);bad['faces'][0]['word'][0]['sign'] *= -1
    reject('altered actual signed face word',lambda:joint.validate_graph(bad))
    for name,mutate in [
        ('wrong signed kappa',lambda x:x.update(kappa='-1/64')),
        ('forged passing omission action label',lambda x:x.update(full_six_face_action=False)),
        ('omitted numerator tail',lambda x:x.update(numerator_interval=joint.interval(F(x['numerator_partial']),F(x['numerator_partial'])))),
        ('forged denominator normalization',lambda x:x.update(partition_interval=joint.interval(F(1),F(1)))),
        ('forged expectation enclosure',lambda x:x.update(expectation_interval=joint.interval(F(0),F(0))))]:
        bad = copy.deepcopy(cases['d2_positive']);mutate(bad)
        reject(name,lambda bad=bad:joint.verify(bad))
    for field in ('fixtures','joint_moments','refinements'):
        bad = copy.deepcopy(evidence);bad[field].pop()
        reject('missing complete '+field+' entry',lambda bad=bad:joint.verify_collection(bad))
    joint.moment([0,0,0])
    reject('Boolean zero exponent after warmed cache',lambda:joint.moment([False,0,0]))
    reject('negative exponent',lambda:joint.moment([-1,1,0]))
    reject('moment outside total-degree budget',lambda:joint.moment([8,8,1]))
    reject('wrong exponent dimension',lambda:joint.moment([0,0]))
    reject('Boolean multiplicity index',lambda:joint.multiplicity(1,True))
    reject('Boolean V-only coefficient',lambda:joint.certify('1/64',False))
    reject('nonpositive requested precision',lambda:joint.certify('1/64',target='0'))
    reject('invalid ladder degree',lambda:joint.certify('1/64',degree=7))
    reject('invalid tail geometry',lambda:joint.certify('1',degree=0))
    reject('forged signed interval with Boolean lower endpoint',lambda:joint.divide({'lower':False,'upper':'1','width':'1'},joint.interval(F(1),F(2))))
    reject('retained public-helper Boolean endpoints and omitted width',lambda:joint.divide({'lower':True,'upper':True},{'lower':True,'upper':True}))
    reject('nonpositive denominator interval',lambda:joint.divide(joint.interval(F(-1),F(1)),joint.interval(F(0),F(1))))
    reject('unphysical surrounding scalar coordinate',lambda:joint.gram_family('2'))
    old = joint.WEIGHTS
    try:
        joint.WEIGHTS = (2,)
        reject('runtime omission of required weight cases',lambda:joint.collection())
    finally:
        joint.WEIGHTS = old
    returned = joint.polynomial();returned[(0,0,0)] = F(999)
    check('returned observable polynomial cannot poison subsequent exact coefficients',joint.coefficients(2)[0][2] == F(5,648))
    (out/'completecollection.json').write_text(json.dumps(evidence,indent=2)+'\n')
    (out/'actualgraph.json').write_text(json.dumps(evidence['graph'],indent=2)+'\n')
    refinement_rows = [{'degree':c['degree'],'lower':c['expectation_interval']['lower'],'upper':c['expectation_interval']['upper'],
                        'width':c['expectation_interval']['width'],'status':c['status'],'sign_status':c['sign_status']} for c in refinements]
    weight_rows = [{'fixture':name,'V_only_coefficient':c['V_only_coefficient'],'kappa':c['kappa'],'degree':c['degree'],
                    'lower':c['expectation_interval']['lower'],'upper':c['expectation_interval']['upper'],'width':c['expectation_interval']['width'],
                    'status':c['status']} for name,c in cases.items()]
    for name,rows in [('refinement.csv',refinement_rows),('weights.csv',weight_rows)]:
        with (out/name).open('w',newline='') as stream:
            writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    result={'schema':'ym18-c2-results-v1','status':'passed','checks_count':len(checks),'checks':checks,
            'source_sha256':joint.SOURCE_SHA,'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'evidence_sha256':hashlib.sha256((out/'completecollection.json').read_bytes()).hexdigest(),
            'fixture_count':9,'moment_count':969,'primary':cases['d2_positive']['expectation_interval'],
            'scope':'author exact arithmetic and implementation checks; independent acceptance is separate'}
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir()) if p.is_file() and p.name!='manifest.json'}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'status':'passed','checks_count':len(checks),'evidence_sha256':result['evidence_sha256']}))


if __name__ == '__main__':
    main()
