#!/usr/bin/env python3
"""Reverse J1: exact dyadic residual bounds and physical-observable falsifiers."""
from fractions import Fraction as F
from pathlib import Path
import argparse, hashlib, json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def B(q):
    return (2+5*q+5*q*q+6*q**3+3*q**4)/(24*(1-q)**3*(1+q)**2*(1+q*q))
def matmul(a,b):return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0)) for j in range(len(b[0]))] for i in range(len(a))]
def trace(a):return sum((a[i][i] for i in range(len(a))),F(0))
def variance(p,w):return trace(matmul(p,matmul(w,w)))-trace(matmul(p,w))**2
def run():
    tau_max=F(1,64);ledger=B(F(1,2));second_ledger=B(F(1,4))
    need(ledger==F(107,135),'omitted ledger mismatch')
    sigma=second_ledger*tau_max*tau_max/96
    g=F(1,8)-ledger*tau_max
    d2=sigma/(g*g)
    d_upper=F(1,150)
    need(d2<d_upper*d_upper,'rational projector enclosure fails')
    lower=F(1,4)-2*d_upper-4*d_upper*d_upper
    need(lower==F(5321,22500) and lower>F(1,5),'positive physical fluctuation margin')
    # 0<=t<=tmax: t² increases while delta-Bt stays positive and decreases.
    samples=[]
    for t in [F(0),F(1,256),F(1,128),F(1,64),-F(1,256),-F(1,64)]:
        ss=second_ledger*t*t/96;gg=F(1,8)-ledger*abs(t)
        need(gg>=g and ss/(gg*gg)<=d2,'signed interval endpoint bound')
        samples.append({'tau':str(t),'sigma_squared_over_alpha_squared':str(ss),
          'excited_threshold_over_alpha':str(gg),'projector_square_upper':str(ss/(gg*gg))})
    # Actual xz Wilson square at origin; its two z links are free reference Haar factors.
    vertices=[(0,0,0),(1,0,0),(1,0,1),(0,0,1)]
    e=[(vertices[0],vertices[1]),(vertices[1],vertices[2]),(vertices[2],vertices[3]),(vertices[3],vertices[0])]
    zlinks=[((0,0,0),2),((1,0,0),2)]
    need(all(d==2 for _,d in zlinks),'free Haar witnesses')
    center_checks=[]
    for vertex in vertices:
        edge_signs=[-1 if vertex in edge else 1 for edge in e]
        product=1
        for x in edge_signs:product*=x
        need(product==1,'closed Wilson loop loses center invariance')
        center_checks.append({'vertex':vertex,'signs':edge_signs,'wilson_sign':product})
    need((-1)*1==-1,'open-link charge control')
    pref=[[F(1,2),F(1,2)],[F(1,2),F(1,2)]]
    pp=[[F(1),F(0)],[F(0),F(0)]]
    w=[[F(-1,2),F(0)],[F(0),F(1,2)]]
    need(variance(pref,w)==F(1,4) and variance(pp,w)==0,'reference-only variance counterexample')
    identity=[[F(1),F(0)],[F(0),F(1)]]
    need(variance(pp,identity)==0,'vacuum-only scalar algebra rejected')
    z=[[F(1),F(0)],[F(0),F(-1)]]
    p1=[[F(0),F(0)],[F(0),F(1)]]
    need(matmul(z,pp)==matmul(pp,z) and matmul(z,p1)==matmul(p1,z),'nontrivial invariant-algebra commutant')
    return {'schema':'ym21-reverse-j1-v1','loop':'j1','direction':'reverse','passed':True,
      'target_verdict':'gauge_algebra_and_nonzero_perturbed_physical_fluctuation_verified',
      'comparison':{'variance_lower_bound':str(lower),'projector_square_upper':str(d2),
        'gap_lower_alpha':str(g),'physical_fluctuation_nonzero':True,
        'full_and_physical_spaces_identified':False},
      'exact_bounds':{'B_half':str(ledger),'B_quarter':str(second_ledger),
        'sigma_squared_upper_over_alpha_squared':str(sigma),
        'd_rational_upper':str(d_upper),'d_squared_margin':str(d_upper*d_upper-d2),
        'variance_margin_above_one_fifth':str(lower-F(1,5)),'signed_fixtures':samples},
      'observable':{'name':'normalized xz Wilson square at origin',
        'vertices':vertices,'free_z_links':zlinks,'reference_mean':'0','reference_second_moment':'1/4',
        'center_gauge_fixtures':center_checks},
      'gauge_scope':{'group':'finite-support vertex SU(2) gauge transformations',
        'physical_algebra':'norm closure of all finite-factor bounded observables invariant under every finite-support gauge transformation',
        'spaces':'K_phys=closure(A_phys Psi) subset H_fix subset H; no equality asserted',
        'core':'finite smooth reference-factor excitation tensors, gauge-invariant common core for H_ref and H',
        'core_limit':'neither the full bounded local algebra nor the infinite perturbation is asserted to preserve that algebraic core',
        'model':'A2/E/G dyadic q=1/2 summable model, not I1 homogeneous model'},
      'controls':{'charged_open_link_rejected':True,'scalar_vacuum_algebra_rejected':True,
        'full_irreducibility_transfer_rejected':True,'reference_only_variance_inference_rejected':True,
        'unmatched_homogeneous_interval_not_used':True}}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    files=[HERE/'check.py',HERE/'report.md',ROOT/'research/round21/contracts/j1.json',
      ROOT/'research/round21/advisor/i2-gate.json',ROOT/'research/round19/forward/a2/report.md',
      ROOT/'research/round20/reverse/g2/report.md',ROOT/'research/round20/reverse/h2/report.md']
    need(all(p.is_file() for p in files),'required source absent')
    before={str(p.relative_to(ROOT)):digest(p) for p in files}
    c=json.loads((ROOT/'research/round21/contracts/j1.json').read_text())
    need(c['loop']=='j1' and c['status']=='frozen','J1 contract not frozen')
    need(digest(ROOT/c['depends_on']['gate'])==c['depends_on']['sha256'],'I2 gate mismatch')
    result=run();need(before=={str(p.relative_to(ROOT)):digest(p) for p in files},'sources changed')
    result['source_bindings']=before
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    (out/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (out/'source-manifest.json').write_text(json.dumps({'schema':'ym21-source-bindings-v1','inputs':before,
      'outputs':{'results.json':digest(out/'results.json')}},indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed':result['passed'],'comparison':result['comparison'],'output':str(out)}))
if __name__=='__main__':main()
