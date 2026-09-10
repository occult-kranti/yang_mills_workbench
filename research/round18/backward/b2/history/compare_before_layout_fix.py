"""Independent complete B2 interval replay plus isolated admission regression."""
from pathlib import Path
from fractions import Fraction as F
import argparse,copy,csv,hashlib,json,subprocess,sys
from bounds import root_enclosure,int_floor_root,interval_check
from check import RADII

PINS={'b1-gate.json':'344f3e5442e63a59f51389dc7f3c8a63d3e3c6cc2ff0aac9f4672b18a8020086',
      'b1-report.md':'b271d4f1d48da3fa01dd722b66338b31316fdfd965a3d4dbbecfb87596ad2796','graph.json':'9e630191189fb3f69145e5cdbc91eceac138f95d44d7bed825b87b572b322e62'}
PREMISES={'physical_space':'full untruncated L2(SU2^20) with Gauss at all twelve vertices and no charges',
 'P_basis':'bare vacuum and all eleven orthonormal fundamental face characters','Q_electric_lower_over_alpha':'9/2','P_face_electric_over_alpha':'3',
 'P_face_magnetic_quadratic_form':'0','cross_norm_squared_over_alpha_squared_r_squared_upper':'21/4','vacuum_trial_energy':'0',
 'codimension_one_space':'psi perpendicular to the bare vacuum, not necessarily the interacting ground','cross_is_full_QVP':True,'complement_is_full_Q':True,'graph_sha256':PINS['graph.json']}
TARGET=F(1,10**12)


def strict(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(strict(a[k],b[k]) for k in a)
    if type(a) in (list,tuple):return len(a)==len(b) and all(strict(x,y) for x,y in zip(a,b))
    return a==b


def interval(lo,hi):return {'lower':str(lo),'upper':str(hi),'width':str(hi-lo)}
def scaled(i,a):return interval(a*F(i['lower']),a*F(i['upper']))


def dyadic(q,bits):
    """Uniquely identify the grid enclosure by integer bisection; check Newton overlap."""
    q=F(q);pn,pd=int_floor_root(q.numerator),int_floor_root(q.denominator)
    if pn*pn==q.numerator and pd*pd==q.denominator:lo=hi=F(pn,pd)
    else:
        d=1<<bits;k=int_floor_root(q.numerator*d*d//q.denominator);lo,hi=F(k,d),F(k+1,d)
    interval_check(q,(lo,hi));nl,nh=root_enclosure(q,min(bits+8,128))
    if max(lo,nl)>min(hi,nh):raise ValueError('independent Newton and dyadic intervals are disjoint')
    return lo,hi


def constants(bits):
    a,b=dyadic(70,bits);c,d=dyadic(3,bits)
    return {'sqrt70':interval(a,b),'sqrt3':interval(c,d),'R_star':interval((27-3*b)/16,(27-3*a)/16),
      'star_E0_upper_formula':interval((24-15*d)/16,(24-15*c)/16),'D_star':interval((3+15*c-3*b)/16,(3+15*d-3*a)/16),
      'analytic_positivity':{'R_star_squared_test':'81>70','endpoint_matrix_determinant':'99/256','star_energy_negative_squared_test':'675>576'}}


def scalar(r,bits):
    r=F(r);c=F(9,2)-11*r;b2=F(21,4)*r*r;q=(3-c)**2+4*b2;lo,hi=dyadic(q,bits);L,H=(3+c-hi)/2,(3+c-lo)/2
    det=(3-L)*(c-L)-b2
    if min(3-L,c-L,det)<0:raise ValueError('independent congruence rejects scalar shift')
    return {'r':str(r),'c':str(c),'b_squared':str(b2),'discriminant':str(q),'sqrt_discriminant':interval(lo,hi),'R':interval(L,H),
      'lower_shift_determinant':str(det),'box_member':r<=F(3,8),'bound_status':'positive' if L>0 else 'zero-insufficient' if L==0 else 'negative-insufficient'}


def fixture_inputs():
    return [('allzero','1',['0']*11,48,None,True),('endpoint_allplus','1',['3/8']*11,48,None,True),
      ('endpoint_allminus','1',['-3/8']*11,48,None,True),('endpoint_alternating','1',['3/8' if i%2==0 else '-3/8' for i in range(11)],48,None,True),
      ('sparse_interior','1',['1/8']+['0']*10,48,None,True),('mixed_signed_interior','1',['1/8','-1/16','0','3/32','0','-1/32']+['0']*5,48,None,True),
      ('scaled_double','2',['3/4']*11,48,'1',True),('scaled_half','1/2',['3/16']*11,48,'1/4',True),('coarse_endpoint','1',['3/8']*11,0,None,True),
      ('outside_two_fifths','1',['2/5']*11,48,None,False),('outside_one_half','1',['1/2']*11,48,None,False)]


def expected_certificate(a,ls,bits,amin,claim,source_sha):
    a=F(a);ls=list(map(F,ls));amin=None if amin is None else F(amin);r=max(map(abs,ls))/a;member=r<=F(3,8);endpoint=all(abs(x)==3*a/8 for x in ls)
    s=scalar(r,bits);k=constants(bits);qsum=sum((x*x for x in ls),F(0));lo,hi=dyadic(9*a*a+qsum,bits)
    e0=interval((3*a-hi)/2,(3*a-lo)/2);e1=scaled(s['R'],a);gap=interval(F(e1['lower'])-F(e0['upper']),F(e1['upper'])-F(e0['lower']))
    whole=scaled(k['R_star'],a) if member else None;common=scaled(k['R_star'],amin) if member and amin is not None else None
    if common is not None and F(common['lower'])<0:common=interval(F(0),F(common['upper']))
    return {'schema':'ym18-b2-certificate-v1','source_sha256':source_sha,'premise_sha256':PINS,'proof_premises':PREMISES,
      'alpha':str(a),'alpha_min':None if amin is None else str(amin),'couplings':list(map(str,ls)),'precision_bits':bits,'requested_dimensionless_width':str(TARGET),'claim_box':claim,
      'maximum_absolute_ratio':str(r),'sum_absolute_couplings':str(sum(map(abs,ls),F(0))),'sum_coupling_squares':str(qsum),'box_member':member,'all_endpoint_magnitudes':endpoint,
      'scalar_comparison':s,'constants':k,'full_E1_lower_formula_interval':e1,'star_E0_upper_formula_interval':e0,'instance_gap_lower_formula_interval':gap,
      'whole_box_gap_lower_formula_interval':whole,'common_scale_gap_lower_formula_interval':common,'endpoint_gap_lower_formula_interval':scaled(k['D_star'],a) if endpoint else None,
      'analytic_box_status':'positive-proved' if member else 'outside-selected-box',
      'whole_box_enclosure_status':'not-applicable' if not member else 'positive-target-met' if F(k['R_star']['lower'])>0 and F(k['R_star']['width'])<=TARGET else 'insufficient-precision',
      'endpoint_enclosure_status':'not-applicable' if not endpoint else 'positive-target-met' if F(k['D_star']['lower'])>0 and F(k['D_star']['width'])<=TARGET else 'insufficient-precision',
      'interval_semantics':'Intervals enclose analytic lower-bound formulas or trial-energy formulas; no upper endpoint bounds the physical gap from above.',
      'scope':'fixed actual two-cube physical operator; no homogeneous volume-uniform or continuum conclusion'}


def expected_collection(source_sha):
    return {'schema':'ym18-b2-collection-v1','source_sha256':source_sha,'premise_sha256':PINS,'physical_contract':PREMISES,'precision_bits':48,
      'dimensionless_width_target':str(TARGET),'frozen_box':{'coefficient_count':11,'maximum_absolute_ratio':'3/8','coverage':'analytic whole signed box, not sampled coverage'},
      'constants':constants(48),'fixtures':[{'id':n,'certificate':expected_certificate(a,ls,bits,amin,claim,source_sha)} for n,a,ls,bits,amin,claim in fixture_inputs()],
      'samples':[scalar(r,48) for r in RADII],
      'controls':{'deleted_cross_scalar':{'vector':'(1,sqrt(21))','norm_squared':'22','true_scalar_form':'3','true_scalar_Rayleigh':'3/22','false_diagonal_lower':'3/8',
        'scope':'counterexample to a scalar inference, not a computed physical excited state'},
       'missing_codimension_one':{'state':'bare vacuum','actual_P_quadratic_form':'0','false_face_only_lower_over_alpha':'3'},
       'missing_P_face':{'actual_omitted_face_energy_over_alpha':'3','false_complement_lower_over_alpha':'9/2'},
       'Ritz_gap_substitution':{'full_diagonal':['0','1/8','3'],'trial_indices':[0,2],'full_gap':'1/8','Ritz_gap':'3','scope':'separate generic finite-matrix inference counterexample'},
       'coarse_radical_failure':{'bits':0,'R_star':constants(0)['R_star'],'D_star':constants(0)['D_star'],'meaning':'actual requested precision failure, not a theorem counterexample'},
       'matching':{'alpha':'g^2/(2a)','lambda':'2/(g^2 a)','ratio':'4/g^4','box_condition':'g^4>=32/3','weak_bare_limit_admitted':False,
                   'meaning':'applicability obstruction for this bound, not absence of a continuum mass gap'}}}


def verify_collection(value,source_sha):
    if not strict(value,expected_collection(source_sha)):raise ValueError('complete independent B2 collection mismatch')
    return True


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--producer',type=Path,required=True);ap.add_argument('--evidence',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ns=ap.parse_args()
    source=ns.producer.resolve();evidence=ns.evidence.resolve();out=ns.output.resolve();own=Path(__file__).resolve().parent
    if out.is_relative_to(own):raise ValueError('output outside source required')
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();source_sha=sha(source/'gap.py');v=json.loads((evidence/'collection.json').read_text());e=expected_collection(source_sha);checks=[]
    def gate(name,ok):
        if type(ok) is not bool or not ok:raise ValueError(name)
        checks.append({'name':name,'passed':True})
    m=json.loads((source/'source-manifest.json').read_text());actual_sources={str(p.relative_to(source)):sha(p) for p in source.rglob('*') if p.is_file() and p.name!='source-manifest.json' and '__pycache__' not in p.parts}
    gate('complete frozen source history and premise manifest agrees',strict(m['files'],actual_sources) and all(sha(source/'premises'/n)==d for n,d in PINS.items()))
    gate('eleven ordered actual coefficient fixtures are complete',strict([f['id'] for f in v['fixtures']],[f['id'] for f in e['fixtures']]))
    for x,y in zip(v['fixtures'],e['fixtures']):gate('complete radical transport and scope: '+y['id'],strict(x,y))
    gate('all eight scalar samples and congruence diagnostics independently agree',strict(v['samples'],e['samples']))
    gate('whole-box and endpoint constants agree with exact brackets and Newton overlap',strict(v['constants'],e['constants']))
    gate('full collection proof antecedents and interval semantics replay',strict(v,e))
    csv_rows=[]
    for r,s in zip(RADII,e['samples']):
        c=expected_certificate('1',[r]*11,48,None,False,source_sha);i=c['instance_gap_lower_formula_interval']
        csv_rows.append({'r':r,'R_lower':s['R']['lower'],'R_upper':s['R']['upper'],'R_width':s['R']['width'],
          'instance_gap_lower':i['lower'],'instance_gap_upper':i['upper'],'box_member':str(s['box_member']),'status':s['bound_status']})
    with (evidence/'coupling.csv').open(newline='') as f:csv_value=list(csv.DictReader(f))
    gate('plotted coupling CSV agrees with exact full-form and trial formulas',strict(csv_value,csv_rows))
    mutations=[]
    def mutate(name,fn):
        b=copy.deepcopy(v);fn(b);mutations.append((name,b))
    mutate('missing actual tail premise rejected',lambda b:b['physical_contract'].pop('complement_is_full_Q'))
    mutate('missing scalar cross premise rejected',lambda b:b['fixtures'][0]['certificate']['proof_premises'].pop('cross_is_full_QVP'))
    mutate('outside coefficient relabelled inside the box rejected',lambda b:b['fixtures'][-1]['certificate'].update(box_member=True))
    mutate('coarse precision falsely accepted rejected',lambda b:b['fixtures'][8]['certificate'].update(endpoint_enclosure_status='positive-target-met'))
    mutate('upper gap claim silently introduced rejected',lambda b:b['fixtures'][1]['certificate'].update(interval_semantics='physical gap upper and lower bounds'))
    mutate('wrong outward radical bound rejected',lambda b:b['constants']['sqrt70'].update(upper='8'))
    mutate('Boolean precision alias rejected',lambda b:b['fixtures'][8]['certificate'].update(precision_bits=False))
    mutate('source digest replacement rejected',lambda b:b.update(source_sha256='0'*64))
    mutate('external passed record cannot replace evidence',lambda b:b.update(status='passed'))
    for name,b in mutations:gate(name,not strict(b,e))
    # Only this isolated boundary test imports the author module; arithmetic above is independent.
    program="""import sys,json,copy
from fractions import Fraction
sys.path.insert(0,sys.argv[1]);import gap
results={}
for name,change in [('false_full_complement',lambda:gap.REQUIRED_PREMISES.update(complement_is_full_Q=False)),('changed_precision_target',lambda:setattr(gap,'TARGET',Fraction(1)))]:
 old=copy.deepcopy(gap.REQUIRED_PREMISES);target=gap.TARGET
 try:
  change()
  try:gap.certify('1',['0']*11,proof_premises=dict(gap.REQUIRED_PREMISES));results[name]=False
  except ValueError:results[name]=True
 finally:gap.REQUIRED_PREMISES=old;gap.TARGET=target
print(json.dumps(results))
"""
    command=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])+['-c',program,str(source)]
    child=subprocess.run(command,text=True,capture_output=True,check=True);admission=json.loads(child.stdout)
    for name,ok in admission.items():gate('repaired actual producer admission rejects '+name,ok)
    hashes={**{'producer/'+n:d for n,d in actual_sources.items()},'producer/source-manifest.json':sha(source/'source-manifest.json'),
      **{'evidence/'+n:sha(evidence/n) for n in ('collection.json','coupling.csv')},**{'independent/'+n:sha(own/n) for n in ('bounds.py','check.py','compare.py')}}
    result={'schema':'ym18-independent-b2-comparison-v1','status':'passed','checks_count':len(checks),'checks':checks,'input_sha256':hashes,
      'oracle':'Exact dyadic cells identified with integer bisection and checked against independent rational Newton enclosures; scalar PSD shifts independently checked. Producer import only for isolated repaired admission controls.',
      'scope':'Full signed finite-graph coefficient-box theorem; all intervals enclose bound formulas and do not upper-bound the physical gap.'}
    out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'passed','checks_count':len(checks)}))


if __name__=='__main__':main()
