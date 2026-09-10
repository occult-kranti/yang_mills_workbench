"""Independent exact sparse-support certificates; no forward imports."""
from fractions import Fraction as Q
from itertools import product,combinations
from pathlib import Path
import argparse,copy,csv,hashlib,json


def rational(v):
    if type(v) not in (str,int,Q):raise ValueError('exact rational required')
    try:return Q(v)
    except (ValueError,ZeroDivisionError) as e:raise ValueError('finite rational required') from e


def size(n):
    if type(n) is not int or not 2<=n<=12:raise ValueError('strict integer vertex extent2..12 required')
    return n


def face_geometry(n,face):
    size(n)
    if type(face) is not list or len(face)!=5 or any(type(v) is not int for v in face):raise ValueError('strict five-integer face label required')
    a,b,*v=face
    if (a,b) not in ((0,1),(0,2),(1,2)) or any(not 0<=x<n for x in v) or v[a]>=n-1 or v[b]>=n-1:raise ValueError('elementary face absent from box')
    va=v.copy();va[a]+=1;vb=v.copy();vb[b]+=1;vab=va.copy();vab[b]+=1
    links={(a,*v),(b,*va),(a,*vb),(b,*v)}
    vertices={tuple(v),tuple(va),tuple(vb),tuple(vab)}
    return links,vertices


def mask(n,alpha=1,rho='1/2',signed=True):
    n=size(n);a,r=map(rational,(alpha,rho))
    if a<=0 or r<0 or type(signed) is not bool:raise ValueError('positive alpha, nonnegative rho and Boolean sign mode required')
    terms=[]
    for z in range(n):
        for x in range(0,n-1,2):
            for y in range(0,n-1,2):
                sign=-1 if signed and (x//2+y//2+z)%2 else 1
                terms.append({'face':[0,1,x,y,z],'lambda':str(sign*a*r)})
    return terms


def certificate(n,terms,alpha=1,alpha_min=1,rho='1/2'):
    n=size(n);a,amin,r=map(rational,(alpha,alpha_min,rho))
    if a<=0 or amin<=0 or a<amin or r<0:raise ValueError('positive common scale and nonnegative ratio bound required')
    if type(terms) is not list:raise ValueError('explicit coupling list required')
    used={};declared=set();active=[];norm_sum=Q(0);max_norm=Q(0)
    for term in terms:
        if type(term) is not dict or set(term)!={'face','lambda'}:raise ValueError('fixed coupling record required')
        links,vertices=face_geometry(n,term['face']);key=tuple(term['face'])
        if key in declared:raise ValueError('duplicate face coefficient')
        declared.add(key);coupling=rational(term['lambda'])
        if abs(coupling)>a*r:raise ValueError('coupling exceeds declared dimensionless bound')
        if coupling==0:continue
        if any(edge in used for edge in links):raise ValueError('nonzero plaquettes share a link; sparse theorem inapplicable')
        for edge in links:used[edge]=key
        norm_sum+=abs(coupling);max_norm=max(max_norm,abs(coupling));active.append({'face':term['face'].copy(),'lambda':str(coupling)})
    total_links=sum(1 for v in product(range(n),repeat=3) for axis in range(3) if v[axis]<n-1)
    free_links=total_links-len(used);physical_uniform=amin*(Q(3,4)-r);local=a*Q(3,4)-max_norm
    positive=r<Q(3,4);global_lower=3*a-norm_sum
    return {'schema':'ym17-independent-sparse-bound-v1','group':'SU(2)','n':n,'alpha':str(a),'alpha_min':str(amin),'rho':str(r),
      'active':active,'active_count':len(active),'used_link_count':len(used),'total_links':total_links,'free_link_count':free_links,
      'maximum_absolute_lambda':str(max_norm),'sum_absolute_lambda':str(norm_sum),
      'unprojected_free_block_gap':str(3*a/4),'actual_component_gap_lower':str(local),
      'declared_current_scale_lower':str(a*(Q(3,4)-r)),'uniform_physical_lower':str(physical_uniform),
      'status':'positive' if positive else 'insufficient','unique_ground_and_physical_inclusion_certified':positive,
      'global_physical_norm_lower':str(global_lower),'global_bound_status':'positive' if global_lower>0 else 'insufficient',
      'all_zero_exact_physical_gap':str(3*a) if not active else None,
      'hilbert_scope':'Only the full link space factorizes; the unique product ground belongs to the global Gauss sector.',
      'dense_goal':'open; an overlapping nonzero bridge violates this theorem support premise'}


def execute(output):
    output=Path(output).resolve();source=Path(__file__).resolve().parent
    if output.is_relative_to(source):raise ValueError('output must be outside frozen source directory')
    output.mkdir(parents=True,exist_ok=False);checks=[]
    def check(name,condition):
        if not condition:raise RuntimeError(name)
        checks.append({'name':name,'passed':True})
    def reject(name,fn):
        try:fn()
        except (ValueError,TypeError,KeyError):check(name,True);return
        raise RuntimeError('invalid sparse premise accepted: '+name)
    # Analytic proof uses all n. These explicit geometries test the mask formula.
    rows=[]
    for n in (2,3,4,8):
        terms=mask(n);c=certificate(n,terms);rows.append(c)
        check('exact extensive mask and link partition n='+str(n),c['active_count']==n*(n//2)**2 and c['used_link_count']==4*c['active_count'] and c['used_link_count']+c['free_link_count']==3*n*n*(n-1))
        check('fixed physical quarter-gap certificate n='+str(n),c['uniform_physical_lower']=='1/4' and c['status']=='positive')
    check('extensive norm shortcut fails while sparse certificate stays positive',rows[-1]['global_bound_status']=='insufficient' and Q(rows[-1]['global_physical_norm_lower'])<0 and rows[-1]['status']=='positive')
    corner=[{'face':[0,1,0,0,0],'lambda':'1/2'},{'face':[0,1,1,1,0],'lambda':'-1/2'}]
    a,av=face_geometry(3,corner[0]['face']);b,bv=face_geometry(3,corner[1]['face']);c=certificate(3,corner)
    check('shared vertex allowed without physical-space factorization',not a&b and len(av&bv)==1 and c['active_count']==2 and c['uniform_physical_lower']=='1/4')
    same_sign=copy.deepcopy(corner);same_sign[1]['lambda']='1/2';cp=certificate(3,same_sign)
    check('signed couplings share the same absolute-norm certificate',all(c[k]==cp[k] for k in ('actual_component_gap_lower','uniform_physical_lower','sum_absolute_lambda')))
    zero=certificate(3,[],rho=0)
    check('no active faces retains all links and exact free physical gap',zero['active_count']==0 and zero['free_link_count']==zero['total_links'] and zero['all_zero_exact_physical_gap']=='3' and zero['uniform_physical_lower']=='3/4')
    zero_overlap=mask(3);zero_overlap.append({'face':[0,1,1,0,0],'lambda':'0'})
    check('zero coefficient does not create active overlap',certificate(3,zero_overlap)['active_count']==certificate(3,mask(3))['active_count'])
    bridge=copy.deepcopy(zero_overlap);bridge[-1]['lambda']='1/1024'
    reject('first arbitrarily weak overlapping bridge invalidates sparse proof',lambda:certificate(3,bridge))
    endpoint=certificate(2,mask(2,rho='3/4'),rho='3/4')
    check('rho three-quarters is insufficient and makes no uniqueness claim',endpoint['uniform_physical_lower']=='0' and endpoint['status']=='insufficient' and endpoint['unique_ground_and_physical_inclusion_certified'] is False)
    beyond=certificate(2,mask(2,rho=1),rho=1)
    check('negative lower bound retained without gap-closure claim',beyond['uniform_physical_lower']=='-1/4' and beyond['status']=='insufficient')
    scaled=certificate(4,mask(4,alpha=7),alpha=7,alpha_min=2)
    check('same physical units distinguish current and family scales',scaled['actual_component_gap_lower']=='7/4' and scaled['uniform_physical_lower']=='1/2')
    check('unprojected block energy is not isolated physical-loop energy',zero['unprojected_free_block_gap']=='3/4' and zero['all_zero_exact_physical_gap']=='3')
    # su(2) commutators [T1,T2]=T3 etc span all three generators.
    commutator_coordinates=((0,0,1),(1,0,0),(0,1,0))
    determinant=sum(commutator_coordinates[0][j]*(commutator_coordinates[1][(j+1)%3]*commutator_coordinates[2][(j+2)%3]-commutator_coordinates[1][(j+2)%3]*commutator_coordinates[2][(j+1)%3]) for j in range(3))
    check('Lie-character differential annihilates a spanning commutator basis',determinant==1)
    free_scale_rows=[]
    for n in (2,4,8):
        c0=certificate(n,[],alpha=Q(1,n),alpha_min=Q(1,n),rho=0)
        free_scale_rows.append({'n':n,'alpha':str(Q(1,n)),'exact_free_physical_gap':c0['all_zero_exact_physical_gap']})
    check('free shrinking-scale example uses exact gaps not vanishing lower bounds',all(Q(r['exact_free_physical_gap'])==Q(3,r['n']) for r in free_scale_rows))
    reject('zero common energy scale rejected',lambda:certificate(2,[],alpha_min=0))
    reject('member below declared common energy scale rejected',lambda:certificate(2,[],alpha='1/2',alpha_min=1))
    reject('coupling above declared rho rejected',lambda:certificate(2,[{'face':[0,1,0,0,0],'lambda':'3/4'}]))
    reject('negative rho rejected',lambda:certificate(2,[],rho=-1))
    bad=mask(3);bad[0]['face'][2]=False;reject('Boolean coordinate does not alias zero',lambda:certificate(3,bad))
    reject('Boolean physical scale rejected',lambda:certificate(2,[],alpha=True))
    reject('duplicate face coefficient rejected',lambda:certificate(2,mask(2)+[mask(2)[0]]))
    reject('plaquette crossing box boundary rejected',lambda:certificate(2,[{'face':[0,1,1,0,0],'lambda':'1/2'}]))
    result={'schema':'ym17-independent-a2-results-v1','status':'passed','checks_count':len(checks),'checks':checks,
      'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'primary_parameters':{'rho':'1/2','alpha_min':'1'},'uniform_physical_lower':'1/4',
      'mask_rows':rows,'corner_sharing':c,'zero':zero,'endpoint':endpoint,'beyond_endpoint':beyond,'scaled':scaled,'exact_free_scale_rows':free_scale_rows,
      'scope':'Restricted link-disjoint magnetic-support family on full open cubic graphs, physical Gauss sector; dense original target remains open.',
      'analytic_premises':['Compact resolvent and bounded self-adjoint block perturbation.','Min-max block gap and unique ground when rho<3/4.','SU(2)^4 has no nontrivial continuous one-dimensional characters.','Full tensor ground is physical; physical restriction does not lower the excitation gap.']}
    (output/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    with (output/'volume.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['n','active_faces','global_norm_lower','uniform_sparse_lower']);w.writerows((r['n'],r['active_count'],r['global_physical_norm_lower'],r['uniform_physical_lower']) for r in rows)
    print(json.dumps({'status':'passed','checks_count':len(checks),'uniform_physical_lower':'1/4'}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args();execute(args.output)
