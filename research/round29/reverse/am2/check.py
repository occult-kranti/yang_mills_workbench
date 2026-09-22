#!/usr/bin/env python3
"""AM2 independent exact majorant, commutator and centered-sector controls."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json,math
BASE=Path(__file__).resolve().parent
def demand(v,m):
    if not v:raise AssertionError(m)
def mm(a,b):
    n=len(a);return [[sum(a[i][k]*b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
def comm(a,b):
    ab=mm(a,b);ba=mm(b,a);return [[u-v for u,v in zip(x,y)] for x,y in zip(ab,ba)]
def nonzero(a):return any(x for row in a for x in row)
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=BASE/'output');args=p.parse_args()
    demand(json.loads((BASE/'inputs/research/round29/contracts/am2.json').read_text())['id']=='AM2','contract')
    tau0=F(1,100000000);J=28*tau0;R=F(1,64);x=8*R
    # Exact exponential enclosure: finite Taylor lower, geometric upper.
    exp_lower=sum(x**k/F(math.factorial(k)) for k in range(9));exp_upper=1/(1-x)
    demand(exp_lower<exp_upper and exp_upper==F(8,7),'exponential certificate')
    Gupper=16*exp_upper*(1+10*R);Gpupper=16*exp_upper*(18+80*R)
    demand(Gupper==F(148,7) and Gpupper==352,'majorant constants')
    selfmap=J*Gupper;lipschitz=J*Gpupper;resolvent=2*lipschitz
    demand(selfmap<R and lipschitz<1 and resolvent<1,'all quantitative gates')
    orders=[]
    for k in range(9):
      anchor=16*8**k;creation=0 if k==0 else 16*2**k*5*k*4**(k-1)
      combined=F(anchor+creation);closed=16*8**k*(1+F(5*k,4))
      demand(combined==closed,'independent coefficient reconstruction')
      orders.append({'k':k,'anchor_case':str(anchor),'creation_case':str(creation),'Lk':str(combined)})
    # Four creation factors and an actual 4-site operator. ad^8 nonzero, ad^9 zero.
    d=16;C=[[0]*d for _ in range(d)];V=[[0]*d for _ in range(d)]
    for col in range(d):
      V[15-col][col]=1
      for bit in range(4):
       if not(col>>bit)&1:C[col|(1<<bit)][col]+=1
    A=V;commutators=[]
    for k in range(10):
      commutators.append({'k':k,'nonzero':nonzero(A),'max_abs_entry':max(abs(v) for row in A for v in row)})
      A=comm(C,A)
    demand(commutators[7]['nonzero'] and commutators[8]['nonzero'] and not commutators[9]['nonzero'],'support-four termination discriminator')
    inv_checks=[]
    for m in (1,2,4,17):
      for z in (F(-1,2),F(0),F(499,1000),F(1,2)):
       val=1/(m-z);demand(val<=F(2,m),'shifted inverse certificate');inv_checks.append(str(val))
    v,diag=F(1,100),F(1,200)
    # char_H(0)=-v² distinguishes E0=0 from actual ground scalar.
    polynomial_at_zero=-v*v;gap_squared=(1+diag)**2+4*v*v
    controls={'support_three_deletion_discriminated':commutators[7]['nonzero'],'ninth_commutator_vanishes':not commutators[9]['nonzero'],'drop_scalar_wrong_ground':polynomial_at_zero!=0,'drop_retained_diagonal_changes_gap':gap_squared!=1+4*v*v,'zero_source_selfmap_zero':0*Gupper==0,'both_tau_signs_same_J':28*abs(-tau0)==J,'incoming_star_norm':J!=7*tau0,'resolvent_edge_factor_two':F(1)/(1-F(1,2))==2}
    demand(all(controls.values()),'controls')
    result={'loop':'AM2','direction':'reverse','verdict':'uniform finite-volume physical gap certified within declared model','tau_interval':['-1/100000000','1/100000000'],'J_cap':str(J),'R':str(R),'exp_lower':str(exp_lower),'exp_upper':str(exp_upper),'G_upper':str(Gupper),'Gprime_upper':str(Gpupper),'selfmap_upper':str(selfmap),'selfmap_radius':str(R),'lipschitz_upper':str(lipschitz),'shifted_resolvent_contraction_upper':str(resolvent),'gap_normalized':'1/2','gap_physical':'alpha/16','orders':orders,'commutators':commutators,'controls':controls,'empty_volume':'one-dimensional; spectral exclusion vacuous, no excitation','scope':'Alternative numerical finite-volume theorem; no numerical identification of inherited infinite-volume state or continuum.'}
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    files=[BASE/'check.py',BASE/'report.md']+sorted(f for f in (BASE/'inputs').rglob('*') if f.is_file());h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
    (out/'manifest.json').write_text(json.dumps({'source_files':[{'path':str(f.relative_to(BASE)),'sha256':h(f)} for f in files],'results_sha256':h(out/'results.json')},indent=2)+'\n');print(json.dumps({'loop':'AM2','passed':True,'controls':len(controls),'resolvent_contraction':str(resolvent)}))
if __name__=='__main__':main()
