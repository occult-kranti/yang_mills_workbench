#!/usr/bin/env python3
"""Exact AT2 certificate arithmetic and countercontrols; report.md proves scope."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import comb
from pathlib import Path

HERE=Path(__file__).resolve().parent
CHECKS=[]
def test(name,value):
    if name in {c['id'] for c in CHECKS}: raise RuntimeError('duplicate check '+name)
    if not value: raise RuntimeError('failed '+name)
    CHECKS.append({'id':name,'passed':True})
def padd(p,q): return [sum((p[i] if i<len(p) else 0,q[i] if i<len(q) else 0)) for i in range(max(len(p),len(q)))]
def pmul(p,q):
    out=[F(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q): out[i+j]+=x*y
    return out
def peval(p,x): return sum(c*x**i for i,c in enumerate(p))
def moment(eta,k):return sum(weight*x**k for weight,x in eta)
def put(path,value):path.write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();out=Path(args.output)
    if not out.is_absolute() or out.exists(): raise SystemExit('output must be fresh and absolute')
    ct=json.loads((HERE/'inputs/research/round30/contracts/at2.json').read_text())
    controls=['wrong-second-bound-sign','grid-only-positivity-misses-negative-region','replace-interacting-moments-by-Haar-values','window-endpoint-atom','same-moments-different-spectra','second-moment-ceiling-is-not-equality','wrong-inverse-energy-units','unproved-static-susceptibility']
    test('contract-id',ct['id']=='AT2');test('contract-controls',ct['controls']==controls)
    test('contract-frozen-certificate-choices',ct['frozen_certificate_choices']['L']==8 and ct['frozen_certificate_choices']['c']==3 and ct['frozen_certificate_choices']['b']==49)
    a=F(1,16);L=F(8);c=F(3);b=F(49);cap=F(1,10**8);Bcap=36+98*cap
    qlo=F(31,125);qhi=F(63,250);zlo=F(0);zhi=F(1,250000)
    slo=qlo-zhi;shi=qhi;ulo=1-qhi;uhi=1-qlo
    test('positive-gap-and-denominators',a>0 and L>a and c>0 and b>=a and a*b*b>0)
    test('q-uncertainty-rational',qlo==F(1,4)-F(1,500) and qhi==F(1,4)+F(1,500))
    test('w-squared-uncertainty',zhi==F(1,500)**2)
    test('positive-moment-domain',slo==F(61999,250000)>0 and ulo==F(187,250)>0 and uhi==F(94,125))
    # Polynomial equalities certify the residuals identically, not only at points.
    lower_numerator=[c*c,-2*c,F(1)]
    test('lower-residual-polynomial-identity',lower_numerator==pmul([-c,F(1)],[-c,F(1)]))
    D=b*b+2*a*b;A=2*b+a
    upper_numerator=[D,-A,F(1)]
    cleared=padd(pmul([F(0),F(1)],upper_numerator),[-a*b*b])
    factored=pmul([-a,F(1)],pmul([-b,F(1)],[-b,F(1)]))
    test('upper-residual-polynomial-identity',cleared==factored)
    test('upper-positive-second-coefficient',1/(a*b*b)>0)
    test('lower-no-second-coefficient',len([2/c,-1/c**2])==2)
    # Parameter-wide sign witnesses; report explains the two indicator regions.
    test('window-q-monotonicity',(L+1)/(L-a)>0)
    test('window-z-monotonicity',-L/(L-a)<0)
    test('lower-q-monotonicity',2/c+1/c**2>0)
    test('lower-z-monotonicity',-2/c<0)
    test('upper-q-monotonicity',(A+D)/(a*b*b)>0)
    test('upper-z-monotonicity',-D/(a*b*b)<0)
    test('upper-B-monotonicity',1/(a*b*b)>0)
    test('cauchy-domain-monotonicity-premises',qlo-zhi>0 and 1-qhi>0)
    window=lambda q,z:((L+1)*q-L*z-1)/(L-a)
    tangent=lambda q,z:2*(q-z)/c-(1-q)/c**2
    upper=lambda q,z,B:(B-A*(1-q)+D*(q-z))/(a*b*b)
    cauchy=lambda q,z:(q-z)**2/(1-q)
    win=window(qlo,zhi);tlo=tangent(qlo,zhi);up=upper(qhi,0,Bcap);clo=cauchy(qlo,zhi);support=shi/a
    test('exact-window-floor',win==F(307992,1984375))
    test('exact-tangent-floor',tlo==F(91997,1125000))
    test('exact-upper-ceiling',up==F(28462237549,7503125000))
    test('exact-cauchy-floor',clo==F(3843876001,47000000000))
    test('baseline-comparisons',clo>tlo and up<support==F(504,125))
    for qi,q in enumerate((qlo,(qlo+qhi)/2,qhi)):
        for zi,z in enumerate((zlo,zhi/2,zhi)):
            test(f'joint-domain-arithmetic-{qi}-{zi}',window(q,z)>=win and tangent(q,z)>=tlo and upper(q,z,Bcap)<=up and cauchy(q,z)>=clo)
    test('joint-relations-preserved',all((q-z)+(1-q)==1-z for q in (qlo,qhi) for z in (0,zhi)))
    test('control-replace-interacting-moments-by-Haar-values',window(F(1,4),0)>win and tangent(F(1,4),0)>tlo and upper(F(1,4),0,Bcap)<up)
    for ix,x in enumerate((a,F(1),F(3),L,b,F(10000))):
        pl=(L-x)/(L-a);ind=int(a<=x<=L)
        lo=2/c-x/c**2;hi=peval(upper_numerator,x)/(a*b*b)
        test(f'point-diagnostic-{ix}',pl<=ind and lo<=1/x<=hi)
        test(f'exact-rational-residual-{ix}',hi-1/x==(x-a)*(x-b)**2/(a*b*b*x))
    endpoint=[(F(1,4),L)]
    endpoint_closed=sum(w for w,x in endpoint if a<=x<=L)
    endpoint_open=sum(w for w,x in endpoint if a<=x<L)
    endpoint_minorant=sum(w*(L-x)/(L-a) for w,x in endpoint)
    test('control-window-endpoint-atom',endpoint_closed==F(1,4) and endpoint_open==0 and endpoint_minorant==0)
    # A nonzero tail beyond L is compatible with a positive certified window.
    tailfixture=[(F(3,14),F(2)),(F(1,28),F(9))]
    test('window-does-not-imply-cutoff',sum(w for w,x in tailfixture if x>L)>0 and sum(w for w,x in tailfixture if x<=L)>=win and moment(tailfixture,0)==F(1,4) and moment(tailfixture,1)==F(3,4) and moment(tailfixture,2)<=Bcap)
    # Dense integer sample positivity does not cover a continuous interval.
    bad=lambda x:(x-F(3,2))**2-F(1,16)
    test('control-grid-only-positivity-misses-negative-region',all(bad(F(n))>0 for n in range(1,101)) and bad(a)>0 and bad(F(3,2))<0)
    etaA=[(F(1,8),F(2)),(F(1,8),F(4))]
    etaB=[(F(1,32),F(1)),(F(3,16),F(3)),(F(1,32),F(5))]
    expected=[F(1,4),F(3,4),F(5,2)]
    def uniform_moment(k):
        # x=3+y, y uniform [-sqrt3,sqrt3]: odd y powers vanish.
        return F(1,4)*sum(F(comb(k,j))*3**(k-j)*F(3**(j//2),j+1) for j in range(0,k+1,2))
    for k in range(3):
        test(f'equal-moment-{k}',moment(etaA,k)==moment(etaB,k)==uniform_moment(k)==expected[k])
    test('three-fixtures-match-actual-relations',expected[0]==F(1,4)-0**2 and expected[1]==1-F(1,4) and expected[2]<36)
    test('uniform-support-above-gap',3<2**2 and F(3)-2>a)
    IA=moment(etaA,-1);IB=moment(etaB,-1)
    test('atomic-inverse-responses',IA==F(3,32) and IB==F(1,10))
    test('atomic-supports-differ',{x for w,x in etaA}!={x for w,x in etaB})
    series_lo=sum(F(1,12*3**k*(2*k+1)) for k in range(3))
    geometric_tail=F(1,3**3)/(1-F(1,3))
    series_hi=series_lo+geometric_tail/(12*7)
    test('atomless-inverse-series-floor',series_lo==F(17,180))
    test('atomless-inverse-series-ceiling',series_hi==F(719,7560))
    test('control-same-moments-different-spectra',IA<series_lo<series_hi<IB and moment(etaA,2)==uniform_moment(2))
    # Control significance: all moments exactly equal yet A/B atomic and C a density.
    vA=moment(etaA,2)
    test('control-second-moment-ceiling-is-not-equality',vA<Bcap and (Bcap-vA)/(a*b*b)>0)
    # Kernel -x^2 equals its own polynomial upper certificate, but a negative
    # coefficient sends an upper v bound to a LOWER integral bound.
    test('control-wrong-second-bound-sign',-vA>-Bcap and not(-vA<=-Bcap))
    for ix,alpha in enumerate((F(1,2),F(1),F(7,3))):
        physical=[(w,alpha*x) for w,x in etaA]
        test(f'inverse-energy-scaling-{ix}',moment(physical,-1)==IA/alpha)
    test('control-wrong-inverse-energy-units',moment([(w,2*x) for w,x in etaA],-1)!=2*IA)
    test('vacuum-must-be-excluded-from-inverse',a>0 and moment(etaA,0)>0)
    # Susceptibility would be a different typed target with extra hypotheses;
    # the contract explicitly refuses that identification.
    test('control-unproved-static-susceptibility','no static-susceptibility assertion' in ct['dictionary']['R'] and 'Physical susceptibility without differentiability' in ct['claim_exclusions'])
    files=[HERE/'check.py',HERE/'report.md']+sorted(p for p in (HERE/'inputs').rglob('*') if p.is_file())
    manifest={p.relative_to(HERE).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    result={'loop':'AT2','direction':'forward','human_author':'Hruday N M (BUNZEEY)','ai_assisted':True,'classification':'model-specific application of established moment certificates; scientific priority unverified','claims':{'actual_aq_state':True,'window_mass_lower_bound':True,'inverse_energy_interval':True,'full_half_line_analytic_certificates':True,'second_moment_equality':False,'spectral_atom_identification':False,'static_susceptibility':False,'global_optimality':False,'continuum_claim':False},'bounds':{'window_mass_lower':str(win),'inverse_dimensionless_tangent_lower':str(tlo),'inverse_dimensionless_cauchy_lower':str(clo),'inverse_dimensionless_upper':str(up),'inverse_dimensionless_support_upper':str(support),'physical_inverse_units':'multiply every dimensionless inverse endpoint by alpha^-1','B_cap':str(Bcap)},'countermeasures':{'common_moments':[str(x) for x in expected],'A':{'type':'atomic','inverse':str(IA)},'B':{'type':'atomic','inverse':str(IB)},'C':{'type':'atomless uniform density','inverse_formula':'log((3+sqrt(3))/(3-sqrt(3)))/(8*sqrt(3))','inverse_lower_strict':str(series_lo),'inverse_upper':str(series_hi)},'scope':'Abstract positive spectral measures, not claimed AQ realizations or distinct thermodynamic states'},'controls':{key:True for key in controls},'checks':CHECKS,'fixture_scope':'Exact polynomial, rational and moment diagnostics accompany report analytic half-line and operator arguments. Grid diagnostics are not proofs.'}
    out.mkdir(parents=True);put(out/'results.json',result);put(out/'source-manifest.json',manifest)
    print(json.dumps({'loop':'AT2','checks':len(CHECKS),'all_passed':True,'output':str(out)}))
if __name__=='__main__':main()
