"""Actual loopback HTTP smoke checks for both documented launch modes."""
from pathlib import Path
import importlib.util
import threading
import unittest
import urllib.request
import urllib.error

ROOT=Path(__file__).resolve().parents[1]
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class LaunchTests(unittest.TestCase):
    def exercise(self,server,prefix):
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        base=f'http://127.0.0.1:{server.server_port}'
        try:
            for name in ('','research-plaquette.js','plaquette-gaps.csv','research-round10.zip',
                         'research-bridges-data.js','research-bridges.js',
                         'bridge-drive-summary.csv','bridge-closure.csv','research-round12.zip',
                         'research-exceptions-data.js','research-exceptions.js',
                         'research-team-data.js','research-team.js','team-covariance.csv',
                         'team-certificate.csv','research-round14-certificates.json',
                         'exception-moments.csv','exception-locality.csv','exception-response.csv',
                         'research-round13-certificates.json','research-round13.zip'):
                with urllib.request.urlopen(base+prefix+name,timeout=3) as response:
                    self.assertEqual(response.status,200);self.assertGreater(len(response.read()),20)
            with self.assertRaises(urllib.error.HTTPError) as failure:
                urllib.request.urlopen(base+prefix+'missing-no-file',timeout=3)
            self.assertEqual(failure.exception.code,404)
        finally:server.shutdown();server.server_close();thread.join(timeout=3)
    def test_local_research_launch(self):
        m=module('workbench_start',ROOT/'start.py');self.exercise(m.make_server(0,dist=ROOT/'dist'),'/')
    def test_project_prefix_preview(self):
        m=module('workbench_preview',ROOT/'scripts/preview_pages.py');server,prefix=m.make_server(0);self.exercise(server,prefix)
if __name__=='__main__':unittest.main()
