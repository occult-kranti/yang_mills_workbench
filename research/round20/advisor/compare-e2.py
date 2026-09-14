#!/usr/bin/env python3
import copy,json,pathlib,importlib.util
from fractions import Fraction as F
R=pathlib.Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('e2_reverse_geometry',R/'reverse/e2/check.py');rev=importlib.util.module_from_spec(sp);sp.loader.exec_module(rev)
def compare(a,b):
 fail=[]
 for x,y in zip(a['error_fixtures'],b['rows']):
  if x['M']!=y['M'] or x['unit_local_error_bound']!=y['local_observable_error_over_norm']:fail.append('local error')
  if 2*F(x['epsilon_over_alpha'])!=F(y['epsilon_over_E_star']) or 2*F(x['g_M_over_alpha'])!=F(y['g_M_over_E_star']):fail.append('energy scales')
 for x in a['phase_fixtures']:
  y=rev.box(x['N'],set())
  if x['omitted_faces']!=y['omitted_faces'] or x['reference_components']!=y['selected_components'] or x['free_witnesses_verified']!=y['omitted_faces']:fail.append('phase geometry')
 if len(a['error_fixtures'])!=9 or len(b['rows'])!=9 or len(a['phase_fixtures'])!=8 or len(b['geometry_fixtures'])!=8:fail.append('fixture count')
 if not all(a['controls'].values()) or not all(x['passed'] for x in b['controls']):fail.append('controls')
 return fail
if __name__=='__main__':
 a=json.loads((R/'forward/e2/output/results.json').read_text());b=json.loads((R/'reverse/e2/output/results.json').read_text());fail=compare(a,b);m=copy.deepcopy(a);m['phase_fixtures'][0]['omitted_faces']-=1;bad=bool(compare(m,b))
 j={'loop':'e2','status':'accepted' if not fail and bad else 'rejected','compared_error_rows':9,'independent_same_shape_geometry_reconstructions':8,'failures':fail,'executed_mutations':{'omitted_face_loss_rejected':bad},'independence':'Forward groups selected faces by strip anchor; reverse reconstructs link-incidence union components at the forward shapes without importing forward code.'};(R/'advisor/e2-comparison.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j))
 if j['status']!='accepted':raise SystemExit(1)
