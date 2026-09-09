"""Independent round-three checks; never imports the production solver.

This verifier uses direct two-state spinor evolution, exact spectral-flow
integrals and elementary analytical invariants. Numerical agreement is an
empirical check, not an interval-arithmetic certificate.
"""
from pathlib import Path
import json, math, hashlib, sys
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.special import digamma, polygamma

ROOT = Path(__file__).resolve().parent
SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]], complex)
SZ = np.diag([1., -1.]).astype(complex)


def sector_number(eta=1., K=0., b=10., n=1, aE=1., Tg=.5,
                  TE=1., L=16., rtol=2e-12, atol=2e-14, max_step=.05):
    """Separate implementation of fixed-sector Hamiltonian and overlap."""
    bound = L*max(1., Tg, TE)
    c = math.sqrt(2*b*n)
    output = []
    for spin in (-1, 1):
        def h(s):
            a = 1 + eta*(1 + math.tanh(s/Tg))/2
            p = K + aE*TE*math.tanh(s/TE)
            return p*SZ + a*SX - spin*c*SY
        _, initial_basis = np.linalg.eigh(h(-bound))
        initial = initial_basis[:, 0]
        solution = solve_ivp(lambda s,y: -1j*h(s)@y, (-bound,bound), initial,
                             method='DOP853', rtol=rtol, atol=atol, max_step=max_step)
        if not solution.success:
            raise RuntimeError(solution.message)
        _, final_basis = np.linalg.eigh(h(bound))
        y = solution.y[:, -1]
        N = float(abs(np.vdot(final_basis[:, 1], y))**2)
        norm = float(np.vdot(y,y).real)
        output.append({'N':N, 'normalized_N':N/norm, 'norm_error':abs(norm-1)})
    return {'sum': sum(x['N'] for x in output),
            'normalized_sum':sum(x['normalized_N'] for x in output), 'sectors':output}


def occupations_audit():
    # K=0 spinor Sauter formula simplifies, avoiding any production implementation.
    omega = math.sqrt(22.)
    exact_two_spins = 2*(math.sinh(math.pi)/math.sinh(math.pi*omega))**2
    flat = sector_number(eta=0.)
    # E=0 expansion-only Hamiltonian has longitudinal a_g=1.5+.5*tanh(2s).
    # A fixed unitary maps it to another exactly solvable Sauter system.
    wi,wo=math.sqrt(21.),math.sqrt(24.)
    T=.5
    exact_expansion=(math.cosh(2*math.pi*.5*T)-math.cosh(math.pi*T*(wo-wi)))/(math.sinh(math.pi*T*wi)*math.sinh(math.pi*T*wo))
    expansion=sector_number(aE=0., rtol=2e-13, atol=2e-15)
    runs = []
    for L, tol in [(4.,2e-12), (8.,2e-12), (12.,2e-12),
                   (16.,2e-12), (16.,2e-13), (20.,2e-13)]:
        data = sector_number(L=L, rtol=tol, atol=tol/100)
        runs.append({'L':L, 'rtol':tol, **data})
    # Normalization cannot certify direction: both vectors have exact unit norm.
    tilt = 1e-3
    exact_state = np.array([0.,1.])
    wrong_state = np.array([math.sin(tilt),math.cos(tilt)])
    directional_counterexample = {
        'norm_residual':abs(float(wrong_state@wrong_state)-1),
        'occupation_error':float(wrong_state[0]**2),
        'state_error_norm':float(np.linalg.norm(wrong_state-exact_state))}
    # A radially scaled exact eigenstate has norm error but still zero occupation.
    radial = (1+1e-6)*exact_state
    radial_counterexample = {'norm_residual':float(radial@radial-1),
                            'occupation_error':float(radial[0]**2)}
    # Static Hamiltonians are exact no-production cases. Projector subtraction
    # can produce O(eps) signed answers; a direct overlap remains nonnegative.
    cancellations = []
    for p,m,c in [(1.,1.,math.sqrt(200)),(.13,.7,math.sqrt(20)),(9.,.2,1.1)]:
        h = p*SZ + m*SX + c*SY
        eig,v = np.linalg.eigh(h)
        y = np.exp(1j*eig[1]*7)*v[:,0]
        projector = .5*(np.eye(2)+h/eig[1])
        cancellations.append({'p':p,'m':m,'c':c,
            'true_N':0.,'projector_N':float(np.vdot(y,projector@y).real),
            'overlap_N':float(abs(np.vdot(v[:,1],y))**2)})
    old = json.loads((ROOT/'evidence/prior_curved_sector_results.json').read_text())
    old_flat = old['cases'][0]
    return {'flat_exact_two_spins':exact_two_spins,'independent_flat':flat,
            'expansion_only_exact_two_spins':exact_expansion,
            'independent_expansion_only':expansion,
            'expansion_only_abs_error':abs(expansion['sum']-exact_expansion),
            'independent_flat_abs_error':abs(flat['sum']-exact_two_spins),
            'old_full_flat_abs_error':abs(old_flat['full_4x4_occupation']-exact_two_spins),
            'old_full_flat_relative_error':abs(old_flat['full_4x4_occupation']/exact_two_spins-1),
            'old_sector_flat_abs_error':abs(old_flat['sector_sums']['rotated']-exact_two_spins),
            'end_time_and_tolerance_runs':runs,
            'unit_norm_wrong_direction':directional_counterexample,
            'wrong_norm_exact_direction':radial_counterexample,
            'projector_cancellation_zero_production':cancellations}


def finite_window_and_response_checks():
    # Direct quadratures independently verify the finite-window boundary term,
    # C'(a) and the B->0 weak-frequency vacuum-polarization coefficient.
    M,A,K=1.,1.,2.
    numerical=quad(lambda k:(k-A)/math.sqrt((k-A)**2+M*M),-K,K,epsabs=1e-13)[0]
    analytic=math.sqrt((K-A)**2+M*M)-math.sqrt((-K-A)**2+M*M)
    x=.7
    C=lambda aa:quad(lambda k:M*M/(4*((k-aa)**2+M*M)**2.5),-K,K,epsabs=1e-13)[0]
    D=quad(lambda k:5*M*M*(k-A)/(8*((k-A)**2+M*M)**3.5),-K,K,epsabs=1e-13)[0]
    da=1e-4
    C_a=(-C(A+2*da)+8*C(A+da)-8*C(A-da)+C(A-2*da))/(12*da)
    # p'=x and a'=-x, hence C'=-x*dC/da=-2Dx.
    derivative_residual=-x*C_a+2*D*x
    # Removing the vacuum term S_vac from S in Maxwell makes W'-xF=e² x S_vac.
    e2=4*math.pi/137.035999084
    t_integral=quad(lambda t:16/(15*t*t),1,math.inf,epsabs=1e-13)[0]
    # Also check longitudinal reduction at three independent transverse masses.
    longitudinal=[]
    for mass2 in [1.,2.,10.]:
        value=quad(lambda k:mass2/(k*k+mass2)**3.5,-math.inf,math.inf,epsabs=1e-13)[0]
        longitudinal.append({'M2':mass2,'quadrature':value,'exact':16/(15*mass2**2)})
    computed=e2*t_integral/(64*math.pi**2)
    expected=e2/(60*math.pi**2)
    # Direct low-frequency longitudinal quadrature at b=10, evaluated without
    # substituting its analytic k integral. The remaining n-tail is explicit.
    b=10.; n=np.arange(8193); masses2=1+2*b*n; degeneracy=np.where(n==0,1.,2.)
    nn,ww=np.polynomial.legendre.leggauss(96)
    theta=nn*math.pi/2; wtheta=ww*math.pi/2; ct=np.cos(theta)
    coefficients=[]
    for nu in [.01,.02,.04]:
        kernels=ct[None,:]**5/(4*masses2[:,None]*(4*masses2[:,None]-nu*nu*ct[None,:]**2))
        measured=e2*b/(4*math.pi**2)*float(degeneracy@(kernels@wtheta))
        coefficients.append({'nu':nu,'delta_chi_over_nu_squared':measured})
    fit=np.polynomial.polynomial.polyfit([row['nu']**2 for row in coefficients],
        [row['delta_chi_over_nu_squared'] for row in coefficients],2)[0]
    finite_exact=e2*b/(60*math.pi**2)*float(np.sum(degeneracy/masses2**2))
    infinite_exact=e2*b/(60*math.pi**2)*(1+float(polygamma(1,1+1/(2*b)))/(2*b*b))
    return {'finite_window_vacuum_integral':numerical,'endpoint_formula':analytic,
            'finite_window_identity_error':abs(numerical-analytic),
            'C_time_derivative_identity_error':abs(derivative_residual),
            'missing_vacuum_term_energy_residual_without_density_weight':e2*x*numerical,
            'B_zero_nu_squared_coefficient_quadrature':computed,
            'B_zero_nu_squared_coefficient_exact':expected,
            'B_zero_coefficient_abs_error':abs(computed-expected),
            'longitudinal_quadrature_checks':longitudinal,
            'finite_B_frequency_quadrature':{'b':b,'ncut':8192,'theta_nodes':96,
                'coefficients':coefficients,'nu_squared_extrapolated':float(fit),
                'finite_sum_analytic':finite_exact,'extrapolation_abs_error':abs(float(fit)-finite_exact),
                'infinite_landau_trigamma_reference':infinite_exact,
                'omitted_landau_tail_in_coefficient':infinite_exact-finite_exact},
            'scope':'coefficients and finite regulator identities, not continuum causal closure'}


def independent_spinor_backreaction(a0=0., translate_window=True,
                                    remove_vacuum_term=False):
    """Couple wavefunctions to Maxwell; production uses Bloch vectors instead.

    Finite shared quadrature is intentional for an implementation comparison.
    Integrated pump work is an additional ODE, not a trapezoidal postprocess.
    """
    b,ncut,Kmax,nK,Tpump,tfinal=10.,2,6.,32,4.,8.
    e2=4*math.pi/137.035999084
    chi=e2/(12*math.pi**2)*(b-math.log(2*b)-digamma(1+1/(2*b)))
    nodes,weights=np.polynomial.legendre.leggauss(nK)
    k=np.concatenate([Kmax*nodes+(a0 if translate_window else 0.) for n in range(ncut+1)])
    mass=np.concatenate([np.full(nK,math.sqrt(1+2*b*n)) for n in range(ncut+1)])
    w=np.concatenate([weights*Kmax*b*(1 if n==0 else 2)/(4*math.pi**2) for n in range(ncut+1)])
    norm=quad(lambda u: math.exp(-1/(u*(1-u))) if 0<u<1 else 0.,0,1,epsabs=1e-14)[0]
    def force(t):
        u=t/Tpump
        return math.exp(-1/(u*(1-u)))/(Tpump*norm) if 0<u<1 else 0.
    p0=k-a0
    omega0=np.sqrt(mass**2+p0**2)
    # Stable negative eigenvectors of [[p,M],[M,-p]]; m is strictly positive.
    theta=np.arctan2(mass,p0)
    initial=np.array([-np.sin(theta/2),np.cos(theta/2)],complex)
    state=np.concatenate(([a0,0.,0.],initial.ravel()))
    def quantities(t,y):
        aa,xx=y[0].real,y[1].real
        v=y[3:].reshape(2,-1)
        p=k-aa
        om=np.sqrt(mass*mass+p*p)
        rz=abs(v[0])**2-abs(v[1])**2
        rx=2*(v[0].conj()*v[1]).real
        vacuum=p/om
        S=float(w@(rz+(0 if remove_vacuum_term else vacuum)))
        C=float(w@(mass*mass/(4*om**5)))
        D=float(w@(5*mass*mass*p/(8*om**7)))
        Z=1+chi-e2*C
        return aa,xx,v,p,om,rz,rx,S,C,D,Z
    def derivative(t,y):
        aa,xx,v,p,om,rz,rx,S,C,D,Z=quantities(t,y)
        if Z<=0: raise RuntimeError('nonpositive matched kinetic coefficient')
        dv=-1j*np.array([p*v[0]+mass*v[1],mass*v[0]-p*v[1]])
        return np.concatenate(([-xx,(force(t)-e2*(S+D*xx*xx))/Z,xx*force(t)],dv.ravel()))
    times=np.linspace(0,tfinal,81)
    result=solve_ivp(derivative,(0,tfinal),state,method='DOP853',rtol=2e-10,atol=2e-12,
                     max_step=.02,t_eval=times)
    if not result.success: raise RuntimeError(result.message)
    energies=[]; norm_errors=[]
    for t,y in zip(times,result.y.T):
        aa,xx,v,p,om,rz,rx,S,C,D,Z=quantities(t,y)
        energies.append(Z*xx**2/2+e2*float(w@(mass*rx+p*rz+om)))
        norm_errors.append(float(np.max(abs(np.sum(abs(v)**2,axis=0)-1))))
    work=result.y[2].real
    energy=np.array(energies)
    return {'parameters':{'b':b,'ncut':ncut,'Kmax':Kmax,'nK':nK,'Tpump':Tpump,
                'tfinal':tfinal,'target_E':1.,'a0':a0,'rtol':2e-10,'atol':2e-12,'max_step':.02},
            't':times.tolist(),'a_minus_a0':(result.y[0].real-a0).tolist(),
            'E':result.y[1].real.tolist(),'energy':energy.tolist(),'pump_work':work.tolist(),
            'max_energy_work_residual':float(np.max(abs(energy-energy[0]-work))),
            'max_spinor_norm_error':max(norm_errors),'translate_window':translate_window,
            'remove_vacuum_term':remove_vacuum_term}


def spectral_flow_integral(A, A0, window=(-10.,10.)):
    """Exact piecewise integral of r_z + sgn(k-A) for massless LLL.

    For the initially filled negative branch r_z=-sgn(k-A0), the state does
    not rotate. Kinetic-vacuum subtraction is required before integration.
    """
    lo,hi=window
    def sign_integral(center):
        split=min(max(center,lo),hi)
        return hi+lo-2*split
    return sign_integral(A)-sign_integral(A0)


def massless_reference():
    # lambda=e^2 |eB|/(4 pi^2 mu^2), tau=mu*t. Exact J=-2 lambda(A-A0).
    coupling=.1
    omega=math.sqrt(2*coupling)
    e0=1.
    sol=solve_ivp(lambda t,y: [-y[1], 2*coupling*y[0]],(0.,20.),[0.,e0],
                  rtol=2e-12,atol=2e-14,method='DOP853',dense_output=True)
    t=np.linspace(0,20,1001)
    aa,ee=sol.sol(t)
    exact_A=-e0/omega*np.sin(omega*t)
    exact_E=e0*np.cos(omega*t)
    energy=.5*ee**2+coupling*aa**2
    examples=[]
    for A0,A in [(0.,.7),(.3,-1.1),(0.,4.)]:
        original=spectral_flow_integral(A,A0,(-3.,3.))
        C=7.3
        translated=spectral_flow_integral(A+C,A0+C,(-3.+C,3.+C))
        incorrectly_untranslated=spectral_flow_integral(A+C,A0+C,(-3.,3.))
        examples.append({'A0':A0,'A':A,'finite_integral':original,
                         'infinite_window_answer':-2*(A-A0),
                         'translated_gauge_integral':translated,
                         'incorrect_fixed_window_gauge_integral':incorrectly_untranslated})
    return {'lambda':coupling,'omega_squared':2*coupling,
            'A_max_error':float(np.max(abs(aa-exact_A))),
            'E_max_error':float(np.max(abs(ee-exact_E))),
            'max_energy_drift':float(np.max(abs(energy-energy[0]))),
            'gauge_and_window_counterexamples':examples,
            'meaning':'analytical massless LLL anomaly benchmark, not finite-mass 4D current closure'}


def compact_small_mass_bound():
    # Duhamel estimate for arbitrary real prescribed p(t), unit Bloch norm,
    # finite time T, and exact massive negative-energy initial state at A=0.
    K,T=3.,2.
    rows=[]
    for m in [1e-1,1e-2,1e-3,1e-4,1e-5]:
        bound=4*m*m*T*math.asinh(K/m)+8*K*m*m*T*T
        rows.append({'m':m,'integrated_absolute_change_bound':bound,
                     'bound_divided_by_m':bound/m})
    return {'K':K,'T':T,'rows':rows,
        'scope':'compact momentum region; does not prove uniform UV or long-time expansion'}


def main():
    result={'occupations':occupations_audit(),'massless_reference':massless_reference(),
            'finite_window_and_response':finite_window_and_response_checks(),
            'small_mass_compact_bound':compact_small_mass_bound()}
    result['spinor_backreaction']=independent_spinor_backreaction()
    translated=independent_spinor_backreaction(a0=7.3)
    unshifted=independent_spinor_backreaction(a0=7.3,translate_window=False)
    missing=independent_spinor_backreaction(remove_vacuum_term=True)
    reference=np.array(result['spinor_backreaction']['E'])
    result['spinor_backreaction_gauge_test']={
        'translated_window_max_E_difference':float(np.max(abs(np.array(translated['E'])-reference))),
        'untranslated_window_max_E_difference':float(np.max(abs(np.array(unshifted['E'])-reference))),
        'translated_energy_work_residual':translated['max_energy_work_residual'],
        'missing_vacuum_energy_work_residual':missing['max_energy_work_residual'],
        'missing_vacuum_max_E_difference':float(np.max(abs(np.array(missing['E'])-reference)))}
    result['checks']={
        'flat_exact_reference':result['occupations']['independent_flat_abs_error']<1e-18,
        'expansion_exact_reference':result['occupations']['expansion_only_abs_error']<1e-14,
        'unit_norm_counterexample_detected':result['occupations']['unit_norm_wrong_direction']['occupation_error']>1e-7,
        'massless_exact_oscillator':result['massless_reference']['E_max_error']<1e-9,
        'frequency_coefficient':result['finite_window_and_response']['finite_B_frequency_quadrature']['extrapolation_abs_error']<1e-10,
        'spinor_common_energy_identity':result['spinor_backreaction']['max_energy_work_residual']<2e-8,
        'gauge_translated_grid':result['spinor_backreaction_gauge_test']['translated_window_max_E_difference']<1e-10,
        'wrong_window_detected':result['spinor_backreaction_gauge_test']['untranslated_window_max_E_difference']>1e-4,
        'missing_vacuum_detected':result['spinor_backreaction_gauge_test']['missing_vacuum_energy_work_residual']>1e-2,
        'finite_boundary_integral':result['finite_window_and_response']['finite_window_identity_error']<1e-12}
    result['all_checks_passed']=all(result['checks'].values())
    result['provenance']={'python':sys.version.split()[0], 'numpy':np.__version__,
        'verification_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'prior_evidence_sha256':hashlib.sha256((ROOT/'evidence/prior_curved_sector_results.json').read_bytes()).hexdigest(),
        'production_solver_imported':False,
        'meaning':'empirical finite-grid checks and deliberate falsifiers; no interval certificate'}
    (ROOT/'independent_results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    if not result['all_checks_passed']:
        raise AssertionError(result['checks'])
    print(json.dumps({'flat_error':result['occupations']['independent_flat_abs_error'],
                      'old_flat_relative_error':result['occupations']['old_full_flat_relative_error'],
                      'anomaly_E_error':result['massless_reference']['E_max_error']}))


if __name__=='__main__': main()
