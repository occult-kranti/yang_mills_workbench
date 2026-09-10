"""Bisect exactly the insufficient cells of the frozen A1 cover."""
import hashlib,importlib.util,json
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent
A1=ROOT.parent/'A1'
A1_COVER_SHA='c0850838befc29a730f40e1fc3cffa32dd316264ab7fce191fc5eebf747a7f9a'
A1_EVIDENCE_SHA='b27eb6f20363912422e3febe0500ec1aef2e2b64f9ba21b3663652f8d3d4ac2a'
SOURCE_BYTES=Path(__file__).read_bytes()
SOURCE_SHA=hashlib.sha256(SOURCE_BYTES).hexdigest()
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
if digest(A1/'cover.py')!=A1_COVER_SHA or digest(A1/'output/cover.json')!=A1_EVIDENCE_SHA:
    raise ValueError('frozen A1 input mismatch')
spec=importlib.util.spec_from_file_location('ym15_a1_cover',A1/'cover.py')
cover=importlib.util.module_from_spec(spec);spec.loader.exec_module(cover)

def _input():
    if Path(__file__).read_bytes()!=SOURCE_BYTES or digest(A1/'cover.py')!=A1_COVER_SHA or digest(A1/'output/cover.json')!=A1_EVIDENCE_SHA:
        raise ValueError('source or A1 input changed')
    initial=json.loads((A1/'output/cover.json').read_text())
    cover.verify(initial)
    return initial

def run(max_iterations=8,max_cells=4096):
    if type(max_iterations) is not int or not 0<=max_iterations<=16:
        raise ValueError('max_iterations must be an integer in[0,16], not Boolean')
    if type(max_cells) is not int or not 8<=max_cells<=4096:
        raise ValueError('max_cells must be an integer in[8,4096], not Boolean')
    current=_input();levels=[current];transitions=[]
    stop='positive-cover' if current['status']=='certified-positive-cover' else None
    for step in range(max_iterations):
        if stop: break
        failed=current['insufficient_indices']
        if len(current['cells'])+len(failed)>max_cells:
            stop='cell-cap';break
        edges=[current['cells'][0]['left']]
        for i,cell in enumerate(current['cells']):
            if i in failed: edges.append(cell['center'])
            edges.append(cell['right'])
        refined=cover.build(edges,24)
        transitions.append({'from_level':len(levels)-1,'bisected_indices':failed,
                            'previous_cell_count':current['cell_count'],
                            'new_cell_count':refined['cell_count']})
        levels.append(refined);current=refined
        if current['status']=='certified-positive-cover':stop='positive-cover'
    if stop is None: stop='iteration-cap'
    return {'schema':'ym15-adaptive-cover-v1','source_sha256':SOURCE_SHA,
            'a1_source_sha256':A1_COVER_SHA,'a1_evidence_sha256':A1_EVIDENCE_SHA,
            'policy':'bisect only cells with nonpositive exact transported lower',
            'max_iterations':max_iterations,'max_cells':max_cells,
            'levels':levels,'transitions':transitions,'stop_reason':stop,
            'completed_refinements':len(transitions),
            'total_evaluated_cells':sum(x['cell_count'] for x in levels),
            'status':current['status'],'final_cell_count':current['cell_count'],
            'final_minimum_lower':current['minimum_lower']}

def verify(record):
    if type(record) is not dict or record.get('schema')!='ym15-adaptive-cover-v1':
        raise ValueError('wrong adaptive schema')
    expected=run(record.get('max_iterations'),record.get('max_cells'))
    if not cover.typed_equal(record,expected):
        raise ValueError('adaptive source, arithmetic or policy replay failed')
    return True
