"""Execute the independent C2 angular/radial integral and exact remainder checks."""
from fractions import Fraction as F
from pathlib import Path
import argparse,copy,csv,hashlib,json
from geometry import graph,validate,boundary,word_holonomy,TETRA,IDENTITY
from angular import COMMUTING,data,comparison,encoded,radial_data,angular_moment,semicircle,quotient,boundary_values


def run(output):
    output=Path(output).resolve()
    if output.is_relative_to(Path(__file__).resolve().parent):raise ValueError('output outside frozen source required')
    output.mkdir(parents=True,exist_ok=False);checks=[]
    def check(name,ok):
        if not ok:raise RuntimeError(name)
        checks.append({'name':name,'passed':True})
    def reject(name,fn):
        try:fn()
        except (ValueError,TypeError,KeyError):check(name,True);return
        raise RuntimeError('invalid parameter accepted '+name)
    g=graph();geo=validate(g);boundaries={}
    for name,H in [('T',TETRA),('C',COMMUTING)]:
        links,paths,chosen=boundary(g,H)
        check('actual four-cube paths realize boundary '+name,all(word_holonomy(path['word'][1:],links)==h for path,h in zip(paths,H)) and len(set(chosen))==4)
        boundaries[name]={'paths':paths,'assignments':{str(k):list(map(str,v)) for k,v in links.items()},'H':encoded(H)}
    check('sixteen noncentral faces omit the conditional link',len(geo['outer_faces'])==16 and all(geo['central'] not in [e for e,_ in g['faces'][i]['word']] for i in geo['outer_faces']))
    check('S2 and semicircle normalizations differ correctly',angular_moment((2,0,0))==F(1,3) and angular_moment((2,2,0))==F(1,15) and semicircle(2)==F(1,4) and semicircle(4)==F(1,8))
    Tpoly,Tindividual=radial_data(TETRA);Cpoly,Cindividual=radial_data(COMMUTING)
    check('tetrahedral individual radial polynomials vanish identically',Tindividual==[{}]*4)
    levels=[comparison('1/8',n) for n in (0,4,8,12,16)];zero=comparison(0,16);negative=comparison('-1/8',16);half=comparison('1/16',16)
    check('zero-action joint expectations independently reproduce C1 and commuting values',zero['T']['expectation_interval']==(-F(1,405),-F(1,405)) and zero['C']['expectation_interval']==(F(13,1215),F(13,1215)) and zero['contrast_interval']==(F(16,1215),F(16,1215)))
    check('all primary fixtures have identical nonzero action and partition',all(r['T']['b']==r['C']['b']==(F(1,4),F(0),F(0),F(0)) and r['T']['Z_coefficients']==r['C']['Z_coefficients'] for r in levels))
    grams={name:[[sum(a*b for a,b in zip(hi,hj)) for hj in H] for hi in H] for name,H in [('T',TETRA),('C',COMMUTING)]}
    check('equal action vectors do not identify boundary Gram tensors',grams['T']!=grams['C'])
    check('wrong action-only closure contradicted by exact numerator coefficients',levels[-1]['T']['A_coefficients']!=levels[-1]['C']['A_coefficients'] and levels[-1]['contrast_interval'][0]>0)
    check('predetermined coarse levels remain insufficient',[r['status'] for r in levels]==['insufficient']*3+['positive']*2)
    check('degree-eight failure is precision not sign',levels[2]['sign_status']=='positive' and levels[2]['contrast_width']>F(1,10**12))
    final=levels[-1]
    check('final individual and contrast widths all meet requested target',all(final[x]['width']<=F(1,10**12) for x in ('T','C')) and final['contrast_width']<=F(1,10**12))
    check('finite-coupling contrast has rigorous positive lower and opposite individual signs',final['contrast_interval'][0]>0 and final['T']['expectation_interval'][1]<0<final['C']['expectation_interval'][0])
    check('complete remainder bounds shrink with degree',all(levels[i]['contrast_width']>levels[i+1]['contrast_width']>0 for i in range(4)))
    check('negative common coupling gives same even-observable enclosures',negative['contrast_interval']==final['contrast_interval'] and negative['T']['expectation_interval']==final['T']['expectation_interval'] and negative['T']['b'][0]==-F(1,4))
    check('half-coupling fixture independently meets target',half['status']=='positive' and half['contrast_interval']!=final['contrast_interval'])
    all_zero=data(COMMUTING,(0,)*4,16);balanced=data(COMMUTING,('1/8','-1/8','1/8','1/8'),16)
    check('nonzero coefficients with zero b use exact Haar branch',balanced['coefficients']!=(0,)*4 and balanced['b']==(0,)*4 and balanced['branch']=='zero-b Haar' and balanced['tail']==0 and balanced['Z_interval']==(1,1) and balanced['expectation_interval']==all_zero['expectation_interval'])
    check('zero action retains exact zero remainder for every degree',all(comparison(0,n)['contrast_width']==0 for n in (0,4,8,12,16)))
    check('signed quotient uses all four corners',quotient((F(-2),F(-1)),(F(1),F(2)))==(-2,-F(1,2)))
    # The original low-degree denominator uncertainty must not disappear.
    primary0=levels[0]
    numerator_only=(primary0['C']['A_value']-primary0['T']['A_value'])/primary0['T']['Z_value']
    check('point Taylor quotient cannot replace complete wide enclosure',primary0['contrast_width']>1 and primary0['contrast_interval'][0]<numerator_only<primary0['contrast_interval'][1])
    angular_moment((0,0,0));semicircle(0)
    reject('warm Boolean angular exponent rejected before cache',lambda:angular_moment((False,0,0)))
    reject('warm Boolean semicircle exponent rejected before cache',lambda:semicircle(False))
    reject('negative angular exponent rejected',lambda:angular_moment((-2,0,0)))
    reject('negative scalar moment index rejected',lambda:semicircle(-1))
    reject('malformed angular tuple rejected',lambda:angular_moment((0,0)))
    malformed=list(COMMUTING);malformed[0]=(True,F(0),F(0),F(0));reject('nested Boolean boundary coordinate rejected',lambda:data(tuple(malformed),(0,)*4,16))
    malformed=list(COMMUTING);malformed[0]=(F(1),F(1),F(0),F(0));reject('nonunit boundary rejected',lambda:data(tuple(malformed),(0,)*4,16))
    reject('Boolean coefficient rejected',lambda:data(TETRA,(True,0,0,0),16))
    reject('Boolean degree rejected',lambda:comparison('1/8',True))
    reject('negative degree rejected',lambda:comparison('1/8',-1))
    reject('degree above declared cap rejected',lambda:comparison('1/8',17))
    reject('nonpositive precision rejected',lambda:comparison('1/8',16,0))
    reject('generic non-axis action vector is not silently rotated',lambda:data(TETRA,('1/8',0,0,0),16))
    reject('remainder geometric condition enforced',lambda:comparison('2',0))
    result={'schema':'ym17-independent-c2-results-v1','status':'passed','checks_count':len(checks),'checks':checks,
      'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('*.py') if p.name!='compare.py'},
      'radial_polynomials':encoded({'T':Tpoly,'C':Cpoly}),'individual_radial_polynomials':encoded({'T':Tindividual,'C':Cindividual}),
      'direction_grams':encoded(grams),'primary_degrees':[0,4,8,12,16],'primary_statuses':[r['status'] for r in levels],
      'final_contrast_interval':encoded(final['contrast_interval']),'final_contrast_width':str(final['contrast_width']),
      'final_T_interval':encoded(final['T']['expectation_interval']),'final_C_interval':encoded(final['C']['expectation_interval']),
      'scope':'Finite fixed-boundary central-link conditional integral with complete exponential remainders; same b and Z do not determine the observable; no bulk or spectral inference.'}
    evidence={'levels':encoded(levels),'zero':encoded(zero),'negative':encoded(negative),'half':encoded(half),'all_zero':encoded(all_zero),'balanced_zero_b':encoded(balanced)}
    for name,obj in [('results.json',result),('evidence.json',evidence),('boundary_fixtures.json',boundaries)]:
        (output/name).write_text(json.dumps(obj,indent=2)+'\n')
    with (output/'convergence.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['degree','contrast_lower','contrast_upper','contrast_width','status']);writer.writeheader()
        writer.writerows({'degree':r['degree'],'contrast_lower':str(r['contrast_interval'][0]),'contrast_upper':str(r['contrast_interval'][1]),'contrast_width':str(r['contrast_width']),'status':r['status']} for r in levels)
    print(json.dumps({'status':'passed','checks_count':len(checks),'contrast_lower':float(final['contrast_interval'][0]),'width':float(final['contrast_width'])}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();run(a.output)
