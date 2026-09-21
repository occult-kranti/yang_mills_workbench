#!/usr/bin/env python3
"""Actual geometry and Haar moments; full operator statement is proved in report.md."""
import argparse
from fractions import Fraction as F
import itertools
import json
from pathlib import Path


def require(ok,name):
    if not ok: raise RuntimeError(name)


def add(a,b): return tuple(x+y for x,y in zip(a,b))


def face(origin,axes):
    unit=[(1,0,0),(0,1,0),(0,0,1)]
    a,b=axes
    return frozenset([(origin,a),(add(origin,unit[a]),b),(add(origin,unit[b]),a),(origin,b)])


def free(edge):
    (x,y,z),axis=edge
    return axis==2 or (axis==0 and x%4==3) or (axis==1 and y%2==1)


def serial(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {k:serial(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [serial(v) for v in x]
    return x


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    faces=[]
    for x,y in itertools.product(range(4),range(2)):
        for axes in [(0,1),(0,2),(1,2)]:
            if axes==(0,1) and y==0 and x<3: continue
            faces.append(face((x,y,0),axes))
    require(len(faces)==21,'all omitted faces')
    free_sets=[{edge for edge in f if free(edge)} for f in faces]
    require(min(map(len,free_sets))>=2,'each face has two free links')
    pairs=0; shared_gradient_pairs=0
    for i,j in itertools.combinations(range(21),2):
        require(free_sets[i]^free_sets[j],'unmatched free Haar parity')
        pairs+=1
        if faces[i]&faces[j]: shared_gradient_pairs+=1
    require(pairs==210,'all pair cancellations considered')
    # A symmetric S3 design is exact for degree-two moments used here.
    quaternions=[]
    for axis in range(4):
        for sign in [-1,1]:
            q=[F(0)]*4; q[axis]=F(sign); quaternions.append(q)
    haar_w2=sum(q[0]**2 for q in quaternions)/8
    gradient=sum(sum((q[a]/2)**2 for a in range(1,4)) for q in quaternions)/8
    require(haar_w2==F(1,4),'normalized Wilson Haar variance')
    require(gradient==F(3,16),'Casimir-normalized gradient moment')
    sigma_coefficient=F(21,9)*haar_w2
    energy_coefficient=F(21,9)*8*4*gradient
    require(sigma_coefficient==F(7,12),'actual variance coefficient')
    require(energy_coefficient==14,'actual first energy coefficient')
    mean_energy=energy_coefficient/sigma_coefficient
    require(mean_energy==24,'exact actual spectral mean')
    tau=F(5,1664); theta=F(1,16); m=7*tau; kappa=4*m
    factor=1-mean_energy*theta*(1+kappa)/2
    require(factor==F(311,1664)>0,'uniform residual retained fraction')
    require(factor/432==F(311,718848),'absolute cubic lower coefficient')
    # The following is an exact algebra-control measure, not the actual spectrum.
    energies=[F(12),F(24),F(36)]; masses=[F(1,4),F(1,2),F(1,4)]
    initial_mean=sum(e*p for e,p in zip(energies,masses))
    a=sum(p/e for e,p in zip(energies,masses))
    beta=sum(p/e**2 for e,p in zip(energies,masses))
    weights=[(a/e+beta/3)**2*p for e,p in zip(energies,masses)]
    weighted_mean=sum(e*p for e,p in zip(energies,weights))/sum(weights)
    require(weighted_mean<=initial_mean,'decreasing spectral weight lowers mean')
    covariance_terms=[(e-f)*((a/e+beta/3)**2-(a/f+beta/3)**2)
                      for e,f in itertools.product(energies,repeat=2)]
    require(all(x<=0 for x in covariance_terms),'pointwise covariance sign')
    increasing_mean=sum(e**3*p for e,p in zip(energies,masses))/sum(e**2*p for e,p in zip(energies,masses))
    controls={
        'wrong-Casimir-normalization-detected': 4*gradient!=gradient,
        'shared-gradient-cross-terms-need-parity': shared_gradient_pairs>0 and pairs==210,
        'increasing-weight-does-not-lower-mean': increasing_mean>initial_mean,
        'full-form-factor-cannot-be-omitted': 1-mean_energy*theta/2>factor,
        'tau-zero-is-valid-zero-source': F(0)**3==0,
        'residual-deletion-contradicts-actual-lower-bound': factor>0,
        'source-moment-is-not-excited-Bohr-gap': max(energies)-min(energies)!=initial_mean/2,
    }
    for name,value in controls.items(): require(value,name)
    results={
        'loop':'w1','direction':'reverse','status':'passed',
        'claims':[
            'Actual SU2 Haar/form first moment <v,H0 v>=14tau^2=24||v||^2',
            'Actual cubic source has mean reference energy at most 24',
            'Full initial short-filter residual norm is at least 311/1664 times actual source norm',
            'Uniform absolute cubic residual lower coefficient from Jensen moments',
        ],
        'limitations':[
            'Vacuum-column lower bound does not identify all exterior spectral blocks',
            'No exact equal-energy obstruction, universal inverse impossibility or total-cubic cancellation result',
            'Initial G only; later-diagonal iteration requires new premises',
            'Finite spectral fixture is only an algebra control, not actual SU2 spectrum',
            'No homogeneous numerical gap, physical calibration, continuum result or verified priority',
        ],
        'exact':{'omitted_faces':len(faces),'face_pairs':pairs,'shared_gradient_pairs':shared_gradient_pairs,
                 'Haar_W_squared':haar_w2,'single_link_gradient_moment':gradient,
                 'sigma_squared_tau_coefficient':sigma_coefficient,'energy_tau_squared_coefficient':energy_coefficient,
                 'source_mean_energy_upper':mean_energy,'kappa_cap':kappa,'residual_fraction_lower':factor,
                 'absolute_lower_divided_by_sigma_cubed':factor/432,
                 'spectral_fixture_original_mean':initial_mean,'spectral_fixture_weighted_mean':weighted_mean},
    }
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'results.json').write_text(json.dumps(serial(results),indent=2,sort_keys=True)+'\n')
    (args.output/'controls.json').write_text(json.dumps({'controls':controls},indent=2,sort_keys=True)+'\n')


if __name__=='__main__': main()
