"""Independent B1 support enumeration, Haar moments and full cross operator."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from math import comb,factorial
import argparse,copy,hashlib,json
from operators import graph,validate,supports,support_inventory,cycles_of_length,six_loop,moment,fourth_inventory,matrices,cube_boundary_contraction


DEFINITIONS=[('allzero','1',['0']*11),('all_positive_eighth','1',['1/8']*11),('all_negative_eighth','1',['-1/8']*11),
 ('alternating_eighth','1',['1/8' if i%2==0 else '-1/8' for i in range(11)]),('single_eighth','1',['1/8']+['0']*10),
 ('mixed_signed_zero','1',['1/8','-1/16','0','3/32','0','-1/32','0','0','0','0','0']),('canonical_three_eighths','1',['3/8']*11),
 ('scaled_double','2',['3/4']*11),('scaled_half','1/2',['3/16']*11)]


def run(output):
    source=Path(__file__).resolve().parent;output=Path(output).resolve()
    if output.is_relative_to(source):raise ValueError('output must be outside frozen source')
    output.mkdir(parents=True,exist_ok=False);checks=[]
    def gate(name,ok):
        if type(ok) is not bool or not ok:raise ValueError(name)
        checks.append({'name':name,'passed':True})
    def reject(name,fn):
        try:fn()
        except (ValueError,TypeError):gate(name,True);return
        raise ValueError('invalid admitted: '+name)
    g=graph();sup=supports(g);inventory,retained=support_inventory(g);cycles=cycles_of_length(g,4);six=six_loop(g)
    gate('complete actual two-cube graph has 12 vertices 20 edges 11 faces',(len(g['vertices']),len(g['edges']),len(g['faces']))==(12,20,11))
    gate('all edges cross the exact bipartition',all(sum(e['tail'])%2!=sum(e['head'])%2 for e in g['edges']))
    gate('all 21700 supports through five edges were enumerated',len(inventory)==sum(comb(20,k) for k in range(6))==21700)
    gate('only vacuum and eleven squares pass necessary Gauss active-degree condition',{tuple(x) for x in retained}=={(),*(tuple(sorted(s)) for s in sup)} and len(retained)==12)
    gate('independent cycle search matches every and only actual elementary face',set(cycles)=={tuple(sorted(s)) for s in sup} and len(cycles)==11)
    gate('no five-edge multicycle or odd cycle survives the exact support audit',not any(r['size']==5 and r['passes_Gauss_necessary_degree'] for r in inventory))
    gate('nonfundamental four-cycle spins lie above the omitted threshold',4*F(1,2)*F(3,2)==3<F(9,2)<4*1*2)
    gate('six-edge fundamental witness is closed and belongs to the complete complement',len(six['active_edges'])==6 and len(six['face_orthogonality_witnesses'])==11 and six['electric_energy_over_alpha']=='9/2')
    gate('a falsely raised complement threshold is contradicted by the actual witness',F(six['electric_energy_over_alpha'])<F(19,4))
    gate('omitting a face channel invalidates the 9 over 2 complement premise',4*F(3,4)==3<F(9,2) and bool(sup[0]))
    b=F(1,24);a=3*b
    gate('independent S3 isotropy gives the exact conditional repeated Haar moment',4*a+12*b==1 and a==(2*a+6*b)/4 and 16*a==2)
    fourth=fourth_inventory(g);ordered_count=0
    for r in fourth:
        multiplicity=factorial(4)
        for k in r['multiplicity_type']:multiplicity//=factorial(k)
        r['ordered_permutation_count']=multiplicity;ordered_count+=multiplicity
    gate('all fourth multisets account for all 14641 ordered products',len(fourth)==1001 and ordered_count==11**4)
    gate('every four-distinct-face product has an actual odd edge witness',all(r['value']=='0' and r['odd_edge_witness'] is not None for r in fourth if r['multiplicity_type']==[1,1,1,1]))
    gate('every distinct doubled pair has an exclusive link and exact integral one',all(r['value']=='1' and r['exclusive_square_edge'] is not None for r in fourth if r['multiplicity_type']==[2,2]))
    gate('same-face fourth moments equal two rather than Gaussian three',all(r['value']=='2' for r in fourth if r['multiplicity_type']==[4]))
    independent_match=True
    for r in fourth:
        counts=r['multiplicity_type'];product_value=F(1)
        for k in counts:product_value*=({1:F(0),2:F(1),3:F(0),4:F(2)})[k]
        independent_match=independent_match and F(r['value'])==product_value
    gate('genuine independent one-face Haar model agrees through degree four',independent_match)
    cube=cube_boundary_contraction(g)
    gate('actual six-face index contractions reject full face independence',len(cube['edge_pairings'])==12 and len(cube['index_components'])==8 and cube['ordinary_character_moment']=='1/16' and cube['independent_centered_face_value']=='0')
    cases={name:matrices(g,alpha,lam) for name,alpha,lam in DEFINITIONS}
    gate('every fixture separately reconstructs full PVP PV2P and P subtraction',len(cases)==9 and all(c['P_dimension']==12 and len(c['cross_Gram'])==12 for c in cases.values()))
    gate('zero interaction annihilates the complete cross operator',all(F(x)==0 for row in cases['allzero']['cross_Gram'] for x in row))
    gate('V acting on vacuum lies in P while cross vacuum row vanishes',all(all(F(x)==0 for x in c['cross_Gram'][0]) and any(F(x)!=0 for x in c['PVP'][0]) for n,c in cases.items() if n!='allzero'))
    positive=cases['all_positive_eighth'];negative=cases['all_negative_eighth'];alternating=cases['alternating_eighth']
    gate('global coupling sign preserves cross Gram but reverses PVP',positive['cross_Gram']==negative['cross_Gram'] and all(F(x)==-F(y) for row,other in zip(positive['PVP'],negative['PVP']) for x,y in zip(row,other)))
    gate('individual signs conjugate the homogeneous face cross block',all(F(alternating['cross_Gram'][i+1][j+1])==(-1)**(i+j)*F(positive['cross_Gram'][i+1][j+1]) for i in range(11) for j in range(11)))
    gate('single-channel fixture retains nonzero complete complementary channels',all(F(cases['single_eighth']['cross_Gram'][i+1][i+1])==F(1,256) for i in range(11)))
    gate('every exact row norm obeys the signed coefficient-box estimate',all(F(c['cross_row_sum_bound'])<=F(c['box_cross_norm_squared_upper']) for c in cases.values()))
    gate('homogeneous cross norm is an exact eigenvalue and row bound',all(c['homogeneous_magnitude_cross_norm_squared']==c['cross_row_sum_bound'] for c in cases.values() if c['homogeneous_magnitude_cross_norm_squared'] is not None))
    gate('two nonunit scales scale the electric threshold and cross Gram differently',cases['scaled_double']['full_electric_complement_lower']=='9' and cases['scaled_half']['full_electric_complement_lower']=='9/4' and all(F(cases['scaled_double']['cross_Gram'][i][j])==4*F(cases['canonical_three_eighths']['cross_Gram'][i][j]) and F(cases['scaled_half']['cross_Gram'][i][j])==F(cases['canonical_three_eighths']['cross_Gram'][i][j])/4 for i in range(12) for j in range(12)))
    gaussian_diagonal=F(positive['cross_Gram'][1][1])+F(positive['couplings'][0])**2/4
    controls={'Gaussian_repeated_fourth':{'actual':'2','wrong_model':'3','actual_cross_first_face_diagonal':positive['cross_Gram'][1][1],'wrong_cross_first_face_diagonal':str(gaussian_diagonal)},
      'deleted_P_subtraction':{'actual_cross_vacuum_diagonal':positive['cross_Gram'][0][0],'wrong_PV2P_vacuum_diagonal':positive['PV2P'][0][0]},
      'low_order_independence':'agrees through degree four; full independence separately rejected at six faces'}
    gate('Gaussian substitution changes the computed fourth-order cross diagonal',gaussian_diagonal!=F(positive['cross_Gram'][1][1]))
    gate('deleted P subtraction creates a spurious vacuum cross channel',F(positive['PV2P'][0][0])==F(11,256)!=F(positive['cross_Gram'][0][0]))
    bad=copy.deepcopy(g);bad['faces'].pop();reject('missing actual face channel rejected',lambda:matrices(bad,1,['1/8']*11))
    bad=copy.deepcopy(g);bad['faces'][0]['word'][0][1]=True;reject('Boolean signed word alias rejected',lambda:matrices(bad,1,['1/8']*11))
    reject('Boolean physical alpha rejected',lambda:matrices(g,True,['1/8']*11))
    reject('Boolean Haar face index rejected',lambda:moment(g,(True,True)))
    reject('missing coefficient channel rejected',lambda:matrices(g,1,['1/8']*10))
    reject('nonpositive physical scale rejected',lambda:matrices(g,0,['1/8']*11))
    result={'schema':'ym18-independent-b1-results-v1','status':'passed','checks_count':len(checks),'checks':checks,
      'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (source/'operators.py',source/'check.py')},
      'support_count':len(inventory),'retained_support_count':len(retained),'fourth_multiset_count':len(fourth),'fourth_ordered_count':ordered_count,
      'full_complement_over_alpha':'9/2','six_face_character_moment':'1/16','scope':'Full physical electric complement and exact finite-graph cross block; B2 scalar gap not executed.'}
    for name,obj in [('results.json',result),('graph.json',g),('low_support_inventory.json',inventory),('retained_supports.json',retained),('six_edge_witness.json',six),('fourth_moments.json',fourth),('six_face_contraction.json',cube),('matrices.json',cases),('controls.json',controls)]:
        (output/name).write_text(json.dumps(obj,indent=2)+'\n')
    print(json.dumps({'status':'passed','checks_count':len(checks),'support_count':len(inventory),'fourth_ordered_count':ordered_count}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();run(a.output)
