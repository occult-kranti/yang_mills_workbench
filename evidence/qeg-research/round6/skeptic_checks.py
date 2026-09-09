#!/usr/bin/env python3
"""Independent exact identities and numerical falsifiers; no production imports.
The numerical checks are high-precision comparisons, not interval proofs.
"""
from pathlib import Path
from fractions import Fraction
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
LOCAL_DEPS = HERE.parent / 'round5' / 'deps'
if LOCAL_DEPS.exists():
    sys.path.insert(0, str(LOCAL_DEPS))
import sympy as sp
import mpmath as mp
mp.mp.dps = 65
checks=[]
def check(name, passed, **evidence):
    checks.append({'id':name,'passed':bool(passed),'evidence':evidence})
def text(v):
    return mp.nstr(v, 28)

# Exact primitive and sign conventions; independent algebra from P2.
p,M=sp.symbols('p M', real=True, positive=True)
A=p*(3*M**2+2*p**2)/(12*M**2*(M**2+p**2)**sp.Rational(3,2))
g=M**2/(4*(M**2+p**2)**sp.Rational(5,2))
check('primitive_derivative', sp.simplify(sp.diff(A,p)-g)==0)
check('whole_line_integral',sp.simplify(2*sp.limit(A,p,sp.oo)-1/(3*M**2))==0)
check('wrong_factor_two_detected',sp.simplify(sp.diff(2*A,p)-g)!=0)
K=sp.symbols('K',positive=True)
I=2*A.subs(p,K)
check('window_monotonicity',sp.simplify(sp.diff(I,K)-2*g.subs(p,K))==0)
check('small_window_limit',sp.simplify(sp.limit(I/K,K,0)-1/(2*M**3))==0)

# Exact rational extension from N=4 to arbitrary finite Landau cutoff at fixed K.
F=Fraction
pref=F(100)/(137*F(314,100))
core=1+2*(F(1,84)+F(1,246)+F(1,427)+F(1,729))
old=pref*core
new=pref*(core+F(2,90))
check('old_rational_certificate',old==F(66325137500,274510827927) and old<F(1,4), bound=str(old))
check('fixed_window_all_landau_certificate',new==F(67743204500,274510827927) and new<F(1,4), bound=str(new), margin=str(F(1,4)-new))
y=sp.symbols('y',nonnegative=True)
tail=sp.integrate((1+20*y)**sp.Rational(-3,2),(y,4,sp.oo))
check('landau_tail_integral',tail==sp.Rational(1,90), exact=str(tail))

alpha=1/mp.mpf('137.035999084')
e2=4*mp.pi*alpha

def susceptibility(b):
    z=1/(2*b)
    return e2/(12*mp.pi**2)*(b-mp.log(2*b)-mp.digamma(1+z))
def primitive(p,m):
    u=p/mp.sqrt(m*m+p*p)
    return (u-u**3/3)/(4*m*m)
def mode_window(m,k,a):
    return primitive(k-a,m)+primitive(k+a,m)
def coeff(k,n,b,a=0):
    return b/(4*mp.pi**2)*mp.fsum((1 if j==0 else 2)*mode_window(mp.sqrt(1+2*b*j),k,a) for j in range(n+1))
def coeff_infty_sum(n,b):
    return b/(12*mp.pi**2)*mp.fsum((1 if j==0 else 2)/(1+2*b*j) for j in range(n+1))
def coeff_infty_psi(n,b):
    z=1/(2*b)
    return (b+mp.digamma(n+1+z)-mp.digamma(1+z))/(12*mp.pi**2)

# Independent numerical integration has a different computational path from primitive.
for idx,(m,k,a) in enumerate([(1,20,0),(1,20,19),(3,7,-4),(9,20,30)]):
    m,k,a=map(mp.mpf,(m,k,a))
    points=sorted(set([-k,k]+[t for t in (a-m,a,a+m) if -k<t<k]))
    integral=mp.quad(lambda q:m*m/(4*(m*m+(q-a)**2)**mp.mpf('2.5')),points)
    actual=mode_window(m,k,a)
    check(f'independent_integral_{idx}',abs(integral-actual)<mp.mpf('1e-55'), abs_error=text(abs(integral-actual)))

for idx,(b,n) in enumerate([(mp.mpf('0.1'),0),(mp.mpf(3),2),(mp.mpf(10),4),(mp.mpf(10),1000)]):
    direct=coeff_infty_sum(n,b)
    compact=coeff_infty_psi(n,b)
    z_from_model=1+susceptibility(b)-e2*direct
    z_cancelled=1-e2/(12*mp.pi**2)*(mp.log(2*b)+mp.digamma(n+1+1/(2*b)))
    check(f'digamma_sum_{idx}',abs(direct-compact)<mp.mpf('1e-55'), abs_error=text(abs(direct-compact)))
    check(f'matched_cancellation_{idx}',abs(z_from_model-z_cancelled)<mp.mpf('1e-55'), abs_error=text(abs(z_from_model-z_cancelled)))

b=mp.mpf(10)
# Exact integral is even and maximized at window center. Samples supplement proof.
c0=coeff(mp.mpf(20),4,b)
vals=[]
for a in [mp.mpf(0),mp.mpf('0.25'),mp.mpf(4),mp.mpf(20),mp.mpf(40)]:
    cp=coeff(mp.mpf(20),4,b,a)
    cm=coeff(mp.mpf(20),4,b,-a)
    vals.append(cp)
    check('continuum_even_'+str(a),abs(cp-cm)<mp.mpf('1e-55'))
check('continuum_sampled_strict_decrease',all(vals[i]>vals[i+1] for i in range(len(vals)-1)), values=[text(v) for v in vals])

# A physically normalized but deliberately underresolved exact two-node rule.
k=mp.mpf(200)
node=k/mp.sqrt(3)
w=b*k/(4*mp.pi**2)
quad_at_node=w*mp.fsum(1/(4*(1+(q-node)**2)**mp.mpf('2.5')) for q in [-node,node])
quad_at_zero=w*mp.fsum(1/(4*(1+q*q)**mp.mpf('2.5')) for q in [-node,node])
z_disc_node=1+susceptibility(b)-e2*quad_at_node
z_disc_zero=1+susceptibility(b)-e2*quad_at_zero
z_cont_min=1+susceptibility(b)-e2*coeff(k,0,b)
check('discrete_transfer_counterexample',z_disc_node<0 and z_disc_zero>0 and z_cont_min>0,
      discrete_Z_at_node=text(z_disc_node),discrete_Z_at_zero=text(z_disc_zero),exact_integral_min_Z=text(z_cont_min), susceptibility=text(susceptibility(b)), parameters={'b':10,'N':0,'K':200,'nK':2})

# Distinguish the three cutoff operations; modest numbers show trends only.
sequence=[]
for n in [4,16,64,256,1024]:
    k=mp.sqrt(1+2*b*n)
    c=coeff(k,n,b)
    harmonic=mp.fsum((1 if j==0 else 2)/(1+2*b*j) for j in range(n+1))
    low=b/(4*mp.pi**2)*5/(12*mp.sqrt(2))*harmonic
    sequence.append({'N':n,'K':text(k),'e2C':text(e2*c),'lower_bound_e2C':text(e2*low),'Z':text(1+susceptibility(b)-e2*c)})
    check('cofinal_lower_bound_'+str(n),c>=low,e2C=text(e2*c),e2_lower=text(e2*low))
check('cofinal_coefficient_increases',all(mp.mpf(sequence[i]['e2C'])<mp.mpf(sequence[i+1]['e2C']) for i in range(len(sequence)-1)))
check('finite_display_is_not_zero_crossing',all(mp.mpf(r['Z'])>0 for r in sequence), note='Asymptotic obstruction is analytic; no sampled zero crossing claimed.')

# The fixed-K series converges, while a joint limit diverges.
fixed_k=mp.mpf(20)
cs=[coeff(fixed_k,n,b) for n in [4,32,256,2048]]
check('fixed_K_partial_sums_bound',all(e2*c<mp.mpf(new.numerator)/new.denominator for c in cs), e2C=[text(e2*c) for c in cs], rational_bound=str(new))
check('fixed_N_longitudinal_limit',abs(coeff(mp.mpf('1e5'),4,b)-coeff_infty_sum(4,b))<mp.mpf('1e-14'))

# Exact stationary-vacuum tangent energy; independent of a nonlinear family extension.
u,q,z0,ee,ww,ex,ey,ez,ff=sp.symbols('u q z0 ee ww ex ey ez ff',real=True)
p0=sp.symbols('p0',real=True)
omega=sp.sqrt(M*M+p0*p0)
h=sp.Matrix([M,0,p0])
t=sp.Matrix([0,0,1])/omega-p0*h/omega**3
eta=sp.Matrix([ex,ey,ez])
svec=eta+q*t
sdot=2*h.cross(svec)+u*t
udot=(ff-ee*ww*svec[2])/z0
qenergy_dot=2*z0*u*udot+2*ee*ww*omega*svec.dot(sdot)
expected=2*u*ff-2*ee*ww*u*p0*h.dot(eta)/omega**2
check('equilibrium_energy_general_residual',sp.simplify(qenergy_dot-expected)==0)
check('equilibrium_tangent_plane_work',sp.simplify((qenergy_dot-2*u*ff).subs(ex,-p0*ez/M))==0)
check('equilibrium_tangent_plane_preserved',sp.simplify(h.dot(2*h.cross(svec)))==0)
check('equilibrium_wrong_shift_detected',sp.simplify((2*z0*u*udot+2*ee*ww*omega*(eta-q*t).dot(2*h.cross(svec)-u*t)-2*u*ff).subs(ex,-p0*ez/M))!=0)
# An exact secular mode: field and shifted quantum tangent stay bounded, raw eta grows.
time=sp.symbols('time',real=True)
h1=sp.Matrix([1,0,0]); r1=-h1
eta1=sp.Matrix([0,-sp.Rational(1,2),-time]); q1=time
eta_rhs=2*h1.cross(eta1)+2*sp.Matrix([0,0,q1]).cross(r1)
check('stationary_secular_eta_solution',sp.simplify(eta1.diff(time)-eta_rhs)==sp.zeros(3,1))
check('stationary_secular_maxwell_solution',sp.simplify(eta1[2]+q1)==0)
check('stationary_secular_bounded_energy',sp.simplify(sp.Rational(3,4)+(eta1+sp.Matrix([0,0,q1])).dot(eta1+sp.Matrix([0,0,q1]))-1)==0, exact_Q='1', raw_eta_norm_squared='t^2+1/4', field_tangent='1')

# Bounded exact-matrix and numerical propagator check requested before promotion.
Amat=sp.Matrix([[0,0,-sp.Rational(4,3)],[0,0,-2],[1,2,0]])
Gmat=sp.diag(sp.Rational(3,4),1,1)
check('equilibrium_matrix_weighted_skew',Amat.T*Gmat+Gmat*Amat==sp.zeros(3,3))
import numpy as np
from scipy.linalg import expm
An=np.array(Amat,dtype=float); Gn=np.array(Gmat,dtype=float)
y0=np.array([0.3,-0.2,0.4]); Q0=float(y0@Gn@y0)
propagator=[]
for st in [0.0,0.3,1.0,10.0]:
    yn=expm(st*An)@y0
    Qn=float(yn@Gn@yn)
    propagator.append({'t':st,'u':float(yn[0]),'s_y':float(yn[1]),'s_z':float(yn[2]),'Q':Qn,'relative_Q_defect':abs(Qn-Q0)/Q0})
maxdef=max(r['relative_Q_defect'] for r in propagator)
check('equilibrium_matrix_propagator',maxdef<5e-13, maximum_relative_Q_defect=maxdef, threshold=5e-13, samples=propagator, exact_initial_Q='107/400')

# Existing field envelope applies to the archived samples but this is not an ODE rerun.
accept=json.loads((HERE.parent/'round4'/'physics_acceptance.json').read_text())
mx=accept['observable_summary']['x']['maximum_sampled']
check('archived_field_below_analytic_envelope',mx<4/3, archived_max=mx, envelope='4/3', data_source='round4/physics_acceptance.json', no_trajectory_rerun=True)

output={'schema':'qeg-round6-independent-skeptic-checks-v1','date':'2026-09-09','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'production_solver_imported':False,'arithmetic':{'symbolic':'SymPy','rational':'fractions.Fraction','numerical_precision_decimal_digits':mp.mp.dps,'numerical_interval_enclosure':False},'checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),'all_passed':all(c['passed'] for c in checks),'cofinal_sequence':sequence,'scope':'Algebraic certificates, high-precision identity comparisons, and counterexamples. Does not prove continuum QED, time integration error, or an actual physical pole.'}
(HERE/'skeptic_checks_results.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({'passed':output['passed'],'total':output['total'],'all_passed':output['all_passed'],'failed':[c['id'] for c in checks if not c['passed']]},indent=2))
if not output['all_passed']:
    raise SystemExit(1)
