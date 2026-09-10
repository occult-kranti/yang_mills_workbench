"""Bounded independent coordinate and admissibility audit for Round18 C1."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial
import argparse,copy,hashlib,json,shutil,subprocess,sys,tempfile
import coordinates as c


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ns=ap.parse_args()
    own=Path(__file__).resolve().parent;out=ns.output.resolve()
    if out.is_relative_to(own):raise ValueError('outputs must remain outside source')
    checks=[]
    def gate(name,ok):
        if type(ok) is not bool or not ok:raise ValueError('failed check: '+name)
        checks.append({'name':name,'passed':True})
    def rejects(name,fn):
        try:fn()
        except (ValueError,TypeError):gate(name,True);return
        raise ValueError('incorrect acceptance: '+name)
    evidence=c.collection();items={x['id']:x['data'] for x in evidence['fixtures']}
    gate('all eleven independent actual-coordinate fixtures reconstructed',len(items)==11 and len(evidence['fixtures'])==11)
    gate('sphere normalization, parity, variance and fourth moments',c.sphere([0]*4)==1 and c.sphere([1,0,0,0])==0 and c.sphere([2,0,0,0])==F(1,4) and c.sphere([4,0,0,0])==F(1,8) and c.sphere([2,2,0,0])==F(1,24))
    for name,d in items.items():
        rows=d['primitive_moments'];A=[];Z=[]
        for n in range(7):
            group=rows[16*n:16*(n+1)]
            A.append(str(sum((F(4**r['subset_mask'].bit_count()*(-1)**(4-r['subset_mask'].bit_count()),81)*F(r['moment']) for r in group),F(0))/factorial(n)))
            Z.append(str(F(group[0]['moment'])/factorial(n)))
        gate('112 primitives reconstruct direct observable polynomial: '+name,len(rows)==112 and A==d['numerator_coefficients'] and Z==d['partition_coefficients'])
    for base in ('tetra','commuting'):
        a=items[base+'_common']
        gate('complete common rotation and reflection invariance: '+base,all(items[base+s]['joint_Gram']==a['joint_Gram'] and items[base+s]['numerator_coefficients']==a['numerator_coefficients'] and items[base+s]['partition_coefficients']==a['partition_coefficients'] for s in ('_hadamard','_reflected')))
    t,h=items['tetra_common'],items['commuting_common']
    gate('equal action and partition do not determine the joint observable',t['b']==h['b'] and t['partition_coefficients']==h['partition_coefficients'] and t['joint_Gram']!=h['joint_Gram'] and F(t['numerator_coefficients'][0])==-F(1,405) and F(h['numerator_coefficients'][0])==F(13,1215))
    gate('rank deficient one and two dimensional spans accepted',items['rank1_equal']['admissibility']['rank']==1 and items['rank2']['admissibility']['rank']==2 and h['admissibility']['rank']==2)
    gate('zero action with zero and nonzero coefficients remains valid',all(items[n]['b']==['0']*4 and items[n]['numerator_coefficients'][1:]==['0']*6 and items[n]['partition_coefficients']==['1']+['0']*6 for n in ('tetra_zero_kappa','commuting_zero_b_nonzero_kappa')))
    gate('all central odd coefficients vanish and factorial normalization holds',all(all(d['numerator_coefficients'][n]=='0' and d['partition_coefficients'][n]=='0' for n in (1,3,5)) and F(d['partition_coefficients'][2])==sum((F(x)**2 for x in d['b']),F(0))/8 for d in items.values()))
    Gbad=[['0']*5 for _ in range(5)]
    for i in range(1,5):Gbad[i][i]='1'
    Gbad[1][2]=Gbad[2][1]='2'
    gate('leading-minor-only method has a concrete false admissibility case',all(c.determinant([[F(Gbad[i][j]) for j in range(n)] for i in range(n)])==0 for n in range(1,6)) and c.determinant([[F(Gbad[i][j]) for j in (1,2)] for i in (1,2)])==-3)
    rejects('non-PSD Gram rejected despite zero leading minors',lambda:c.validate_gram(Gbad,['0']*4))
    rejects('rank five ambient mismatch rejected',lambda:c.validate_gram([[str(int(i==j)) for j in range(5)] for i in range(5)],['0']*4))
    G=copy.deepcopy(h['joint_Gram']);G[0][0]=str(F(G[0][0])+1)
    rejects('PSD rank three Gram with forged action norm rejected',lambda:c.validate_gram(G,h['kappa']))
    G=copy.deepcopy(h['joint_Gram']);G[0][0]=str(4*F(G[0][0]))
    for i in range(1,5):G[0][i]=G[i][0]=str(2*F(G[0][i]))
    rejects('realizable Gram with undeclared doubled action rejected',lambda:c.validate_gram(G,h['kappa']))
    G=copy.deepcopy(h['joint_Gram']);G[1][1]='2'
    rejects('wrong unit direction rejected',lambda:c.validate_gram(G,h['kappa']))
    G=copy.deepcopy(h['joint_Gram']);G[0][1]='0'
    rejects('asymmetric Gram rejected',lambda:c.validate_gram(G,h['kappa']))
    G=copy.deepcopy(h['joint_Gram']);G[1][1]=True
    rejects('nested Boolean Gram value rejected before arithmetic',lambda:c.validate_gram(G,h['kappa']))
    rejects('noncanonical rational rejected',lambda:c.validate_gram(h['joint_Gram'],['2/32']*4))
    rejects('wrong matrix dimension rejected',lambda:c.validate_gram(h['joint_Gram'][:-1],h['kappa']))
    c.sphere([0]*4);c.coordinate_moment(t['vectors'],[0]*5)
    rejects('warm sphere cache cannot alias Boolean exponents',lambda:c.sphere([False,0,0,0]))
    rejects('warm coordinate cache cannot alias Boolean exponents',lambda:c.coordinate_moment(t['vectors'],[False,0,0,0,0]))
    rejects('negative exponent rejected',lambda:c.coordinate_moment(t['vectors'],[-1,0,0,0,0]))
    rejects('wrong moment dimension rejected',lambda:c.coordinate_moment(t['vectors'],[0]*4))
    v=copy.deepcopy(t['vectors']);v[1][0]=True
    rejects('warm coordinate cache cannot alias nested Boolean vector',lambda:c.coordinate_moment(v,[0]*5))
    result=c.coordinate_moment(t['vectors'],[0]*5)
    rejects('cached exact moment is immutable',lambda:setattr(result,'numerator',0))
    changed=copy.deepcopy(evidence);changed['fixtures'][0]['data']['numerator_coefficients'][0]='0'
    gate('caller mutation cannot corrupt later coefficient construction',c.collection()['fixtures'][0]['data']['numerator_coefficients'][0]=='-1/405')
    rejects('changed coefficient evidence rejected',lambda:c.verify(changed))
    changed=copy.deepcopy(evidence);changed['degree']=True
    rejects('Boolean degree metadata rejected',lambda:c.verify(changed))
    changed=copy.deepcopy(evidence);changed['fixtures'].pop()
    rejects('omitted fixture rejected',lambda:c.verify(changed))
    changed=copy.deepcopy(evidence);changed['schema']='passed'
    rejects('forged external pass schema rejected',lambda:c.verify(changed))
    with tempfile.TemporaryDirectory(prefix='ym18-c1-source-') as td:
        dest=Path(td)/'coordinates.py';shutil.copyfile(own/'coordinates.py',dest)
        program="import sys;from pathlib import Path;sys.path.insert(0,sys.argv[1]);import coordinates as c;p=Path(c.__file__);p.write_bytes(p.read_bytes()+b'\\n# mutation\\n');\ntry:c.sphere([0]*4)\nexcept ValueError:print('rejected')\nelse:raise RuntimeError('changed source admitted')"
        child=subprocess.run([sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])+['-c',program,td],capture_output=True,text=True,check=True)
        gate('changed loaded coordinate source rejected',child.stdout.strip()=='rejected')
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    results={'schema':'ym18-independent-c1-results-v1','status':'passed','checks_count':len(checks),'checks':checks,
      'source_sha256':{n:sha(own/n) for n in ('coordinates.py','check.py')},'scope':evidence['scope']}
    out.mkdir(parents=True,exist_ok=True)
    for n,v in [('collection.json',evidence),('results.json',results)]:(out/n).write_text(json.dumps(v,indent=2)+'\n')
    print(json.dumps({'status':'passed','checks_count':len(checks)}))


if __name__=='__main__':main()
