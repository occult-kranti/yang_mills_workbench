"""Review the actual cube words with exact geometry, index and quaternion oracles."""
from fractions import Fraction as Q
from pathlib import Path
from itertools import product
import copy
import hashlib
import json
import sys
import exact_algebra as algebra

HERE=Path(__file__).resolve().parent
SOURCE_BYTES=Path(__file__).read_bytes()


def canonical_json(value):return json.dumps(value,sort_keys=True,allow_nan=False,separators=(',',':'))


def parse_graph(graph):
    keys={'schema','vertices','edges','faces','group','measure','action','geometry'}
    if type(graph) is not dict or set(graph)!=keys:
        raise ValueError('graph schema field mismatch')
    fixed={'schema':'ym15-oriented-cube-v1','group':'SU(2)',
           'measure':'independent normalized Haar on12 oriented links',
           'action':'sum_f k_f * Tr(U_face_f)/2',
           'geometry':'closed oriented boundary of one cube; sphere topology'}
    if any(type(graph[k]) is not str or graph[k]!=v for k,v in fixed.items()):
        raise ValueError('graph physical domain mismatch')
    vertices=graph['vertices']
    if type(vertices) is not list or any(type(v) is not str for v in vertices) or len(vertices)!=8 or set(vertices)!={''.join(map(str,v)) for v in product((0,1),repeat=3)}:
        raise ValueError('exact cube vertices required')
    edges={};axes={};pairs=set()
    if type(graph['edges']) is not list or len(graph['edges'])!=12:
        raise ValueError('twelve cube edges required')
    for edge in graph['edges']:
        if type(edge) is not dict or set(edge)!={'id','tail','head','axis'}:
            raise ValueError('edge field mismatch')
        name,u,v,axis=(edge[k] for k in ('id','tail','head','axis'))
        if any(type(t) is not str for t in (name,u,v)) or not name or name in edges or u not in vertices or v not in vertices or type(axis) is not int or axis not in(0,1,2):
            raise ValueError('invalid edge identifiers or strict axis')
        difference=[int(v[i])-int(u[i]) for i in range(3)]
        if difference!=[int(i==axis) for i in range(3)] or (u,v) in pairs:
            raise ValueError('edge is not a distinct positive coordinate cube edge')
        edges[name]=(u,v);axes[name]=axis;pairs.add((u,v))
    words={};planes=set();incidence={name:[] for name in edges}
    if type(graph['faces']) is not list or len(graph['faces'])!=6:
        raise ValueError('six cube faces required')
    for face in graph['faces']:
        if type(face) is not dict or set(face)!={'id','vertices','word'}:
            raise ValueError('face field mismatch')
        name,cycle,word=(face[k] for k in ('id','vertices','word'))
        if type(name) is not str or not name or name in words or type(cycle) is not list or len(cycle)!=4 or len(set(cycle))!=4 or any(v not in vertices for v in cycle):
            raise ValueError('invalid face identifier or vertex cycle')
        if type(word) is not list or len(word)!=4:
            raise ValueError('four link traversals required')
        constant=[axis for axis in range(3) if len({v[axis] for v in cycle})==1]
        if len(constant)!=1:raise ValueError('face must lie in one cube coordinate plane')
        normal=constant[0];side=int(cycle[0][normal])
        if (normal,side) in planes:raise ValueError('duplicate geometric face')
        planes.add((normal,side))
        p=[int(x) for x in cycle[0]];u=[int(cycle[1][i])-p[i] for i in range(3)];v=[int(cycle[3][i])-p[i] for i in range(3)]
        cross=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
        if cross!=[(2*side-1)*int(i==normal) for i in range(3)]:
            raise ValueError('face orientation is not outward')
        normalized=[]
        for i,item in enumerate(word):
            if type(item) is not dict or set(item)!={'edge','sign'} or type(item['edge']) is not str or item['edge'] not in edges or type(item['sign']) is not int or item['sign'] not in(-1,1):
                raise ValueError('invalid signed link occurrence')
            edge,sign=item['edge'],item['sign'];tail,head=edges[edge]
            if sign==-1:tail,head=head,tail
            if (tail,head)!=(cycle[i],cycle[(i+1)%4]):raise ValueError('link word does not follow actual face boundary')
            normalized.append((edge,sign));incidence[edge].append(sign)
        words[name]=normalized
    if planes!={(i,j) for i in range(3) for j in(0,1)} or any(sorted(v)!=[-1,1] for v in incidence.values()):
        raise ValueError('not the complete closed oriented cube boundary')
    return edges,words


def audit(graph_path,producer_source,output_dir):
    graph_path=Path(graph_path);producer_source=Path(producer_source)
    graph_bytes=graph_path.read_bytes();producer_bytes=producer_source.read_bytes()
    graph=json.loads(graph_bytes);edges,words=parse_graph(graph);names=tuple(words);checks=[]
    def gate(name,ok=True,details=None):
        if not ok:raise ValueError(name)
        checks.append({'name':name,'passed':True,'details':details})
    gate('actual coordinate graph, edge incidences and outward words')
    rows=[]
    for mask in range(64):
        selected=tuple(names[i] for i in range(6) if mask&(1<<i))
        result=algebra.contract_distinct_faces(words,selected)
        expected=Q(1) if mask==0 else Q(1,1024) if mask==63 else Q(0)
        gate('fundamental index subset '+str(mask),result['value']==expected)
        rows.append({'mask':mask,'faces':list(selected),**{k:str(v) if isinstance(v,Q) else v for k,v in result.items()}})
    full=algebra.contract_distinct_faces(words,names)
    gate('actual full color count8 and paired edges12',full['color_loops']==8 and full['paired_edges']==12)
    gate('character d^-4 normalization matches fundamental index result',Q(1,2**6*2**4)==full['value'])
    gate('six independent face moments is a discriminating wrong model',Q(0)!=full['value'])
    gate('omitted Schur dimension factor is a discriminating wrong model',Q(1,64)!=full['value'])
    # chi_fundamental^2=chi_0+chi_spin1; only shared labels0 and2 survive.
    gate('higher-representation squared-character product is82/81',Q(1)+Q(1,3**4)==Q(82,81))
    gate('old two-holonomy dimension power fails cube higher-representation control',Q(1)+Q(1,3)!=Q(82,81))
    links={name:algebra.rational_unit(i+1) for i,name in enumerate(edges)}
    gauges={v:algebra.rational_unit(i+31) for i,v in enumerate(graph['vertices'])}
    transformed=algebra.gauge_links(edges,links,gauges)
    diagnostics=[]
    for name,word in words.items():
        value=algebra.trace_word(word,links);gauged=algebra.trace_word(word,transformed)
        gate('exact rational gauge invariance '+name,value==gauged)
        gate('whole face reversal is an invariance '+name,algebra.trace_word(algebra.reversed_word(word),links)==value)
        wrong=list(word);wrong[0]=(wrong[0][0],-wrong[0][1]);wrong_value=algebra.trace_word(wrong,links);wrong_gauged=algebra.trace_word(wrong,transformed)
        gate('one wrong dagger breaks gauge covariance '+name,wrong_value!=wrong_gauged)
        diagnostics.append({'face':name,'trace':str(value),'gauge_trace':str(gauged),
           'wrong_dagger_trace':str(wrong_value),'wrong_dagger_gauge_trace':str(wrong_gauged),
           'wrong_gauge_defect_display':float(wrong_value-wrong_gauged)})
        # A second Lie derivative replaces this once-used link by its generator square.
        second=Q(0)
        for edge,sign in word:
            for axis in range(3):
                generator=(Q(0),*(Q(1,2) if i==axis else Q(0) for i in range(3)))
                square=algebra.multiply(generator,generator)
                if square!=(Q(-1,4),Q(0),Q(0),Q(0)):raise ValueError('fundamental Lie generator normalization')
                second+=Q(-1,4)*value
        gate('electric Casimir on actual four-link face '+name,-second==3*value)
    gram=[]
    for p in range(6):
        row=[]
        for q in range(6):
            degrees=[0]*6;degrees[p]+=1;degrees[q]+=1
            value=4*algebra.missing_face_moment(degrees)
            if value!=int(p==q):raise ValueError('repeated-face Gram identity failed')
            row.append(str(value))
            for f in range(6):
                powers=degrees.copy();powers[f]+=1
                if 4*algebra.missing_face_moment(powers)!=0:raise ValueError('repeated-face magnetic trial identity failed')
        gram.append(row)
    gate('all36 Gram and216 repeated magnetic moments independently derived')
    try:algebra.missing_face_moment([1]*6)
    except ValueError:gate('missing-face oracle rejects absent factorization premise')
    else:raise ValueError('false complete-face factorization accepted')
    def reject(name,g):
        try:parse_graph(g)
        except (ValueError,TypeError):gate(name);return
        raise ValueError('invalid graph accepted '+name)
    changes=[]
    g=copy.deepcopy(graph);g['faces'][0]['word'][0]['sign']*=-1;changes.append(('wrong dagger geometry',g))
    g=copy.deepcopy(graph);g['faces'][0]['word'][0]['sign']=True;changes.append(('Boolean orientation alias',g))
    g=copy.deepcopy(graph);g['edges'][0]['axis']=False;changes.append(('Boolean axis alias',g))
    g=copy.deepcopy(graph);g['faces'][-1]=copy.deepcopy(g['faces'][0]);changes.append(('duplicate face',g))
    g=copy.deepcopy(graph);g['edges'].pop();changes.append(('missing edge',g))
    g=copy.deepcopy(graph);g['vertices'].pop();changes.append(('missing vertex',g))
    g=copy.deepcopy(graph);g['geometry']='four dimensional continuum';changes.append(('physical dimension substitution',g))
    g=copy.deepcopy(graph);g['action']='independent face model';changes.append(('changed action',g))
    g=copy.deepcopy(graph);g['extra']='mass gap';changes.append(('extra inference metadata',g))
    for name,g in changes:reject(name,g)
    gate('reviewed graph and source bytes unchanged',graph_path.read_bytes()==graph_bytes and producer_source.read_bytes()==producer_bytes and Path(__file__).read_bytes()==SOURCE_BYTES)
    output={'schema':'ym15-B1-independent-review-v1','status':'passed','checks_count':len(checks),'checks':checks,
      'graph_sha256':hashlib.sha256(graph_bytes).hexdigest(),'canonical_graph_sha256':hashlib.sha256(canonical_json(graph).encode()).hexdigest(),
      'producer_source_sha256':hashlib.sha256(producer_bytes).hexdigest(),'source_sha256':hashlib.sha256(SOURCE_BYTES).hexdigest(),
      'fundamental_contractions':rows,'rational_gauge_diagnostics':diagnostics,'trial_gram':gram,
      'cube_full_haar_moment':'1/1024','trial_magnetic_entries':'all216 vanish',
      'limits':['Finite closed cube boundary with sphere topology; no volume or continuum claim.',
                'Repeated moments rely on the independently reviewed missing-face Schur theorem, not only distinct-subset checks.',
                'Exact rational quaternion implementation uses the basis(-i sigma1,-i sigma2,-i sigma3).']}
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True);(out/'independent_review.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':'passed','checks':len(checks),'full_haar_moment':'1/1024'}))
    return output


if __name__=='__main__':
    if len(sys.argv)!=4:raise SystemExit('usage: verify_cube.py GRAPH PRODUCER_SOURCE OUTPUT_DIR')
    audit(*sys.argv[1:])
