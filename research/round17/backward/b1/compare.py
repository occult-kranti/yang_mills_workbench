"""Independent forward table comparison with exact-square bracket admission."""
from pathlib import Path
from fractions import Fraction as F
import argparse,copy,hashlib,json
from check import geometry,trial_entries,bound


SCOPE='Untruncated physical dense two-cube operator; separate E1 lower and trial E0 upper; bracket encloses sufficient lower-bound formula, not actual gap; sparse theorem inapplicable'


def strict(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(strict(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(strict(x,y) for x,y in zip(a,b))
    return a==b


def convert(g):
    vertices=[list(map(int,v.split(','))) for v in g['vertices']];emap={e['id']:i for i,e in enumerate(g['edges'])}
    edges=[{'id':i,'tail':list(map(int,e['tail'].split(','))),'head':list(map(int,e['head'].split(',')))} for i,e in enumerate(g['edges'])];faces=[]
    for i,f in enumerate(g['faces']):
        vs=[list(map(int,v.split(','))) for v in f['vertices']];spans=[max(v[a] for v in vs)-min(v[a] for v in vs) for a in range(3)]
        faces.append({'id':i,'axes':[a for a in range(3) if spans[a]],'base':[min(v[a] for v in vs) for a in range(3)],'vertices':vs,'word':[[emap[t['edge']],t['sign']] for t in f['word']]})
    return {'schema':'ym17-independent-dense-two-cube-v1','vertices':vertices,'edges':edges,'faces':faces}


def main(source,evidence,output):
    source,evidence,output=map(Path,(source,evidence,output));output=output.resolve()
    if output.is_relative_to(Path(__file__).resolve().parent):raise ValueError('output outside source required')
    output.mkdir(parents=True,exist_ok=False);h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();r=json.loads((evidence/'evidence.json').read_text());fg=json.loads((source/'graph.json').read_text());g=convert(fg);inc,girth=geometry(g);gram,mag=trial_entries(g);checks=[]
    def check(name,ok):
        if not ok:raise RuntimeError(name)
        checks.append({'name':name,'passed':True})
    check('actual source graph independently converted with girth four',girth==4 and r['source_sha256']==h(source/'trial.py'))
    check('all 144 saved Gram entries independently reconstructed',r['gram_entries']==[[i,j,str(gram[i][j])] for i in range(12) for j in range(12)])
    check('all 1584 saved insertions independently reconstructed',r['individual_insertions']==[[i,j,f,str(mag[f][i][j])] for i in range(12) for j in range(12) for f in range(11)])
    definitions=[('zero','1',['0']*11,48),('old_endpoint','1',['3/11']*11,48),('new_endpoint','1',['12/43']*11,48),('negative','1',['-3/11']*11,48),('unequal_signed','1',['1/8','-1/4']+['0']*9,48),('scaled','2',['6/11']*11,48),('coarse_old_endpoint','1',['3/11']*11,0)]
    check('complete seven-fixture parameter inventory',[(f['id'],f['certificate']['alpha'],f['certificate']['coefficients'],f['certificate']['bits']) for f in r['fixtures']]==definitions)
    def verify(c):
        a=F(c['alpha']);ls=list(map(F,c['coefficients']));bits=c['bits'];tol=F(c['precision'])
        if a<=0 or len(ls)!=11 or type(bits) is not int or not 0<=bits<=512 or tol<=0:raise ValueError('invalid physical parameters')
        d=3*a;L=sum(map(abs,ls));Q=sum(x*x for x in ls);q=d*d+Q;lo,hi=map(F,c['sqrt_bracket'])
        if not 0<=lo<=hi or lo*lo>q or hi*hi<q:raise ValueError('invalid exact-square enclosure')
        if lo!=hi and (hi-lo!=F(1,2**bits) or (lo*2**bits).denominator!=1):raise ValueError('incorrect dyadic width or grid')
        ours=bound(a,c['coefficients']);ilo,ihi=map(F,(ours['sqrt']['lower'],ours['sqrt']['upper']))
        if max(lo,ilo)>min(hi,ihi):raise ValueError('independent Newton enclosure disjoint')
        E=[[d*gram[i][j] if j else F(0) for j in range(12)] for i in range(12)]
        V=[[-sum(ls[f]*mag[f][i][j] for f in range(11)) for j in range(12)] for i in range(12)];H=[[E[i][j]+V[i][j] for j in range(12)] for i in range(12)]
        matrix=lambda M:[[str(x) for x in row] for row in M];e0=((d-hi)/2,(d-lo)/2);gap=((d+lo)/2-L,(d+hi)/2-L);common=len(set(map(abs,ls)))==1;ratio=abs(ls[0])/a if common else None
        expected={'schema':'ym17-two-cube-twelve-state-v1','source_sha256':h(source/'trial.py'),'haar_source_sha256':h(source/'haar_graph.py'),'graph_file_sha256':h(source/'graph.json'),'alpha':str(a),'coefficients':list(map(str,ls)),'face_order':[f['id'] for f in fg['faces']],'bits':bits,'precision':str(tol),
          'gram':matrix(gram),'electric_matrix':matrix(E),'potential_matrix':matrix(V),'trial_H':matrix(H),'delta':str(d),'L':str(L),'Q':str(Q),'radicand':str(q),'sqrt_bracket':list(map(str,(lo,hi))),
          'trial_minimum_bracket':list(map(str,e0)),'full_E0_upper':str(e0[1]),'full_E1_lower':str(d-L),'gap_bound_bracket':list(map(str,gap)),'gap_lower':str(gap[0]),'width':str(gap[1]-gap[0]),
          'precision_status':'target-met' if gap[1]-gap[0]<=tol else 'insufficient-width','sign_status':'positive' if gap[0]>0 else 'zero-insufficient' if gap[0]==gap[1]==0 else 'negative-insufficient' if gap[1]<0 else 'inconclusive',
          'common_magnitude_ratio':str(ratio) if common else None,'common_exact_classification':'positive' if common and ratio<F(12,43) else 'zero-insufficient' if common and ratio==F(12,43) else 'negative-insufficient' if common else 'not-common-magnitude','scope':SCOPE}
        if not strict(c,expected):raise ValueError('matrix, spectral bound or scope mismatch')
        return True
    for fixture in r['fixtures']:check('independent matrices and square-bound replay '+fixture['id'],verify(fixture['certificate']))
    old=r['fixtures'][1]['certificate'];new=r['fixtures'][2]['certificate']
    for name,c in [('trial gap substituted as physical lower',copy.deepcopy(old)),('zero endpoint relabeled positive',copy.deepcopy(new))]:
        if name.startswith('trial'):c['gap_lower']=str(F(c['delta'])-F(c['full_E0_upper']))
        else:c['sign_status']='positive'
        try:verify(c)
        except ValueError:check('reject '+name,True)
        else:raise RuntimeError('wrong spectral inference accepted')
    check('common threshold retained with dense goal open',r['finite_threshold']=='12/43' and r['dense_uniform_goal']=='open')
    result={'schema':'ym17-independent-b1-comparison-v1','status':'passed','checks_count':len(checks),'checks':checks,'reviewed_input_sha256':{'producer/'+f:h(source/f) for f in ('trial.py','haar_graph.py','graph.json','check.py','report.md')},'producer_evidence_sha256':h(evidence/'evidence.json'),'discrepancies':[],'scope':'All actual matrix entries and seven exact spectral fixtures; independent Newton enclosures and exact-square verification of producer dyadic brackets.'}
    (output/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'passed','checks_count':len(checks)}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--producer',required=True);p.add_argument('--evidence',required=True);p.add_argument('--output',required=True);a=p.parse_args();main(a.producer,a.evidence,a.output)
