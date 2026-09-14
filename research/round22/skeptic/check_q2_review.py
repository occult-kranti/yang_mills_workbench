#!/usr/bin/env python3
"""Compare both frozen Q2 spectra against independent pre-freeze derivation."""
import argparse,hashlib,json,subprocess,sys,tempfile
from fractions import Fraction as F
from pathlib import Path

def need(ok,why):
    if ok is not True:raise RuntimeError(why)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def matrix(a):return [[F(x) for x in r] for r in a]
def serial(a):return [[str(x) for x in r] for r in a]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    out=parser.parse_args().output;need(not out.exists(),'fresh output required')
    root=Path(__file__).resolve().parents[3];base=root/'research/round22/skeptic'
    prep=base/'check_q2_preparation.py';prepared=base/'q2-preparation-checks.json'
    with tempfile.TemporaryDirectory(prefix='ym22-q2-review-independent-') as folder:
        target=Path(folder)/'preparation.json'
        run=subprocess.run([sys.executable,'-B',*(['-O'] if sys.flags.optimize else []),str(prep),'--output',str(target)],capture_output=True,text=True)
        need(run.returncode==0,'independent preparation failure: '+run.stderr)
        need(target.read_bytes()==prepared.read_bytes(),'independent frozen preparation drift')
    inputs={str(p.relative_to(root)):sha(p) for p in [prep,prepared]}
    own=json.loads(prepared.read_text());weights={F(r['energy_over_alpha']):matrix(r['matrix']) for r in own['spectral_weights']}
    fpath=root/'research/round22/forward/q2/output/results.json';rpath=root/'research/round22/reverse/q2/output/results.json'
    forward=json.loads(fpath.read_text());reverse=json.loads(rpath.read_text())
    for p in [fpath,rpath]:inputs[str(p.relative_to(root))]=sha(p)
    fw={F(e):matrix(w) for e,w in forward['claims']['spectral_weights'].items()}
    rw={F(r['energy_over_alpha']):matrix(r['matrix']) for r in reverse['claims']['leading_spectral_weights']}
    need(fw==weights==rw,'independently prepared exact spectrum differs')
    first=[[sum((e*w[i][j] for e,w in weights.items()),F(0)) for j in range(2)] for i in range(2)]
    at_one=[[sum((w[i][j]/(e+1) for e,w in weights.items()),F(0)) for j in range(2)] for i in range(2)]
    need(first==matrix(forward['spectral_first_moment']),'first moments differ from graph comparator')
    need(at_one==matrix(forward['self_energy_z_alpha_dimensionless']),'fixed-energy self-energy differs')
    need(at_one==[[F(19,16),F(1,16)],[F(1,16),F(2285061,3979360)]],'exact nonconstant channel reserve')
    need(first[0][0]==F(57,4) and first[1][1]==F(285,8),'scalar reference ambiguity unresolved')
    need(F(250)*F(1,100)**3/3==F(1,12000),'uniform-delay endpoint coefficient')
    need(F(250)*F(1,100)**3/9==F(1,36000),'uniform-self-energy endpoint coefficient')
    result={'schema':'ym22-skeptic-independent-comparison-v1','loop':'q2','passed':True,
       'driver_sha256':sha(Path(__file__)),'input_hashes':inputs,'producer_imports':False,
       'frozen_independent_preparation_byte_exact':True,'both_spectra_match_independent_preparation':True,
       'spectral_weights':own['spectral_weights'],'first_spectral_moment':serial(first),
       'self_energy_z_alpha_over_alpha_lambda_squared':serial(at_one),
       'endpoint_uniform_delay_error':'alpha^2/(12000e)','endpoint_uniform_self_energy_error':'alpha/36000',
       'scope':'Actual graph and algebra controls are in the unchanged pre-freeze checker; this comparison verifies exact agreement and additional displayed evaluations. Domain statements remain analytic.',
       'research_loops_added':0}
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'loop':'q2','passed':True,'spectral_matrices_compared':7}))
if __name__=='__main__':main()
