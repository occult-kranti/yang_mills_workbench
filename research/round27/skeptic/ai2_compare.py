#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
B=Path(__file__).resolve().parents[3];H=Path(__file__).resolve().parent
n=0
def need(ok,msg):
 global n
 if not ok:raise RuntimeError(msg)
 n+=1
p=B/'research/round27'
a=json.loads((p/'forward/ai2/output/results.json').read_text());b=json.loads((p/'reverse/ai2/output/results.json').read_text());s=json.loads((H/'ai2-independent.json').read_text())
for direction in ('forward','reverse'):
 f=p/direction/'ai2/output/results.json';r=H/f'ai2-{direction}-replay/results.json'
 need(f.read_bytes()==r.read_bytes(),direction+' fresh replay equality')
 data=json.loads(f.read_text())
 for path,digest in data['bindings'].items():need(hashlib.sha256((B/path).read_bytes()).hexdigest()==digest,'current binding '+path)
for r in s['rows']:
 power,k,probe=r['u_exponent'],r['k'],str(r['probe'])
 ar=next(x for x in a['rows'] if x['power']==power and x['k']==k)
 br=next(x for x in b['decisions'] if x['power']==power and x['k']==k)
 need(ar['scalar_discrimination'][probe]['disjoint']==br['probes'][probe]['certified_disjoint']==r['certified_disjoint'],'disjoint classification')
 need(F(ar['scalar_discrimination'][probe]['imaginary_center_distance'])==F(br['probes'][probe]['imaginary_center_separation'])==F(r['imaginary_separation']),'exact distance')
 for i,hyp in enumerate(('H1','H2')):
  aa=ar['hypotheses'][i];bb=next(x for x in b['samples'] if x['power']==power and x['k']==k and x['hypothesis']==hyp)
  need(F(aa['centers'][probe]['real'])==F(bb['centers'][probe]['real'])==F(r[f'center{i+1}_re']),'exact real center')
  need(F(aa['centers'][probe]['imag'])==F(bb['centers'][probe]['imag'])==F(r[f'center{i+1}_im']),'exact imaginary center')
  need(F(r[f'radius{i+1}'])>=F(aa['radius']) and F(r[f'radius{i+1}'])>=F(bb['full_radius']),'independent conservative radius dominance')
  need(F(aa['physical_time_in_hbar_over_alpha'])==F(bb['physical_time_in_hbar_over_alpha'])==F(r['physical_time_hbar_over_alpha']),'same physical time')
 need(not ar['simple_ratio_intervals_disjoint'] and not br['ratio_intervals_disjoint'],'ratio limitations retained')
for i,reg in enumerate(s['regions']):
 need(reg['N']==a['collars'][i]['retained_faces']==b['geometry']['collars'][i]['faces'],'three-way actual collar count')
result={'status':'PASS','checks':n,'scope':'Post-exchange source binding, replay and exact three-way comparison; not extra physics loop','bindings':{str(x.relative_to(B)):hashlib.sha256(x.read_bytes()).hexdigest() for x in [p/'forward/ai2/output/results.json',p/'reverse/ai2/output/results.json',H/'ai2-independent.json',Path(__file__).resolve()]}}
(H/'ai2-comparison.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','checks':n}))
