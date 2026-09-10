"""Focused read-only A2 producer comparison after independent derivation."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
import argparse,hashlib,json
from check import certificate,face_geometry


def parse_face(label):
    axes,base=label.split(':');return [int(axes[0]),int(axes[1]),*map(int,base.split(','))]


def edge_name(edge):return str(edge[0])+':'+','.join(map(str,edge[1:]))


def main(source,evidence,output):
    source,evidence,output=map(Path,(source,evidence,output));output=output.resolve()
    if output.is_relative_to(Path(__file__).resolve().parent):raise ValueError('output outside source required')
    output.mkdir(parents=True,exist_ok=False);hashfile=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r=json.loads((evidence/'evidence.json').read_text());checks=[]
    def check(name,ok):
        if not ok:raise RuntimeError(name)
        checks.append({'name':name,'passed':True})
    check('forward evidence binds actual sparse source',r['source_sha256']==hashfile(source/'sparse.py'))
    expected_ids=['even-mask-n'+str(n) for n in (2,3,4,6,8)]+['shared_vertex_signed','zero','zero_bridge','rho_boundary','scaled']
    check('all ten required fixtures retained',r['schema']=='ym17-a2-evidence-v1' and [f['id'] for f in r['fixtures']]==expected_ids)
    for fixture in r['fixtures']:
        c=fixture['certificate'];n=c['graph_n'];terms=[{'face':parse_face(k),'lambda':v} for k,v in c['couplings'].items()];ours=certificate(n,terms,c['alpha'],c['alpha_min'],c['rho'])
        active={k:Q(v) for k,v in c['couplings'].items() if Q(v)};blocks=[];used=set()
        for face,value in sorted(active.items()):
            links,_=face_geometry(n,parse_face(face));used|=links
            blocks.append({'plaquette':face,'lambda':str(value),'links':sorted(map(edge_name,links)),'unprojected_gap_lower':str(3*Q(c['alpha'])/4-abs(value))})
        all_links={(axis,*v) for v in product(range(n),repeat=3) for axis in range(3) if v[axis]<n-1};remaining=sorted(map(edge_name,all_links-used))
        positive=ours['status']=='positive'
        same=(c['source_sha256']==r['source_sha256'] and c['geometry_source_sha256']==hashfile(source/'geometry.py') and c['blocks']==blocks and c['free_edges']==remaining and c['covered_link_count']==len(all_links) and c['active_count']==len(active) and c['zero_coefficients']==sorted(k for k,v in c['couplings'].items() if Q(v)==0) and Q(c['actual_max_ratio'])==Q(ours['maximum_absolute_lambda'])/Q(c['alpha']) and c['uniform_family_lower_bound']==ours['uniform_physical_lower'] and c['ground_uniqueness_certified'] is positive and c['ground_Gauss_inclusion_certified'] is positive and c['status']==('certified-positive-sparse-gap' if positive else 'insufficient-lower-bound'))
        check('independent block/free partition and spectral bound '+fixture['id'],same)
        if fixture['id'].startswith('even-mask-'):
            scheduled={tuple([0,1,x,y,z]) for z in range(n) for x in range(0,n-1,2) for y in range(0,n-1,2)}
            if {tuple(t['face']) for t in terms}!=scheduled or any(Q(t['lambda'])!=Q(1,2) for t in terms):raise RuntimeError('declared extensive fixture altered')
        if c['scope']!={'Hilbert':'full link tensor decomposition first; global Gauss invariant restriction afterwards','graph':'original full open cubic link graph; every unlisted magnetic coefficient is0','assumptions':'pairwise link-disjoint nonzero plaquettes; alpha>=alpha_min>0; max|lambda|/alpha<=rho<3/4','dense_uniform_target':'open; overlapping interactions are outside this theorem'}:raise RuntimeError('changed theorem scope')
    check('whole volume ledger independently reconstructed',len(r['volume'])==5 and all(v['active_plaquettes']==v['n']*(v['n']//2)**2 and v['links']==3*v['n']**2*(v['n']-1) and v['free_links']==v['links']-4*v['active_plaquettes'] and Q(v['global_physical_norm_lower'])==3-Q(v['active_plaquettes'],2) and v['sparse_lower']=='1/4' and v['global_bound_status']==('positive' if 3-Q(v['active_plaquettes'],2)>0 else 'insufficient') for v in r['volume']))
    check('dense target remains open',r['dense_uniform_goal']=='open')
    report={'schema':'ym17-independent-a2-comparison-v1','status':'passed','checks_count':len(checks),'checks':checks,'reviewed_input_sha256':{'producer/'+f:hashfile(source/f) for f in ('sparse.py','geometry.py','check.py','report.md')},'producer_evidence_sha256':hashfile(evidence/'evidence.json'),'discrepancies':[],'scope':'Independent actual link-support and exact spectral-bound comparison; no forward imports.'}
    (output/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'passed','checks_count':len(checks)}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--producer',required=True);p.add_argument('--evidence',required=True);p.add_argument('--output',required=True);a=p.parse_args();main(a.producer,a.evidence,a.output)
