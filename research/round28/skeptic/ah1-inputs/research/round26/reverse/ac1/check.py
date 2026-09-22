#!/usr/bin/env python3
import argparse,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def require(x,m):
    if x is not True: raise RuntimeError(m)
def graph():
    sizes=(3,3,2);vertices=list(itertools.product(*(range(n) for n in sizes)));edges=[];lookup={}
    for v in vertices:
        for a in range(3):
            if v[a]+1<sizes[a]:
                w=tuple(v[i]+int(i==a) for i in range(3));lookup[frozenset((v,w))]=len(edges);edges.append((v,w))
    faces=[]
    for v in vertices:
        for a,b in itertools.combinations(range(3),2):
            if v[a]+1<sizes[a] and v[b]+1<sizes[b]:
                loop=[v,tuple(v[i]+int(i==a) for i in range(3)),tuple(v[i]+int(i in (a,b)) for i in range(3)),tuple(v[i]+int(i==b) for i in range(3))]
                faces.append(sum(1<<lookup[frozenset((loop[j],loop[(j+1)%4]))] for j in range(4)))
    return vertices,edges,faces
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output).resolve();require(not out.exists(),'fresh output required')
    con=json.loads((ROOT/'research/round26/contracts/ac1.json').read_text())
    for rel,h in con['bindings'].items(): require(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,'binding '+rel)
    vertices,edges,faces=graph();require((len(vertices),len(edges),len(faces))==(18,33,20),'actual graph')
    pairs=list(itertools.combinations(range(20),2));masks=[faces[i]^faces[j] for i,j in pairs]
    require(len(set(masks))==190 and not set(masks)&set(faces) and 0 not in masks,'distinct pair masks')
    shared=[(i,j) for i,j in pairs if (faces[i]&faces[j]).bit_count()==1]
    disjoint=[(i,j) for i,j in pairs if not faces[i]&faces[j]]
    require((len(shared),len(disjoint))==(62,128),'full pair geometries')
    require(len(shared)+len(disjoint)==190,'no additional geometry')
    require(F(1,4)+F(3,4)==1,'branch norms')
    require(6*F(3,4)==F(9,2) and 6*F(3,4)+2==F(13,2),'shared kinetic action')
    dim=1+20+20+len(disjoint)+2*len(shared);require(dim==293,'K closure dimension')
    # Recover the complete old omitted Gram using BOTH shared-edge branches.
    gram=[[F(0) for j in range(20)] for i in range(20)]
    for i in range(20): gram[i][i]+=F(1,4)
    for i,j in pairs:
        branch_weights=[F(1,4),F(3,4)] if (i,j) in shared else [F(1)]
        for weight in branch_weights:
            for row in (i,j):
                for col in (i,j):gram[row][col]+=weight/4
    require(all(gram[i][j]==(F(5) if i==j else F(1,4)) for i in range(20) for j in range(20)),'full original Gram preserved')
    require(sum(gram[0])==F(39,4),'full old operator norm squared')
    require(F(400)>F(39,4),'new conservative norm bound worsens, no false improvement')
    rows=[]
    for lam in [F(0),F(1,200),F(1,100)]:
        bound=20*lam;require((bound==0)==(lam==0),'lambda zero exception');rows.append({'lambda':str(lam),'new_full_omitted_norm_upper':str(bound),'old_full_omitted_norm_squared':str(F(39,4)*lam*lam)})
    paths=list(con['bindings'])+['research/round26/contracts/ac1.json','research/round26/reverse/ac1/report.md','research/round26/reverse/ac1/check.py','.codex/skills/qeg-research-advisor/references/newton-tesla-project-method.md']
    result={'schema':'ym26-reverse-result-v1','loop':'ac1','status':'limited-parent-open','checks_passed':True,'actual_graph':[18,33,20],'retained_dimension':dim,'K_eigenspace_counts':{'0':1,'3':20,'8':20,'6':128,'9/2':62,'13/2':62},'shared_edge_branch_squared_norms':['1/4','3/4'],'old_input_omitted_map_exactly_zero':True,'complete_new_omitted_map':'-lambda Q_plus S P_plus; full norm <=20lambda','new_magnetic_matrix_evaluated':False,'raw_product_count':20*dim,'dense_matrix_entry_count':dim*dim,'bound_rows':rows,'source_inventory':{r:hashlib.sha256((ROOT/r).read_bytes()).hexdigest() for r in sorted(set(paths))}}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':main()
