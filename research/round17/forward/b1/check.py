"""Run exact dense two-cube trial reconstruction and decisive spectral controls."""
import argparse,copy,csv,hashlib,json
from fractions import Fraction as F
from pathlib import Path
import trial,haar_graph

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args();source=Path(__file__).resolve().parent;out=Path(args.output).resolve()
    if out==source or source in out.parents:raise ValueError('output must be outside frozen source')
    out.mkdir(parents=True,exist_ok=True);checks=[]
    def check(name,ok):
        if not ok:raise RuntimeError(name)
        checks.append(name)
    def reject(name,fn):
        try:fn()
        except (ValueError,TypeError,KeyError):checks.append('reject: '+name);return
        raise RuntimeError('invalid accepted: '+name)
    g=trial.graph();inc=haar_graph.validate_graph(g)
    check('actual dense graph12V20E11F',(len(g['vertices']),len(g['edges']),len(g['faces']))==(12,20,11))
    check('dense supports violate sparse theorem premise',any(len(x)>1 for x in inc.values()))
    check('graph bipartite no odd cycles',all(sum(map(int,e['tail'].split(',')))%2!=sum(map(int,e['head'].split(',')))%2 for e in g['edges']))
    check('simple square attains girth4',all(len(set(f['vertices']))==4 for f in g['faces']))
    gram=[];insertions=[];repeated_cases=0
    for i in range(12):
        for j in range(12):
            value=trial.matrix_moment(i,j)
            if value!=int(i==j):raise RuntimeError('Gram identity fails')
            gram.append([i,j,str(value)])
            for f in range(11):
                value=trial.matrix_moment(i,j,f)
                expected=F(1,2) if (i==0 and j==f+1) or (j==0 and i==f+1) else F(0)
                if value!=expected:raise RuntimeError('individual magnetic insertion fails')
                insertions.append([i,j,f,str(value)])
                if i>0 and j>0 and (i==j or i==f+1 or j==f+1):repeated_cases+=1
    check('all144Gram entries reconstructed',len(gram)==144)
    check('all1584individual insertion entries reconstructed',len(insertions)==1584)
    check('repeated-index products explicitly evaluated',repeated_cases>0)
    fixtures=[]
    definitions=[('zero','1',['0']*11,48),('old_endpoint','1',['3/11']*11,48),('new_endpoint','1',['12/43']*11,48),
      ('negative','1',['-3/11']*11,48),('unequal_signed','1',['1/8','-1/4']+['0']*9,48),('scaled','2',['6/11']*11,48),('coarse_old_endpoint','1',['3/11']*11,0)]
    for name,alpha,ls,bits in definitions:
        c=trial.certify(alpha,ls,bits);check('certificate replay '+name,trial.verify(c));fixtures.append({'id':name,'certificate':c})
    cases={x['id']:x['certificate'] for x in fixtures};old=cases['old_endpoint'];new=cases['new_endpoint']
    check('zero Q has exact free gap',cases['zero']['gap_lower']=='3')
    check('old boundzero improvedlowerpositive',old['full_E1_lower']=='0' and F(old['gap_lower'])>0 and old['precision_status']=='target-met')
    check('new endpoint exactradical135/43',new['sqrt_bracket']==['135/43','135/43'])
    check('new endpoint remainszero insufficient',new['gap_lower']=='0' and new['sign_status']=='zero-insufficient')
    check('signed magnitudes same bound',cases['negative']['gap_bound_bracket']==old['gap_bound_bracket'])
    check('unequal coefficients avoid common shortcut',cases['unequal_signed']['common_exact_classification']=='not-common-magnitude')
    check('physical scaling radicand factorfour',F(cases['scaled']['radicand'])==4*F(old['radicand']))
    check('coarse bound does not passprecision',cases['coarse_old_endpoint']['precision_status']=='insufficient-width')
    # Exact retained false inference: the trial's second level is delta, but E1(full) is bounded separately.
    check('full E1 lower distinct from trial second level',old['full_E1_lower']!=old['delta'])
    for label,mut in [('trial gap substituted as full bound',lambda c:c.update(gap_lower=c['sqrt_bracket'][0])),
      ('wrong vacuum-face factor',lambda c:c['trial_H'][0].__setitem__(1,'-3/11')),
      ('sparse scope imported',lambda c:c.update(scope='link-disjoint product-ground theorem')),
      ('forged zero endpoint positive',lambda c:c.update(sign_status='positive'))]:
        c=copy.deepcopy(new if label=='forged zero endpoint positive' else old);mut(c);reject(label,lambda c=c:trial.verify(c))
    reject('Boolean cached matrix index',lambda:trial.matrix_moment(True,0,0))
    reject('Boolean radical precision',lambda:trial.certify('1',['0']*11,True))
    reject('zero alpha',lambda:trial.certify('0',['0']*11))
    reject('missing face coupling',lambda:trial.certify('1',['0']*10))
    reject('nonpositive requested width',lambda:trial.certify('1',['0']*11,48,'0'))
    ratios=['0','1/8','1/4','3/11','12/43','3/10'];rows=[]
    for r in ratios:
        c=trial.certify('1',[r]*11);rows.append({'r':r,'global_lower':str(3-11*F(r)),'improved_lower':c['gap_lower'],'improved_upper':c['gap_bound_bracket'][1],'classification':c['common_exact_classification']})
    evidence={'schema':'ym17-b1-evidence-v1','source_sha256':trial.SOURCE_SHA,'gram_entries':gram,'individual_insertions':insertions,'repeated_index_cases':repeated_cases,
      'fixtures':fixtures,'coupling_rows':rows,'finite_threshold':'12/43','dense_uniform_goal':'open','B2':'not executed'}
    (out/'evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
    with (out/'coupling.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    result={'schema':'ym17-b1-results-v1','status':'passed','checks_count':len(checks),'checks':checks,'source_sha256':trial.SOURCE_SHA,
      'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'evidence_sha256':hashlib.sha256((out/'evidence.json').read_bytes()).hexdigest(),
      'old_endpoint_lower_float':float(F(old['gap_lower'])),'old_endpoint_width':old['width'],'new_endpoint_lower':'0',
      'scope':'Finite dense physical graph bound from independent fullE1 lower plus trialE0 upper; sparse and dense-uniform claims excluded'}
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    (out/'manifest.json').write_text(json.dumps({'schema':'ym17-b1-output-manifest-v1','files':{x:hashlib.sha256((out/x).read_bytes()).hexdigest() for x in ['evidence.json','coupling.csv','results.json']}},indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
if __name__=='__main__':main()
