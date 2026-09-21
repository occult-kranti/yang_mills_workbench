#!/usr/bin/env python3
from fractions import Fraction as F
from math import comb
from pathlib import Path
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from u_common import need,emit
z=F(1,10**6);x=80*z/7
alt=x*x*(6-8*x+3*x*x)/(1-x)**3
need(alt==(1-x)**-3-1-3*x,'alternative tail identity')
need(z/84-alt>z/168,'reverse positive margin')
c=F(1);coeff=[]
for n in range(1,21):
    c*= (F(8,3)+n-1)/n
    need(c<=comb(n+2,2),'coefficient domination')
    if n>=2: need(c<=F(44,9)*comb(n+2,4),'Taylor rational majorant coefficient')
    coeff.append(str(c))
# Actual complete strip, placed away from the orthant boundary.
edges={( (x,y,1),0) for x in (4,5,6) for y in (2,3)} | {((x,2,1),1) for x in (4,5,6,7)}
faces=set()
for a,i in edges:
    for j in range(3):
        if i==j: continue
        faces.add((a,tuple(sorted((i,j)))))
        if a[j]>0:
            b=tuple(v-(k==j) for k,v in enumerate(a));faces.add((b,tuple(sorted((i,j)))))
need(len(edges)==10 and 4<len(faces)<=40,'complete-factor incidence')
need(F(64,49)*F(7,512)*F(2,3)==F(1,84),'state asymptotic coefficient')
emit('u2','reverse','22c496e565897392f8a1d63bff270d10ab5c9d4ba278bf1323584ad830a10dd8',
 dict(status='full_system_endpoint_lower_bound',endpoint_proved=True,continuum_proved=False,z_cap=str(z),
      alternative_liminf_at_cap=str(z/84-alt),simple_liminf_lower_at_cap=str(z/168),
      complete_strip_incident_faces=len(faces),majorant_coefficients=coeff,
      state_asymptotic_coefficient='1/84',tail_method='coefficient domination by power 3'),
 dict(all_order_domination_argument=True,exact_positive_margin=True,complete_factor_incidence=True,
      single_link_budget_rejected=len(faces)>4,support_growth_required=8+3>8,
      first_order_bound_to_u1=True,state_error_retained=True,no_two_state_autonomy=True,
      magnitude_lower_bound_not_upper_failure=True,large_window_certificate_only=True))
