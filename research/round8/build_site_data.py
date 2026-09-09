#!/usr/bin/env python3
"""Assemble Review 8 from persisted research records; plots retain exact CSV rows."""
from pathlib import Path
import csv
import json
import shutil

HERE=Path(__file__).resolve().parent
SITE=HERE.parents[1]
DIST=SITE/'dist'

def rows(name):
    with (HERE/'gap'/name).open() as f:return list(csv.DictReader(f))

def make():
    tests=json.loads((HERE/'gap/test_results.json').read_text())
    proof=json.loads((HERE/'proof_results.json').read_text())
    audit=json.loads((HERE/'audit/regression_results.json').read_text())
    comparison=json.loads((HERE/'audit/history_comparison.json').read_text())
    if tests['status']!='pass' or proof['status']!='passed' or audit['status']!='passed':
        raise RuntimeError('A required evidence record is not passing')
    if not comparison['files'] or not all(r['same_bytes'] for r in comparison['files']):
        raise RuntimeError('Historical default trajectories changed')
    mesh=rows('fixed_volume_refinement.csv');volume=rows('finite_volume.csv');spectral=rows('hidden_light_state.csv')
    series=lambda data,x,y,m:dict(name=m[1],points=[[float(r[x]),float(r[y])] for r in data if float(r['mass'])==m[0]])
    D={'date':'2026-09-09','plots':{
      'mesh':{'title':'Mesh refinement at L = 10','xLabel':'Number of periodic sites N','yLabel':'Nonzero-mode frequency ω₁',
              'csv':'/gap-fixed-volume.csv','series':[series(mesh,'N','omega',(0.,'m = 0, k = 1')),series(mesh,'N','fixed_L_continuum_omega',(0.,'Continuum k = 1 at fixed L'))],
              'caption':'Exact periodic free-scalar diagnostic, not Yang–Mills. The k=0 mode is excluded. N increases while L=10 stays fixed; a=L/N. Values and reference are the exact rows in the CSV.'},
      'volume':{'title':'Physical volume grows at fixed a = 0.125','xLabel':'Physical box length L','yLabel':'Nonzero-mode frequency ω₁','csv':'/gap-volume.csv',
                'series':[series(volume,'L','omega',(0.,'Massless, k = 1')),series(volume,'L','omega',(.4,'Massive control, m = 0.4'))],
                'caption':'The massless nonzero-mode frequency tends to zero. The massive control tends to its declared mass. This is a free lattice model and not an extracted Yang–Mills gap.'},
      'plateau':{'title':'A tiny lighter-state overlap defeats an early plateau','xLabel':'Physical time t (model units)','yLabel':'Exact effective mass m_eff','csv':'/gap-spectral.csv',
                 'series':[dict(name='Exact effective mass',points=[[float(r['time']),float(r['effective_mass'])] for r in spectral]),dict(name='Lowest overlapping mass = 0.1',points=[[float(r['time']),float(r['light_mass'])] for r in spectral])],
                 'caption':'C(t)=10⁻¹² exp(−0.1t)+exp(−t), δ=0.5. Equal contributions at t≈30.7011. At t=20 the effective mass is ≈0.999925; at t=40 it is ≈0.100168. No noise or gauge configurations are simulated.'}
    }}
    # Derive the nonzero massive fixture from the recorded data, not a assumed value.
    massive=sorted({float(r['mass']) for r in volume if float(r['mass'])>0})
    if len(massive)!=1:raise RuntimeError('Ambiguous massive control')
    D['plots']['volume']['series'][1]=series(volume,'L','omega',(massive[0],f'Massive control, m = {massive[0]:g}'))
    for name,out in [('fixed_volume_refinement.csv','gap-fixed-volume.csv'),('finite_volume.csv','gap-volume.csv'),('hidden_light_state.csv','gap-spectral.csv')]:shutil.copy(HERE/'gap'/name,DIST/out)
    shutil.copy(HERE/'proof_results.json',DIST/'millennium-proof-map.json')
    D['sources']=[
      dict(id='clay-target',short='Clay: current status',title='Yang–Mills & the Mass Gap',authors='Clay Mathematics Institute',date='Maintained page; checked 9 September 2026',url='https://www.claymath.org/millennium/yang-mills-the-maths-gap/',use='Official unsolved status.',depth='Full maintained page',limit='The status page is not a proof of a proposed solution.'),
      dict(id='clay-prize',short='Clay: prize allocation',title='The Millennium Prize Problems',authors='Clay Mathematics Institute',date='Maintained page; checked 9 September 2026',url='https://www.claymath.org/millennium-problems/',use='$1 million allocation per problem; solved/unsolved listing.',depth='Full maintained page',limit='Closest connection is a project judgment based on the problem statements.'),
      dict(id='clay-statement',short='Jaffe–Witten: official formulation',title='Quantum Yang–Mills Theory',authors='Arthur Jaffe and Edward Witten',date='Official Millennium problem description; current hosted copy',url='https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf',use='Compact-simple group requirement, four-dimensional quantum existence and spectral target.',depth='Relevant formulation and construction sections read by advisor',limit='No independent audit of every cited construction theorem.'),
      dict(id='strong',short='Shen–Zhu–Zhu',title='A stochastic analysis approach to lattice Yang–Mills at strong coupling',authors='Hao Shen, Rongchan Zhu, Xiangchan Zhu',date='2022 preprint; CMP 2023',url='https://arxiv.org/abs/2204.12737',use='Rigorous strong-coupling infinite-volume lattice result; explicit regime boundary.',depth='Primary abstract and introductory material',limit='Detailed proof not rerun; no four-dimensional continuum theorem inferred.'),
      dict(id='glueball',short='Athenodorou–Teper',title='SU(N) gauge theories in 3+1 dimensions: glueball spectrum, string tensions and topology',authors='Andreas Athenodorou and Michael Teper',date='2021',url='https://arxiv.org/abs/2106.00364',use='Primary numerical spectrum and continuum-extrapolation reference.',depth='Primary abstract',limit='Configurations and fitted tables were not reproduced in this turn.'),
      dict(id='stochastic',short='Chevyrev',title='Stochastic quantisation of Yang–Mills',authors='Ilya Chevyrev',date='2022',url='https://arxiv.org/abs/2202.13359',use='Two- and three-dimensional finite-volume stochastic construction context.',depth='Primary abstract and scope statement',limit='Does not establish the four-dimensional prize target.'),
      dict(id='gross',short='Gross–Wilczek',title='Ultraviolet Behavior of Non-Abelian Gauge Theories',authors='David J. Gross and Frank Wilczek',date='25 June 1973',url='https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.30.1343',use='Nonabelian asymptotic freedom and difference from QED running.',depth='Primary abstract and bibliographic record',limit='No independent all-orders derivation or infrared mass-gap claim.'),
      dict(id='qed',short='Gell-Mann–Low',title='Quantum Electrodynamics at Small Distances',authors='Murray Gell-Mann and Francis E. Low',date='1954',url='https://journals.aps.org/pr/abstract/10.1103/PhysRev.95.1300',use='QED short-distance renormalization context.',depth='Primary abstract and bibliographic record',limit='The displayed one-loop equation is a stated perturbative model, not a physical pole theorem.'),
      dict(id='os',short='Osterwalder–Schrader',title="Axioms for Euclidean Green’s Functions",authors='Konrad Osterwalder and Robert Schrader',date='1973',url='https://doi.org/10.1007/BF01645738',use='Original Euclidean reconstruction framework.',depth='Primary bibliographic page reviewed by advisor',limit='Full reconstruction proof not freshly audited; its hypotheses remain explicit open obligations here.')
    ]
    D['audit']={
      'scope':'Line-by-line review of the two latest scientific solvers, proof-obligation builder and validators, plus targeted dependency checks. Original finite_scalar.py (530 lines), gravity_sim.py (661 lines), proof_obligations.py (153 lines), validate_simulations.py (157 lines), and relevant round 6 comparison/guard interfaces were examined. Full historical generations and third-party dependencies were not exhaustively reviewed.',
      'layers':[
        ['Original and corrected finite scalar suites','Passed','All default suite gates; numerical trajectories retained.'],
        ['Original and corrected gravity suites','Passed','Eight finite-time cases and declared analytic fixtures.'],
        ['Root implementation validator','47 checks passed','Rerun on the corrected suites, including optimized Python.'],
        ['New defect regressions',f"{len(audit['checks'])} checks passed",'Original failures reproduced; corrected behavior checked in normal and optimized Python.'],
        ['Independent numerical subset','21 checks passed','Non-symbolic checks only.'],
        ['Independent symbolic subset','Blocked: SymPy unavailable','21 checks were not rerun; historical results remain archived.'],
        ['Historical default histories',f"{len(comparison['files'])} CSV files byte-identical",'Compared original and corrected default runs.'],
        ['New spectral and finite-volume diagnostics',f"{tests['passed']} checks passed",'Independent matrix eigenvalues, Decimal references, edge inputs and exact toy formulas.'],
        ['Independent spectral data check','321 rows checked','Advisor used separate 80-digit Decimal arithmetic; max difference <6.7e-16.'],
        ['New proof replay','8-rule and 7-rule routes passed','Probability-certificate withdrawal and unproved-prize-seed controls reject unsupported paths.']
      ],
      'findings':[
        dict(status='Fixed',title='A custom matching coefficient changed the comparison problem',failure='g0_baseline_compare accepted chi_b=0.2 but compared against a baseline using a different coefficient.',impact='Spurious maximum differences of about 0.096536 in potential and 0.024136 in field; the tested default matched-coefficient result was unaffected.',fix='Map exactly supported matching prescriptions; explicitly report arbitrary unsupported coefficients unavailable. The archived solver is not modified to disguise the mismatch.',test='Original mismatch reproduced; all three representable prescriptions agree; unsupported custom chi_b is explicitly unavailable.'),
        dict(status='Fixed',title='Finite states could produce nonfinite diagnostics',failure='The g=nu=0, phi0=y0=1e155 test retained finite state entries but overflowed energy terms into NaN.',impact='A completed integration did not imply meaningful energy or work diagnostics.',fix='Check initial and derived observables for finiteness and raise a semantic failure for unrepresentable diagnostics.',test='Original nonfinite output reproduced; corrected solver rejects it instead of returning a success-like record.'),
        dict(status='Fixed',title='An empty gravity collection could pass vacuously',failure='build_results([]) used all() on empty collections and started with status passed.',impact='No trajectories could be mistaken for seven passing trajectory gates; failed populated gates could disagree with the top-level status.',fix='Reject empty input and derive semantic status from actually evaluated trajectory and analytic gates.',test='Empty-run rejection and deliberately failed gates are checked; the full eight-case suite still passes.'),
        dict(status='Limited',title='Small perturbation differences do not certify response-grid convergence',failure='The older perturbation-step comparison varied epsilon, while the node refinement measured only the base field and potential.',impact='It did not establish a response quadrature error bound or an observed second-order finite-difference slope.',fix='Keep those claims scoped and add a separate fixed-physical-domain response-grid experiment.',test='New response-grid results, when present, are recorded separately from perturbation-size comparisons.')
      ],
      'verdict':'The corrected validators and APIs preserve the accepted default trajectories while closing three demonstrated acceptance failures. The spectral lemmas and toy calculations reject invalid routes to a mass-gap claim. They do not supply continuum Einstein–QED closure or solve Yang–Mills.'
    }
    D['experiments']=[
      dict(status='Executed',title='Separate a finite-box frequency from a continuum gap',hypothesis='A stable positive finite-box result can coexist with zero infinite-volume spectral onset.',method='Exact periodic nonzero-mode dispersion, independent matrix eigenvalues, fixed-L mesh refinement and fixed-a volume growth.',reject='Reject the implementation if exact-reference errors or zero-mode labels fail.',scope='A counterexample to the inference from finite positivity; no Yang–Mills conclusion.'),
      dict(status='Executed',title='Expose hidden lighter spectral weight',hypothesis='A tiny low-energy overlap produces an early heavy effective-mass plateau.',method='Stable two-exponential correlator, short and long times, high-precision checks and exact support inequalities.',reject='Reject the implementation if effective masses violate positivity-derived bounds beyond arithmetic tolerance.',scope='Correct interpretation of this positive toy correlator; no lower-bound certification from a fit.'),
      dict(status='Planned',title='Refine the scalar response on a fixed physical domain',hypothesis='The delayed response converges in momentum nodes, independently of epsilon refinement.',method='Hold N, K, state, pulse and epsilon fixed; compare field, potential and scalar responses as quadrature nodes increase.',reject='If histories fail to converge, withhold a response precision claim and diagnose quadrature or time integration.',scope='A finite-model response statement only; this does not remove physical cutoffs.'),
      dict(status='Planned',title='Derive one common current and directional quantum stress',hypothesis='A single causal renormalization prescription produces independently calculated observables obeying the force Ward identity.',method='Start in a prescribed smooth axial geometry; vary one common quantum functional to obtain current, energy and both pressures; test conservation without defining pressure from that identity.',reject='Stop if counterterms, state or support work differ across observables, or if the Ward defect persists under refinement.',scope='The next genuine Einstein–QED interface obligation; metric evolution follows only after it is closed.'),
      dict(status='Planned',title='Establish a bounded nonabelian numerical baseline',hypothesis='A declared finite SU(2) Wilson implementation reproduces gauge-invariance and exact small-system fixtures.',method='New action/state contract; gauge-transformation checks, plaquette identities, exact controls and autocorrelation-aware sampling before any spectrum extraction.',reject='Do not pursue spectral interpretation while invariance, sampling or physical normalization fails.',scope='Finite-regulator implementation readiness. A mass-gap proof still needs all continuum obligations.'),
      dict(status='Planned',title='Audit one-loop running and logarithm conventions',hypothesis='Independent integration reproduces opposite QED and pure Yang–Mills ultraviolet running.',method='Compare analytic inverse-coupling formulas with ODE integration in log(mu/mu0); test the factor of two for log(mu squared).',reject='Stop before perturbative applicability fails; reject mismatched sign or scale conventions.',scope='Verification of a declared perturbative model, not all-orders physics or a Landau-pole resolution.')
    ]
    D['documents']={
      'advisor.md':(HERE/'spectral-proof.md').read_text(),
      'diagnostics.md':(HERE/'gap/README.md').read_text(),
      'code-audit.md':(HERE/'audit/audit-review.md').read_text(),
      'proof-route.md':'# Review 8 proof routes\n\nThe assumptions and complete argument are in spectral-proof.md. The replay uses the previously audited ground-Horn engine, h=0, and separate forward cost certification. It does not check mathematical inference inside a rule.\n\n'+json.dumps({k:dict(status=v['result']['status'],cost=v['result'].get('certified_cost'),steps=v['result'].get('certified_proof')) for k,v in proof['routes'].items()},indent=2)
    }
    response=json.loads((HERE/'audit/response_grid_results.json').read_text())
    if response['status']!='resolved_working_threshold':raise RuntimeError('Response working threshold not resolved')
    with (HERE/'audit/response_grid_histories.csv').open() as f:response_rows=list(csv.DictReader(f))
    D['response']=response
    D['plots']['response']={'title':'Delayed field response at three momentum resolutions','xLabel':'Dimensionless time s','yLabel':'Centered field response ∂x/∂λ','csv':'/scalar-response-grid.csv',
      'series':[dict(name=f'{n} nodes per Landau level',points=[[float(r['t']),float(r['x'])] for r in response_rows if int(r['nK'])==n]) for n in response['nodes']],
      'caption':'Finite fixed-domain model; N=1 inclusive Landau cutoff, K=20, b=10, g=0.1, ν=0.5. Probe starts at s=4.5. Curves nearly overlap; the table gives the resolved adjacent-grid differences. Raw centered responses, including the zero pre-probe samples, are in the CSV.'}
    shutil.copy(HERE/'audit/response_grid_histories.csv',DIST/'scalar-response-grid.csv')
    D['experiments'][2].update(status='Executed',method='Held physical cutoffs, source and ε=5e−5 fixed. Recorded a, x, φ and y centered responses at 64, 128 and 256 quadrature nodes per level.',scope='128→256 maximum field discrepancy 1.38903e−6 is below the predeclared 2e−5 working scale. Adjacent-grid agreement is not a rigorous total-error bound.')
    D['audit']['layers'].append(['New scalar response node refinement','Working threshold met at 128→256','64→128 fails the 2e−5 absolute criterion; all four responses and pre-probe sample counts recorded.'])
    D['audit']['findings'][-1].update(fix='Added the separate response-grid experiment; retained the original precision claims at their actual scope.',test='Field-response adjacent-grid discrepancy falls from 2.87154e−4 to 1.38903e−6. This supports a working finite-grid scale, not a continuum or rigorous error bound.')
    (DIST/'research-millennium-data.js').write_text('window.OBSERVATORY_MILLENNIUM = '+json.dumps(D,ensure_ascii=False,allow_nan=False)+';\n')
    (HERE/'site_data.json').write_text(json.dumps(D,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'plots':len(D['plots']),'sources':len(D['sources']),'new_checks':tests['passed'],'audit_regressions':len(audit['checks'])}))

if __name__=='__main__':make()
