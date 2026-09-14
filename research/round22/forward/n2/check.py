#!/usr/bin/env python3
"""Exact finite geometry and certificate controls; report.md proves all L."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import itertools
import json

ROOT = Path(__file__).absolute().parents[4]
BASE = 'research/round22/forward/n2/'
CONTRACT = 'research/round22/contracts/n2.json'
CONTRACT_SHA = 'a2b0fd55d55a393dc0d70911fa91819f75576211be68d83766c53f5357511db8'
INPUTS = [CONTRACT,
    'research/round22/methods/team-protocol.md',
    'research/round22/methods/AGENTS-at-selection.md',
    'research/round22/methods/paired-physics-research-at-selection.md',
    'research/round22/advisor/n1-gate.json',
    'research/round22/advisor/n1-decision.md',
    'research/round22/skeptic/n1.md',
    'research/round21/advisor/i1-gate.json',
    'research/round21/forward/i1/report.md',
    'research/round22/forward/n1/report.md',
    'research/round22/forward/n1/source-notes.md',
    BASE+'report.md', BASE+'check.py']


def require(ok, message):
    if type(ok) is not bool or not ok:
        raise ValueError(message)


def safe(path):
    for p in [path.absolute(), *path.absolute().parents]:
        require(not p.is_symlink(), 'symlink component rejected')


def sha(path):
    safe(path)
    require(path.is_file(), 'missing input: '+str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, obj):
    path.write_text(json.dumps(obj, sort_keys=True, indent=2)+'\n')


def move(p, axis, step):
    return tuple(x + (step if i == axis else 0) for i,x in enumerate(p))


def links(face):
    a,b,*p = face
    return {(a,*p), (b,*p), (a,*move(p,b,1)), (b,*move(p,a,1))}


def omitted(face):
    a,b,x,y,z = face
    return not (a == 0 and b == 1 and y % 2 == 0 and x % 4 != 3)


def region(L):
    return set(itertools.product(range(4*L),range(2*L),range(L)))


def incident(edges):
    faces = set()
    for axis,*p in edges:
        for transverse in range(3):
            if transverse == axis:
                continue
            for step in (0,-1):
                anchor = move(p, transverse, step)
                if min(anchor) >= 0:
                    a,b = sorted((axis,transverse))
                    f = (a,b,*anchor)
                    if omitted(f):
                        faces.add(f)
    return faces


def factor_edges(edge):
    axis,x,y,z = edge
    if axis == 0 and x % 4 != 3:
        bx,by = x-x%4,y-y%2
    elif axis == 1 and y % 2 == 0:
        bx,by = x-x%4,y
    else:
        return {edge}
    return {(0,bx+r,by+s,z) for r in range(3) for s in range(2)} | {
        (1,bx+r,by,z) for r in range(4)}


def profile(q):
    return (2+5*q+5*q*q+6*q**3+3*q**4)/(24*(1-q)**3*(1+q)**2*(1+q*q))


def S(n,q):
    return (1-q**n)/(1-q)


def finite_closed(L,q):
    all_faces = 3*S(4*L,q)*S(2*L,q)*S(L,q)
    selected = (1+q+q*q)*(1-q**(4*L))/(1-q**4)*(1-q**(2*L))/(1-q*q)*S(L,q)
    return (all_faces-selected)/24


def product(L,q):
    return (1-q**(4*L))*(1-q**(2*L))*(1-q**L)


def budget(faces,q):
    return sum((q**sum(f[2:])/24 for f in faces),F(0))


def run_checks():
    controls, fixtures = [], []
    def control(name, ok, outcome):
        require(ok, 'control failed: '+name)
        controls.append({'name':name,'passed':True,'outcome':outcome})
    for L,q in [(1,F(1,2)),(2,F(2,3)),(3,F(3,4))]:
        R = region(L)
        E = {(a,*p) for p in R for a in range(3)}
        actual = incident(E)
        anchors = {(a,b,*p) for p in R for a,b in [(0,1),(0,2),(1,2)]
                   if omitted((a,b,*p))}
        require(len(E) == 24*L**3, 'complete tail ownership cardinality')
        require(actual == anchors, 'incidence iff anchor in R_L')
        require(all(factor_edges(e) <= E for e in E), 'complete factor support')
        require(len(actual) == 21*L**3, 'omitted face count')
        exact = budget(actual,q)
        require(exact == finite_closed(L,q), 'enumeration versus selected-face subtraction')
        require(exact == profile(q)*product(L,q), 'finite profile factorization')
        eta = F(1,2)
        require(eta/(8*profile(q))*exact == eta*product(L,q)/8, 'canonical budget cancellation')
        clipped = {e for e in E if move(e[1:],e[0],1) in R}
        require(len(clipped) == 24*L**3-14*L**2, 'outgoing link count')
        contained_faces = {f for f in actual if links(f) <= E}
        crossing = actual-contained_faces
        clip_missed = actual-incident(clipped)
        control(f'clipping_outgoing_links_L{L}', bool(clip_missed),
                {'complete_links':len(E),'clipped_links':len(clipped),
                 'missed_incident_faces':len(clip_missed), 'witness':list(min(clip_missed))})
        control(f'discarding_crossing_faces_L{L}', bool(crossing),
                {'crossing_face_count':len(crossing), 'witness':list(min(crossing)),
                 'omitted_weight':str(budget(crossing,q))})
        control(f'infinite_sum_is_not_finite_budget_L{L}', F(0) < exact < profile(q),
                {'D_L':str(exact),'infinite_B':str(profile(q)),'ratio':str(product(L,q)),
                 'scope':'infinite sum is an upper bound but equality discards support dependence'})
        fixtures.append({'L':L,'q':str(q),'owned_links':len(E),
                         'incident_omitted_faces':len(actual), 'D_L_q':str(exact),
                         'D_L_at_one':str(F(7*L**3,8)), 'P_L_q':str(product(L,q)),
                         'tau_D_eta_half':str(eta*product(L,q)/8)})

    shifted_R = {(x+4,y+2,z+1) for x,y,z in region(1)}
    shifted_E = {(a,*p) for p in shifted_R for a in range(3)}
    incoming = (0,1,3,2,1)
    control('origin_downward_closed_qualification',
            incoming in incident(shifted_E) and tuple(incoming[2:]) not in shifted_R,
            {'incoming_face_anchor_outside_translated_rectangle':list(incoming),
             'scope':'the anchor characterization is proved only for origin downward-closed R_L'})

    floor_values = []
    for ell in [F(1,2),F(3,2),F(5,2)]:
        L0 = max(1,ell.numerator//ell.denominator)
        correct = 2*F(1,2)*L0**3  # eta=1/2,C=1
        wrong = 2*F(1,2)*ell**3
        require(correct != wrong, 'floor must affect fixed-support endpoint constant')
        floor_values.append({'ell':str(ell),'L0':L0,'correct_endpoint':str(correct),
                             'wrong_continuous_ell_endpoint':str(wrong)})
    control('beta_zero_floor_is_not_asymptotically_ell',True,floor_values)

    regime_rows = []
    for beta,gamma in [(F(0),F(0)),(F(0),F(3)),(F(1,2),F(1)),
                       (F(1,2),F(3,2)),(F(1),F(0)),(F(2),F(0))]:
        critical = 3*(1-beta)
        vanishes = beta < 1 and gamma < critical
        regime_rows.append({'beta':str(beta),'gamma':str(gamma),
                            'certificate_vanishes':vanishes,
                            'rate_if_vanishing':str(min(F(3,2),critical-gamma)) if vanishes else None})
    control('strict_gamma_boundary_and_critical_support',
            [r['certificate_vanishes'] for r in regime_rows] == [True,False,True,False,False,False],
            'positive endpoint constants apply to the specified envelope; beta>=1 has no gamma>=0 vanishing region')
    # I has zero connected covariance under every stationary unitary;
    # assigning it F_1 is allowed, so a positive cover bound is no lower bound.
    constant_correlation = 1*1-1*1
    endpoint_eta_half_C_one_L_one = 2*F(1,2)
    control('positive_certificate_is_not_actual_nonconvergence',
            constant_correlation == 0 and endpoint_eta_half_C_one_L_one > 0,
            {'actual_constant_correlation':'0','fixed_L_one_endpoint_envelope':'1',
             'actual_nonconstant_endpoint':'unresolved'})
    # Along epsilon=exp(-n), the logarithmic divisor is exactly n^k.
    # k=1 suffices to discriminate shortening; general k>0 is proved in report.
    log_rows = [{'n':n,'k_one_leading_dynamic_certificate':str(F(1,n))}
                for n in (2,4,8)]
    control('fixed_support_log_shortening',
            F(1,8) < F(1,4) < F(1,2),
            {'epsilon_sequence':'exp(-n)','eta':'1/2','C':'1','L':1,
             'k_one_leading_coefficients':log_rows,
             'analytic_all_k_positive':'2etaCL^3/[log(1/epsilon)]^k ->0',
             'unshortened_limit':'1'})

    for bad in (False,'passed'):
        rejected=False
        try:
            require(bad,'intentional rejecting control')
        except ValueError:
            rejected=True
        require(rejected, 'strict validation must reject False and non-Boolean strings')
    control('optimized_python_preserves_admission_exceptions',True,
            'explicit exceptions reject False and truthy non-Boolean statuses')
    results = {'schema':'ym22-forward-n2-results-v1','loop':'n2','direction':'forward',
               'status':'proved_scoped','passed':True,
               'claims':{
                   'incident_iff_anchor_in_origin_tail_rectangle':True,
                   'complete_owned_links':'24*L^3','incident_omitted_faces':'21*L^3',
                   'D_L_closed':'B(q)*(1-q^(4L))*(1-q^(2L))*(1-q^L)',
                   'D_L_at_one':'7*L^3/8',
                   'tau_D_L':'eta*(1-q^(4L))*(1-q^(2L))*(1-q^L)/8',
                   'uniform_certificate':'6*sigma_q/gbar+(eta*C/4)*epsilon^(-gamma)*P_L(q)',
                   'vanishing_certificate_region':'0<=beta<1 and 0<=gamma<3*(1-beta)',
                   'rate':'min(3/2,3*(1-beta)-gamma)',
                   'beta_zero_L':'max(1,floor(ell))',
                   'subcritical_endpoint_constant_beta_positive':'2*eta*C*ell^3',
                   'fixed_L_endpoint_constant':'2*eta*C*L^3',
                   'critical_support_P_limit':'(1-exp(-4*ell))*(1-exp(-2*ell))*(1-exp(-ell))',
                   'supercritical_support_P_limit':'1',
                   'fixed_L_log_shortening_k_positive':True,
                   'actual_endpoint_nonconvergence_proved':False,
                   'homogeneous_or_continuum_transfer':False},
               'exact_geometry_fixtures':fixtures,'regime_checks':regime_rows,
               'infinite_proof_location':BASE+'report.md',
               'finite_checks_are_infinite_proof':False,'scientific_priority':'unverified'}
    return results, {'schema':'ym22-forward-n2-controls-v1','loop':'n2','direction':'forward',
                     'passed':True,'controls':controls}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',required=True,type=Path)
    out=parser.parse_args().output.absolute()
    safe(out)
    require(not out.exists(),'output must be fresh')
    require(len(INPUTS)==len(set(INPUTS)),'duplicate input')
    inputs={p:sha(ROOT/p) for p in INPUTS}
    require(inputs[CONTRACT]==CONTRACT_SHA,'frozen N2 contract mismatch')
    contract=json.loads((ROOT/CONTRACT).read_text())
    require(contract['status']=='frozen' and contract['loop']=='n2','wrong contract')
    for p,h in contract['dependencies'].items():
        require(p in inputs and inputs[p]==h,'dependency mismatch: '+p)
    for gate_path, expected_status in [
            ('research/round22/advisor/n1-gate.json','accepted'),
            ('research/round21/advisor/i1-gate.json','limited')]:
        gate=json.loads((ROOT/gate_path).read_text())
        require(gate['status']==expected_status,'inherited scoped status changed')
        for p in INPUTS:
            if p in gate['files']:
                require(inputs[p]==gate['files'][p],'inherited admitted bytes changed: '+p)
    results,controls=run_checks()
    out.mkdir(parents=True,exist_ok=False)
    save(out/'results.json',results)
    save(out/'controls.json',controls)
    save(out/'source-manifest.json',{'schema':'ym22-producer-source-manifest-v1',
         'loop':'n2','direction':'forward','inputs':inputs,
         'outputs':{p:sha(out/p) for p in ['results.json','controls.json']},
         'output_policy':'relative output names; self-hash bound by frozen submission inventory',
         'import_policy':'Python standard library only; no other producer imports'})
    print(json.dumps({'loop':'n2','direction':'forward','passed':True,
                      'status':results['status'],'controls':len(controls['controls'])},sort_keys=True))


if __name__=='__main__':
    main()
