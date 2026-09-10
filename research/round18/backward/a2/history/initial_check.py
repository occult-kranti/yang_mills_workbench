"""Independent executed A2 gates. CLI writes only outside the source directory."""
from pathlib import Path
from fractions import Fraction as F
import argparse,copy,csv,hashlib,json
from geometry import build,validate,partition,cluster_count,weights_formula,weight,certify,schedule,coefficient_ledger,series


EXTRAS=[('negative_tau',4,'1','1','1/2','1/2','1/8','-1/64'),
 ('signed_clusters',5,'1','1','-1/2','1/2','-1/8','1/64'),
 ('zero_tau',4,'1','1','1/2','1/2','1/8','0'),
 ('zero_left',4,'1','1','0','1/2','1/8','1/64'),
 ('no_cluster_zero_parameters',3,'1','1','0','0','0','1/64'),
 ('zero_uniform_margin',4,'1','1','1/2','1/2','1/8','1/8'),
 ('beyond_uniform_margin',4,'1','1','1/2','1/2','1/8','1/4'),
 ('scaled_double',4,'2','1','1','1','1/4','1/64'),
 ('scaled_half',4,'1/2','1/4','1/4','1/4','1/16','1/64')]


def run(output):
    output=Path(output).resolve();source=Path(__file__).resolve().parent
    if output.is_relative_to(source):raise ValueError('output outside frozen source required')
    output.mkdir(parents=True,exist_ok=False);checks=[]
    def gate(name,ok):
        if type(ok) is not bool or not ok:raise ValueError(name)
        checks.append({'name':name,'passed':True})
    def reject(name,fn):
        try:fn()
        except (ValueError,TypeError):gate(name,True);return
        raise ValueError('invalid premise admitted: '+name)
    graphs={};certificates={};partitions={}
    for n in range(2,10):
        g=build(n);p=partition(n,g);c=certify(n,g=g);graphs[str(n)]=g;certificates[str(n)]=c;partitions[n]=p
        gate('all graph and partition identities for n='+str(n),c['counts']['clusters']==cluster_count(n) and len(p['used'])==10*cluster_count(n) and len(p['remaining'])==3*n*(n-1)**2-3*cluster_count(n))
    gate('every retained link carries an electric term',all(len(g['edges'])==3*int(n)**2*(int(n)-1) for n,g in graphs.items()))
    gate('actual remaining signed faces all have an unused Haar factor',all(tuple(r['unused_edge']) in {tuple(e) for e,_ in next(f['word'] for f in graphs[str(n)]['faces'] if f['face']==r['face'])} and tuple(r['unused_edge']) not in partitions[n]['used'] for n in partitions for r in partitions[n]['remaining']))
    cases={r['case'] for p in partitions.values() for r in p['remaining']}
    gate('all four analytic geometry cases occur including incomplete boundary',cases=={'unused z-link','unused odd y-interval','unused separating x-interval','unused incomplete boundary x-interval'})
    gate('closed finite weight formulas equal separately enumerated sums',all(sum((weight(tuple(r['face'])) for r in p['remaining']),F(0))==weights_formula(n)['remaining'] for n,p in partitions.items()))
    gate('positive orthant sum gives the all-volume bound exactly one',schedule('dyadic_orthant')==1 and all(0<F(c['weights']['remaining'])<1 for c in certificates.values()))
    gate('canonical common physical margin is 7 over 64',all(c['common_physical_lower']=='7/64' and c['uniform_two_norm_over_alpha']=='3/32' for c in certificates.values()))
    gate('all primary actual faces have nonzero coefficients',all(all(F(r['coefficient'])!=0 for r in coefficient_ledger(n)) and certificates[str(n)]['full_actual_face_support'] for n in range(2,10)))
    gate('small boxes have no artificial cluster but retain valid free reference',all(certificates[str(n)]['counts']['clusters']==0 and certificates[str(n)]['reference_actual_free_gap_if_no_clusters']=='3/4' and certificates[str(n)]['reference_conservative_lower']=='1/8' for n in (2,3)))
    extras={name:certify(n,a,amin,l,r,m,t) for name,n,a,amin,l,r,m,t in EXTRAS}
    gate('signs affect coefficients without changing norm-based margins',extras['negative_tau']['common_physical_lower']==extras['signed_clusters']['common_physical_lower']=='7/64')
    gate('zero tail is valid but loses actual full support',extras['zero_tau']['common_physical_lower']=='1/8' and extras['zero_tau']['full_actual_face_support'] is False)
    gate('zero cluster coefficient defeats full support only when that cluster exists',extras['zero_left']['full_actual_face_support'] is False and extras['no_cluster_zero_parameters']['full_actual_face_support'] is True)
    gate('zero uniform margin is insufficient despite positive finite estimate',extras['zero_uniform_margin']['uniform_status']=='zero-insufficient' and extras['zero_uniform_margin']['common_physical_lower']=='0' and F(extras['zero_uniform_margin']['finite_one_norm_lower'])>0)
    gate('negative uniform margin cannot be rescaled using a lower energy floor',extras['beyond_uniform_margin']['uniform_status']=='negative-insufficient' and extras['beyond_uniform_margin']['common_physical_lower'] is None)
    gate('two nonunit physical scales remain distinct from dimensionless parameters',extras['scaled_double']['uniform_lower_at_alpha']=='7/32' and extras['scaled_double']['common_physical_lower']=='7/64' and extras['scaled_half']['uniform_lower_at_alpha']=='7/128' and extras['scaled_half']['common_physical_lower']=='7/256')
    # The limit is explanatory only and is not a premise in certify().
    limit=1-F(7,96)/(1-F(1,16))/(1-F(1,4))*2
    overshoots=[n for n in range(2,10) if weights_formula(n)['remaining']>limit]
    gate('candidate remainder limit is not a safe finite-volume upper bound',limit==F(107,135) and bool(overshoots))
    reject('homogeneous nondecaying schedule rejected as summable',lambda:schedule('constant_nonzero'))
    reject('Boolean volume rejected',lambda:build(True))
    reject('unbounded graph materialization rejected before allocation',lambda:build(10**9))
    reject('Boolean coupling rejected',lambda:certify(4,tau=True))
    reject('false common scale rejected',lambda:certify(4,alpha_min='2'))
    reject('unsupported end strength rejected',lambda:certify(4,left='3/4'))
    reject('unsupported bridge strength rejected',lambda:certify(4,middle='1/4'))
    bad=copy.deepcopy(graphs['4']);bad['edges'].pop();reject('discarded electric link rejected',lambda:partition(4,bad))
    bad=copy.deepcopy(graphs['4']);bad['faces'][0]['word'][0][1]=True;reject('warm numeric Boolean sign alias rejected',lambda:partition(4,bad))
    bad=copy.deepcopy(graphs['4']);bad['faces'][0]['word'][0][1]=-1;reject('wrong actual face orientation rejected',lambda:partition(4,bad))
    result={'schema':'ym18-independent-a2-results-v1','status':'passed','checks_count':len(checks),'checks':checks,
      'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (source/'geometry.py',source/'check.py')},
      'primary_volumes':certificates,'extra_fixtures':extras,'uniform_primary_lower':'7/64','orthant_sum':'1',
      'candidate_limit':str(limit),'finite_limit_overshoots':overshoots,
      'scope':'All-volume inhomogeneous finite-box exception from analytic geometry and summable weights; no thermodynamic spectral limit or homogeneous dense Yang-Mills claim.'}
    for name,obj in [('results.json',result),('graphs.json',graphs),('unused_witnesses.json',{str(n):p['remaining'] for n,p in partitions.items()}),('coefficients.json',{str(n):coefficient_ledger(n) for n in range(2,10)})]:
        (output/name).write_text(json.dumps(obj,indent=2)+'\n')
    with (output/'volume.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['n','clusters','selected_faces','remaining_faces','total_weight','selected_weight','remaining_weight','finite_gap_lower','uniform_gap_lower'])
        for n,c in certificates.items():w.writerow([n,c['counts']['clusters'],c['counts']['selected_faces'],c['counts']['remaining_faces'],*c['weights'].values(),c['finite_one_norm_lower'],c['common_physical_lower']])
    print(json.dumps({'status':'passed','checks_count':len(checks),'uniform_primary_lower':'7/64','limit_overshoots':overshoots}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args();run(args.output)
