"""Meaningful algebra, contract and certificate mutation tests; survives -O."""
import copy
import itertools
import json
from pathlib import Path
import moment_bounds as m

CHECKS=[]
def check(name,ok):
    if not ok:raise RuntimeError(name)
    CHECKS.append({'name':name,'passed':True})
def rejects(name,fn):
    try:fn()
    except (ValueError,ArithmeticError):check(name,True)
    else:check(name,False)

def determinant(a):
    n=len(a);value=m.F(0)
    for perm in itertools.permutations(range(n)):
        sign=(-1)**sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n));term=m.F(sign)
        for i,j in enumerate(perm):term*=a[i][j]
        value+=term
    return value

def main():
    for values in [(0,0,0),(0,1,0),(1,2,1),(1,1,1),(1,-1,1),(-1,0,1)]:
        a,b,c=map(m.F,values);M=[[a,b],[b,c]];v=m.negative_witness(M)
        psd=a>=0 and c>=0 and a*c>=b*b
        check('Independent 2x2 PSD criterion '+str(values),(v is None)==psd)
        if v is not None:check('Retained negative direction '+str(values),m.quadratic(M,v)<0)
    for entries in itertools.product((-1,0,1),repeat=6):
        a,b,c,d,e,f=map(m.F,entries);M=[[a,b,c],[b,d,e],[c,e,f]]
        minors=[M[i][i] for i in range(3)]+[M[i][i]*M[j][j]-M[i][j]**2 for i in range(3) for j in range(i+1,3)]+[determinant(M)]
        psd=all(x>=0 for x in minors);v=m.negative_witness(M)
        if (v is None)!=psd or v is not None and m.quadratic(M,v)>=0:raise RuntimeError('Three-by-three principal-minor reference mismatch: '+str(entries))
    check('All 729 symmetric ternary 3x3 matrices against all principal minors',True)
    for k in ('-5','-1/1000','1/1000','1','5','100'):
        c=m.certify(k,3,40);check('Exact interval replay '+k,m.verify(c))
        moments=m.affine(k,6)
        for n in range(5):
            for j in (0,1):
                previous=moments[n-1][j] if n else 0
                check('Affine recurrence '+str((k,n,j)),n*previous-(n+3)*moments[n+1][j]+m.F(k)*(moments[n][j]-moments[n+2][j])==0)
    zero=m.certify(0,3);check('Zero-coupling mean and variance exact',zero['mean_interval']==['0','0'] and zero['variance_interval']==['1/4','1/4'] and m.verify(zero))
    check('Haar moments',m.haar(2)==m.F(1,4) and m.haar(4)==m.F(1,8) and m.haar(5)==0)
    positive=m.certify(5,4,40);negative=m.certify(-5,4,40)
    check('Signed coupling exact interval symmetry',list(map(m.F,negative['mean_interval']))==[-m.F(x) for x in reversed(positive['mean_interval'])])
    check('Variance symmetry',positive['variance_interval']==negative['variance_interval'])
    for value in (True,1.0,float('nan'),'nan','1/0',None):rejects('Invalid rational '+repr(value),lambda v=value:m.rat(v))
    for args in [(1,True,40),(1,0,40),(1,7,40),(1,2,True),(1,2,0),(1,2,97),(101,2,40)]:rejects('Unsupported parameter '+str(args),lambda a=args:m.certify(*a))
    for M in ([],[[1,0],[1,1]],[[1,2]],[[True]]):rejects('Invalid matrix '+repr(M),lambda a=M:m.negative_witness(a))
    rejects('Zero division branch',lambda:m.affine(0,4))
    for field in ('schema','scope','source_sha256','status','kappa','level','bits','method','mean','variance','vector','slope','root','inner','slack','empty','extra'):
        c=copy.deepcopy(positive)
        if field in ('schema','scope','source_sha256','status','method'):c[field]='incorrect'
        elif field=='kappa':c[field]='6'
        elif field=='level':c[field]=3
        elif field=='bits':c[field]=41
        elif field=='mean':c['mean_interval'][0]='1'
        elif field=='variance':c['variance_interval']=['0','0']
        elif field=='vector':c['witnesses'][0]['vector'][0]='0'
        elif field=='slope':c['witnesses'][0]['slope']='0'
        elif field=='root':c['witnesses'][0]['root']='0'
        elif field=='inner':c['feasible_inner_points']=['-1','1']
        elif field=='slack':c['optimization_slack_per_side']='1'
        elif field=='empty':c['witnesses']=[]
        else:c['mass_gap_proved']=True
        rejects('Certificate mutation '+field,lambda c=c:m.verify(c))
    c=copy.deepcopy(zero);c['moments'][2]='0';rejects('Zero branch hidden variance',lambda:m.verify(c))
    report={'status':'passed','optimized':not __debug__,'count':len(CHECKS),'source_sha256':m.source_hash(),'checks':CHECKS}
    out=Path(__file__).parent/'output';out.mkdir(exist_ok=True);(out/('tests_optimized.json' if not __debug__ else 'tests.json')).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'passed','count':len(CHECKS),'optimized':not __debug__}))

if __name__=='__main__':main()
