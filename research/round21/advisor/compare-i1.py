#!/usr/bin/env python3
"""Independent reviewed invariants, pair agreement and executable rejection controls."""
import argparse,copy,json
from pathlib import Path
LOOP='i1'
EXPECTED={'block_link_count': 24, 'coarse_support_offsets': [[0, 0, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0]], 'free_link_count': 14, 'normalized_budget_coefficient': '7', 'numerical_stability_constants_evaluated': False, 'omitted_anchor_face_count': 21, 'selected_link_count': 10}
STATUSES={'forward': ('verified_dictionary_quantitative_threshold_insufficient', None), 'reverse': (None, True)}
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'))
def validate(f,r):
 for d,x in [('forward',f),('reverse',r)]:
  if x.get('loop')!=LOOP or x.get('direction')!=d:raise ValueError('identity')
  if (x.get('status'),x.get('passed'))!=STATUSES[d]:raise ValueError('execution status drift')
  if canon(x.get('comparison'))!=canon(EXPECTED):raise ValueError('reviewed scientific invariant mismatch')
 if canon(f['comparison'])!=canon(r['comparison']):raise ValueError('direction disagreement')
def leaves(x,path=()):
 if isinstance(x,dict):
  for k,v in x.items():yield from leaves(v,path+(k,))
 elif isinstance(x,list):
  for k,v in enumerate(x):yield from leaves(v,path+(k,))
 else:yield path,x
def main():
 p=argparse.ArgumentParser();p.add_argument('--forward',type=Path,required=True);p.add_argument('--reverse',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 f=json.loads(a.forward.read_text());r=json.loads(a.reverse.read_text());validate(f,r);controls=[]
 for side in range(2):
  for path,value in leaves(EXPECTED):
   pair=[copy.deepcopy(f),copy.deepcopy(r)];target=pair[side]['comparison']
   for k in path[:-1]:target=target[k]
   target[path[-1]]= (not value) if type(value) is bool else value+1 if type(value) in (int,float) else str(value)+'_wrong'
   try:validate(*pair)
   except ValueError:controls.append({'side':side,'path':list(path),'rejected':True})
   else:raise ValueError('mutation survived')
 for side in range(2):
  pair=[copy.deepcopy(f),copy.deepcopy(r)];pair[side]['comparison']={}
  try:validate(*pair)
  except ValueError:controls.append({'side':side,'path':['entire_payload'],'rejected':True})
  else:raise ValueError('missing payload admitted')
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps({'loop':LOOP,'status':'accepted','comparison':EXPECTED,'mutation_controls':controls,'scope':'Arithmetic and evidence agreement; written proof and target limits remain in advisor gate.'},indent=2,sort_keys=True)+'\n')
 print(json.dumps({'loop':LOOP,'status':'accepted','mutation_controls':len(controls)}))
if __name__=='__main__':main()
