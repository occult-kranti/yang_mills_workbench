#!/usr/bin/env python3
import copy,json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]
def compare(a,b):
 fail=[]
 for k in ['pure_gram','mixed_gram','pure_gram_rank','mixed_gram_rank']:
  if a[k]!=b[k]:fail.append(k)
 x=next(x for x in a['gap_fixtures'] if x['alpha_over_E_star']=='2' and x['tau']=='1/64')
 if x['gap_lower_over_E_star']!=b['scale']['GNS_gap_floor/E_star'] or a['energy_generator']!=b['scale']['energy_generator']:fail.append('physical generator')
 if not all(a['controls'].values()) or not all(x['passed'] for x in b['controls']):fail.append('controls')
 return fail
if __name__=='__main__':
 a=json.loads((R/'forward/g2/output/results.json').read_text());b=json.loads((R/'reverse/g2/output/results.json').read_text());fail=compare(a,b);m=copy.deepcopy(a);m['pure_gram_rank']=4;bad=bool(compare(m,b))
 j={'loop':'g2','status':'accepted' if not fail and bad else 'rejected','failures':fail,'executed_mutations':{'mixed_pure_GNS_confusion_rejected':bad},'independence':'Two complete core/commutant/GNS proofs; exact matrix-unit Gram and physical generator records agree.'};(R/'advisor/g2-comparison.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j))
 if j['status']!='accepted':raise SystemExit(1)
