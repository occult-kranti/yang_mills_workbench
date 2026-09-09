#!/usr/bin/env python3
"""Pre-render equation assets and inspect prospective formula sizing."""
from pathlib import Path
import json
from build_guide import Renderer, load_refs

ROOT=Path(__file__).resolve().parent
r=Renderer(ROOT/'guide.md', load_refs(ROOT/'guide_references.json'))
blocks=r.pandoc()
math=[]
def walk(x):
    if isinstance(x, dict):
        if x.get('t')=='Math':
            mode, expr=x['c']; math.append((mode['t']=='DisplayMath',expr))
        for val in x.values(): walk(val)
    elif isinstance(x,list):
        for v in x:walk(v)
walk(blocks)
for display,expr in dict.fromkeys(math):
    if display:r.display_math_block(expr)
    else:r.inlines([{'t':'Math','c':[{'t':'InlineMath'},expr]}])
r.write_diagnostics(ROOT/'guide_formula_preflight.json')
print(json.dumps({'math_instances':len(math),'unique':len(set(math)),'failures':r.formula_failures,'layout_warnings':r.layout_warnings},indent=2))
