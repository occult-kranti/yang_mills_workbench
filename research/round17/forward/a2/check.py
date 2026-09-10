"""Check the sparse-support theorem's exact hypotheses and numerical constants."""
import argparse,copy,csv,hashlib,json
from fractions import Fraction as F
from pathlib import Path
import geometry,sparse

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    source=Path(__file__).resolve().parent;out=Path(args.output).resolve()
    if out==source or source in out.parents:raise ValueError('output must be outside frozen sources')
    out.mkdir(parents=True,exist_ok=True);checks=[]
    def check(name,ok):
        if not ok:raise RuntimeError(name)
        checks.append(name)
    def reject(name,fn):
        try:fn()
        except (ValueError,TypeError,KeyError):checks.append('reject: '+name);return
        raise RuntimeError('invalid theorem hypothesis accepted: '+name)
    fixtures=[];volume=[]
    for n in [2,3,4,6,8]:
        g=geometry.box(n);mask=sparse.even_mask(n);count=sparse.active_count(n)
        check('exact extensive mask count n'+str(n),len(mask)==count and len(set(mask))==count)
        c=sparse.certify(g,{p:'1/2' for p in mask});check('sparse replay n'+str(n),sparse.verify(g,c))
        check('full original link partition n'+str(n),c['covered_link_count']==len(g['edges']) and len(c['free_edges'])+4*count==len(g['edges']))
        check('uniform quarter lower n'+str(n),c['uniform_family_lower_bound']=='1/4' and c['ground_Gauss_inclusion_certified'])
        fixtures.append({'id':'even-mask-n'+str(n),'certificate':c})
        volume.append({'n':n,'active_plaquettes':count,'links':len(g['edges']),'free_links':len(c['free_edges']),
                       'alpha':'1','rho':'1/2','sparse_lower':'1/4','global_physical_norm_lower':str(3-F(count,2)),
                       'global_bound_status':'positive' if 3-F(count,2)>0 else 'insufficient'})
    check('global norm fails while sparse theorem stayspositive',any(F(x['global_physical_norm_lower'])<0 for x in volume))
    # Large n checks are algebraic/lazy, without allocating the graph.
    n=10**9
    check('arbitrary-size count no graph allocation',sparse.active_count(n)==n*(n//2)**2)
    check('lazy first anchor for large n',next(sparse.even_anchors(n))==(0,0,0))
    reject('unbudgeted materialized large mask',lambda:sparse.even_mask(n))
    g=geometry.box(3);p='01:0,0,0';corner='01:1,1,0';edge='01:1,0,0'
    vertex=sparse.certify(g,{p:'1/2',corner:'-1/2'})
    check('shared vertex is allowed',geometry.overlap(g,p,corner)['relation']=='shared-vertex-only' and vertex['active_count']==2)
    check('signed couplings same common bound',vertex['uniform_family_lower_bound']=='1/4')
    zero=sparse.certify(g,{p:'0',edge:'0'},rho='0')
    check('zero coefficients are free factors',zero['active_count']==0 and len(zero['free_edges'])==len(g['edges']) and zero['uniform_family_lower_bound']=='3/4')
    zerobridge=sparse.certify(g,{p:'1/2',edge:'0'})
    check('zero overlapping coefficient does not break sparse premise',zerobridge['active_count']==1)
    boundary=sparse.certify(g,{p:'3/4'},rho='3/4')
    check('boundary is insufficient not gapclosure',boundary['uniform_family_lower_bound']=='0' and boundary['status']=='insufficient-lower-bound' and not boundary['ground_uniqueness_certified'])
    scaled=sparse.certify(g,{p:'1'},alpha='2',alpha_min='2',rho='1/2')
    check('common energy scale multiplies lower',scaled['uniform_family_lower_bound']=='1/2')
    for name,c in [('shared_vertex_signed',vertex),('zero',zero),('zero_bridge',zerobridge),('rho_boundary',boundary),('scaled',scaled)]:
        check('special replay '+name,sparse.verify(g,c));fixtures.append({'id':name,'certificate':c})
    reject('first added nonzero shared-link bridge',lambda:sparse.certify(g,{p:'1/2',edge:'1/100'}))
    reject('rho misses actual coupling',lambda:sparse.certify(g,{p:'2/3'},rho='1/2'))
    reject('no common positive energy lower',lambda:sparse.certify(g,{p:'1/2'},alpha_min='0'))
    reject('Boolean extent',lambda:sparse.even_anchors(True))
    reject('Boolean coupling',lambda:sparse.certify(g,{p:True}))
    bad=copy.deepcopy(vertex);bad['scope']['Hilbert']='physical Hilbert factorizes into plaquette spaces'
    reject('forged physical-Hilbert factorization',lambda:sparse.verify(g,bad))
    bad=copy.deepcopy(boundary);bad['ground_uniqueness_certified']=True;bad['status']='certified-positive-sparse-gap'
    reject('forged boundary positivity',lambda:sparse.verify(g,bad))
    evidence={'schema':'ym17-a2-evidence-v1','source_sha256':sparse.SOURCE_SHA,'fixtures':fixtures,'volume':volume,
      'family_theorem':'Delta_physical>=alpha_min*(3/4-rho), link-disjoint nonzero supports, common rho<3/4, common alpha>=alpha_min>0',
      'dense_uniform_goal':'open','next_goals_B_C':'not executed; advisor must revise from A feedback'}
    (out/'evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
    with (out/'volume.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(volume[0]));w.writeheader();w.writerows(volume)
    result={'schema':'ym17-a2-results-v1','status':'passed','checks_count':len(checks),'checks':checks,
      'source_sha256':sparse.SOURCE_SHA,'geometry_source_sha256':sparse.GEOMETRY_SHA,'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'evidence_sha256':hashlib.sha256((out/'evidence.json').read_bytes()).hexdigest(),'uniform_example_lower':'1/4',
      'scope':'Volume-uniform sparse-support theorem at fixed physical energy scale; dense overlapping target open'}
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    (out/'manifest.json').write_text(json.dumps({'schema':'ym17-a2-output-manifest-v1','files':{f:hashlib.sha256((out/f).read_bytes()).hexdigest() for f in ['evidence.json','volume.csv','results.json']}},indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
if __name__=='__main__':main()
