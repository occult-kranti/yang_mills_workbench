"""Presentation release checks with isolated synthetic evidence, not physics results."""
from copy import deepcopy
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('round28_build_site', ROOT / 'research/round28/build_site.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class BuildSiteTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.loops = [f'g{n}' for n in range(1, 11)]
        self.write('research/round28/advisor/sequence.json', {'loops': ['g1'], 'target_loops': 10})
        self.write('research/round28/advisor/progress.json', {'completed_loops': [], 'active_loop': 'g1'})
        self.write('research/round28/contracts/g1.json', {'loop': 'g1', 'goal': 'G'})

    def write(self, path, value):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(value) if not isinstance(value, str) else value)
        return target

    def gate(self, loop, sequence):
        paths = [f'research/round28/contracts/{loop}.json', f'research/round28/forward/{loop}/report.md', f'research/round28/reverse/{loop}/report.md', f'research/round28/skeptic/{loop}.md']
        self.write(paths[0], {'loop':loop, 'goal':f'G{(sequence+1)//2}'})
        for path in paths[1:]:
            self.write(path, 'Synthetic evidence fixture, not a mathematical claim.')
        gate = {'loop': loop, 'sequence': sequence, 'verdict': 'accepted_with_limits', 'completed_at': 'fixture', 'accepted': 'Synthetic scoped result.', 'limitations': ['No physical claim from this fixture.'], 'bindings': {path: sha256((self.root/path).read_bytes()).hexdigest() for path in paths}}
        self.write(f'research/round28/advisor/{loop}-gate.json', gate)
        return gate

    def build(self, **kwargs):
        return builder.build(self.root, **kwargs)

    def test_pending_does_not_read_producer_science(self):
        self.write('research/round28/forward/g1/report.md', 'UNREVIEWED PRIVATE DRAFT')
        self.write('research/round28/advisor/summaries.json', {'g1': {'title':'Unreviewed proposed title', 'equations':[{'expression':'UNREVIEWED EQUATION'}]}})
        data = self.build()
        self.assertEqual(data['progress']['completed'], 0)
        self.assertEqual(data['progress']['selected'], 1)
        self.assertFalse(data['progress']['cycle_complete'])
        self.assertNotIn('UNREVIEWED', json.dumps(data))
        self.assertEqual(data['loops'][0]['stage'], 'in-progress')

    def test_one_gate_is_one_completed_loop(self):
        self.gate('g1',1)
        data = self.build()
        self.assertEqual(data['progress']['completed'],1)
        self.assertEqual(data['progress']['remaining'],9)
        self.assertEqual(data['loops'][0]['accepted'],'Synthetic scoped result.')
        self.assertEqual(len(data['loops'][0]['gate_sha256']),64)
        self.write('research/round28/advisor/summaries.json', {'g1': {'title':'Synthetic question', 'bullets':[], 'equations':[]}})
        with self.assertRaisesRegex(ValueError,'ten source-bound reviewed gates'):
            self.build(require_complete=True)

    def test_binding_mutation_blocks_rebuild(self):
        self.gate('g1',1)
        self.write('research/round28/forward/g1/report.md','Altered result')
        with self.assertRaisesRegex(ValueError,'changed gate input'):
            self.build()

    def test_claimed_completion_without_gate_is_rejected(self):
        self.write('research/round28/advisor/progress.json',{'completed_loops':['g1']})
        with self.assertRaisesRegex(ValueError,'without a valid final gate'):
            self.build()

    def test_gate_must_include_both_reports_and_skeptic(self):
        gate=self.gate('g1',1)
        gate['bindings'].pop('research/round28/skeptic/g1.md')
        self.write('research/round28/advisor/g1-gate.json',gate)
        with self.assertRaisesRegex(ValueError,'both reports and skeptic'):
            self.build()

    def test_later_gate_cannot_skip_pending_loop(self):
        self.write('research/round28/advisor/sequence.json',{'loops':['g1','g2'],'target_loops':10})
        self.gate('g2',2)
        with self.assertRaisesRegex(ValueError,'later gate precedes'):
            self.build()

    def test_duplicate_sequence_rejected(self):
        self.write('research/round28/advisor/sequence.json',{'loops':['g1','g1'],'target_loops':10})
        with self.assertRaisesRegex(ValueError,'duplicate selected sequence'):
            self.build()

    def test_source_depth_and_url_counts_preserved(self):
        self.write('research/round28/experts/sources.json',{'reading_records':[{'record_id':'s1','lens':'newton','category':'historical_primary','reading_depth':'Only selected passages.','recorded_urls':['https://example.org/source'],'original_record':{'title':'A historical source','record_vs_interpretation':'Method only.'}}], 'counts':{'formal_reading_records':1,'unique_recorded_urls':1}})
        data=self.build()
        self.assertEqual(data['survey']['records'][0]['depth'],'Only selected passages.')
        self.assertEqual(data['survey']['records'][0]['use'],'Method only.')
        self.assertEqual(data['survey']['counts']['readings'],1)
        survey=json.loads((self.root/'research/round28/experts/sources.json').read_text())
        survey['counts']['formal_reading_records']=2
        self.write('research/round28/experts/sources.json',survey)
        with self.assertRaisesRegex(ValueError,'reading-count mismatch'):
            self.build()

    def source_ledgers(self):
        initial={'reading_records':[{'record_id':'s1','lens':'feynman','category':'technical_primary','reading_depth':'Abstract only.','recorded_urls':['https://example.org/paper'],'original_record':{'title':'An existing study'}}], 'screening_records':[{'id':'screen1','url':'https://example.org/metadata','reading_depth':'Metadata only.'}], 'counts':{'formal_reading_records':1,'unique_recorded_urls':1,'screening_or_reopen_records':1,'unique_urls_including_screening':2}}
        supplement={'reading_records':[{'record_id':'s2','lens':'feynman','category':'technical_primary','reading_depth':'Selected proof passages only.','recorded_urls':['https://example.org/paper'],'original_record':{'title':'A deeper reading of the same study','limits':'No whole-paper proof audit.'}},{'record_id':'s3','lens':'feynman','category':'bibliographic_primary','reading_depth':'Publication metadata only.','recorded_urls':['https://example.org/institution'],'original_record':{'title':'Institutional publication record'}}], 'screening_records':[{'id':'screen2','url':'https://example.org/search','reading_depth':'Search result only; access failed.'}], 'counts':{'formal_reading_records':2,'unique_recorded_urls':2,'screening_or_reopen_records':1}, 'interpretation_limits':['Repeated reading is not an additional independent study.']}
        self.write('research/round28/experts/sources.json',initial)
        self.write('research/round28/experts/source-supplement.json',supplement)
        return initial,supplement

    def test_optional_supplement_merges_records_but_deduplicates_urls(self):
        self.source_ledgers()
        original=(self.root/'research/round28/experts/sources.json').read_bytes()
        data=self.build()['survey']
        self.assertEqual(data['counts']['readings'],3)
        self.assertEqual(data['counts']['urls'],2)
        self.assertEqual(data['counts']['screening'],2)
        self.assertEqual(data['counts']['urls_including_screening'],4)
        self.assertEqual(data['records'][2]['category'],'bibliographic_primary')
        self.assertEqual(data['records'][2]['depth'],'Publication metadata only.')
        self.assertEqual(data['screening'][1]['reading_depth'],'Search result only; access failed.')
        self.assertEqual(len(data['sources']),4)
        self.assertEqual(len(data['ledgers']),2)
        self.assertIn('Repeated reading is not an additional independent study.',data['interpretation_limits'])
        self.assertEqual((self.root/'research/round28/experts/sources.json').read_bytes(),original)

    def test_supplement_count_mismatch_fails(self):
        _,supplement=self.source_ledgers()
        supplement['counts']['screening_or_reopen_records']=2
        self.write('research/round28/experts/source-supplement.json',supplement)
        with self.assertRaisesRegex(ValueError,'screening_or_reopen_records mismatch'):
            self.build()

    def test_duplicate_ids_between_ledgers_fail(self):
        _,supplement=self.source_ledgers()
        supplement['reading_records'][0]['record_id']='s1'
        self.write('research/round28/experts/source-supplement.json',supplement)
        with self.assertRaisesRegex(ValueError,'duplicate source record ID s1'):
            self.build()

    def test_changed_supplement_input_fails(self):
        _,supplement=self.source_ledgers()
        path='research/round28/experts/deepened-record.md'
        original=self.write(path,'Selected source passages, metadata excluded.')
        supplement['input_bindings']=[{'path':path,'sha256':sha256(original.read_bytes()).hexdigest()}]
        self.write('research/round28/experts/source-supplement.json',supplement)
        self.write(path,'Changed record.')
        with self.assertRaisesRegex(ValueError,'changed survey input'):
            self.build()

    def test_final_cycle_requires_ten_distinct_gates_and_assessment(self):
        self.write('research/round28/advisor/sequence.json',{'loops':self.loops,'target_loops':10})
        summaries={}
        for number,loop in enumerate(self.loops,1):
            self.gate(loop,number)
            summaries[loop]={'title':'Synthetic reviewed question '+loop,'bullets':[],'equations':[]}
        self.write('research/round28/advisor/summaries.json',summaries)
        self.write('research/round28/advisor/goal-pairs.json',{'initial_goals':[{'id':'G'+str(n+1),'loops':self.loops[2*n:2*n+2]} for n in range(3)],'later_goals':[{'id':'G'+str(n+1),'loops':self.loops[2*n:2*n+2]} for n in range(3,5)]})
        self.write('research/round28/network.json',{'nodes':[{'id':loop,'route':'round28-'+loop} for loop in self.loops],'edges':[]})
        self.write('research/round28/advisor/roadmap.json',{'next_goals':[]})
        self.write('research/round28/advisor/panel-progress.json',{'percentage_statement':'No numeric proof percentage.','obligations':[{'name':'Construction','status':'Open','missing':'Proof.'}]})
        data=self.build(require_complete=True)
        self.assertEqual(data['progress']['completed'],10)
        self.assertTrue(data['progress']['cycle_complete'])
        (self.root/'research/round28/advisor/g10-gate.json').unlink()
        with self.assertRaisesRegex(ValueError,'ten source-bound reviewed gates'):
            self.build(require_complete=True)

    def test_bundle_cannot_close_script(self):
        output=self.root/'bundle.js'
        builder.write_bundle({'title':'</script><script>bad()</script>','line':'a\u2028b'},output)
        written=output.read_text()
        self.assertNotIn('</script>',written)
        self.assertIn(r'<\/script>',written)
        self.assertIn(r'\u2028',written)


if __name__=='__main__':
    unittest.main()
