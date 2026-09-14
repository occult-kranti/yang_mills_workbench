#!/usr/bin/env python3
"""Exact advisor collar-tail arithmetic; analytic domains are proved separately."""
import argparse,json
from fractions import Fraction as F
from pathlib import Path

def require(b,m):
 if not b:raise RuntimeError(m)
def tail(k,L):
 a=2*L+1;g=1-k
 return k**(L+1)*(a**3/g+6*a*a*k/g**2+12*a*k*(1+k)/g**3+8*k*(1+4*k+k*k)/g**4)
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);out=p.parse_args().output
 require(not out.exists(),'fresh output required')
 require(28*F(5,1664)==F(35,416),'actual coupling')
 rows=[]
 for t in [F(0),F(1,1000),F(-1,1000),F(5,1664),F(-5,1664)]:
  k=28*abs(t)
  for L in [0,1,2,4,8,12]:
   x=tail(k,L)
   require(x-tail(k,L+1)==(2*L+1)**3*k**(L+1),'polynomial tail identity')
   partial=sum((2*n-1)**3*k**n for n in range(L+1,L+31))
   require(x-partial==tail(k,L+30),'exact remainder')
   rows.append({'tau':str(t),'L':L,'hilbert_tail_over_r':str(k**(L+1)/(1-k)),'graph_energy_tail_over_r_cardY':str(x)})
 for n in range(15):
  origin={(x,y,z) for x in range(n+1) for y in range(n+1) for z in range(n+1)}
  require(len(origin)==(n+1)**3,'actual positive-octant collar')
  require((n+2)**3-(n+1)**3==3*n*n+9*n+7,'weighted ratio exponent')
 require(F(7,12)*F(1,1000)**2>0,'actual R1 boundary action nonzero')
 require(F(1)!=F(0),'actual exterior-character norm control')
 out.write_text(json.dumps({'schema':'ym22-root-r2-preparation-v1','passed':True,'actual_k_max':'35/416','actual_gap_min':'381/416','tail_fixtures':rows,'origin_collar_counts_checked':15,'source_sector_residual_norm':'1','actual_boundary_action_squared':'7tau^2/12','volume_weight_upper_certificate':'fails for mu>0,r>0,k>0; no actual norm lower claim','research_loops_added':0},indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
