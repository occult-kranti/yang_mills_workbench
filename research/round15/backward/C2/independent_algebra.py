"""Independent rational trial matrix and monotone Newton radical brackets."""
from fractions import Fraction as Q


def determinant(matrix):
    a=[list(row) for row in matrix];n=len(a);out=Q(1)
    for i in range(n):
        pivot=next((j for j in range(i,n) if a[j][i]),None)
        if pivot is None:return Q(0)
        if pivot!=i:a[i],a[pivot]=a[pivot],a[i];out=-out
        value=a[i][i];out*=value
        for j in range(i+1,n):
            factor=a[j][i]/value
            for k in range(i+1,n):a[j][k]-=factor*a[i][k]
    return out


def trial_matrix(alpha,couplings):
    if type(alpha) is not Q or alpha<=0 or type(couplings) is not tuple or len(couplings)!=6 or any(type(c) is not Q for c in couplings):
        raise ValueError('positive rational alpha and six rational coefficients required')
    matrix=[[Q(0)]*7 for _ in range(7)]
    for p,c in enumerate(couplings,1):matrix[p][p]=3*alpha;matrix[p][0]=matrix[0][p]=-c/2
    return matrix


def bracket_radical(value,tolerance=Q(1,10**24)):
    if type(value) is not Q or value<0 or type(tolerance) is not Q or tolerance<=0:raise ValueError('nonnegative rational radicand and positive tolerance required')
    if value==0:return Q(0),Q(0),0
    upper=Q(1)
    while upper*upper<value:upper*=2
    lower=value/upper;steps=0
    while upper-lower>tolerance:
        upper=(upper+value/upper)/2
        lower=value/upper;steps+=1
        if steps>32:raise ValueError('explicit implementation iteration cap reached')
    if not 0<=lower<=upper or lower*lower>value or upper*upper<value:raise ValueError('Newton bracket invariant failed')
    return lower,upper,steps


def common_sign(ratio):
    if type(ratio) is not Q or ratio<0:raise ValueError('nonnegative rational ratio required')
    if ratio<=Q(1,4):return 'positive'
    difference=6*ratio*(12-23*ratio)
    return 'positive' if difference>0 else 'zero' if difference==0 else 'negative'


def polynomial_check(alpha,couplings):
    matrix=trial_matrix(alpha,couplings);delta=3*alpha;squares=sum(c*c for c in couplings)
    checks=[]
    # Both determinant and proposed factor are monic degree7 polynomials.
    # Agreement at8 distinct rational arguments proves their equality.
    for t in map(Q,range(-2,6)):
        shifted=[[(t if i==j else Q(0))-matrix[i][j] for j in range(7)] for i in range(7)]
        actual=determinant(shifted);expected=(t-delta)**5*(t*t-delta*t-squares/4)
        if actual!=expected:raise ValueError('trial characteristic polynomial mismatch')
        checks.append({'t':str(t),'determinant':str(actual)})
    return checks
