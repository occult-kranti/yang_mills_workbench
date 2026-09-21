"""Index recorded research studies and every numbered feedback-loop gate."""
from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'research/round25'

# Before explicit two-loop contracts, a run means the named study, not each ODE
# sample or unit test. Numerical refinements remain grouped under their study.
EARLY={
3:[
 ('production','Source-off electric reversal','Recorded finite-regulator endpoint x(50)≈-0.03757 on the accepted 4096-node, Landau 0–8, K=40 run.','Finite homogeneous Maxwell–Dirac mean field; no continuum or gravity solution.'),
 ('refinement','Regulator and node refinements','2048→4096 node histories differ by 3.26e-9; a separate Landau-level comparison changes the endpoint by 5.06e-8.','Component diagnostics, not rigorous trajectory enclosures.'),
 ('controls','Matching and independent formulations','Weak-response, spinor/Bloch, bosonized and gravitational identity checks document what survives model changes.','Conservation can hold for a consistently wrong prescription.'),
 ('benchmark','Retained precision failure','The advisor absolute benchmark was approximately 1.82e-18.','The requested 1e-18 gate failed; successful script exit did not close it.')],
4:[
 ('response','Source-amplitude tangent','A checked amplitude derivative and finite-difference comparisons extend the finite-regulator response.','Quantum noise, regulator removal and gravitational closure remain open.'),
 ('audit','Source and report reconciliation','Source hashes, saved traces, initial failed diagnostics and corrected acceptance are retained.','A corrected finite-model response is not a new continuum theorem.')],
5:[
 ('theorem','Finite-model existence and response','Conditional global existence and complete tangent equations with explicit coefficient assumptions.','Exact rational interpretation of floating inputs does not certify transcendental rounding.'),
 ('planner','Two-front proof planning','A finite reviewed rule library reaches the selected conditional theorem; separate replay and a subset oracle check routes.','This is a proof-obligation planner, not a general proof-assistant kernel.'),
 ('gravity','Bianchi-I constraint bridge','Conditional constraint propagation connects the reduced equations to a gravity consistency question.','Common covariant quantum current and directional stress remain unconstructed.')],
6:[
 ('coefficient','Exact finite-window coefficient','A continuous-momentum formula, global maximum and rational Z>3/4 certificate at fixed b=10,K=20.','Finite physical cutoffs and positive quadrature assumptions remain.'),
 ('cofinal','Cofinal cutoff obstruction','The unmodified matching cannot preserve a uniform positive coefficient margin when both cutoffs are removed cofinally.','An obstruction to that matching route, not proof that every renormalization fails.'),
 ('tangent','Stationary second variation','Positive second variation controls electric and transformed transverse tangents.','An explicit example defeats boundedness of the raw tangent.'),
 ('repair','Core and coefficient audit','Recorded source-center and coefficient defects were repaired, with failed intermediate gates preserved.','Numerical diagnostics are not interval enclosures of a full trajectory.')],
7:[
 ('finite-scalar','Scalar-coupled finite model','A declared scalar coupling extends the regulated mean-field experiment with explicit balances.','It changes the model and does not remove quantum ultraviolet questions.'),
 ('gravity-scalar','Reduced gravitational simulation','A separate scalar/gravity reduced model and checks expose its closure assumptions.','No common renormalized quantum current/stress construction.'),
 ('subtraction','Reference-subtraction and bounded-addition tests','A restricted subtraction identity and a bounded-addition obstruction delimit possible repairs.','A new free variable is not an automatic ultraviolet completion.')],
8:[
 ('spectral','Spectral and finite-volume counterexamples','Exact lattice/spectral-mixture diagnostics and two conditional spectral lemmas distinguish finite gaps from physical limits.','No accepted implication reaches the Millennium target.'),
 ('delayed','Delayed scalar-response study','A new grid study and three acceptance/implementation repairs make delayed response testable.','Numerical comparisons are finite-model evidence; 21 unavailable symbolic replays stayed blocked.'),
 ('proof','Conditional proof replay','Frozen conventional spectral premises support the recorded finite-rule routes.','Planner success is not formal verification of the analytic lemmas.')],
9:[
 ('haar','Nonabelian identity hierarchy','Finite SU(2) Haar identities, uniqueness conditions and exact counterexamples define a proof-obligation map.','No literature novelty or continuum solution claimed.'),
 ('wilson','Four-dimensional Wilson lattice runs','Six chains at beta 0,0.5,2.2 record stochastic finite-lattice diagnostics.','The beta=2.2 uncertainty/hot-cold comparison was insufficient because autocorrelation exceeded threshold.'),
 ('transfer','Central-convolution spectrum','An exact spectrum and physical-time scaling benchmark separate central convolution from an interacting gauge-projected transfer matrix.','The benchmark is not the required full transfer construction.')],
10:[
 ('gap','Certified full one-plaquette gap','Delta≥0.999999 alpha for every 0≤lambda/alpha≤10, including representation tail and coupling continuity.','One finite square; the one-plaquette/Mathieu mechanism is established prior work.'),
 ('drive','Driven one-square diagnostics','A declared smooth ramp includes source-work and representation/time-step comparisons.','No rigorous dynamic-tail enclosure from those diagnostics alone.'),
 ('quotient','Three-trace reconstruction','x,y,z classify two SU(2) matrices up to simultaneous conjugation, with the exact constrained body.','x,y alone fail; the coupled operator was a subsequent task.')],
11:[
 ('operator','Physical two-plaquette operator','The seven-link, six-Gauss-constraint operator retains shared-link and mixed derivatives on the three-trace quotient.','Infinite representation space on a finite spatial graph.'),
 ('gap','Continuous two-plaquette gap certificate','Full finite-graph gap≥0.96 alpha on the closed coefficient square [0,2]²; exact matched-point interval retained.','Tail and continuity arguments are essential; Ritz differences alone do not prove a full gap.'),
 ('dynamics','Driven checks and falsifiers','Independent dynamics, domain and proof-wrapper checks preserve the actual shared-link model.','They do not supply an infinite-volume or continuum construction.')],
12:[
 ('dynamic-tail','Rigorous representation-error theorem','A full-Hilbert dynamic error bound and separate exact rational computed-state fixture extend finite-graph evolution.','Initial state, domain and drive assumptions remain explicit.'),
 ('volume','Growing-graph bound and counterbenchmark','Volume dependence and a tensor example expose why finite-graph certificates need uniform estimates.','Gibbs and Hamiltonian gaps are different claims.'),
 ('closure','Compact hierarchy audit','Exact identities and variance reject a defined closure and check source formulas version by version.','A compact static hierarchy does not automatically determine dynamics.')],
13:[
 ('locality','Local finite-time volume limit','A complete factorial boundary tail controls local dynamics at fixed spacing and time.','Dynamics alone do not construct a vacuum or gap.'),
 ('stability','Qualitative homogeneous stability','Application of a known stability theorem gives gap≥3alpha/8 for sufficiently small magnetic/electric ratio.','The admissible threshold is existential and numerically unevaluated.'),
 ('moments','Compact moment certificates and uniqueness','Twenty-eight rational finite-moment certificates and the complete recurrence/support hierarchy identify a unique tilted Haar measure.','No full-hierarchy convergence rate; optimization slack must vanish.'),
 ('response','Exact scalar response','u′=Var(x), kappa u′+3u=kappa(1-u²), with regularity fixing the origin branch.','The scalar belongs to the specified compact Euclidean measure.')]
}

def sha(p): return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def gate_paths(n):
    base=ROOT/f'research/round{n}/advisor'
    if n==15:return sorted((base/'loop-gates').glob('*.json'))
    pattern='loop*_gate.json' if n==14 else '*-gate.json'
    return [p for p in sorted(base.glob(pattern)) if re.fullmatch(r'(?:[a-z]+[12]|loop[12])[-_]gate\.json',p.name)]
def flatten(v):
    if isinstance(v,str):return [v]
    if isinstance(v,list):return [str(x) for x in v]
    return []
def main():
    rounds=[];bindings={};gate_count=0
    for n,studies in EARLY.items():
        base=f'evidence/qeg-research/round{n}' if n<=7 else f'research/round{n}'
        source=base+'/README.md';bindings[source]=sha(source)
        rows=[{'id':id,'title':title,'verdict':'historical study — scope below',
               'bullets':[result,limit],'sources':[source],'kind':'study'} for id,title,result,limit in studies]
        rounds.append({'round':n,'runs':rows,'scope':'Recorded studies and grouped refinements; not retrospective two-loop contracts'})
    extra24=json.loads((ROOT/'research/round24/advisor/contributions.json').read_text())
    bindings['research/round24/advisor/contributions.json']=sha('research/round24/advisor/contributions.json')
    for n in range(14,26):
        rows=[]
        for p in gate_paths(n):
            d=json.loads(p.read_text());path=str(p.relative_to(ROOT));bindings[path]=sha(path)
            loop=d.get('loop',d.get('phase',p.stem.split('-')[0]));verdict=d.get('verdict',d.get('status','see gate'))
            bullets=[]
            for k in ['claim','mathematical_result','accepted','finding','scope','target_verdict','feedback','limitations','limits','remaining_open']:
                bullets+=flatten(d.get(k))
            if n==24:
                x=next(x for x in extra24['loops'] if x['loop']==loop)
                title=x['title'];bullets=[x['statement'],*x['equations'],x['feedback'],*x['limits']]
            else:title=next(iter(bullets),str(loop).upper())
            bullets=list(dict.fromkeys(bullets))
            if not bullets:raise ValueError('no source-backed summary '+path)
            sources=[path]
            for direction in ['forward','reverse','backward','solo']:
                report=f'research/round{n}/{direction}/{str(loop).lower()}/report.md'
                if (ROOT/report).exists():sources.append(report)
            if n==19 and loop=='c2':
                bullets.append('Later admission repairs are recorded separately in Round20 and Round21; the historical theorem scope is unchanged.')
            if n==23 and loop in ['t2','u1','u2'] or n==25:
                bullets.append('Single-agent correlated derivation and skeptical self-review; not independent review.')
            rows.append({'id':loop,'title':title,'verdict':verdict,'bullets':bullets,'sources':sources,'kind':'physics_loop','gate_sha256':bindings[path]})
            gate_count+=1
        if not rows:raise ValueError('missing round '+str(n))
        rounds.append({'round':n,'runs':rows,'scope':'Each entry is one research loop; replays, reviews and repairs are not extra loops'})
    result={'title':'Every recorded round: results and project increments',
      'coverage':'Rounds 3–25. No independently identifiable Round1/2 packages are present in this repository; their results are not invented. Earlier records use named studies; explicit loop gates begin at Round14.',
      'novelty':'Project increments are new to this workbench or repaired here. Literature priority is unverified; established methods are not claimed as inventions.',
      'method':'Newton: reconstruct the missing premise. Tesla: include the surrounding mechanism. Preserve each historical verdict and the later correction that changes its use.',
      'counts':{'rounds':len(rounds),'entries':sum(len(r['runs']) for r in rounds),'numbered_physics_loops':gate_count},
      'rounds':rounds,'source_sha256':bindings}
    (OUT/'all-results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    md=['# All recorded results and project increments',result['coverage'],result['novelty']]
    for r in rounds:
        md.append(f"## Round {r['round']}")
        for x in r['runs']:
            md.append(f"### {x['id']}: {x['title']}\n\nVerdict: {x['verdict']}")
            md.append('\n'.join('- '+b for b in x['bullets']))
            md.append('Sources: '+' · '.join(f'[{Path(p).name}](https://github.com/occult-kranti/yang_mills_workbench/blob/main/{p})' for p in x['sources']))
    (OUT/'ALL_RESULTS.md').write_text('\n\n'.join(md)+'\n')
    print(json.dumps(result['counts']))
if __name__=='__main__':main()
