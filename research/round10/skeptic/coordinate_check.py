"""Exact Gaussian-rational checks of the two-loop SU(2) trace domain."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json


def c(real=0, imag=0):
    return F(real), F(imag)


def add(a,b):
    return a[0]+b[0], a[1]+b[1]


def mul(a,b):
    return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def neg(a):
    return -a[0],-a[1]


def conjugate(a):
    return a[0],-a[1]


def matrix_product(a,b):
    return [[add(mul(a[i][0],b[0][j]),mul(a[i][1],b[1][j]))
             for j in range(2)] for i in range(2)]


def dagger(a):
    return [[conjugate(a[j][i]) for j in range(2)] for i in range(2)]


def matrix(q):
    # q0 I + i(q1 sigma1 + q2 sigma2 + q3 sigma3), exact entries.
    w,x,y,z=map(F,q)
    return [[c(w,z),c(y,x)],[c(-y,x),c(w,-z)]]


def half_trace(a):
    real,imag=add(a[0][0],a[1][1])
    if imag:
        raise ValueError("SU(2) trace must be real")
    return real/2


def domain(x,y,z):
    x,y,z=map(F,(x,y,z))
    return -1<=x<=1 and -1<=y<=1 and (z-x*y)**2 <= (1-x*x)*(1-y*y)


def main():
    checks=[]
    def gate(name,condition,details=None):
        checks.append({"name":name,"passed":bool(condition),"details":details})
    identity=[[c(1),c(0)],[c(0),c(1)]]
    fixtures=[(1,0,0,0),(-1,0,0,0),(0,0,0,1),(0,1,0,0),
              (F(3,5),F(4,5),0,0),(F(1,2),F(1,2),F(1,2),F(1,2))]
    matrices=[matrix(q) for q in fixtures]
    for index,a in enumerate(matrices):
        determinant=add(mul(a[0][0],a[1][1]),neg(mul(a[0][1],a[1][0])))
        gate(f"fixture{index} exact SU2",matrix_product(a,dagger(a))==identity and determinant==c(1))
    rows=[];all_domain=True;all_trace=True;all_polynomial=True
    for i,u in enumerate(matrices):
        for j,v in enumerate(matrices):
            x,y,z=half_trace(u),half_trace(v),half_trace(matrix_product(u,v))
            dot=sum(F(fixtures[i][k])*F(fixtures[j][k]) for k in (1,2,3))
            margin=(1-x*x)*(1-y*y)-(z-x*y)**2
            polynomial=1-x*x-y*y-z*z+2*x*y*z
            all_domain &= domain(x,y,z) and -1<=z<=1
            all_trace &= z==x*y-dot
            all_polynomial &= margin==polynomial
            rows.append({"U_fixture":i,"V_fixture":j,"x":str(x),"y":str(y),
                         "z":str(z),"domain_margin":str(margin)})
    gate("all36 exact pair domains",all_domain)
    gate("all36 traces match scalar product",all_trace)
    gate("all36 domain polynomial identities",all_polynomial)
    gate("central degeneracies force z=xy",all(
        F(row["z"])==F(row["x"])*F(row["y"])
        for row in rows if abs(F(row["x"]))==1 or abs(F(row["y"]))==1))
    u=matrices[2];parallel=matrices[2];orthogonal=matrices[3]
    gate("separate traces lose joint invariant",
         half_trace(u)==half_trace(parallel)==half_trace(orthogonal)==0
         and half_trace(matrix_product(u,parallel))==-1
         and half_trace(matrix_product(u,orthogonal))==0)
    gate("reject impossible interior triple",not domain(0,0,F(11,10)))
    gate("reject invalid central triple",not domain(1,F(1,2),0))
    gate("reject invalid individual trace",not domain(F(11,10),1,F(11,10)))
    gate("accept both central boundaries",domain(1,F(1,2),F(1,2)) and domain(-1,F(1,2),F(-1,2)))
    path=Path(__file__).resolve()
    result={"status":"passed" if checks and all(x["passed"] for x in checks) else "failed",
            "check_count":len(checks),"checks":checks,"exact_pair_rows":rows,
            "source_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
            "scope":"Two-loop gauge-orbit coordinate lemma only; separate from119 round10 gates and any gap extension."}
    path.with_name("coordinate_check.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":result["status"],"checks":len(checks)}))
    if result["status"]!="passed":raise SystemExit(1)


if __name__=="__main__":main()
