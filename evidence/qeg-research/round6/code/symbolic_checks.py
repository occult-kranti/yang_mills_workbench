"""Exact local algebra supporting the conventional proofs; not a proof assistant."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parent
DEPS=ROOT.parent.parent/'round5/deps'
if DEPS.is_dir():sys.path.insert(0,str(DEPS))
import sympy as s
checks=[]
def zero(name,expr):
 r=s.simplify(expr);checks.append({'name':name,'method':'symbolic identity','residual':str(r),'passed':r==0})
 if r != 0: raise RuntimeError(f'{name}: nonzero residual {r}')
p,M,w,x,F,g,chi=s.symbols('p M w x F g chi',real=True)
rx,ry,rz,ex,ey,ez,q=s.symbols('rx ry rz ex ey ez q',real=True)
r=s.Matrix([rx,ry,rz]);eta=s.Matrix([ex,ey,ez]);h=s.Matrix([M,0,p]);hp=s.Matrix([0,0,q]);om=s.sqrt(M*M+p*p)
rd=2*h.cross(r);ed=2*h.cross(eta)+2*hp.cross(r)
zero('Bloch norm derivative',2*r.dot(rd))
zero('Tangent scalar product derivative',rd.dot(eta)+r.dot(ed))
Ui=w*(h.dot(r)+om);Si=w*(rz+p/om)
zero('One-mode energy source identity',s.diff(Ui,p)*x+sum(s.diff(Ui,z)*dz for z,dz in zip(r,rd))-x*Si)
Ci=w*M*M/(4*om**5);Di=5*w*M*M*p/(8*om**7)
zero('Counterterm time derivative',s.diff(Ci,p)*x+2*Di*x)
zero('Delta S',s.diff(Si,p)*q+s.diff(Si,rz)*ez-w*(ez+M*M*q/om**3))
zero('Delta C',s.diff(Ci,p)*q+5*w*M*M*p*q/(4*om**7))
zero('Delta D',s.diff(Di,p)*q-5*w*M*M*(M*M-6*p*p)*q/(8*om**9))
C,D,S,U,Z=s.symbols('C D S U Z',real=True)
Zd=2*g*D*x;xd=(F-g*(S+D*x*x))/Z
zero('Work identity',Zd*x*x/2+Z*x*xd+g*x*S-x*F)
dF,dC,dD,dS,u=s.symbols('dF dC dD dS u',real=True)
dxd=(dF-g*(dS+dD*x*x+2*D*x*u)+g*dC*xd)/Z
direct=s.diff(xd,F)*dF+s.diff(xd,S)*dS+s.diff(xd,D)*dD+s.diff(xd,x)*u+s.diff(xd,Z)*(-g*dC)
zero('Complete quotient variation',direct-dxd)
dJ=dS-dC*xd-C*dxd+dD*x*x+2*D*x*u+chi*dxd/g
zero('Direct tangent current Maxwell identity',(dxd-dF+g*dJ).subs(Z,1+chi-g*C))
# The differentiated identity follows algebraically from W'=xF and commuting
# partial derivatives of the smooth flow; this substitution checks its RHS.
eps=s.symbols('eps');zero('Differentiated source work',s.diff((x+eps*u)*(F+eps*dF),eps).subs(eps,0)-(u*F+x*dF))
Hp,Hl,rho,pp,pl,k,L,Q=s.symbols('Hp Hl rho pp pl k L Q',real=True)
theta=2*Hp+Hl;constraint=Hp*Hp+2*Hp*Hl-k*rho-L
dHp=(L-k*pl-3*Hp*Hp)/2
dHl=L-k*pp-dHp-Hp*Hp-Hl*Hl-Hp*Hl
drho=Q-2*Hp*(rho+pp)-Hl*(rho+pl)
dconstraint=s.diff(constraint,Hp)*dHp+s.diff(constraint,Hl)*dHl+s.diff(constraint,rho)*drho
zero('Bianchi-I constraint with Ward defect',dconstraint+theta*constraint+k*Q)
E,B,Jq,Je=s.symbols('E B Jq Je',real=True)
rEM=(E*E+B*B)/2;dE=-2*Hp*E-Jq-Je;dB=-2*Hp*B
wardEM=s.diff(rEM,E)*dE+s.diff(rEM,B)*dB+2*Hp*(rEM+rEM)+Hl*(rEM-rEM)
zero('Electromagnetic Ward work',wardEM+E*(Jq+Je))
zero('Quantum plus field external work deficit',wardEM+E*Jq+E*Je)
# Two deliberately wrong identities must not reduce to zero.
mutant_missing_quotient=s.simplify(direct-(dxd-g*dC*xd/Z))
mutant_wrong_Bianchi=s.simplify(dconstraint+2*theta*constraint+k*Q)
for name,res in [('Omit quotient derivative',mutant_missing_quotient),('Use wrong constraint damping factor',mutant_wrong_Bianchi)]:
 if res==0: raise RuntimeError(f'{name}: deliberately wrong identity escaped detection')
 checks.append({'name':name,'method':'deliberate symbolic defect detected','nonzero_defect':str(res),'passed':True})
out={'scope':'Exact symbolic equalities and detected defects. Analytic inequalities, ODE theorem imports and physical validity are separate proof obligations.','sympy_version':s.__version__,'checks':checks,'all_checks_passed':all(c['passed'] for c in checks),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(ROOT.parent/'symbolic_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'passed':out['all_checks_passed'],'symbolic_system':s.__version__}))
