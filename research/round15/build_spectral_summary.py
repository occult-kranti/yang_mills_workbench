#!/usr/bin/env python3
"""Map accepted spectral evidence to explicitly one-sided website records."""
from pathlib import Path
from fractions import Fraction as Q
import csv,hashlib,json
HERE=Path(__file__).resolve().parent

def main():
    def read(n):return json.loads((HERE/n).read_bytes())
    def rows(n):
        with (HERE/n).open(newline='') as f:return list(csv.DictReader(f))
    c=read('forward/C2/output/central_certificate.json')
    gate=read('advisor/loop-gates/C2.json')
    if gate['central']['certified_gap_lower']!=c['certified_gap_lower'] or Q(c['certified_gap_lower'])<=0:raise ValueError('Unaccepted central result')
    lower=float(Q(c['certified_gap_lower']))
    coupling=rows('forward/C2/output/coupling.csv');volume=rows('forward/C1/output/volume.csv')
    if next(r for r in coupling if r['ratio']=='1/2')['c1_lower']!='0':raise ValueError('Earlier failed boundary omitted')
    boundary=next(r for r in coupling if r['ratio']=='12/23')
    if boundary['status']!='zero-bound-insufficient' or boundary['c2_lower']!='0':raise ValueError('Exact boundary omitted')
    state=read('backward/C1/output/independent_state_review.json')
    for key,path in [('advisor_source_sha256','advisor/cube_state_check.py'),('advisor_proof_sha256','advisor/cube_state_check.md')]:
        if state[key]!=hashlib.sha256((HERE/path).read_bytes()).hexdigest():raise ValueError('Changed reviewed state audit')
    summary={'original_uniform_goal':'open',
      'summary':f'The physical cube bound at alpha=1 and six lambda=1/2 improves from0 to at least{lower:.16g}. The sufficient common-magnitude range extends from|lambda|/alpha<1/2 to<12/23. The original volume-uniform numerical threshold remains open.',
      'equation':'δ=3α, L=Σ_p|λ_p|, Q=Σ_pλ_p²\nE₁≥δ−L and E₀≤(δ−√(δ²+Q))/2\nΔ_cube≥(δ+√(δ²+Q))/2−L\nAt six λ_p=α/2: Δ_cube≥α(√42−6)/4\nCertified at α=1: Δ_cube≥'+c['certified_gap_lower'],
      'loop1_outcome':'Full finite-graph gap bound accepted; cube lambda=alpha/2 lower0 is insufficient; original uniform constants remain open.',
      'loop2_outcome':f'Full physical cube gap lower bound{lower:.16g} at the failed C1 boundary; finite sufficient range extends to12/23.',
      'feedback_finding':'The C1 full-operator bound was exactly zero at six lambda=alpha/2.',
      'feedback_action':'Use exact B1 trial moments to improve the E0 upper bound, retaining the separate full E1 lower bound and all radical error.',
      'additional_reviews':[{'name':'Independent Gibbs-state challenge','status':'13 independent exact checks passed','scope':'Quaternion differentiation versus advisor rational complex matrices, plus smoothness/full-support eigenstate argument.'}],
      'failures':[{'finding':'C1 draft verifier accepted deletion of the zero-coupling cube fixture.','action':'Retained failed draft; strict collection schema, fixture parameters and volume ledger now required.','limit':'All supplied certificates passing was insufficient evidence of required collection completeness.'},
       {'finding':'C1 sufficient cube gap bound reached zero at lambda=alpha/2.','action':'Combine an improved variational E0 upper bound with the full E1 lower bound.','limit':'A finite sufficient range; no proof of uniform-volume gap or actual gap closure at the new endpoint.'},
       {'finding':'The coarse0-bit radical enclosure cannot certify the central positive margin.','action':'Retain computational insufficiency separately from the exact common-range theorem;48bits meet the precision target.','limit':'The radical interval encloses a lower-bound expression, not the unknown physical gap.'},
       {'finding':'A nonzero Gibbs square root was proposed as the physical cube eigenstate.','action':'Independent exact configurations show Hpsi/psi is nonconstant for every matched common magnetic coefficient.','limit':'Trial vectors remain valid variational tools without being exact eigenstates.'},
       {'finding':'A dimensionless uniform smallness threshold alone omitted the physical energy scale.','action':'Add the explicit common alpha>=alpha_min>0 premise to the open bridge and next roadmap.','limit':'At zero magnetic coupling, alpha tending to zero makes the free physical gap tend to zero.'}],
      'plot_files':{'C_coupling':'forward/C2/output/coupling.csv','C_volume':'forward/C1/output/volume.csv'},
      'plots':{
       'C_coupling':{'title':'Cube: variational improvement repairs the old boundary','xLabel':'Common |lambda| / alpha','yLabel':'Sufficient gap lower bound / alpha','csv':'/cycles-c-coupling.csv',
         'caption':'Exact rational lower endpoints, rounded for plotting. These are sufficient full-operator lower bounds, not computed eigenvalues or upper bounds on the actual gap. At12/23 the improved estimate is exactly zero; failure of the estimate does not prove gap closure.',
         'series':[{'name':label,'points':[[float(Q(r['ratio'])),float(Q(r[field]))] for r in coupling]} for field,label in [('c1_lower','C1 min-max plus Haar vacuum'),('c2_lower','C2 variational improvement')]]+ [{'name':'Zero','points':[[0,0],[.6,0]]}]},
       'C_volume':{'title':'The global-norm sufficient threshold deteriorates with volume','xLabel':'Number of elementary plaquettes P','yLabel':'Sufficient |lambda| / alpha threshold:3/P','csv':'/cycles-c-volume.csv',
         'caption':'Actual open-box counts P=3n(n−1)^2, n=2,3,4,6, with a common physical alpha scale. This is the declining C1 sufficient threshold; C2 has only been proved for the single cube. No inference that the true gap closes.',
         'series':[{'name':'C1 finite-volume threshold','points':[[int(r['plaquettes']),float(Q(r['positive_threshold_lambda_over_alpha']))] for r in volume]}]}}}
    (HERE/'spectral-summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n');print('Accepted spectral summary built')
if __name__=='__main__':main()
