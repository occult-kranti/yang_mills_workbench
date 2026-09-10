import copy,csv,hashlib,json,sys
from fractions import Fraction as F
from pathlib import Path
import variational as v
out=Path(sys.argv[1] if len(sys.argv)>1 else 'output');out.mkdir(parents=True,exist_ok=True)
gates=[]
def gate(name,ok):
    if not ok:raise RuntimeError(name)
    gates.append(name)
def reject(name,fn):
    try:fn()
    except (ValueError,TypeError,KeyError):gates.append(name);return
    raise RuntimeError('invalid accepted: '+name)
fixtures=[]
for bits in [0,8,24,48]:
    c=v.certify(couplings=['1/2']*6,bits=bits);fixtures.append({'id':'central-bits'+str(bits),'certificate':c})
    gate('central replay bits'+str(bits),v.verify(c))
gate('coarse lower insufficient retained',fixtures[0]['certificate']['status']=='inconclusive-enclosure')
gate('coarse precision failures retained',all(x['certificate']['precision_status']=='insufficient-precision' for x in fixtures[:3]))
central=fixtures[-1]['certificate']
gate('central positive full operator bound',F(central['certified_gap_lower'])>0)
gate('central total precision target',central['precision_status']=='target-met')
gate('independent E1 bound exactly zero',central['full_E1_lower']=='0')
gate('trial ground upper strictly negative',F(central['full_E0_upper'])<0)
extra=[
('zero','1',['0']*6),('negative','1',['-1/2']*6),
('heterogeneous','1',['1/2','-1/4','0','1/8','-1/8','0']),
('scaled','2',['1']*6),('boundary','1',['12/23']*6),('beyond','1',['3/5']*6)]
for name,alpha,ls in extra:
    c=v.certify(alpha,ls);gate(name+' replay',v.verify(c));fixtures.append({'id':name,'certificate':c})
byid={x['id']:x['certificate'] for x in fixtures}
gate('zero Q no division and exact free gap',byid['zero']['certified_gap_lower']=='3')
gate('negative common coupling same bound',byid['negative']['gap_bound_interval']==central['gap_bound_interval'])
gate('heterogeneous common range withheld',byid['heterogeneous']['common_range_status']=='not-common-magnitude')
gate('linear scaling exact analytic radicand',F(byid['scaled']['radicand'])==4*F(central['radicand']))
gate('scaled lower consistent with exact scaling',F(byid['scaled']['certified_gap_lower'])>=2*F(central['certified_gap_lower']))
gate('boundary radical exact75/23',byid['boundary']['sqrt_interval']==['75/23','75/23'])
gate('new boundary zero insufficient',byid['boundary']['status']=='zero-bound-insufficient' and byid['boundary']['certified_gap_lower']=='0')
gate('beyond sufficient window negative',byid['beyond']['status']=='negative-bound-insufficient')
ratios=['0','1/4','2/5','9/20','49/100','1/2','51/100','13/25','12/23','53/100','11/20','3/5']
rows=[]
for r in ratios:
    c=v.certify(couplings=[r]*6)
    expected='strictly-positive-exact-bound' if F(r)<F(12,23) else 'zero-bound-insufficient' if F(r)==F(12,23) else 'negative-bound-insufficient'
    gate('analytic range '+r,c['common_range_status']==expected)
    rows.append({'ratio':r,'ratio_float':float(F(r)),'c1_lower':str(3-6*F(r)),
                 'c2_lower':c['certified_gap_lower'],'c2_upper':c['gap_bound_interval'][1],
                 'c2_lower_float':float(F(c['certified_gap_lower'])),'status':c['status']})
mutations=[
('missing fixture hashes',lambda c:c.update(input_hashes={})),
('wrong trial dimension',lambda c:c['gram'].pop()),
('wrong Gram normalization',lambda c:c['gram'][1].__setitem__(1,'1/4')),
('missing offdiagonal factor',lambda c:c['trial_hamiltonian'][0].__setitem__(1,'-1/2')),
('fake excited potential entry',lambda c:c['trial_hamiltonian'][1].__setitem__(1,'4')),
('wrong independent E1 bound',lambda c:c.update(full_E1_lower='1')),
('trial gap as full gap',lambda c:c.update(certified_gap_lower=c['sqrt_interval'][0])),
('wrong radical lower',lambda c:c['sqrt_interval'].__setitem__(0,'4')),
('dropped radical width',lambda c:c.update(bound_interval_width='0')),
('Boolean bits',lambda c:c.update(bits=True)),
('Boolean diagonal entry',lambda c:c['gram'][0].__setitem__(0,True)),
('missing coupling',lambda c:c['couplings'].pop()),
('changed scope',lambda c:c['scope'].update(uniform_threshold='proved for all volumes')),
('extra premise',lambda c:c.update(assume='gap'))]
for name,mut in mutations:
    c=copy.deepcopy(central);mut(c);reject(name,lambda c=c:v.verify(c))
reject('zero alpha',lambda:v.certify('0',['0']*6))
reject('negative alpha',lambda:v.certify('-1',['0']*6))
reject('Boolean alpha',lambda:v.certify(True,['0']*6))
reject('Boolean coupling',lambda:v.certify(couplings=[True]*6))
reject('float coupling',lambda:v.certify(couplings=[0.5]*6))
reject('Boolean bits API',lambda:v.certify(couplings=['0']*6,bits=True))
reject('negative bits',lambda:v.certify(couplings=['1/2']*6,bits=-1))
reject('bit cap',lambda:v.certify(couplings=['1/2']*6,bits=4097))
reject('zero precision',lambda:v.certify(couplings=['1/2']*6,precision='0'))
reject('noncanonical rational',lambda:v.certify(couplings=['2/4']*6))
reject('negative radical',lambda:v.sqrt_interval(F(-1),8))
reject('Boolean common ratio',lambda:v.common_range(True))
collection={'schema':'ym15-c2-fixture-collection-v1','fixtures':fixtures,'coupling_rows':rows,
            'ordered_fixture_ids':[x['id'] for x in fixtures]}
(out/'certificates.json').write_text(json.dumps(collection,indent=2)+'\n')
(out/'central_certificate.json').write_text(json.dumps(central,indent=2)+'\n')
with (out/'coupling.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with (out/'precision.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['bits','bound_lower','bound_upper','width','lower_float','status','precision_status'])
    for x in fixtures[:4]:
        c=x['certificate'];w.writerow([c['bits'],*c['gap_bound_interval'],c['bound_interval_width'],float(F(c['certified_gap_lower'])),c['status'],c['precision_status']])
result={'status':'passed','gate_count':len(gates),'gates':gates,'source_sha256':v.SOURCE_SHA,
        'test_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'central_certificate_sha256':hashlib.sha256((out/'central_certificate.json').read_bytes()).hexdigest(),
        'collection_sha256':hashlib.sha256((out/'certificates.json').read_bytes()).hexdigest(),
        'central_lower_float':float(F(central['certified_gap_lower'])),
        'bound_interval_width_float':float(F(central['bound_interval_width'])),
        'common_magnitude_threshold':'12/23','original_uniform_threshold':'open'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='gates'},indent=2))
