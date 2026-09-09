"""Round-six regressions: setup controls, fail-closed verification, provenance."""
from pathlib import Path
import copy, hashlib, importlib.util, json, math, os, subprocess, sys, tempfile, unittest
from unittest.mock import patch
import numpy as np
ROOT=Path(__file__).resolve().parent

def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod);return mod
new=load('response_round6',ROOT/'code/response.py')
old=load('response_round4',ROOT.parent/'round4/code/response.py')
ps=load('proof_search_round6',ROOT/'code/proof_search.py')
oldps=load('proof_search_round5',ROOT.parent/'round5/proof_search.py')
guard=load('evidence_guard_round6',ROOT/'code/evidence_guard.py')
runner_module=load('code_runner_round6',ROOT/'code/run_checks.py')

def fixture(verification='manual derivation/review',cost=1):
 return {'initial_facts':['A'],'goals':['T'],'nodes':[{'id':i,'statement':i,'scope':'finite','kind':('declared_hypothesis' if i=='A' else 'theorem'),'assumption_ids':[],'verification':verification if i=='A' else 'manual derivation/review','source':'test','version':'1'} for i in ['A','T']], 'rules':[{'id':'r','premises':['A'],'conclusion':'T','cost':cost,'scope':'finite','proof_ref':'test','review_status':'reviewed'}]}
P={'nK':12,'ncut':0,'Kmax':3,'b':1,'Tpump':.3,'tfinal':1.2,'probe_start':.5,'probe_duration':.3,'sample_count':61,'max_step':.015,'rtol':2e-9,'atol':2e-11}
RESULTS={}

class CoreRegression(unittest.TestCase):
 def test_nonzero_probe_preparation_and_centered_difference(self):
  r=new.run_scenario(new.Params(**P),mode='delayed_probe',probe_amp=.5,epsilons=(.03,.01,.003),include_legacy=True)
  errors=[x['max_abs_error'] for x in r['finite_difference']]
  self.assertLess(errors[-1],1e-8);self.assertGreater(errors[0]/errors[1],5)
  self.assertTrue(r['gauge']['passed']);self.assertEqual(r['legacy_effect']['status'],'not_comparable')
  self.assertTrue(all(r['gates'].values()))
  RESULTS['nonzero_probe']={'fd_errors':errors,'gauge':r['gauge'],'gates':r['gates']}
 def test_default_equations_unchanged(self):
  a=old._solve(old.Params(**P));b=new._solve(new.Params(**P))
  maxdiff=max(float(np.max(np.abs(np.asarray(a['macro'][k])-np.asarray(b['macro'][k])))) for k in a['macro'])
  self.assertEqual(maxdiff,0);RESULTS['matched_baseline_max_diff']=maxdiff
 def test_mode_and_probe_validation_before_solver(self):
  for kwargs in [{'mode':'misspelled'},{'probe_amp':math.nan},{'probe_amp':math.inf},{'probe_amp':.2},{'canonical_shift':math.inf},{'gauge':'yes'}]:
   with self.subTest(kwargs=kwargs),patch.object(new,'solve_ivp',side_effect=AssertionError('must fail before solver')):
    with self.assertRaises(new.ResponseFailure):new._solve(new.Params(**P),**kwargs)
 def test_bad_epsilon_sequences_rejected_before_solver(self):
  for eps in [(),(0,),(-.01,),(math.nan,),(math.inf,),(.01,.01)]:
   with self.subTest(eps=eps),patch.object(new,'_solve',side_effect=AssertionError('must fail before solver')):
    with self.assertRaises(new.ResponseFailure):new.run_scenario(new.Params(**P),epsilons=eps)
 def test_invalid_regulator_and_tolerances(self):
  for key,val in [('ncut',-1),('ncut',True),('nK',2.5),('nK',math.inf),('Kmax',0),('b',math.nan),('rtol',0),('max_step',math.inf),('sample_count',2),('z_floor',0)]:
   with self.subTest(key=key,val=val):
    with self.assertRaises(new.ResponseFailure):new._solve(new.Params(**{**P,key:val}))
 def test_missing_integrator_samples_rejected(self):
  class Empty:success=True;y=np.empty((0,0))
  with patch.object(new,'solve_ivp',return_value=Empty()):
   with self.assertRaisesRegex(new.ResponseFailure,'incomplete'):new._solve(new.Params(**P))
 def test_no_causal_samples_does_not_pass_vacuously(self):
  r=new.run_scenario(new.Params(**{**P,'probe_start':0,'probe_duration':2}),mode='delayed_probe',epsilons=(.01,),include_legacy=False)
  self.assertFalse(r['gates']['delayed_pre_tangent_pass']);self.assertFalse(r['gates']['delayed_post_work_constant_pass'])
  self.assertIsNone(r['diagnostics']['delayed_pre_tangent_max']);self.assertIsNone(r['diagnostics']['delayed_post_work_variation'])
  json.dumps(r,allow_nan=False)
 def test_work_constancy_waits_until_both_sources_stop(self):
  p=new.Params(**{**P,'Tpump':1.0,'probe_start':.1,'probe_duration':.2})
  r=new.run_scenario(p,mode='delayed_probe',probe_amp=.5,epsilons=(.01,),include_legacy=False)
  self.assertTrue(r['gates']['delayed_post_work_constant_pass'])
  self.assertEqual(r['diagnostics']['delayed_post_work_samples'],10)
 def test_source_changed_during_run_rejected(self):
  with patch.object(new,'source_hash',side_effect=['before','after']):
   with self.assertRaisesRegex(new.ResponseFailure,'source changed'):new.run_scenario(new.Params(**P),epsilons=(.01,),include_legacy=False)
 def test_unsafe_node_verification_rejected(self):
  for status in ['proposed','conjectural','unsafe','unresolved','numerical evidence',' unverified ']:
   with self.subTest(status=status):
    with self.assertRaises(ps.ContractError):ps.load_library(fixture(status))
 def test_declared_conditions_are_distinct_from_conjectures(self):
  result=ps.plan(fixture())
  self.assertFalse(result["conditional"]);self.assertTrue(result["conditional_on_declared_assumptions"])
  self.assertEqual(result["declared_assumption_ids"],["A"]);self.assertEqual(result["conjectural_assumptions"],[])
 def test_exact_large_integer_cost(self):
  result=ps.plan(fixture(cost=10**400));self.assertEqual(result['certified_cost'],10**400)
 def test_existing_fixture_costs_unchanged(self):
  d=json.loads((ROOT.parent/'round5/search_fixture.json').read_text())
  for name,data in [('base',d)]+list(d['scenarios'].items()):
   with self.subTest(name=name):
    a=oldps.plan(data);b=ps.plan(data);self.assertEqual(a['status'],b['status']);self.assertEqual(a.get('certified_cost'),b.get('certified_cost'))
 def test_external_proof_artifact_change_rejected(self):
  with tempfile.TemporaryDirectory(dir=ROOT) as td:
   base=Path(td);proof=base/'proof.md';proof.write_text('reviewed proof v1')
   manifest=base/'manifest.json';manifest.write_text(json.dumps({'files':{'proof.md':hashlib.sha256(proof.read_bytes()).hexdigest()}}))
   guard.verify_manifest(manifest,base)
   proof.write_text('unreviewed changed proof')
   with self.assertRaisesRegex(guard.EvidenceFailure,'changed or missing'):guard.verify_manifest(manifest,base)
 def test_manifest_path_escape_rejected(self):
  with tempfile.TemporaryDirectory(dir=ROOT) as td:
   base=Path(td);manifest=base/'manifest.json';manifest.write_text(json.dumps({'files':{'../outside.md':'0'*64}}))
   with self.assertRaisesRegex(guard.EvidenceFailure,'leaves project'):guard.verify_manifest(manifest,base)
 def test_zero_exit_with_failed_semantic_result_rejected(self):
  with tempfile.TemporaryDirectory(dir=ROOT) as td:
   base=Path(td);(base/'fake.py').write_text('placeholder')
   class Proc:returncode=0;stdout='';stderr=''
   def fake_run(*args,**kwargs):
    (base/'out.json').write_text('{"passed":false}')
    return Proc()
   with patch.object(runner_module,'ROOT',base),patch.object(runner_module.subprocess,'run',side_effect=fake_run):
    report=runner_module.execute(['fake.py'],'out.json',lambda x:x.get('passed') is True)
   self.assertFalse(report['passed']);self.assertTrue(report['fresh_output']);self.assertEqual(report['exit_code'],0)
 def test_symbolic_gate_fails_even_optimized(self):
  src=(ROOT/'code/symbolic_checks.py').read_text().replace("zero('Bloch norm derivative',2*r.dot(rd))","zero('Bloch norm derivative',2*r.dot(rd)+1)")
  with tempfile.TemporaryDirectory(dir=ROOT) as td:
   p=Path(td)/'mutant.py';p.write_text(src)
   env={**os.environ,'PYTHONPATH':str(ROOT.parent/'round5/deps')}
   run=subprocess.run([sys.executable,'-O',str(p)],capture_output=True,text=True,env=env)
   self.assertNotEqual(run.returncode,0);self.assertIn('nonzero residual',run.stderr)
 def test_historical_assert_mutant_false_success_reproduced(self):
  src=(ROOT.parent/'round5/symbolic_checks.py').read_text().replace("zero('Bloch norm derivative',2*r.dot(rd))","zero('Bloch norm derivative',2*r.dot(rd)+1)")
  with tempfile.TemporaryDirectory(dir=ROOT) as td:
   p=Path(td)/'mutant.py';p.write_text(src)
   env={**os.environ,'PYTHONPATH':str(ROOT.parent/'round5/deps')}
   run=subprocess.run([sys.executable,'-O',str(p)],capture_output=True,text=True,env=env)
   self.assertEqual(run.returncode,0);self.assertFalse(json.loads(run.stdout)['passed'])
   RESULTS['historical_optimized_mutant']={'exit_code':run.returncode,'reported_passed':json.loads(run.stdout)['passed']}

if __name__=='__main__':
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(CoreRegression)
 runner=unittest.TextTestRunner(verbosity=2);result=runner.run(suite)
 report={'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'passed':result.wasSuccessful(),'results':RESULTS,'test_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 (ROOT/'code_regression_results.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
 raise SystemExit(0 if result.wasSuccessful() else 1)
