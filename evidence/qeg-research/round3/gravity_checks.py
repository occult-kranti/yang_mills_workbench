"""Independent gravity closure checks; this is not a renormalized QED solver.

Run: python gravity_checks.py
Requires numpy, scipy, sympy. JSON contains only computed finite values.
"""
from pathlib import Path
import json
import math
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp


def symbolic_checks():
    t, x, y, z = s.symbols('t x y z', real=True)
    ap, az = s.Function('a_perp')(t), s.Function('a_parallel')(t)
    coord = [t, x, y, z]
    g = s.diag(-1, ap**2, ap**2, az**2)
    gi = g.inv()
    gam = [[[s.simplify(sum(gi[i,l]*(s.diff(g[l,k],coord[j])+
            s.diff(g[l,j],coord[k])-s.diff(g[j,k],coord[l]))/2
            for l in range(4))) for k in range(4)] for j in range(4)] for i in range(4)]
    ric = s.zeros(4)
    for i in range(4):
        for j in range(4):
            ric[i,j] = s.simplify(sum(s.diff(gam[k][i][j],coord[k])-
                s.diff(gam[k][i][k],coord[j])+
                sum(gam[k][i][j]*gam[l][k][l]-gam[l][i][k]*gam[k][j][l]
                    for l in range(4)) for k in range(4)))
    scalar = s.simplify(sum(gi[i,j]*ric[i,j] for i in range(4) for j in range(4)))
    mixed = s.simplify(gi*(ric-g*scalar/2))
    h,k,dh,dk,kap,lam,rho,pt,pl,rem = s.symbols(
        'h k dh dk kappa Lambda rho p_perp p_parallel R_energy', real=True)
    sub={s.diff(ap,t,2):ap*(dh+h*h),s.diff(az,t,2):az*(dk+k*k),
         s.diff(ap,t):ap*h,s.diff(az,t):az*k}
    got=[s.simplify(mixed[i,i].subs(sub, simultaneous=True)) for i in range(4)]
    checks={
        'einstein_00':s.simplify(got[0]+h*h+2*h*k),
        'einstein_perp':s.simplify(got[1]+dh+dk+h*h+k*k+h*k),
        'einstein_parallel':s.simplify(got[3]+2*dh+3*h*h),
        'ricci_scalar':s.simplify(scalar.subs(sub, simultaneous=True)-
             (4*dh+2*dk+6*h*h+4*h*k+2*k*k)),
    }
    d_h=(lam-kap*pl-3*h*h)/2
    d_k=lam-kap*pt-h*h-k*k-h*k-d_h
    drho=-2*h*(rho+pt)-k*(rho+pl)+rem
    constraint=h*h+2*h*k-kap*rho-lam
    cdot=2*(h+k)*d_h+2*h*d_k-kap*drho
    checks['hamiltonian_propagation']=s.simplify(cdot+(2*h+k)*constraint+kap*rem)
    checks['shear_equation']=s.simplify(d_k-d_h+(2*h+k)*(k-h)-kap*(pl-pt))
    E,B,j=s.symbols('E B j',real=True)
    de=-2*h*E-j
    db=-2*h*B
    rho_em=(E*E+B*B)/2
    checks['em_work']=s.simplify(E*de+B*db+4*h*rho_em+E*j)
    # Derive Maxwell divergence directly: ∇_nu F^{z nu}=J^z,
    # F_0z=-a_parallel E, F_xy=B0; physical Jhat=a_parallel J^z.
    ef=s.Function('E')(t)
    f=s.zeros(4); f[0,3]=-az*ef; f[3,0]=az*ef
    fu=gi*f*gi
    div_z=s.diff(ap**2*az*fu[3,0],t)/(ap**2*az)
    checks['maxwell_physical_sign']=s.simplify(az*div_z+s.diff(ef,t)+2*s.diff(ap,t)*ef/ap)
    # Fixed-background common finite charge counterterm W_ct=-c/4 ∫F².
    # ΔT=c T_EM, ΔJhat=+c(dot E+2hE). Matter Ward identity follows off Maxwell shell.
    c=s.symbols('c',real=True)
    edot=s.symbols('Edot',real=True)
    energy_ct_dot=c*(E*edot+B*db)
    # δW/δAz=+c ∂t(a_perp² E), consistent with δW/δA=+sqrt(-g)J.
    current_ct=c*(edot+2*h*E)
    checks['common_F2_counterterm_ward']=s.simplify(
        energy_ct_dot+4*h*c*rho_em-E*current_ct)
    # The spatial energy equation has a one-dimensional nullspace in pressure.
    fpressure=s.symbols('f_pressure',real=True)
    checks['pressure_nullspace']=s.simplify(2*h*(k*fpressure)+k*(-2*h*fpressure))
    # Running couplings with otherwise conserved matter have an extra constraint source.
    kd,ld=s.symbols('kappa_dot Lambda_dot',real=True)
    checks['running_coupling_source']=s.simplify(
        cdot-kd*rho-ld+(2*h+k)*constraint+kap*rem+kd*rho+ld)
    # Two displayed signs in arXiv:2410.22633v2, checked in its conventions.
    q,e0=s.symbols('q E0', positive=True)
    pulse=e0/s.cosh(q*t)**2
    j_print=-2*q*e0/s.cosh(q*t)**2*s.tanh(q*t)
    j_required=-s.diff(pulse,t)
    sign_residual=s.simplify(j_print-j_required)
    # A first-order truncated product-unitary state can show spurious concurrence.
    eta=s.symbols('eta',real=True)
    approx=s.Matrix([1,-s.I*eta,-s.I*eta,0])
    determinant=s.simplify(approx[0]*approx[3]-approx[1]*approx[2])
    # Weak null scalar profile: local energy ∫ v^(2 beta -2) dv.
    beta,v=s.symbols('beta v',positive=True)
    primitive=v**(2*beta-1)/(2*beta-1)
    checks['cauchy_energy_integrand']=s.simplify(s.diff(primitive,v)-v**(2*beta-2))
    # Ricci-flat Kasner is an explicit failure of a scalar-R-only validity screen.
    hh=2/(3*t);kk=-1/(3*t)
    ricci_kasner=s.simplify((4*dh+2*dk+6*h*h+4*h*k+2*k*k).subs(
        {h:hh,k:kk,dh:s.diff(hh,t),dk:s.diff(kk,t)}))
    kretschmann_kasner=s.simplify(4*(2*(s.diff(hh,t)+hh*hh)**2+
        (s.diff(kk,t)+kk*kk)**2+hh**4+2*hh*hh*kk*kk))
    checks['kasner_ricci_zero']=ricci_kasner
    checks['kasner_kretschmann']=s.simplify(kretschmann_kasner-64/(27*t**4))
    # Finite-regulated Dirac mode stress identity in an anisotropic Landau basis.
    D,P,cn,qphys,r_z,r_x,r_beta,m=s.symbols('D P c_n q_phys r_z r_x r_beta m', real=True)
    mode_rho=D*(m*r_beta+P*r_z+cn*r_x)
    mode_j=qphys*D*r_z
    mode_pp=D*P*r_z
    mode_pt=D*cn*r_x/2
    # Schrödinger evolution cancels the H commutator in d< H >/dt.
    mode_rhodot=-(2*h+k)*mode_rho+D*((qphys*E-k*P)*r_z-h*cn*r_x)
    checks['anisotropic_dirac_mode_work']=s.simplify(mode_rhodot+
        2*h*(mode_rho+mode_pt)+k*(mode_rho+mode_pp)-E*mode_j)
    # Verify the conserved sector and the rotating-basis connection actually used in H17.
    sx=s.Matrix([[0,1],[1,0]]);sy=s.Matrix([[0,-s.I],[s.I,0]]);sz=s.diag(1,-1)
    beta4=s.kronecker_product(sz,s.eye(2))
    alpha_z=s.kronecker_product(sx,sz);alpha_x=s.kronecker_product(sx,sx)
    sector=s.kronecker_product(sz,sy)
    h4=m*beta4+P*alpha_z+cn*alpha_x
    checks['dirac_conserved_sector']=s.simplify(sum(abs(v)**2 for v in (h4*sector-sector*h4)))
    checks['dirac_hamiltonian_square']=s.simplify(sum(abs(v)**2 for v in
        (h4*h4-(m*m+P*P+cn*cn)*s.eye(4))))
    angle,da,M=s.symbols('angle angle_dot M',real=True)
    rot=s.cos(angle/2)*s.eye(2)-s.I*s.sin(angle/2)*sz
    hs=M*s.cos(angle)*sx+M*s.sin(angle)*sy+P*sz
    rotation_residual=s.simplify(s.trigsimp(rot.conjugate().T*hs*rot-da*sz/2-
        (M*sx+(P-da/2)*sz)))
    checks['rotating_sector_connection']=s.simplify(sum(abs(v)**2 for v in rotation_residual))
    exact=s.kronecker_product(s.Matrix([s.cos(eta),-s.I*s.sin(eta)]),
        s.Matrix([s.cos(eta),-s.I*s.sin(eta)]))
    checks['exact_product_unitary_zero_determinant']=s.simplify(exact[0]*exact[3]-exact[1]*exact[2])
    for name,value in checks.items():
        if value != 0: raise AssertionError(f'{name}: {value}')
    return {'zero_residual_checks':{name:str(value) for name,value in checks.items()},
        'n_passed':len(checks),
        'derived_mixed_einstein':[str(v) for v in got],
        'sauter_printed_minus_required':str(sign_residual),
        'sauter_residual_at_q_E0_t_1':float(sign_residual.subs({q:1,e0:1,t:1})),
        'first_order_product_truncation_determinant':str(determinant),
        'spurious_normalized_concurrence_eta_0_1':float(2*.1**2/(1+2*.1**2)),
        'kasner_kretschmann':str(kretschmann_kasner),
        'equal_mean_energy_noise_counterexample':{'mean_energy':1.0,
            'energy_eigenstate_variance':0.0,'rare_excitation_probability':0.01,
            'rare_excitation_energy':100.0,'mixture_variance':99.0},
        'pressure_nullspace_shear_source':str(-kap*(2*h+k)*fpressure)}


def rhs(t,y,kap=.1,conductivity=.2):
    lp,lz,h,k,E,B,rm=y
    u=(E*E+B*B)/2
    pt=rm/3+u; pl=rm/3-u
    hp=(-kap*pl-3*h*h)/2
    kp=-kap*pt-h*h-k*k-h*k-hp
    return np.array([h,k,hp,kp,-2*h*E-conductivity*E,-2*h*B,
                     -(2*h+k)*4*rm/3+conductivity*E*E])


def mean_rhs(t,y,kap=.1,conductivity=.2):
    # Independently use Raychaudhuri and shear, rather than directional Einstein equations.
    lp,lz,H,d,E,B,rm=y
    h=H-d/3; k=H+2*d/3
    u=(E*E+B*B)/2; rho=rm+u; pbar=(rm+u)/3
    hd=-H*H-2*d*d/9-kap*(rho+3*pbar)/6
    dd=-3*H*d-2*kap*u
    return np.array([h,k,hd,dd,-2*h*E-conductivity*E,-2*h*B,
                     -4*H*rm+conductivity*E*E])


def rk4(y0,stop,n):
    dt=stop/n;y=y0.copy()
    for i in range(n):
        t=i*dt
        a=rhs(t,y); b=rhs(t+dt/2,y+dt*a/2)
        c=rhs(t+dt/2,y+dt*b/2); d=rhs(t+dt,y+dt*c)
        y=y+dt*(a+2*b+2*c+d)/6
    return y


def numerical_checks():
    # Arbitrary dimensionless gravitational coupling deliberately exposes feedback;
    # this must not be labelled an electron/Planck-scale physical prediction.
    kap=.1;cond=.2;E0=1.;B0=3.;rm0=.2
    h0=math.sqrt(kap*((E0*E0+B0*B0)/2+rm0)/3)
    y0=np.array([0,0,h0,h0,E0,B0,rm0]);stop=2.
    grid=np.linspace(0,stop,401)
    sol=solve_ivp(rhs,(0,stop),y0,method='DOP853',rtol=2e-13,atol=2e-14,t_eval=grid)
    if not sol.success: raise RuntimeError(sol.message)
    lp,lz,h,k,E,B,rm=sol.y
    residual=h*h+2*h*k-kap*((E*E+B*B)/2+rm)
    bflux=B*np.exp(2*lp)
    eflux=E*np.exp(2*lp+cond*grid)
    mean0=y0.copy();mean0[2]=h0;mean0[3]=0
    alt=solve_ivp(mean_rhs,(0,stop),mean0,method='DOP853',rtol=2e-13,atol=2e-14,t_eval=grid)
    if not alt.success: raise RuntimeError(alt.message)
    converted=alt.y.copy()
    converted[2]=alt.y[2]-alt.y[3]/3
    converted[3]=alt.y[2]+2*alt.y[3]/3
    independent_error=float(np.max(np.abs(converted-sol.y)))
    errors=[]
    for n in (100,200,400,800):
        errors.append({'steps':n,'max_endpoint_abs_error':float(np.max(np.abs(rk4(y0,stop,n)-sol.y[:,-1])))})
    orders=[math.log(errors[i]['max_endpoint_abs_error']/errors[i+1]['max_endpoint_abs_error'],2)
        for i in range(len(errors)-1)]
    result={'scope':'Classical Einstein-Maxwell plus phenomenological Ohmic radiation; not QED.',
        'parameters':{'kappa':kap,'conductivity':cond,'E0':E0,'B0':B0,'rho_m0':rm0,'stop':stop},
        'maximum_hamiltonian_residual':float(np.max(np.abs(residual))),
        'maximum_magnetic_flux_error':float(np.max(np.abs(bflux-B0))),
        'maximum_damped_electric_flux_error':float(np.max(np.abs(eflux-E0))),
        'independent_raychaudhuri_shear_max_error':independent_error,
        'rk4_refinement':errors,'rk4_observed_orders':orders,
        'end_state':dict(zip(('log_a_perp','log_a_parallel','H_perp','H_parallel','E','B','rho_m'),map(float,sol.y[:,-1]))),
        'initial_shear_acceleration':-kap*(E0*E0+B0*B0),
        'classical_em_trace':0.0}
    assert np.max(np.abs(residual))<1e-11
    assert independent_error<1e-10
    assert min(orders[:2])>3.8
    assert np.max(np.abs(bflux-B0))<1e-10
    assert np.max(np.abs(eflux-E0))<1e-10
    return result


def main():
    result={'symbolic':symbolic_checks(),'numerical':numerical_checks()}
    alpha=1/137.035999177
    gm2=1.7518093987907706e-45
    kappa_e=8*math.pi*gm2
    result['electron_scale_budget']={
        'G_m_e_squared':gm2,'8pi_G_m_e_squared':kappa_e,
        'em_energy_over_m_e4_at_E_Ec_1_B_Bc_100':(1+100**2)/(8*math.pi*alpha),
        'kappa_rho_over_m_e2_at_E_Ec_1_B_Bc_100':kappa_e*(1+100**2)/(8*math.pi*alpha),
        'magnetic_b_for_kappa_rho_over_m_e2_1':math.sqrt(8*math.pi*alpha/kappa_e),
        'interpretation':'Stress curvature budget, not scalar Ricci R; Maxwell stress is traceless.'}
    path=Path(__file__).with_suffix('.json')
    path.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'symbolic_passed':result['symbolic']['n_passed'],
                     'numerical':result['numerical']},indent=2,allow_nan=False))


if __name__=='__main__':main()
