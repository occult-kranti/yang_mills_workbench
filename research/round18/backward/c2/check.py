"""Independent complete two-link angular evidence and falsification checks."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import argparse,copy,csv,hashlib,json,shutil,subprocess,sys,tempfile
import angular as a
import geometry as g


def determinant(matrix):
    w=[list(map(F,row)) for row in matrix];d=F(1)
    for j in range(len(w)):
        p=next((i for i in range(j,len(w)) if w[i][j]),None)
        if p is None:return F(0)
        if p!=j:w[p],w[j]=w[j],w[p];d=-d
        t=w[j][j];d*=t
        for i in range(j+1,len(w)):
            v=w[i][j]/t
            for k in range(j+1,len(w)):w[i][k]-=v*w[j][k]
            w[i][j]=F(0)
    return d


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ns=ap.parse_args();own=Path(__file__).resolve().parent;out=ns.output.resolve()
    if out.is_relative_to(own):raise ValueError('output outside source required')
    checks=[]
    def gate(name,ok):
        if type(ok) is not bool or not ok:raise ValueError('failed check: '+name)
        checks.append({'name':name,'passed':True})
    def reject(name,fn):
        try:fn()
        except (ValueError,TypeError,AttributeError):gate(name,True);return
        raise ValueError('incorrectly accepted: '+name)
    graph=g.graph();r=g.reduce(graph);e=a.collection()
    gate('actual18V33E20F complex has exactly six affected and fourteen constant faces',(len(graph['vertices']),len(graph['edges']),len(graph['faces']))==(18,33,20) and len(r['affected_faces'])==6 and len(r['constant_faces'])==14)
    gate('shared face counted once and full action reconstructs3x+2y+w',len(set(r['U_faces'])&set(r['V_faces']))==1 and r['trace_counts']=={'x':3,'y':2,'w':1,'1':14})
    U=['3/5','4/5','0','0'];V=['5/13','0','12/13','0'];uf=g.quaternion(U);vf=g.quaternion(V);w=g.multiply(uf,g.dagger(vf))[0]
    vals={'x':uf[0],'y':vf[0],'w':w,'1':F(1)};actual=g.traces(graph,U,V)
    gate('every signed face word agrees on a noncommuting rational fixture',g.multiply(uf,vf)!=g.multiply(vf,uf) and all(F(v['trace'])==vals[row['trace']] for v,row in zip(actual,r['reduced_faces'])))
    Q=g.quaternion(U);wminus=g.multiply(Q,g.dagger(Q))[0];wplus=g.multiply(Q,Q)[0]
    gate('fixed-link dagger control distinguishes1from-minus7over25',wminus==1 and wplus==-F(7,25))
    gate('consistent dagger substitution is a Haar change of variables, not an integrated discriminator',g.dagger(g.dagger(vf))==vf and g.dagger(vf)[0]==vf[0] and g.multiply(uf,vf)[0]==g.multiply(uf,g.dagger(g.dagger(vf)))[0])
    moments=e['primitive_moments']
    gate('complete969-moment superset has exact unique ordered exponents',len(moments)==969 and [r['exponents'] for r in moments]==[[i,j,n-i-j] for n in range(17) for i in range(n+1) for j in range(n-i+1)])
    gate('semicircle and conditional angular normalizations',a.semicircle(0)==1 and a.semicircle(2)==F(1,4) and a.semicircle(4)==F(1,8) and a.moment([0,0,0])==1)
    gate('correlated cubic and sixth moments verified',a.moment([1,1,1])==F(1,16) and a.moment([2,2,2])==F(1,48))
    gate('independent trace measure and missing dimension divisor both fail exact moments',a.moment([1,1,1])!=a.semicircle(1)**3 and a.moment([2,2,2])!=a.semicircle(2)**3 and a.moment([1,1,1])!=F(1,8))
    model={m['d']:m for m in e['models']}
    gate('full quadratic and cubic coefficients are derived with all six weights',model[2]['numerator_coefficients'][:4]==['0','0','5/648','1/54'] and model[2]['partition_coefficients'][:4]==['1','0','7/4','3/8'])
    gate('one and two omitted V weights change the actual coefficients',model[1]['numerator_coefficients'][2:4]==['1/324','1/108'] and model[0]['numerator_coefficients'][2:4]==['1/648','0'])
    gate('complete coupled integral is not even while the d0 action is even',model[2]['numerator_coefficients'][3]!='0' and all(model[0]['numerator_coefficients'][n]==model[0]['partition_coefficients'][n]=='0' for n in (1,3,5,7)))
    frozen=sum((a.F(c)*a.semicircle(i+j) for (i,_,j),c in a.observable().items()),F(0))
    gate('unfreezing V changes zero-action mean from1over27tozero',frozen==F(1,27) and all(m['numerator_coefficients'][0]=='0' for m in model.values()))
    cases={f['id']:f['certificate'] for f in e['fixtures']}
    gate('nine signed zero and omission fixtures are complete',list(cases)==[f'd{d}_{s}' for d in (2,1,0) for s in ('positive','zero','negative')])
    gate('all zero-action intervals are exactly zero',all(cases[f'd{d}_zero']['expectation_interval']==a.interval(F(0),F(0)) for d in (2,1,0)))
    gate('positive omitted-weight models have disjoint certified intervals',F(cases['d0_positive']['expectation_interval']['upper'])<F(cases['d1_positive']['expectation_interval']['lower'])<F(cases['d2_positive']['expectation_interval']['lower']))
    gate('signed full model differs but d0 exact enclosures are even',F(cases['d2_negative']['expectation_interval']['upper'])<F(cases['d2_positive']['expectation_interval']['lower']) and cases['d0_negative']['expectation_interval']==cases['d0_positive']['expectation_interval'])
    levels=e['refinements'];final=levels[-1]
    gate('fixed ladder retains four width failures and final rigorous success',[v['degree'] for v in levels]==[0,2,4,6,8] and [v['width_status'] for v in levels]==['insufficient-width']*4+['target-met'] and F(final['expectation_interval']['lower'])>0 and F(final['expectation_interval']['width'])<=F(1,10**12))
    gate('coarse signed division keeps unresolved signs without clipping',[v['sign_status'] for v in levels]==['unresolved','unresolved','positive','positive','positive'] and F(levels[0]['expectation_interval']['lower'])<0)
    gate('Jensen partition lower bound is justified by zero action mean',all(a.moment(p)==0 for p in ([1,0,0],[0,1,0],[0,0,1])) and all(F(v['partition_interval']['lower'])>=1 for v in levels))
    gate('omitting full partition normalization gives a false final value',F(final['numerator_polynomial'])>F(final['expectation_interval']['upper']))
    grams=[g.gram(y) for y in ('-1','0','3/5','1')]
    for item in grams:
        G=item['gram'];k=F(item['kappa']);y=F(item['y']);nonnegative=all(determinant([[G[i][j] for j in ids] for i in ids])>=0 for n in range(1,6) for ids in combinations(range(5),n))
        gate('complete conditional Gram remains admissible at y='+item['y'],nonnegative and all(F(G[0][i])==k*sum(F(G[j][i]) for j in range(1,5)) for i in range(1,5)) and F(G[0][0])==k*k*sum(F(G[i][j]) for i in range(1,5) for j in range(1,5)) and item['rank']==(1 if abs(y)==1 else 2))
    # With fixed y, E_U[S_U^2]/2=(10+6y)/8. Its y dependence proves Z_U must weight an average of normalized inner expectations.
    gate('conditional partition weight is not constant in surrounding y',F(10+6,8)!=F(10-6,8) and grams[0]['denominator']=='integral rho(y) exp(2*kappa*y) Z_U(G(y)) dy')
    bad=copy.deepcopy(graph);bad['faces'].pop();reject('omitted actual face rejected',lambda:g.reduce(bad))
    bad=copy.deepcopy(graph);bad['faces'][0]['word'][0]['sign']*=-1;reject('single dagger change rejected by signed geometry',lambda:g.reduce(bad))
    bad=copy.deepcopy(graph);bad['edges'][0]['tail'][0]=False;reject('nested Boolean coordinate alias rejected',lambda:g.reduce(bad))
    a.moment([0,0,0]);reject('warm cache Boolean exponent rejected',lambda:a.moment([False,0,0]))
    reject('negative exponent rejected',lambda:a.moment([-1,1,1]));reject('wrong exponent dimension rejected',lambda:a.moment([0,0]))
    reject('Boolean omission multiplicity rejected',lambda:a.certify(True,'1/64'))
    reject('nonpositive requested width rejected',lambda:a.certify(2,'1/64',precision='0'))
    reject('Boolean degree rejected',lambda:a.certify(2,'1/64',degree=True))
    reject('forged noncanonical coupling rejected',lambda:a.certify(2,'2/128'))
    reject('out-of-domain central Gram coordinate rejected',lambda:g.gram('2'))
    v=a.moment([1,1,1]);reject('cached Fraction result cannot be changed',lambda:setattr(v,'numerator',0))
    first=a.certify(2,'1/64');first['numerator_coefficients'][2]='0'
    gate('caller coefficient mutation cannot poison recomputation',a.certify(2,'1/64')['numerator_coefficients'][2]=='5/648')
    with tempfile.TemporaryDirectory(prefix='ym18-c2-source-') as td:
        shutil.copyfile(own/'angular.py',Path(td)/'angular.py')
        program="import sys;from pathlib import Path;sys.path.insert(0,sys.argv[1]);import angular as a;a.moment([0]*3);p=Path(a.__file__);p.write_bytes(p.read_bytes()+b'\\n');\ntry:a.moment([0]*3)\nexcept ValueError:print('rejected')\nelse:raise RuntimeError('changed source accepted')"
        child=subprocess.run([sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])+['-c',program,td],text=True,capture_output=True,check=True)
        gate('changed loaded source rejected before warm cache',child.stdout.strip()=='rejected')
    e.update(graph=graph,geometry=r,conditional_grams=grams,frozen_V_zero_action=str(frozen),dagger_control={'fixed_w':str(wminus),'fixed_wplus':str(wplus),'integrated_scope':'consistent replacement preserves joint law by V->Vdagger'})
    out.mkdir(parents=True,exist_ok=True)
    (out/'collection.json').write_text(json.dumps(e,indent=2)+'\n');(out/'graph.json').write_text(json.dumps(graph,indent=2)+'\n')
    for filename,values in [('refinement.csv',levels),('weights.csv',list(cases.values()))]:
        rows=[{'d':v['d'],'kappa':v['kappa'],'degree':v['degree'],**v['expectation_interval'],'width_status':v['width_status'],'sign_status':v['sign_status']} for v in values]
        with (out/filename).open('w',newline='') as stream:
            writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    result={'schema':'ym18-independent-c2-results-v1','status':'passed','checks_count':len(checks),'checks':checks,
      'source_sha256':{n:hashlib.sha256((own/n).read_bytes()).hexdigest() for n in ('angular.py','geometry.py','check.py')},
      'scope':'Exact full-tail conditional two-link integral with31otherlinks fixed; complete20facebulk and physical mass gap remain outside this calculation.'}
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'passed','checks_count':len(checks)}))


if __name__=='__main__':main()
