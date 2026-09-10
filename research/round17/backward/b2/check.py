"""Independent exact Haar-polynomial verification of the B2 adjoint trial."""
from fractions import Fraction as F
from pathlib import Path
import argparse,copy,csv,hashlib,json
from geometry import exact,graph,geometry


def shared_face(g):
    geometry(g)
    selected=[i for i,f in enumerate(g['faces']) if all(v[0]==1 for v in f['vertices'])]
    if len(selected)!=1:raise ValueError('one geometric shared yz square required')
    return selected[0]


def haar(k):
    if type(k) is not int or k<0:raise ValueError('nonnegative integer moment required')
    if k%2:return F(0)
    ans=F(1)
    for j in range(1,k//2+1):ans*=F(2*j-1,2*j+2)
    return ans


def moment(powers,inc):
    if len(powers)!=11 or any(type(k) is not int or k<0 for k in powers) or sum(powers)>5:raise ValueError('reviewed eleven-face total degree at most five required')
    if any(sum(powers[f] for f in faces)%2 for faces in inc.values()):return F(0)
    active=[i for i,k in enumerate(powers) if k]
    if not active:return F(1)
    if len(active)==1:return haar(powers[active[0]])
    if len(active)==2:
        p,q=active
        if not any(p in faces and q not in faces for faces in inc.values()):raise ValueError('missing exclusive link for conditional Haar integration')
        return haar(powers[p])*haar(powers[q])
    raise ValueError('unsupported surviving multi-face moment')


def basis(g):
    s=shared_face(g);zero=(0,)*11;polys=[{zero:F(1)}]
    for p in range(11):
        exponents=list(zero);exponents[p]=1;polys.append({tuple(exponents):F(2)})
    exponents=list(zero);exponents[s]=2;polys.append({zero:F(-1),tuple(exponents):F(4)})
    return polys


def multiply(a,b):
    ans={}
    for p,c in a.items():
        for q,d in b.items():
            e=tuple(x+y for x,y in zip(p,q));ans[e]=ans.get(e,F(0))+c*d
    return {p:c for p,c in ans.items() if c}


def entries(g):
    inc,girth=geometry(g);polys=basis(g);gram=[];magnetic=[[] for _ in range(11)];visited=set()
    for a in polys:
        row=[];mrows=[[] for _ in range(11)]
        for b in polys:
            ab=multiply(a,b)
            row.append(sum(c*moment(p,inc) for p,c in ab.items()));visited.update(ab)
            for f in range(11):
                total=F(0)
                for p,c in ab.items():
                    p=list(p);p[f]+=1;p=tuple(p);visited.add(p);total+=c*moment(p,inc)
                mrows[f].append(total)
        gram.append(row)
        for f in range(11):magnetic[f].append(mrows[f])
    # Each ordinary character is a Casimir eigenfunction on each of its four links.
    eigen=[F(0)]+[4*F(1,2)*F(3,2)]*11+[4*F(1)*F(2)]
    electric=[[gram[i][j]*eigen[j] for j in range(13)] for i in range(13)]
    return gram,magnetic,electric,len(visited)


def bilinear(left,matrix,right):
    return sum(left[i]*matrix[i][j]*right[j] for i in range(len(left)) for j in range(len(right)))


def compute(alpha='1',eta='3/3817',g=None,matrices=None):
    a,t=map(exact,(alpha,eta))
    if a<=0:raise ValueError('positive physical energy scale required')
    g=graph() if g is None else g
    G,M,T,_=entries(g) if matrices is None else matrices
    r=F(12,43);H=[[a*(T[i][j]-r*sum(M[p][i][j] for p in range(11))) for j in range(13)] for i in range(13)]
    v=[F(1)]+[F(1,22)]*11+[t]
    norm=bilinear(v,G,v);numerator=bilinear(v,H,v);rayleigh=numerator/norm;e1=-F(3,43)*a;lower=e1-rayleigh
    return {'alpha':str(a),'coupling':str(a*r),'eta':str(t),'norm_squared':str(norm),'energy_numerator':str(numerator),
      'full_ground_upper':str(rayleigh),'full_E1_lower':str(e1),'full_gap_lower_bound':str(lower),
      'state_status':'valid','status':'positive' if lower>0 else 'insufficient','bound_sign':'positive' if lower>0 else 'zero' if not lower else 'negative'}


def run(output):
    output=Path(output).resolve()
    if output.is_relative_to(Path(__file__).resolve().parent):raise ValueError('output outside frozen source required')
    output.mkdir(parents=True,exist_ok=False);checks=[]
    def check(name,ok):
        if not ok:raise RuntimeError(name)
        checks.append({'name':name,'passed':True})
    def reject(name,fn):
        try:fn()
        except (ValueError,TypeError,KeyError):check(name,True);return
        raise RuntimeError('unsupported input accepted: '+name)
    g=graph();s=shared_face(g);inc,girth=geometry(g);G,M,T,count=entries(g);mat=(G,M,T,count)
    check('actual graph and geometric shared face', (len(g['vertices']),len(g['edges']),len(g['faces']),girth)==(12,20,11,4) and g['faces'][s]['base']==[1,0,0])
    check('all 169 Gram entries including adjoint norm',G==[[F(i==j) for j in range(13)] for i in range(13)])
    check('all 169 electric entries distinguish fundamental and adjoint',T==[[F(0) if i!=j or i==0 else F(8) if i==12 else F(3) for j in range(13)] for i in range(13)])
    expected=[]
    for f in range(11):
        pairs={(0,f+1),(f+1,0)}
        if f==s:pairs|={(12,s+1),(s+1,12)}
        expected.append([[F(1,2) if (i,j) in pairs else F(0) for j in range(13)] for i in range(13)])
    check('all 1859 magnetic entries from actual polynomial integrals',M==expected)
    mixed=[]
    for p in range(11):
        if p==s:continue
        powers=[0]*11;powers[p]=powers[s]=2;mixed.append(moment(powers,inc))
    check('two-face even moments use exclusive-link integration',mixed==[F(1,16)]*10)
    check('adjoint ordinary character normalization',16*haar(4)-8*haar(2)+1==1 and 4*haar(2)-1==0)
    v0=[F(1)]+[F(1,22)]*11+[F(0)];z=[F(0)]*12+[F(1)];H=[[T[i][j]-F(12,43)*sum(M[p][i][j] for p in range(11)) for j in range(13)] for i in range(13)]
    coeffs=[bilinear(v0,H,v0),2*bilinear(z,H,v0),bilinear(z,H,z)];normcoeffs=[bilinear(v0,G,v0),2*bilinear(z,G,v0),bilinear(z,G,z)]
    check('matrix-derived Rayleigh polynomial coefficients',coeffs==[-F(3,43)*F(45,44),-F(6,473),F(8)] and normcoeffs==[F(45,44),F(0),F(1)])
    check('old trial is eigenvector only of twelve-state compression',all(sum(H[i][j]*v0[j] for j in range(12))==-F(3,43)*v0[i] for i in range(12)) and bilinear(z,H,v0)==-F(3,473))
    A=F(6,473);B=F(347,43);endpoint=F(6,3817);star=F(3,3817)
    check('exact polynomial factorization proves entire open interval',A==B*endpoint and B>0 and normcoeffs[0]>0)
    fixtures={name:compute(alpha,eta,g,mat) for name,alpha,eta in [('chosen',1,star),('zero',1,0),('endpoint',1,endpoint),('negative',1,-star),('beyond',1,3*star),('scaled',2,star),('small_scale','1/1000',star),('near_endpoint',1,endpoint-F(1,10**12))]}
    check('chosen amplitude gives positive full physical lower bound',F(fixtures['chosen']['full_gap_lower_bound'])>0 and fixtures['chosen']['full_E1_lower']=='-3/43')
    check('both endpoints are valid trials with insufficient zero bound',all(fixtures[n]['state_status']=='valid' and fixtures[n]['bound_sign']=='zero' and fixtures[n]['status']=='insufficient' for n in ['zero','endpoint']))
    check('negative and beyond amplitudes are valid negative-bound trials',all(fixtures[n]['state_status']=='valid' and fixtures[n]['bound_sign']=='negative' for n in ['negative','beyond']))
    check('strict near-endpoint rational positivity',fixtures['near_endpoint']['status']=='positive')
    chosen=F(fixtures['chosen']['full_gap_lower_bound'])
    check('exact arbitrary positive scale restoration',F(fixtures['scaled']['full_gap_lower_bound'])==2*chosen and F(fixtures['small_scale']['full_gap_lower_bound'])==chosen/1000)
    numerator=A*star-B*star*star;denominator=F(45,44)+star*star;derivative=((A-2*B*star)*denominator-2*star*numerator)/(denominator*denominator)
    check('numerator maximum is not quotient maximum',A-2*B*star==0 and numerator>0 and derivative<0)
    check('wrong divided-by-three character normalization detected',(16*haar(4)-8*haar(2)+1)/9!=1)
    check('wrong fundamental electric energy detected',T[12][12]!=3)
    check('omitting new mixed matrix term cannot repair endpoint',(-B*star*star)/(F(45,44)+star*star)<0<chosen)
    altered=copy.deepcopy(g);altered['faces'].reverse()
    for i,f in enumerate(altered['faces']):f['id']=i
    check('geometric shared face survives reordered face inventory',altered['faces'][shared_face(altered)]['base']==[1,0,0] and compute(1,star,altered)['full_gap_lower_bound']==str(chosen))
    bad=copy.deepcopy(g);bad['faces'][s]['word'][0][1]*=-1;reject('wrong dagger rejected',lambda:shared_face(bad))
    bad=copy.deepcopy(g);bad['faces'][s]['base'][0]=True;reject('Boolean shared-face metadata rejected',lambda:shared_face(bad))
    reject('Boolean alpha rejected',lambda:compute(True))
    reject('zero alpha rejected',lambda:compute(0))
    reject('Boolean amplitude rejected',lambda:compute(1,True))
    reject('unreviewed moment degree rejected',lambda:moment([6]+[0]*10,inc))
    ledger=[compute(1,F(k,3817),g,mat) for k in (-3,0,1,2,3,4,5,6,9)]
    encode=lambda x:[[str(v) for v in row] for row in x]
    result={'schema':'ym17-independent-b2-results-v1','status':'passed','checks_count':len(checks),'checks':checks,
      'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'geometry_sha256':hashlib.sha256(Path(__file__).with_name('geometry.py').read_bytes()).hexdigest(),
      'shared_face_index':s,'distinct_polynomial_moments':count,'gram_entry_count':169,'magnetic_entry_count':1859,
      'norm_polynomial':list(map(str,normcoeffs)),'energy_polynomial_at_alpha_one':list(map(str,coeffs)),
      'gap_numerator_polynomial':['0',str(A),str(-B)],'positive_eta_interval':['0',str(endpoint)],
      'chosen_quotient_derivative':str(derivative),'fixtures':fixtures,
      'scope':'Exact sufficient lower bound for the full physical operator on the finite dense two-cube graph, not a dense volume-uniform or continuum theorem.'}
    for name,obj in [('results.json',result),('graph.json',g),('matrices.json',{'Gram':encode(G),'electric_over_alpha':encode(T),'magnetic_face_insertions':[encode(x) for x in M]}),('amplitude_ledger.json',ledger)]:
        (output/name).write_text(json.dumps(obj,indent=2)+'\n')
    with (output/'amplitude_ledger.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['eta','full_gap_lower_bound','state_status','status','bound_sign']);w.writeheader();w.writerows({k:r[k] for k in w.fieldnames} for r in ledger)
    print(json.dumps({'status':'passed','checks_count':len(checks),'chosen_lower':str(chosen),'chosen_lower_decimal':float(chosen)}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args();run(args.output)
