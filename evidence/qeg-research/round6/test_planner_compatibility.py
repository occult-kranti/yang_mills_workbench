"""Run unchanged 24 historical planner tests against the new engine, in memory."""
from pathlib import Path
import hashlib,importlib.util,json,sys,unittest
ROOT=Path(__file__).resolve().parent

def main():
    spec=importlib.util.spec_from_file_location('proof_search',ROOT/'code/proof_search.py')
    engine=importlib.util.module_from_spec(spec);sys.modules['proof_search']=engine;spec.loader.exec_module(engine)
    source=ROOT.parent/'round5/test_proof_search.py'
    tspec=importlib.util.spec_from_file_location('round5_unchanged_tests',source)
    tests=importlib.util.module_from_spec(tspec);tspec.loader.exec_module(tests)
    suite=unittest.defaultTestLoader.loadTestsFromModule(tests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    output={'passed':result.wasSuccessful(),'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'historical_test_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'round6_engine_sha256':hashlib.sha256((ROOT/'code/proof_search.py').read_bytes()).hexdigest(),'historical_sources_modified':False}
    (ROOT/'planner_compatibility_results.json').write_text(json.dumps(output,indent=2)+'\n')
    return 0 if result.wasSuccessful() else 1

if __name__=='__main__':raise SystemExit(main())
