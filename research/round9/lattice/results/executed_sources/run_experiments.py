"""Execute the fixed, predeclared audit workload. Runtime: a few minutes on CPU."""
from __future__ import annotations
import concurrent.futures
import csv
import hashlib
import json
import math
import platform
from pathlib import Path
import sys
import time
import numpy as np
import scipy
from su2_lattice import WilsonLattice, one_plaquette_iid, exact_one_plaquette, series_summary, compare_to_exact, validate_links

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'results'
BETAS = [0.0, 0.5, 2.2]
WARMUP = 512
SAMPLES = 2048


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2, allow_nan=False)+'\n')


def producer_hashes():
    return {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in
            ['su2_lattice.py','test_lattice.py','run_experiments.py','PREDECLARED_CONTRACT.md']}


def chain_job(args):
    beta, start, seed = args
    begin = time.perf_counter()
    lat = WilsonLattice(beta=beta, start=start, seed=seed)
    tag = f'beta_{beta:g}_{start}_seed_{seed}'
    samples = []
    warmup = []
    for sweep in range(WARMUP):
        acceptance = lat.sweep()
        if sweep % 16 == 0 or sweep == WARMUP-1:
            warmup.append([sweep+1, float(lat.plaquettes().mean()), acceptance])
    for sweep in range(SAMPLES):
        acceptance = lat.sweep()
        p = lat.plaquettes()
        samples.append([sweep+1, float(p.mean()), float((p*p).mean()), lat.ward(), acceptance])
    with (OUT/f'{tag}.csv').open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['measured_sweep','plaquette_mean','plaquette_square_mean','ward_mean','acceptance'])
        writer.writerows(samples)
    with (OUT/f'{tag}_warmup.csv').open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['warmup_sweep','plaquette_mean','acceptance'])
        writer.writerows(warmup)
    np.savez_compressed(OUT/f'{tag}_final_links.npz', links=lat.links, lengths=lat.lengths, beta=beta, seed=seed)
    samples = np.asarray(samples)
    stats = {}
    for col, name in [(1,'plaquette'),(2,'plaquette_square'),(3,'ward')]:
        stats[name] = {str(batch):series_summary(samples[:,col], batch) for batch in [16,32,64]}
    checks = {}
    if beta == 0:
        checks['plaquette_mean_exact_0'] = compare_to_exact(stats['plaquette']['64'], 0)
        checks['plaquette_second_exact_quarter'] = compare_to_exact(stats['plaquette_square']['64'], 0.25)
        checks['ward'] = {'status':'trivial_algebraic','target':0.0,'z':None}
    else:
        checks['ward'] = compare_to_exact(stats['ward']['64'], 0)
    payload = {'beta':beta,'lengths':list(lat.lengths),'start':start,'seed':seed,
               'warmup_sweeps':WARMUP,'measured_sweeps':SAMPLES,'measurement_stride':1,
               'acceptance_mean':float(samples[:,4].mean()),'final_link_norm_defect':validate_links(lat.links),
               'elapsed_seconds':time.perf_counter()-begin,'statistics':stats,'exact_diagnostics':checks,
               'raw_csv':f'{tag}.csv','interpretation':'finite-volume sampling diagnostics; no mass inference'}
    save_json(OUT/f'{tag}.json', payload)
    return payload


def iid_suite():
    out = []
    for index, beta in enumerate(BETAS):
        seed = 915000+index
        values, trials = one_plaquette_iid(beta, 20000, seed)
        exact = exact_one_plaquette(beta)
        with (OUT/f'one_plaquette_beta_{beta:g}.csv').open('w',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['sample','scalar_trace'])
            writer.writerows(enumerate(values,1))
        stats = {}
        for label, x, target in [('mean',values,exact['mean']), ('second_moment',values**2,exact['second_moment'])]:
            summary = {'status':'usable','mean':float(x.mean()),'se':float(x.std(ddof=1)/math.sqrt(len(x))), 'n':len(x)}
            stats[label] = summary | compare_to_exact(summary,target)
        out.append({'beta':beta,'seed':seed,'samples':20000,'proposals_generated':trials,
                    'exact':exact,'checks':stats,'interpretation':'one independent SU(2) matrix, not a 4D lattice formula'})
    return out


def main():
    OUT.mkdir(exist_ok=True)
    if (OUT/'experiment_manifest.json').exists():
        raise RuntimeError('Refusing to overwrite a recorded run. Preserve it before an explicitly new experiment.')
    test_result = json.loads((OUT/'deterministic_checks.json').read_text())
    if not test_result['successful']:
        raise RuntimeError('deterministic validation did not pass')
    manifest = {'contract':'PREDECLARED_CONTRACT.md','source_sha256_before':producer_hashes(),
                'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'platform':platform.platform(),
                'parameters':{'betas':BETAS,'lengths':[2,2,2,2],'warmup':WARMUP,'samples':SAMPLES,
                              'chains':['cold','hot'],'seeds':[914000+10*i+j for i in range(3) for j in range(2)]},
                'state':'started','statistical_gates':'predeclared before sampling; no tuned reruns'}
    save_json(OUT/'experiment_manifest.json',manifest)
    iid = iid_suite()
    save_json(OUT/'one_plaquette_diagnostics.json',iid)
    jobs = [(beta,start,914000+10*i+j) for i,beta in enumerate(BETAS) for j,start in enumerate(['cold','hot'])]
    chains = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(chain_job,job) for job in jobs]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            chains.append(result)
            print(f"completed beta={result['beta']} {result['start']}: plaquette={result['statistics']['plaquette']['64']['mean']:.7f}; diagnostics={result['exact_diagnostics']}",flush=True)
    chains.sort(key=lambda c:(c['beta'],c['start']))
    comparisons = []
    for beta in BETAS:
        a,b = [c for c in chains if c['beta'] == beta]
        sa,sb = a['statistics']['plaquette']['64'],b['statistics']['plaquette']['64']
        s = {'status':'usable' if sa['status']==sb['status']=='usable' else 'insufficient',
             'mean':sa['mean']-sb['mean'],'se':math.hypot(sa['se'],sb['se'])}
        comparisons.append({'beta':beta,'cold_minus_hot':s['mean'],'combined_se':s['se'],
                            'comparison':compare_to_exact(s,0)})
    all_diagnostics = {'one_plaquette':iid,'chains':chains,'hot_cold_comparisons':comparisons,
                       'claim':'Implementation and exact finite-lattice identity diagnostics only.',
                       'excluded_claims':['glueball mass extraction','continuum extrapolation','infinite-volume limit','Millennium proof']}
    save_json(OUT/'all_diagnostics.json',all_diagnostics)
    manifest['source_sha256_after'] = producer_hashes()
    if manifest['source_sha256_before'] != manifest['source_sha256_after']:
        manifest['state'] = 'source_changed_during_run'
        save_json(OUT/'experiment_manifest.json',manifest)
        raise RuntimeError('Producer source changed during experiment')
    manifest['state'] = 'completed'
    manifest['output_sha256'] = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.iterdir())
                               if p.is_file() and p.name != 'experiment_manifest.json'}
    save_json(OUT/'experiment_manifest.json',manifest)
    print('Fixed workload completed; all insufficient/flagged outcomes retained.',flush=True)


if __name__ == '__main__':
    main()
