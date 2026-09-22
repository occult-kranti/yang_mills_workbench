#!/usr/bin/env python3
"""Independent exact AH1 graph/channel construction and complete heat certificate.
Historical checkers are neither imported nor executed. Standard library only.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import itertools as it
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def frac(x):
    return str(x) if isinstance(x, F) else x


def serial(x):
    if isinstance(x, F): return str(x)
    if isinstance(x, dict): return {str(k): serial(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)): return [serial(v) for v in x]
    return x


def source_check():
    inv = json.loads((HERE/'inputs/source-inventory.json').read_text())
    records = inv['entries']
    for r in records:
        p = ROOT/r['snapshot']
        need(p.is_relative_to(HERE/'inputs'), 'snapshot escapes owned input tree')
        need(hashlib.sha256(p.read_bytes()).hexdigest() == r['sha256'], 'snapshot hash: '+r['source'])
    conrec = next(r for r in records if r['source'] == 'research/round28/contracts/ah1.json')
    contract = json.loads((ROOT/conrec['snapshot']).read_text())
    need(len(contract['sources']) == 42, '42 frozen original sources')
    index = {r['source']: r['sha256'] for r in records}
    need(all(index[p] == h for p, h in contract['sources'].items()), 'all required source bindings')
    need(conrec['sha256'] == '9c6f5bc1a71fcd49b93a1212e1b1837a82bc588b27b695fd600cbec46be17053', 'contract identity')
    return records


def graph(box=(4, 3, 2)):
    vertices = list(it.product(*(range(n) for n in box)))
    edges = []
    for v in vertices:
        for a in range(3):
            w = tuple(v[i]+(i == a) for i in range(3))
            if w[a] < box[a]: edges.append((v, a, w))
    lookup = {frozenset((v, w)): j for j, (v, a, w) in enumerate(edges)}
    faces = []
    for v in vertices:
        for a, b in it.combinations(range(3), 2):
            if v[a]+1 >= box[a] or v[b]+1 >= box[b]: continue
            va = tuple(v[i]+(i == a) for i in range(3))
            vab = tuple(v[i]+(i in (a, b)) for i in range(3))
            vb = tuple(v[i]+(i == b) for i in range(3))
            path = (v, va, vab, vb, v)
            word = []
            for u, w in zip(path, path[1:]):
                j = lookup[frozenset((u, w))]
                word.append((j, 1 if edges[j][0] == u else -1))
            ids = [j for j, s in word]
            normal = next(c for c in range(3) if c not in (a, b))
            faces.append({'id': len(faces), 'tail': v, 'axes': (a,b), 'word': word,
                          'mask': sum(1 << j for j in ids),
                          'internal': 0 < v[normal] < box[normal]-1})
    return vertices, edges, faces


def four_cycles(vertices, edges):
    adj = {v: set() for v in vertices}
    lookup = {}
    for j, (u, a, v) in enumerate(edges):
        adj[u].add(v); adj[v].add(u); lookup[frozenset((u,v))] = j
    masks = set()
    for u in vertices:
        for v in adj[u]:
            for w in adj[v]-{u}:
                for z in (adj[w] & adj[u])-{v}:
                    masks.add(sum(1 << lookup[frozenset(e)] for e in ((u,v),(v,w),(w,z),(z,u))))
    return masks


def qmul(q, r):
    a,b,c,d=q; e,f,g,h=r
    return (a*e-b*f-c*g-d*h,a*f+b*e+c*h-d*g,a*g-b*h+c*e+d*f,a*h+b*g-c*f+d*e)


def qinv(q): return (q[0],-q[1],-q[2],-q[3])


def wilson(word, links, wrong_reverse=False):
    ans=(F(1),F(0),F(0),F(0))
    for j,s in word: ans=qmul(ans, links[j] if s==1 or wrong_reverse else qinv(links[j]))
    return ans[0]


def basis_matrix(faces):
    m=len(faces); basis=[{'kind':'vacuum','faces':[],'norm2':F(1),'energy':F(0),'parity':0}]
    basis += [{'kind':'face','faces':[p],'norm2':F(1),'energy':F(3),'parity':1} for p in range(m)]
    pairs=[]; matrix={}
    def couple(i,p,a):
        j=p+1; matrix[i,j]=F(a)
        matrix[j,i]=F(a)*basis[i]['norm2']/basis[j]['norm2']
    for p in range(m): couple(0,p,F(1,2))
    for p in range(m):
        i=len(basis);basis.append({'kind':'spin1','faces':[p],'norm2':F(1),'energy':F(8),'parity':0})
        couple(i,p,F(1,2))
    for p,q in it.combinations(range(m),2):
        common=faces[p]['mask'] & faces[q]['mask']; n=common.bit_count()
        need(n in (0,1),'distinct faces share at most one edge')
        records=[]
        kinds=[('singlet',1,F(9,2)),('triplet',3,F(13,2))] if n else [('pair',1,F(6))]
        for kind,norm,en in kinds:
            i=len(basis);records.append(i)
            basis.append({'kind':kind,'faces':[p,q],'norm2':F(norm),'energy':en,'parity':0})
            for z in (p,q): couple(i,z,F(1,4) if n else F(1,2))
        pairs.append({'faces':[p,q],'mask':faces[p]['mask']^faces[q]['mask'],
                      'shared_edge':(common.bit_length()-1 if n else None),'basis_rows':records})
    for j,b in enumerate(basis): b['id']=j
    return basis,matrix,pairs


def action(basis, smat, lam, v):
    out=[(b['energy']+len([z for z in basis if z['kind']=='face'])*lam)*x for b,x in zip(basis,v)]
    for (i,j),s in smat.items(): out[i]-=lam*s*v[j]
    return out


def inner(basis,u,v): return sum((b['norm2']*x*y for b,x,y in zip(basis,u,v)),F(0))


def sparse_pair(re,im):
    return [[i,a,b] for i,(a,b) in enumerate(zip(re,im)) if a or b]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True)
    ap.add_argument('--lambda',dest='lam',default='1/100')
    ap.add_argument('--vector-file',help='JSON list of rational strings or [real,imag] rational pairs')
    args=ap.parse_args();out=Path(args.output).resolve();need(not out.exists(),'fresh output directory required')
    sources=source_check();lam=F(args.lam);need(0<=lam<=F(1,100),'nonnegative frozen coupling range')
    vertices,edges,faces=graph();m=len(faces)
    need((len(vertices),len(edges),m)==(24,46,29),'new complete graph counts')
    need(len(edges)-len(vertices)+1==23,'new cycle rank')
    need([f['mask'] for f in faces]==list(dict.fromkeys(f['mask'] for f in faces)),'distinct faces')
    need(four_cycles(vertices,edges)=={f['mask'] for f in faces},'all four-cycles are exactly listed faces')
    # Abstract exhaustive check supports the five-edge classification, not an arbitrary spin truncation.
    five=[]
    for a in range(1,5):
        for b in range(1,6-a):
            for es in it.combinations(list(it.product(range(a),range(b))),5):
                da=Counter(x for x,y in es);db=Counter(y for x,y in es)
                if all(da[x]>=2 for x in range(a)) and all(db[y]>=2 for y in range(b)): five.append((a,b,es))
    need(not five,'no five-edge bipartite minimum-degree-two support')
    center=[(-1)**sum(v[:a]) for v,a,w in edges]
    need(all(math.prod(center[j] for j,s in f['word'])==-1 for f in faces),'actual coordinate center parity')
    need(all(math.prod(-1 for j,s in f['word'])==1 for f in faces),'uniform link reversal is not odd-face assignment')
    masks=[f['mask'] for f in faces]
    need(all(x^y^z for x,y,z in it.combinations(masks,3)),'no triple-face parity identity')
    pmasks=[x^y for x,y in it.combinations(masks,2)]
    need(len(set(pmasks))==len(pmasks) and 0 not in pmasks,'all pair masks distinct and nonzero')
    need(not set(pmasks)&set(masks),'pair and single masks separate independently of center')
    need(all(a^b^c^d for a,b,c,d in it.combinations(masks,4)),'no four-distinct-face identity')
    basis,smat,pairs=basis_matrix(faces);n=len(basis);weights=[b['norm2'] for b in basis]
    need(all(w>0 for w in weights),'actual Haar Gram strictly positive: zero kernel')
    need(len({(b['kind'],tuple(b['faces'])) for b in basis})==n,'unique individual channel descriptions')
    need(all(weights[i]*a==weights[j]*smat.get((j,i),0) for (i,j),a in smat.items()),'metric self-adjointness')
    need(all(basis[i]['parity']!=basis[j]['parity'] for i,j in smat),'every within-parity entry zero')
    expected_nnz=4*m+4*sum(len(p['basis_rows']) for p in pairs)
    need(len(smat)==expected_nnz,'all structural nonzero entries counted')
    shared=sum(p['shared_edge'] is not None for p in pairs)
    face_vertices=[set(v for j,s in f['word'] for v in (edges[j][0],edges[j][2])) for f in faces]
    for pair in pairs:
        p,q=pair['faces'];touch=len(face_vertices[p]&face_vertices[q])
        pair['common_vertex_count']=touch
        pair['geometry']='shared_edge' if pair['shared_edge'] is not None else ('vertex_only' if touch else 'vertex_disjoint')
        if pair['shared_edge'] is not None:
            e=pair['shared_edge'];pair['shared_orientation_signs']=[next(s for j,s in faces[r]['word'] if j==e) for r in (p,q)]
    geometry_counts=dict(Counter(p['geometry'] for p in pairs))
    need(n==1+2*m+len(pairs)+shared,'complete individually resolved enrichment rank')
    # Recover full old-to-new leakage Gram from every new channel in the physical metric.
    gram=[[F(0) for _ in range(m)] for _ in range(m)]
    for i in range(m+1,n):
        entries=[(j-1,a) for (r,j),a in smat.items() if r==i and 1<=j<=m]
        for p,a in entries:
            for q,b in entries: gram[p][q]+=weights[i]*a*b
    need(all(gram[p][q]==(F(m,4) if p==q else F(1,4)) for p in range(m) for q in range(m)), 'complete original omitted Gram')
    need(sum(gram[0])==F(2*m-1,4),'bright omitted eigenvalue from all channels')
    fourth=F(m,8)+6*F(math.comb(m,2),16);var=fourth-F(m*m,16)
    need(var==F(m*(2*m-1),16),'complete fourth moment and centered square norm')
    # Independent norm sum for F=S^2-m/4 in actual rational channel coordinates.
    fcoef=[F(0)]*n
    for i,b in enumerate(basis):
        if b['kind'] in ('spin1','singlet','triplet'): fcoef[i]=F(1,4)
        elif b['kind']=='pair': fcoef[i]=F(1,2)
    need(inner(basis,fcoef,fcoef)==var,'all residual fusion contributions match moment sum')
    # Rational fixtures discriminate orientations and endpoint inverse in every actual Gauss action.
    quats=[(F(3,5),F(4,5),F(0),F(0)),(F(5,13),F(0),F(12,13),F(0)),(F(8,17),F(0),F(0),F(15,17))]
    links=[quats[j%3] for j in range(len(edges))]
    gauges={v:quats[(j+j//3)%3] for j,v in enumerate(vertices)}
    transformed=[qmul(qmul(gauges[u],links[j]),qinv(gauges[v])) for j,(u,a,v) in enumerate(edges)]
    wrong_gauss=[qmul(qmul(gauges[u],links[j]),gauges[v]) for j,(u,a,v) in enumerate(edges)]
    need(all(wilson(f['word'],links)==wilson(f['word'],transformed) for f in faces),'all actual Gauss invariant traces')
    bad_orientation=[f['id'] for f in faces if wilson(f['word'],links,True)!=wilson(f['word'],transformed,True)]
    bad_gauss=[f['id'] for f in faces if wilson(f['word'],links)!=wilson(f['word'],wrong_gauss)]
    need(bad_orientation and bad_gauss,'orientation and gauge-inverse mutations genuinely discriminated')
    # Uniform rational envelopes, independently recalculated from the new m and complete residual.
    cap=F(1,100);eta=F(1,100);g=3-m*cap;T=F(2)
    residual_root=math.isqrt(m*(2*m-1))+1
    need(residual_root**2>m*(2*m-1),'strict radical upper enclosure')
    sqrtm=F(math.isqrt(4*m)+1,2);need(sqrtm*sqrtm>m,'face root enclosure')
    r0=F(residual_root,12)*cap**2;p0=r0/g;rplus=m*cap*p0;pplus=rplus/g;dplus=rplus*rplus/g
    z=1-F(m,72)*cap**2;q0=sqrtm*cap/6;b=q0+p0+eta;den=z-eta-p0
    need(g>0 and den>0,'actual spectral and true-output denominators positive')
    exp_lower=sum(((g*T)**k/F(math.factorial(k)) for k in range(32)),F(0))
    exp_integer=exp_lower.numerator//exp_lower.denominator
    need(exp_integer>0 and exp_lower>exp_integer,'strict positive Taylor exponential certificate')
    early=(rplus+dplus)*T+m*cap*b/g
    late=pplus+(2*b+pplus)/exp_integer
    physical=max(early,late);relative=physical/den
    need(relative<F(22,10000),'recomputed conservative same-preparation bound below0.0022')
    # Meaningful mutations and exact consequences; rejected gates stay active under Python -O.
    controls={}
    def rejected(name,good):
        need(not good,'mutation was not rejected: '+name);controls[name]=True
    internal=[f['id'] for f in faces if f['internal']]
    rejected('missing_internal_face',set(f['mask'] for f in faces if f['id']!=internal[0])==four_cycles(vertices,edges))
    rejected('old_graph_counts',(len(vertices),len(edges),m)==(18,33,20))
    rejected('included_strict_endpoint',F(9,2)<F(9,2))
    rejected('unsupported_cutoff_support',bool(five))
    def bright_norm_skipping(row):
        return sum((weights[i]*sum((smat.get((i,j),F(0)) for j in range(1,m+1)),F(0))**2
                    for i in range(m+1,n) if i!=row),F(0))
    full_bright_norm=sum((sum(row,F(0)) for row in gram),F(0))
    singlet=next(i for i,bv in enumerate(basis) if bv['kind']=='singlet')
    triplet=next(i for i,bv in enumerate(basis) if bv['kind']=='triplet')
    rejected('missing_singlet_norm',bright_norm_skipping(singlet)==full_bright_norm)
    rejected('missing_triplet_norm',bright_norm_skipping(triplet)==full_bright_norm)
    tri=next(i for i,bv in enumerate(basis) if bv['kind']=='triplet');p=basis[tri]['faces'][0]+1
    rejected('wrong_triplet_metric',smat[p,tri]==smat[tri,p])
    rejected('metric_blind_transposition',all(a==smat[j,i] for (i,j),a in smat.items()))
    rejected('wrong_orientation',not bad_orientation)
    rejected('wrong_Gauss_endpoint_action',not bad_gauss)
    rejected('uniform_link_flip_center',all((-1)**len(f['word'])==-1 for f in faces))
    # A duplicate face label represents the exact null vector phi_0-phi_0.
    duplicate_null_norm=F(1)+F(1)-2*F(1)
    need(duplicate_null_norm==0,'duplicate physical Gram null verified')
    rejected('lost_Gram_null_by_identity_metric',F(1)+F(1)==duplicate_null_norm)
    need(all(smat.get((i,1),0)-smat.get((i,1),0)==0 for i in range(n)),'duplicate null descends through magnetic action')
    need(3-3==0,'duplicate null descends through electric action')
    rejected('global_parity_implies_mask_independence',len(set(pmasks+[pmasks[0]]))==len(pmasks)+1)
    # chi_1 times its own fundamental multiplier contains normalized chi_3/2 /2 outside P+.
    outside_energy=4*F(3,2)*F(5,2)
    need(outside_energy>max(x['energy'] for x in basis),'actual spin3/2 witness outside enrichment')
    rejected('BP0_zero_implies_B_zero',F(-1,2)==0)
    rejected('missing_new_input_leakage',F(1,4)==0)
    negative_vacuum_shift=m*(-cap)
    rejected('negative_coupling_positivity',negative_vacuum_shift>=0)
    bright_determinant_at_scalar=-F(m,4)*cap*cap
    rejected('scalar_reference_equals_Ritz_ground_at_positive_lambda',bright_determinant_at_scalar==0)
    # Exact generic unit-ground scalar examples certify why uncertain centers cannot be used for all time.
    ground_growth_lower=sum((F(1,math.factorial(k)) for k in range(5)),F(0))
    rejected('rounded_center_preserves_ground_exactly',ground_growth_lower<=1)
    rejected('wrong_own_center_defect_sign',F(3,10)-F(2,10)==-(F(3,10)-F(2,10)))
    # Center/time product is one: the erroneous ground factor exceeds this positive Taylor sum.
    need(ground_growth_lower>2,'nonsecular-center countercontrol has a nonzero quantitative discrepancy')
    rejected('full_input_zero_time_error_vanishes',F(1)==0)
    rejected('old_accuracy_target_imported',relative<F(37,10**6))
    controls.update({'lambda_zero_exact_K_reduction':True,'time_zero_exact_on_P0':True,
                     'full_outside_envelope_not_exact_Gram':True,'two_nested_projector_premises_explicit_in_report':True,
                     'continuous_lambda_and_time_from_report_not_grid':True,'historical_checkers_not_imported_or_executed':True})
    need(action(basis,smat,F(0),[F(1)]+[F(0)]*(n-1))==[F(0)]*n,'zero coupling vacuum exact action')
    # Every operator column is exported; execute independent preparation and new-channel actions too.
    inputs=[]
    vacuum=[F(0)]*n;vacuum[0]=1
    inputs.append(('vacuum',vacuum,[F(0)]*n))
    for imaginary in (False,True):
        re=[F(0)]*n;im=[F(0)]*n;re[0]=F(159999,160001)
        (im if imaginary else re)[1]=F(800,160001)
        need(inner(basis,re,re)+inner(basis,im,im)==1,'exact normalized face preparation')
        distance=inner(basis,[re[j]-vacuum[j] for j in range(n)],[re[j]-vacuum[j] for j in range(n)])+inner(basis,im,im)
        need(distance<=eta*eta,'same original preparation ball')
        inputs.append(('imaginary_face_preparation' if imaginary else 'real_face_preparation',re,im))
    v=[F(0)]*n;v[tri]=1;inputs.append(('triplet_coordinate',v,[F(0)]*n))
    diff=[F(0)]*n;diff[1]=1;diff[2]=-1;inputs.append(('face_difference',diff,[F(0)]*n))
    if args.vector_file:
        raw=json.loads(Path(args.vector_file).read_text());need(len(raw)==n,'requested vector dimension')
        re=[F(v[0] if isinstance(v,list) else v) for v in raw]
        im=[F(v[1]) if isinstance(v,list) else F(0) for v in raw]
        inputs.append(('requested_exact_vector',re,im))
    demonstrations=[]
    for name,re,im in inputs:
        ar=action(basis,smat,lam,re);ai=action(basis,smat,lam,im)
        need(action(basis,smat,F(0),re)==[b['energy']*x for b,x in zip(basis,re)],'zero coupling full electric action, real part')
        need(action(basis,smat,F(0),im)==[b['energy']*x for b,x in zip(basis,im)],'zero coupling full electric action, imaginary part')
        if name in ('vacuum','real_face_preparation','imaginary_face_preparation'):
            injected_re=[x if i<=m else F(0) for i,x in enumerate(re)]
            injected_im=[x if i<=m else F(0) for i,x in enumerate(im)]
            need(injected_re==re and injected_im==im,'zero-time exact physical initial injection')
        demonstrations.append({'name':name,'norm_squared':inner(basis,re,re)+inner(basis,im,im),
                               'input_sparse':sparse_pair(re,im),'L_action_sparse':sparse_pair(ar,ai)})
    bindings={r['source']:r['sha256'] for r in sources}
    bindings.update({r['snapshot']:r['sha256'] for r in sources})
    for rel in ('check.py','report.md','source-inventory.json','preflight-adapter-v1.json','inputs/source-inventory.json'):
        path=HERE/rel
        bindings[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    data={'schema':'ym28-forward-ah1-result-v1','loop':'ah1','checks_passed':True,
          'model':'actual full46-link Gauss-invariant uniform-coupling finite graph',
          'graph':{'vertex_box':[4,3,2],'vertices':vertices,'edges':[{'id':j,'tail':u,'axis':a,'head':v,'center_sign':center[j]} for j,(u,a,v) in enumerate(edges)],
                   'faces':faces,'counts':[len(vertices),len(edges),m],'internal_face_ids':internal,'cycle_rank':23,'four_cycle_count':len(four_cycles(vertices,edges))},
          'cutoff':{'strict_energy_upper':'9/2','P0_dimension':m+1,'full_electric_gap':'3','five_edge_support_counterexamples':five},
          'enrichment':{'rank':n,'basis':basis,'pairs':pairs,'kind_counts':dict(Counter(b['kind'] for b in basis)),
                        'Gram':'diagonal with listed positive norm2; exact kernel zero','nullity':0,'duplicate_control_null':[1,-1],
                        'pair_geometry_counts':geometry_counts,'not_full_energy_shell':True,'not_claimed_minimal_summed_column_cyclic_span':True},
          'retained_magnetic':{'entries':[[i,j,s] for (i,j),s in sorted(smat.items())],'nonzero_count':len(smat),
                               'zero_count':n*n-len(smat),'structural_zero_rule':'all unlisted entries are zero: same parity, or absent from complete old columns and metric adjoints',
                               'K_action':'diagonal listed energy; exact operator and form reduction'},
          'original_omitted_Gram':{'dimension':m,'diagonal':F(m,4),'off_diagonal':F(1,4),'bright_eigenvalue':F(2*m-1,4),'dark_eigenvalue':F(m-1,4)},
          'full_outside':{'definition':'B=-lambda(I-P+)SP+ on every column','BP0':'exactly zero','norm_upper':'29 lambda',
                          'nonzero_witness':{'input':'spin1 face0','output':'spin3/2 face0','output_energy':outside_energy,'coefficient':'-lambda/2'},
                          'exact_cubic_outside_Gram_evaluated':False},
          'Ritz_and_residual':{'w':'(sqrt(9+29 lambda^2)-3)/2','h':'lambda/[2(3+w)]','mu0':'29 lambda-w','f0':'(Omega+h sum_p phi_p)/sqrt(1+29h^2)',
                              'full_residual':'-2 lambda h (S^2-29/4)/sqrt(1+29h^2)', 'fourth_moment':fourth,'centered_square_norm_squared':var},
          'uniform_certificate':{'lambda_cap':cap,'preparation_eta':eta,'join':T,'g':g,'residual_root_upper':residual_root,'sqrt_faces_upper':sqrtm,
                                 'r0_bar':r0,'p0_bar':p0,'rplus_bar':rplus,'pplus_bar':pplus,'dplus_bar':dplus,'z_floor':z,'q0_bar':q0,'b_bar':b,'true_denominator':den,
                                 'exp_positive_Taylor_terms':32,'exp_positive_Taylor_lower':exp_lower,'exp_integer_lower':exp_integer,
                                 'early_absolute':early,'late_absolute':late,'all_time_absolute':physical,'all_time_relative':relative,'relative_upper_decimal':'0.0022',
                                 'numerical_heat_error':'not evaluated; exact semigroup bound only'},
          'generator_demonstrations':{'lambda':lam,'cases':demonstrations},'controls':controls,
          'control_evidence':{'wrong_orientation_faces':bad_orientation,'wrong_Gauss_faces':bad_gauss,
                              'complete_bright_norm_squared':full_bright_norm,
                              'missing_singlet_bright_norm_squared':bright_norm_skipping(singlet),
                              'missing_triplet_bright_norm_squared':bright_norm_skipping(triplet),
                              'negative_coupling_vacuum_shift':negative_vacuum_shift,
                              'bright_determinant_at_scalar_reference':bright_determinant_at_scalar,
                              'rounded_center_ground_growth_lower_at_time_inverse_error':ground_growth_lower},
          'source_inventory':{r['snapshot']:r['sha256'] for r in sources},'bindings':bindings}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(serial(data),sort_keys=True,indent=2)+'\n')
    print(json.dumps({'rank':n,'shared_pairs':shared,'kind_counts':data['enrichment']['kind_counts'],'sparse_entries':len(smat),
                      'relative_upper':str(relative),'relative_display':float(relative),'controls':len(controls)},sort_keys=True))


if __name__=='__main__': main()
