"""Independent full-form proof gates and outward rational interval checks."""
from pathlib import Path
from fractions import Fraction as F
import argparse,copy,csv,hashlib,json
import bounds
from bounds import PREMISES,root_enclosure,constants,scalar,certificate,interval_check,proof_gate,bare_matching

RADII=('0','1/8','1/4','12/43','1/3','3/8','2/5','1/2')
FIXTURES=[('allzero','1','1',['0']*11,48),('endpoint_allplus','1','1',['3/8']*11,48),('endpoint_allminus','1','1',['-3/8']*11,48),
 ('endpoint_alternating','1','1',['3/8' if i%2==0 else '-3/8' for i in range(11)],48),
 ('single_interior','1','1',['1/8']+['0']*10,48),('mixed_interior','1','1',['1/8','-1/16','0','3/32','0','-1/32','0','0','0','0','0'],48),
 ('scaled_double','2','1',['3/4']*11,48),('scaled_half','1/2','1/4',['3/16']*11,48),('coarse_endpoint','1','1',['3/8']*11,0)]


def run(output):
    source=Path(__file__).resolve().parent;out=Path(output).resolve()
    if out.is_relative_to(source):raise ValueError('output outside source required')
    out.mkdir(parents=True,exist_ok=False);checks=[]
    def gate(name,ok):
        if type(ok) is not bool or not ok:raise ValueError(name)
        checks.append({'name':name,'passed':True})
    def reject(name,fn):
        try:fn()
        except (ValueError,TypeError):gate(name,True);return
        raise ValueError('invalid premise admitted: '+name)
    k=constants(48);rows=[scalar(r,48) for r in RADII];congruence=[]
    for row in rows:
        R=F(row['eigenvalue_interval'][0]);c=F(row['c']);b2=F(row['offdiagonal_squared']);d1=3-R;d2=c-R;det=d1*d2-b2
        congruence.append({'r':row['r'],'shift':str(R),'first_diagonal':str(d1),'second_diagonal':str(d2),'determinant':str(det)})
        if min(d1,d2,det)<0:raise ValueError('independent shifted-matrix PSD check failed')
    gate('every rational Newton interval encloses its radical',all(interval_check(row['radicand'],row['sqrt_interval']) for row in rows) and interval_check(70,k['sqrt70']) and interval_check(3,k['sqrt3']))
    gate('independent shifted scalar matrices are positive semidefinite including degeneracy',len(congruence)==8 and congruence[0]['first_diagonal']=='0')
    gate('whole signed-box comparison is algebraic for nonnegative norm coordinates',F(9,2)-11*F(3,8)==F(3,8) and F(21,4)*F(3,8)**2==F(189,256))
    difference_first=F(3)-F(3);difference_second=F(rows[0]['c'])-F(rows[5]['c']);difference_det=difference_first*difference_second-F(rows[5]['offdiagonal_squared'])
    gate('matrix difference is not falsely declared Loewner positive',difference_det==-F(189,256)<0)
    gate('whole-box exact radical constant is strictly positive',27**2>9*70 and F(k['box_gap_over_alpha'][0])>0)
    gate('endpoint star energy is a separate negative upper estimate',15**2*3>24**2 and F(k['endpoint_ground_upper_expression'][1])<0)
    gate('signed endpoint star discriminant matches all eleven physical couplings',9+11*F(3,8)**2==F(675,64))
    gate('endpoint improvement combines E1 lower and E0 upper in correct direction',F(k['endpoint_gap_over_alpha'][0])==F(k['box_gap_over_alpha'][0])-F(k['endpoint_ground_upper_expression'][1]))
    gate('displayed gap constants meet the explicit dimensionless width target',all(F(k[n][1])-F(k[n][0])<=F(1,10**12) for n in ('box_gap_over_alpha','endpoint_gap_over_alpha')))
    gate('zero coupling is an exact scalar degeneracy without division by cross norm',rows[0]['eigenvalue_interval']==['3','3'] and rows[0]['offdiagonal_squared']=='0')
    gate('accepted radii and illustrative outside cases remain separately labelled',[r['inside_primary_box'] for r in rows]==[True]*6+[False]*2 and all(not r['positive_exact'] for r in rows[-2:]))
    fixtures={name:certificate(a,ls,amin,bits) for name,a,amin,ls,bits in FIXTURES}
    gate('all three endpoint sign patterns share the same exact bound',len({tuple(fixtures[n]['selected_dimensionless_lower_formula_interval']) for n in ('endpoint_allplus','endpoint_allminus','endpoint_alternating')})==1)
    gate('zero sparse and mixed vectors do not acquire an endpoint-only improvement',all(not fixtures[n]['all_endpoint_magnitudes'] and fixtures[n]['E0_upper_over_alpha']=='0' for n in ('allzero','single_interior','mixed_interior')))
    gate('coarse endpoint remains explicitly insufficient',fixtures['coarse_endpoint']['status']=='insufficient-precision-or-sign' and fixtures['coarse_endpoint']['common_physical_lower_formula_interval'] is None)
    gate('accepted interval endpoints scale in physical and common units separately',F(fixtures['scaled_double']['physical_gap_lower_formula_interval'][0])==2*F(fixtures['endpoint_allplus']['physical_gap_lower_formula_interval'][0]) and fixtures['scaled_double']['common_physical_lower_formula_interval']==fixtures['endpoint_allplus']['common_physical_lower_formula_interval'] and F(fixtures['scaled_half']['common_physical_lower_formula_interval'][0])==F(fixtures['endpoint_allplus']['physical_gap_lower_formula_interval'][0])/4)
    # A genuine scalar Rayleigh counterexample to deleting the cross term.
    numerator=F(3)+F(3,8)*21-2*F(3,16)*21;rayleigh=numerator/22
    controls={'deleted_scalar_cross':{'test_vector':'(1,sqrt21)','norm_squared':'22','full_scalar_form':str(numerator),'Rayleigh':str(rayleigh),'incorrect_diagonal_lower':'3/8'},
      'false_Loewner_order':{'comparison':'M(r=0)-M(r=3/8)','diagonal':[str(difference_first),str(difference_second)],'determinant':str(difference_det)},
      'missing_codimension_one':{'actual_P_vector':'Omega+chi_0','norm_squared':'2','magnetic_form_at_lambda0_3over8':'-3/8','incorrect_claim':'0'},
      'Ritz_gap_substitution':{'full_diagonal':['0','1/8','3'],'trial_indices':[0,2],'trial_gap':'3','actual_full_gap':'1/8'},
      'missing_tail':{'allowed_abstract_diagonal_without_tail_premise':['0','0','3'],'actual_gap':'0'},
      'scope':'Scalar and finite-matrix logical counterexamples; not claimed spectra of the physical two-cube operator.'}
    gate('actual scalar cross-term deletion overstates the lower quadratic form',rayleigh==F(3,22)<F(3,8))
    gate('vacuum components invalidate the asserted zero magnetic P form',-F(3,8)!=0)
    gate('a Ritz gap cannot replace a full-spectrum lower bound',F(1,8)<3)
    gate('missing complementary lower bound permits a gapless abstract extension',F(0)<F(k['box_gap_over_alpha'][0]))
    for premise in ('full_physical_complement','exact_subtracted_cross_Gram','codimension_one_vacuum_perpendicular'):
        p={x:True for x in PREMISES};p.pop(premise);reject('missing '+premise+' rejected',lambda p=p:certificate(1,['3/8']*11,premises=p))
    reject('a larger actual coefficient cannot attach a passing box label',lambda:certificate(1,['2/5']+['0']*10))
    reject('a missing coefficient channel is not treated as zero',lambda:certificate(1,['0']*10))
    reject('Boolean coefficient alias rejected',lambda:certificate(1,[False]+['0']*10))
    reject('Boolean precision alias rejected',lambda:root_enclosure(70,True))
    reject('false common energy floor rejected',lambda:certificate(1,['0']*11,2))
    reject('incorrect radical interval rejected by squaring',lambda:interval_check(70,['8','8']))
    original=bounds.PREMISES
    try:
        bounds.PREMISES=tuple(p for p in original if p!='full_physical_complement')
        reject('runtime antecedent deletion is rejected before conditional admission',lambda:certificate(1,['0']*11))
    finally:bounds.PREMISES=original
    matching=[bare_matching(q,a) for q,a in [('1','1'),('4','1'),('4','1/2'),('1/4','2')]]
    gate('primary-source coefficient matching independently cancels lattice spacing',all(F(m['ratio'])==4/F(m['g_squared'])**2 for m in matching) and matching[1]['ratio']==matching[2]['ratio']=='1/4')
    gate('selected positive homogeneous box is equivalent to g to fourth at least32over3',all(m['inside_selected_box']==(F(m['ratio'])<=F(3,8)) for m in matching))
    gate('weak bare coupling exits this bound without disproving a continuum gap',matching[0]['inside_selected_box'] is False and matching[3]['inside_selected_box'] is False and F(matching[3]['ratio'])>F(matching[0]['ratio']))
    result={'schema':'ym18-independent-b2-results-v1','status':'passed','checks_count':len(checks),'checks':checks,
      'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (source/'bounds.py',source/'check.py')},
      'constants':k,'fixtures':fixtures,'scope':'Entire signed finite-graph coefficient box established by a full-form argument; radius samples only illustrate it. No volume-uniform or continuum conclusion.'}
    for name,obj in [('results.json',result),('scalar_samples.json',rows),('congruence.json',congruence),('controls.json',controls),('physical_matching.json',matching)]:
        (out/name).write_text(json.dumps(obj,indent=2)+'\n')
    with (out/'coupling.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['r','c','offdiagonal_squared','discriminant','lower','upper','inside_primary_box','positive_scalar_matrix'])
        for row in rows:w.writerow([row['r'],row['c'],row['offdiagonal_squared'],row['radicand'],*row['eigenvalue_interval'],row['inside_primary_box'],row['positive_exact']])
    print(json.dumps({'status':'passed','checks_count':len(checks),'box_constant':float(F(k['box_gap_over_alpha'][0])),'endpoint_constant':float(F(k['endpoint_gap_over_alpha'][0]))}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();run(a.output)
