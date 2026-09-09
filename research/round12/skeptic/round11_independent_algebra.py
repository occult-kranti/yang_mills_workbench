#!/usr/bin/env python3
"""Independent exact replay of two-plaquette solver; relocatable input path.

Usage: python [-O] audit_solver.py ../solver/two_plaquette.py --label final
Requires numpy/scipy only because the production solver imports them.
Independent inertia uses characteristic polynomials, not production congruence.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse, ast, copy, hashlib, importlib.util, json, sys
from round11_independent_links import matrix_haar_moment, metric, drift, su2, ENDS, WORDS, trace_jet

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module)
    return module
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pa(p,q):
    out=p.copy()
    for k,v in q.items(): out[k]=out.get(k,F(0))+v
    return {k:v for k,v in out.items() if v}
def ps(p,a): return {k:v*a for k,v in p.items() if v*a}
def pm(p,q):
    out={}
    for k,u in p.items():
        for l,v in q.items():
            m=tuple(k[i]+l[i] for i in range(3));out[m]=out.get(m,F(0))+u*v
    return {k:v for k,v in out.items() if v}
def pd(p,i):
    out={}
    for k,v in p.items():
        if k[i]:
            l=list(k);l[i]-=1;out[tuple(l)]=v*k[i]
    return out
def exact_value(p,q): return sum(v*q[0]**k[0]*q[1]**k[1]*q[2]**k[2] for k,v in p.items())
def my_basis(d): return [k for n in range(d+1) for k in ((a,b,n-a-b) for a in range(n+1) for b in range(n-a+1))]
O={(0,0,0):F(1)}
X,Y,Z=[{tuple(int(i==j) for i in range(3)):F(1)} for j in range(3)]

def divergence_kinetic(p,rho=F(1)):
    coords=(X,Y,Z)
    A=[[None]*3 for _ in range(3)]
    for i,c in enumerate(coords): A[i][i]=ps(pa(O,ps(pm(c,c),-1)),(3+rho)/4 if i<2 else F(3,2))
    A[0][1]=A[1][0]=ps(pa(Z,ps(pm(X,Y),-1)),rho/4)
    A[0][2]=A[2][0]=ps(pa(Y,ps(pm(X,Z),-1)),F(3,4))
    A[1][2]=A[2][1]=ps(pa(X,ps(pm(Y,Z),-1)),F(3,4))
    out={}
    for i in range(3):
        for j in range(3): out=pa(out,ps(pd(pm(A[i][j],pd(p,j)),i),-1))
    return out
def my_inner(p,q): return sum(v*matrix_haar_moment(*k) for k,v in pm(p,q).items())
def my_matrices(d,rho):
    bs=my_basis(d);pss=[{k:F(1)} for k in bs]
    G=[[my_inner(p,q) for q in pss] for p in pss]
    K=[[my_inner(p,divergence_kinetic(q,rho)) for q in pss] for p in pss]
    MX=[[my_inner(p,pm(X,q)) for q in pss] for p in pss]
    MY=[[my_inner(p,pm(Y,q)) for q in pss] for p in pss]
    return bs,G,K,MX,MY
def matmul(A,B): return [[sum((a*b for a,b in zip(row,col)),F(0)) for col in zip(*B)] for row in A]
def gauss_jordan_inverse(A):
    n=len(A);W=[list(row)+[F(i==j) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        k=next(i for i in range(j,n) if W[i][j]);W[j],W[k]=W[k],W[j]
        pivot=W[j][j];W[j]=[v/pivot for v in W[j]]
        for i in range(n):
            if i!=j:
                factor=W[i][j];W[i]=[x-factor*y for x,y in zip(W[i],W[j])]
    return [row[n:] for row in W]
def characteristic_inertia(A):
    """Faddeev–LeVerrier + Descartes; symmetry makes all roots real."""
    n=len(A)
    if any(len(row)!=n for row in A) or A!=[list(row) for row in zip(*A)]: raise ValueError('symmetric square input required')
    B=[[F(i==j) for j in range(n)] for i in range(n)];coeff=[F(1)]
    for k in range(1,n+1):
        B=matmul(A,B);c=-sum(B[i][i] for i in range(n))/k;coeff.append(c)
        for i in range(n): B[i][i]+=c
    zero=0
    while coeff and coeff[-1]==0: zero+=1;coeff.pop()
    def variation(cs):
        signs=[1 if c>0 else -1 for c in cs if c]
        return sum(a!=b for a,b in zip(signs,signs[1:]))
    pos=variation(coeff);neg=variation([c*(-1)**k for k,c in enumerate(coeff)])
    if neg+zero+pos!=n: raise RuntimeError('non-real-rooted or algorithm defect')
    return neg,zero,pos
def shifted(A,G,t): return [[a-t*g for a,g in zip(ar,gr)] for ar,gr in zip(A,G)]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('--label',default='audit');args=ap.parse_args()
    source=args.source.resolve();before=digest(source);m=load(source,'reviewed_two_plaquette')
    records=[];defects=[]
    def check(ok,label,detail=None):
        if not ok: raise RuntimeError(label)
        records.append({'test':label,'passed':True,'detail':detail})
    def rejects(fn,label):
        try: fn()
        except (ValueError,RuntimeError,TypeError,KeyError) as e:
            records.append({'test':label,'passed':True,'rejection':str(e)});return
        raise RuntimeError('Unexpected acceptance: '+label)
    for k in my_basis(8): check(m.moment(k)==matrix_haar_moment(*k),'independent_moment.'+'.'.join(map(str,k)))
    for rho in (F(0),F(1,3),F(1),F(4)):
        for k in my_basis(4): check(m.kinetic({k:F(1)},rho)==divergence_kinetic({k:F(1)},rho),f'divergence_kinetic.{rho}.{k}')
    # Independent jets act on monomials directly, before applying any coordinate formula.
    links={n:su2((F(i+1,i+3),F(2-i,i+4),F(i%3-1,i+2))) for i,n in enumerate(ENDS)}
    q=tuple(trace_jet(links,w)[0] for w in WORDS)
    def sjmul(a,b): return (a[0]*b[0],a[0]*b[1]+a[1]*b[0],a[0]*b[2]+2*a[1]*b[1]+a[2]*b[0])
    jets={(name,axis):[trace_jet(links,w,name,axis) for w in WORDS] for name in ENDS for axis in range(3)}
    for k in my_basis(3):
        val=F(0)
        for js in jets.values():
            out=(F(1),F(0),F(0))
            for exponent,j in zip(k,js):
                for _ in range(exponent): out=sjmul(out,j)
            val-=out[2]
        check(val==exact_value(m.kinetic({k:F(1)}),q),f'raw_link_monomial.{k}')
    for rho in (F(1,3),F(1),F(4)):
        for d in (1,2): check(m.matrices(d,rho)==tuple(my_matrices(d,rho)),f'independent_G_K_X_Y.degree{d}.rho{rho}')
    for degree in range(1,9):
        first=min(m.free_energy(k) for k in my_basis(degree+1) if sum(k)==degree+1)
        check(m.tail_lower(degree)==first,f'sharp_tail_first_layer.{degree}')
        for n in range(degree+1,degree+5):
            check(all(m.free_energy(k)>=m.tail_lower(degree) for k in my_basis(n) if sum(k)==n),f'tail_checked_layer.{degree}.{n}')
    for rho in (F(1,5),F(1,2),F(2),F(5)):
        for degree in range(1,5):
            first=min(m.free_energy(k,rho) for k in my_basis(degree+1) if sum(k)==degree+1)
            check(m.tail_lower(degree,1,rho)==first,f'general_rho_sharp_first_layer.{rho}.{degree}')
    fixtures=[[[F(0)]],[[F(0),F(1)],[F(1),F(0)]],[[F(1),F(2)],[F(2),F(4)]],
              [[F(0),F(0),F(2)],[F(0),F(0),F(0)],[F(2),F(0),F(0)]],
              [[F(2),F(-1),F(1)],[F(-1),F(-3),F(4)],[F(1),F(4),F(0)]]]
    for i,A in enumerate(fixtures): check(m.inertia(A)==characteristic_inertia(A),f'independent_characteristic_inertia.fixture{i}')
    for name,A,index,guess,width in [('exact_root',[[F(0)]],0,3,F(1)),('non_target_root',[[F(-1),F(0),F(0)],[F(0),F(0),F(0)],[F(0),F(0),F(1)]],0,1,F(2))]:
        G=[[F(i==j) for i in range(len(A))] for j in range(len(A))]
        br=m.exact_bracket(A,G,index,guess,width)
        lo,hi=F(br['lower']),F(br['upper'])
        nl,nh=characteristic_inertia(shifted(A,G,lo)),characteristic_inertia(shifted(A,G,hi))
        check(hi-lo<=width and not nl[1] and not nh[1] and nl[0]<=index<nh[0],f'exact_bracket_root_branch.{name}')
    certs=[]
    for d,a,l1,l2,rho in [(1,F(1),F(0),F(0),F(1)),(2,F(1),F(1),F(2),F(1)),(2,F(2,3),F(0),F(1,3),F(1)),(2,F(1),F(1,2),F(0),F(4))]:
        c=m.certificate(d,a,l1,l2,rho);check(m.verify_certificate(c),f'production_replay.{len(certs)}')
        bs,G,K,MX,MY=my_matrices(d,rho);n=len(G)
        H=[[a*K[i][j]+(l1+l2)*G[i][j]-l1*MX[i][j]-l2*MY[i][j] for j in range(n)] for i in range(n)]
        pss=[{k:F(1)} for k in bs];W=pa(ps(X,l1),ps(Y,l2));WP=[pm(W,p) for p in pss]
        W2=[[my_inner(p,q) for q in WP] for p in WP]
        M=[[l1*MX[i][j]+l2*MY[i][j] for j in range(n)] for i in range(n)]
        correction=matmul(matmul(M,gauss_jordan_inverse(G)),M)
        C=[[W2[i][j]-correction[i][j] for j in range(n)] for i in range(n)]
        check(C==m.coupling_square(d,l1,l2,rho),f'independent_cross_block.{len(certs)}')
        check(characteristic_inertia(C)[0]==0,f'cross_block_PSD.{len(certs)}')
        tau=F(c['tail_lower']);threshold=F(c['comparison_threshold'])
        B=[[H[i][j]-C[i][j]/(tau-threshold) for j in range(n)] for i in range(n)]
        for name,A in [('A',H),('B',B)]:
            for bracket in c[name+'_brackets']:
                for endpoint in ('lower','upper'):
                    actual=characteristic_inertia(shifted(A,G,F(bracket[endpoint])))
                    check(list(actual)==bracket[endpoint+'_inertia'],f'characteristic_endpoint.{len(certs)}.{name}.{bracket["index"]}.{endpoint}')
        certs.append(c)
    c=certs[1]
    mutators={
        'missing_scope':lambda z:z.pop('scope'),
        'wrong_scope':lambda z:z.__setitem__('scope','continuum'),
        'wrong_source':lambda z:z.__setitem__('source_sha256','0'*64),
        'empty_brackets':lambda z:z.__setitem__('A_brackets',[]),
        'wrong_dimension':lambda z:z.__setitem__('dimension',1),
        'tail_threshold_collision':lambda z:z.__setitem__('comparison_threshold',z['tail_lower']),
        'wrong_tail':lambda z:z.__setitem__('tail_lower','99999'),
        'wrong_gap':lambda z:z.__setitem__('gap',['100','101']),
        'wrong_status':lambda z:z.__setitem__('status','proved-continuum-gap'),
        'wrong_positive':lambda z:z.__setitem__('positive',not z['positive']),
        'insufficient_precision':lambda z:z.__setitem__('width_requested','1/1000000000000000000000000000000'),
        'wrong_alpha':lambda z:z.__setitem__('alpha','7'),
        'wrong_lambda':lambda z:z.__setitem__('lambda1','9'),
        'wrong_index':lambda z:z['A_brackets'][1].__setitem__('index',0),
        'wrong_inertia':lambda z:z['A_brackets'][0].__setitem__('lower_inertia',[2,0,8]),
        'non_boolean_positive':lambda z:z.__setitem__('positive',1),
        'boolean_inertia':lambda z:z['A_brackets'][0]['lower_inertia'].__setitem__(0,False),
    }
    for name,mutate in mutators.items():
        z=copy.deepcopy(c);mutate(z);rejects(lambda:m.verify_certificate(z),'certificate_mutation_rejected.'+name)
    for params in [(0,0,0,1),(1,-1,0,1),(1,0,-1,1),(1,0,0,-1),(True,0,0,1),(float('nan'),0,0,1)]: rejects(lambda:m.parameters(*params),f'bad_parameters.{params}')
    rejects(lambda:m.certificate(0),'insufficient_degree')
    rejects(lambda:m.certificate(1,1,100,100),'insufficient_tail')
    huge=m.certificate(1,10**20+1,0,0)
    check(m.verify_certificate(huge) and all(F(b['upper'])-F(b['lower'])<=F(huge['width_requested']) for key in ('A_brackets','B_brackets') for b in huge[key]),'large_scale_absolute_precision_fixed')
    pointcerts=[m.certificate(2,1,i,j) for i in range(3) for j in range(3)]
    rectangle=m.rectangle_certificate(pointcerts)
    check(m.verify_rectangle(rectangle),'canonical_rectangle_replay')
    check(rectangle['domain']==[['0','2'],['0','2']] and F(rectangle['gap_lipschitz_l1'])==2,'independent_rectangle_domain_lipschitz')
    intervals={F(0):(F(0),F(1,2)),F(1):(F(1,2),F(3,2)),F(2):(F(3,2),F(2))}
    margins=[];centers=set()
    for cell in rectangle['cells']:
        x,y=map(F,cell['center']);centers.add((x,y));point=cell['point_certificate']
        check(tuple(map(F,cell['x_interval']))==intervals[x] and tuple(map(F,cell['y_interval']))==intervals[y],f'geometric_rectangle_cell.{x}.{y}')
        margin=F(point['gap'][0])-2
        check(F(cell['margin'])==margin and margin>0,f'independent_rectangle_margin.{x}.{y}')
        margins.append(margin)
    check(centers=={(F(x),F(y)) for x in range(3) for y in range(3)} and F(rectangle['gap_lower'])==min(margins),'independent_rectangle_complete_cover')
    rectangle_mutators={
        'integer_positive':lambda z:z.__setitem__('positive',1),
        'hole':lambda z:z['cells'].pop(),
        'wrong_radius':lambda z:z['cells'][0].__setitem__('radius_l1','0'),
        'wrong_interval':lambda z:z['cells'][0].__setitem__('x_interval',['0','1/4']),
        'wrong_lipschitz':lambda z:z.__setitem__('gap_lipschitz_l1','1'),
        'wrong_alpha':lambda z:z.__setitem__('alpha','2'),
        'wrong_source':lambda z:z.__setitem__('source_sha256','0'*64),
        'duplicate_center':lambda z:z['cells'].__setitem__(0,copy.deepcopy(z['cells'][1])),
    }
    for name,mutate in rectangle_mutators.items():
        z=copy.deepcopy(rectangle);mutate(z);rejects(lambda:m.verify_rectangle(z),'rectangle_mutation_rejected.'+name)
    # Retain the initially discovered int-division API defect if still present.
    direct=m.coupling_square(1,22,15);exact=m.coupling_square(1,F(22),F(15))
    if direct!=exact or any(not isinstance(v,F) for row in direct for v in row):
        defects.append({'defect':'coupling_square integer inputs introduce float arithmetic','certificate_path_affected':False,
                        'direct_types':sorted({type(v).__name__ for row in direct for v in row})})
    else: check(True,'coupling_square_public_integer_exactness')
    check(digest(source)==before,'production_source_unchanged_during_audit')
    functions=[{'name':n.name,'first_line':n.lineno,'last_line':n.end_lineno} for n in ast.walk(ast.parse(source.read_text())) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
    result={'status':'passed-with-public-API-defect' if defects else 'passed','source_path_at_run':str(source),'source_sha256':before,
            'audit_source_sha256':digest(__file__),'optimized_python':not __debug__,'gate_count':len(records),'records':records,'defects':defects,
            'reviewed_scope':'entire source, function line ranges below; executed algebra, matrices, four certificates, independent characteristic endpoint inertia, mutation rejection',
            'reviewed_functions':functions,'certificates':certs}
    output=Path(__file__).with_name(args.label+'_results.json');output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'gate_count':len(records),'source_sha256':before,'optimized_python':not __debug__,'output':str(output),'defects':defects}))
if __name__=='__main__': main()
