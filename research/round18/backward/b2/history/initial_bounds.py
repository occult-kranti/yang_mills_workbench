"""Independent rational Newton enclosures and full scalar-form bounds."""
from fractions import Fraction as F

PREMISES=('full_physical_complement','exact_subtracted_cross_Gram','complete_orthonormal_P','codimension_one_vacuum_perpendicular','vacuum_energy_upper_zero')


def rational(q):
    if type(q) not in (str,int,F):raise ValueError('exact rational required')
    return F(q)


def int_floor_root(n):
    if type(n) is not int or n<0:raise ValueError('nonnegative exact integer required')
    lo,hi=0,n+1
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid*mid<=n:lo=mid
        else:hi=mid
    return lo


def root_enclosure(q,bits=56):
    q=rational(q)
    if q<0 or type(bits) is not int or not 0<=bits<=128:raise ValueError('nonnegative radicand and bounded exact precision required')
    pn,pd=int_floor_root(q.numerator),int_floor_root(q.denominator)
    if pn*pn==q.numerator and pd*pd==q.denominator:return F(pn,pd),F(pn,pd)
    upper=max(F(1),q);lower=q/upper;tolerance=F(1,1<<bits)
    while upper-lower>tolerance:
        upper=(upper+q/upper)/2;lower=q/upper
    if not 0<=lower<=upper or not lower*lower<=q<=upper*upper:raise ValueError('Newton interval failed exact radical bounds')
    return lower,upper


def interval_strings(pair):return list(map(str,pair))


def scalar(r,bits=56):
    r=rational(r)
    if r<0:raise ValueError('nonnegative absolute coupling radius required')
    c=F(9,2)-11*r;off2=F(21,4)*r*r;D=(3-c)**2+4*off2;lo,hi=root_enclosure(D,bits)
    lower=(3+c-hi)/2;upper=(3+c-lo)/2
    determinant=3*c-off2
    return {'r':str(r),'c':str(c),'offdiagonal_squared':str(off2),'radicand':str(D),'sqrt_interval':interval_strings((lo,hi)),
      'eigenvalue_interval':interval_strings((lower,upper)),'determinant':str(determinant),
      'positive_exact':c>0 and determinant>0,'inside_primary_box':r<=F(3,8)}


def constants(bits=56):
    a,b=root_enclosure(70,bits);c,d=root_enclosure(3,bits)
    gap=((27-3*b)/16,(27-3*a)/16)
    ground=((24-15*d)/16,(24-15*c)/16)
    endpoint=((3+15*c-3*b)/16,(3+15*d-3*a)/16)
    return {'bits':bits,'sqrt70':interval_strings((a,b)),'sqrt3':interval_strings((c,d)),
      'box_gap_over_alpha':interval_strings(gap),'endpoint_ground_upper_expression':interval_strings(ground),
      'endpoint_gap_over_alpha':interval_strings(endpoint)}


def proof_gate(premises):
    if type(premises) is not dict or set(premises)!=set(PREMISES) or any(type(v) is not bool or not v for v in premises.values()):raise ValueError('all actual full-operator proof premises required')
    return True


def certificate(alpha,couplings,alpha_min=None,bits=56,precision='1/1000000000000',premises=None):
    # This local mathematical gate records explicit assumptions. Root proof admission separately source-replays B1.
    if premises is None:premises={k:True for k in PREMISES}
    proof_gate(premises);a=rational(alpha);amin=a if alpha_min is None else rational(alpha_min);tol=rational(precision)
    if not 0<amin<=a or tol<=0:raise ValueError('common positive physical scale and positive precision required')
    if type(couplings) not in (list,tuple) or len(couplings)!=11:raise ValueError('complete eleven-dimensional physical coefficient vector required')
    ls=[rational(x) for x in couplings];r=max(map(abs,ls))/a
    if r>F(3,8):raise ValueError('coefficient vector lies outside the claimed primary box')
    k=constants(bits);general=scalar(r,bits);gl,gh=map(F,k['box_gap_over_alpha']);el,eh=map(F,k['endpoint_gap_over_alpha'])
    endpoint=all(abs(x)==3*a/8 for x in ls)
    lower,upper=(el,eh) if endpoint else (gl,gh)
    physical=(a*lower,a*upper);floor=(amin*lower,amin*upper)
    # A negative coarse lower endpoint remains insufficient; it cannot be promoted via a common lower scale.
    usable=lower>0 and upper-lower<=tol
    return {'alpha':str(a),'alpha_min':str(amin),'couplings':list(map(str,ls)),'radius':str(r),'bits':bits,'precision':str(tol),
      'premises':dict(premises),'constants':k,'scalar_instance':general,'all_endpoint_magnitudes':endpoint,
      'E0_upper_over_alpha':'0' if not endpoint else k['endpoint_ground_upper_expression'][1],
      'selected_dimensionless_gap_interval':interval_strings((lower,upper)),'physical_gap_interval':interval_strings(physical),
      'common_physical_interval':interval_strings(floor) if lower>=0 else None,'status':'certified-positive' if usable else 'insufficient-precision-or-sign',
      'precision_convention':'maximum dimensionless gap-constant interval width; physical widths scale with alpha',
      'scope':'Finite dense two-cube full physical operator; signed eleven-dimensional box proof is analytic, not inferred from sampled radii.'}


def interval_check(q,pair):
    q=rational(q)
    if type(pair) not in (tuple,list) or len(pair)!=2:raise ValueError('two exact bounds required')
    lo,hi=map(rational,pair)
    if not 0<=lo<=hi or not lo*lo<=q<=hi*hi:raise ValueError('invalid radical enclosure')
    return True


def bare_matching(g_squared,spacing):
    q,a=map(rational,(g_squared,spacing))
    if q<=0 or a<=0:raise ValueError('positive bare coupling squared and spacing required')
    electric=q/(2*a);magnetic=2/(q*a);r=magnetic/electric
    return {'g_squared':str(q),'spacing':str(a),'alpha':str(electric),'lambda':str(magnetic),'ratio':str(r),
      'inside_selected_box':q*q>=F(32,3),'additive_constant_per_face':str(2/(q*a)),
      'scope':'Homogeneous positive convention matching only; failure of this bound at weak bare coupling is not absence of a continuum gap.'}
