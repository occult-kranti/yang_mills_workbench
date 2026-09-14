"""Reject malformed authored metadata identified in the independent UI review."""
import copy,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve();ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'research/round22'))
from presentation_schema import loop_metadata,future_roadmap
from admission import digest,require

def main():
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);out=p.parse_args().output
 require(not out.exists(),'fresh output required')
 good=json.loads((ROOT/'research/round22/site-data.json').read_text())['loops']['q2']
 loop_metadata(good,'q2')
 road={'executed':False,'goals':[{'id':str(i),'title':'Title','target':'Target','missing_premise':'Premise'} for i in range(3)]}
 future_roadmap(road);rows=[]
 for name,field,value in [('string_derivation','steps','abc'),('object_derivation','steps',[{}, {}, {}]),('empty_step','steps',['a',' ','c']),('object_prose','objection',{})]:
  bad=copy.deepcopy(good);bad[field]=value
  try:loop_metadata(bad,'q2')
  except ValueError:rows.append({'control':name,'rejected':True})
  else:raise ValueError('malformed metadata admitted: '+name)
 for name,change in [('executed_future_goal',lambda r:r.update(executed=True)),('nonboolean_future_status',lambda r:r.update(executed=0)),('missing_future_goal',lambda r:r['goals'].pop()),('duplicate_future_goal',lambda r:r['goals'][1].update(id='0'))]:
  bad=copy.deepcopy(road);change(bad)
  try:future_roadmap(bad)
  except ValueError:rows.append({'control':name,'rejected':True})
  else:raise ValueError('contradictory roadmap admitted: '+name)
 out.write_text(json.dumps({'status':'passed','controls':rows,'research_loops_added':0,'driver_sha256':digest(HERE),'schema_source_sha256':digest(ROOT/'research/round22/presentation_schema.py')},indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
