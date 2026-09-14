#!/usr/bin/env python3
"""Independent reverse I1 audit: incidence reconstruction, exact fractions, frozen inputs."""
import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import itertools as it
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
DIMS = (4, 2, 1)
AXES = tuple(tuple(int(i == j) for i in range(3)) for j in range(3))

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def add(a, b):
    return tuple(x + y for x, y in zip(a, b))

def owner(vertex, dims=DIMS):
    return tuple(vertex[i] // dims[i] for i in range(3))

def link(tail, direction):
    return (tuple(tail), direction)

def boundary_edges(a, i, j):
    # Reconstruct the square from consecutive vertices, not a copied tail formula.
    vertices = [a, add(a, AXES[i]), add(add(a, AXES[i]), AXES[j]), add(a, AXES[j])]
    edges = []
    for u, v in zip(vertices, vertices[1:] + vertices[:1]):
        axis = next(k for k in range(3) if u[k] != v[k])
        edges.append(link(min(u, v), axis))
    require(len(set(edges)) == 4, "elementary square lost an independent link")
    return set(edges)

def selected(a, i, j):
    return (i, j) == (0, 1) and a[1] % 2 == 0 and a[0] % 4 < 3

def face_record(a, i, j):
    support = sorted({owner(tail) for tail, _ in boundary_edges(a, i, j)})
    origin = owner(a)
    offsets = [tuple(s[k] - origin[k] for k in range(3)) for s in support]
    return {"anchor": list(a), "plane": [i,j], "selected": selected(a,i,j),
            "support_offsets": [list(s) for s in offsets]}

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def run():
    vertices = list(it.product(*(range(d) for d in DIMS)))
    block = {link(a,i) for a in vertices for i in range(3)}
    strip = set().union(*(boundary_edges((x,0,0),0,1) for x in range(3)))
    free = block - strip
    require(strip <= block, "reference strip crosses its owner block")
    require((len(block),len(strip),len(free)) == (24,10,14), "reference factor count")
    all_faces = [face_record(a,i,j) for a in vertices for i,j in it.combinations(range(3),2)]
    omitted = [r for r in all_faces if not r["selected"]]
    classes = Counter(tuple(tuple(v) for v in r["support_offsets"]) for r in omitted)
    star = sorted({tuple(v) for r in omitted for v in r["support_offsets"]})
    expected_star = sorted([(0,0,0), *AXES])
    require(star == expected_star, "fixed-range support must be exact star")
    require(len(omitted) == 21, "anchored omitted count")
    require(sum(classes.values()) == 21, "missing support class")
    require(all(len(r["support_offsets"]) > 1 for r in omitted), "contained-face counterexample")
    require(max(sum(abs(s[k]-t[k]) for k in range(3))
                for r in omitted for s in r["support_offsets"] for t in r["support_offsets"]) == 2,
            "some interactions span two coarse graph steps")
    # Ownership is by Euclidean division of each tail; translates tile all link tails.
    tiles = {}
    for b in it.product(range(-1,3), repeat=3):
        shift = tuple(b[i]*DIMS[i] for i in range(3))
        for tail,direction in block:
            e = link(add(tail,shift),direction)
            require(e not in tiles, "duplicate tail ownership")
            tiles[e] = b
            require(owner(e[0]) == b, "tail quotient disagrees with tiling")
        for a in vertices:
            for i,j in it.combinations(range(3),2):
                base = face_record(a,i,j)
                moved = face_record(add(a,shift),i,j)
                require(base["selected"] == moved["selected"] and
                        base["support_offsets"] == moved["support_offsets"],
                        "translation or phase class lost")
    # Every literal aligned box equals a padded link-block model plus free links.
    aligned = []
    for counts in [(1,1,1),(2,1,2),(1,2,2),(2,2,3)]:
        upper = tuple(counts[k]*DIMS[k] for k in range(3))
        inside = lambda a: all(0 <= a[k] < upper[k] for k in range(3))
        vv = list(it.product(*(range(n) for n in upper)))
        owned = {link(a,i) for a in vv for i in range(3)}
        literal = {link(a,i) for a in vv for i in range(3) if inside(add(a,AXES[i]))}
        literal_faces = []
        support_faces = []
        for a in vv:
            for i,j in it.combinations(range(3),2):
                edges = boundary_edges(a,i,j)
                key = (a,i,j)
                if edges <= literal:
                    literal_faces.append(key)
                if edges <= owned:
                    support_faces.append(key)
        require(literal_faces == support_faces, "actual-support boundary differs in aligned rectangle")
        selected_edges = set().union(*(boundary_edges(a,i,j) for a,i,j in literal_faces if selected(a,i,j)))
        require(not ((owned-literal) & selected_edges), "dangling link belongs to reference strip")
        aligned.append({"coarse_extents": counts,"literal_links":len(literal),
                        "spectator_links":len(owned-literal),"literal_faces":len(literal_faces)})
    # Any interval clipping a three-square strip retains a contiguous nonempty subset.
    clip_types = set()
    for lo in range(-1,5):
        for hi in range(lo+1,6):
            kept = ''.join('LMR'[x] for x in range(3) if lo <= x and x+1 <= hi)
            if kept:
                clip_types.add(kept)
    require(clip_types == {'L','M','R','LM','MR','LMR'}, "clipped component completeness")
    ratios = {'L':Q(1,2),'M':Q(1,8),'R':Q(1,2)}
    clipped_lower = {s: Q(3,4)-sum((ratios[c] for c in s),Q(0))
                     for s in clip_types if s != 'LMR'}
    clipped_lower['LMR'] = Q(3,4)-max(ratios['L'],ratios['R'])-ratios['M']
    require(min(clipped_lower.values()) == Q(1,8), "onsite physical gap normalization")
    coefficient = Q(len(omitted),24) / Q(1,8)
    require(coefficient == 7, "normalized anchor coefficient")
    # Actual-support versus whole-star empty boundary differ even in a two-block domain.
    domain = {(0,0,0),(1,0,0)}
    separator = boundary_edges((3,0,0),0,1)
    separator_support = {owner(a) for a,_ in separator}
    require(separator_support <= domain and not set(star) <= domain,
            "boundary distinction failed to discriminate")
    controls = {
      "anchor_only_support": {"rejected":True,"actual_crossing_omitted_faces":len(omitted)},
      "contained_face_count_used_as_anchor_count": {"rejected":True,"contained":0,"anchored":len(omitted)},
      "three_by_two_block_keeps_complete_strip": {
          "rejected":len({owner(a,(3,2,1)) for a,_ in strip})>1,
          "strip_owners":len({owner(a,(3,2,1)) for a,_ in strip})},
      "only_two_coarse_sites_per_face": {
          "rejected":any(len(r['support_offsets'])==3 for r in omitted)},
      "whole_star_empty_equals_actual_support": {"rejected":True,
          "witness_anchor":[3,0,0],"witness_plane":[0,1],"actual_support":[list(s) for s in sorted(separator_support)]},
      "twenty_faces_in_budget": {"rejected":Q(20,24)/Q(1,8)!=coefficient,
          "wrong_coefficient":str(Q(20,24)/Q(1,8)),"correct_coefficient":str(coefficient)},
      "generic_bare_bound_on_full_strip": {"rejected":Q(3,4)-sum(ratios.values())<Q(1,8),
          "bare_bound":str(Q(3,4)-sum(ratios.values())),"dressed_bound":str(clipped_lower['LMR'])}
    }
    require(all(c['rejected'] for c in controls.values()), "wrong-model control did not discriminate")
    return {
      "schema":"ym21-reverse-i1-v1", "loop":"i1", "direction":"reverse",
      "passed":True,"target_verdict":"verified_geometry_and_qualitative_source_dictionary",
      "comparison":{
        "block_link_count":len(block),"selected_link_count":len(strip),"free_link_count":len(free),
        "omitted_anchor_face_count":len(omitted),"coarse_support_offsets":[list(s) for s in star],
        "normalized_budget_coefficient":str(coefficient),"numerical_stability_constants_evaluated":False},
      "model":{"group":"SU(2)","spacing":"fixed positive", "alpha_over_E_star":"fixed positive",
        "delta_over_alpha":"1/8","omitted_coefficient_over_alpha":"tau/24",
        "tau":"dimensionless homogeneous Hamiltonian coefficient; not summability regulator",
        "geometry_test_negative_translates":"arithmetic tiling test; physical orthant handled by zero-interaction spectator extension"},
      "geometry":{"links":[[list(a),d] for a,d in sorted(block)],
        "reference_links":[[list(a),d] for a,d in sorted(strip)],
        "free_links":[[list(a),d] for a,d in sorted(free)],
        "face_classes":all_faces,"support_class_counts":[{"support":[list(v) for v in k],"count":v} for k,v in sorted(classes.items())],
        "tested_translation_cells":64,"aligned_boundary_fixtures":aligned,
        "clipped_component_lower_over_alpha":{s:str(q) for s,q in sorted(clipped_lower.items())}},
      "theorem_dictionary":{"source":"https://arxiv.org/pdf/math-ph/0411042",
        "definition_pages":[2],"theorems":[1,2,3],"theorem_pages":[3,4],
        "onsite":"shifted complete strip plus fourteen free links, divided by delta",
        "epsilon":"7*abs(tau)","constants":"c1(S), c2(S) positive existential, unevaluated",
        "sufficient_interval":"0 < abs(tau) < min(c1(S), 1/(2*c2(S)))/7",
        "gap_lower":"alpha/16 under the stated existential interval",
        "physical_representation":"limiting-state GNS, not assumed A2 product sector",
        "literature_novelty":"known theorem applied to selected-strip blocking; scientific priority unverified"},
      "controls":controls,
      "open_obligations":["Numerical c1/c2 extraction","Specific positive numerical tau admission",
          "Boundary-sequence state equivalence beyond the stated source exhaustion",
          "Weak-bare-coupling continuum trajectory and physical mass matching"]}

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    inputs=[HERE/'check.py',HERE/'report.md',HERE/'source-dictionary.json',
            ROOT/'research/round21/contracts/i1.json',ROOT/'research/round19/forward/a1/report.md',
            ROOT/'research/round19/forward/a2/report.md',ROOT/'research/round13/advisor/weak-coupling-stability.md',
            ROOT/'research/round20/advisor/post-ten-roadmap.md']
    require(all(p.is_file() for p in inputs), 'required bound source missing')
    before={str(p.relative_to(ROOT)):sha(p) for p in inputs}
    contract=json.loads((ROOT/'research/round21/contracts/i1.json').read_text())
    require(contract['loop']=='i1' and contract['status']=='frozen','contract not frozen I1')
    result=run()
    after={str(p.relative_to(ROOT)):sha(p) for p in inputs}
    require(before==after,'source changed during execution')
    result['source_bindings']=before
    (out/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    manifest={'schema':'ym21-source-bindings-v1','inputs':before,'outputs':{'results.json':sha(out/'results.json')}}
    (out/'source-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed':result['passed'],'comparison':result['comparison'],'output':str(out)}))

if __name__=='__main__':
    main()
