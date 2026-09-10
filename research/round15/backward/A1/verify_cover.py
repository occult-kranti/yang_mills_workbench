"""Independent parameter-cover replay; never imports producer cover mathematics."""
from fractions import Fraction as Q
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import shutil
import sys
import tempfile

HERE=Path(__file__).resolve().parent
PINS={
 'vendor/verify_certificate.py':'e314cb04cfdda8019c03da63bfc98ce679624d9bb4e1379ef03473ef6907d869',
 'vendor/oracle.py':'c6779c3151f1803e4baf78671d8e775eaa6baf240f3f943541fbcb2bb4ab5169',
}
POINT_PIN='c1141b027f310159494e18a93a8a2afa96073009a9b16f4f7d1a822f96bf4682'
THEOREM_PIN='dac9c72882c5e8cb6fbd7f46d6ec8fcfa585e27dfb8b681bb64b1b47899bd666'
SOURCE_BYTES=Path(__file__).read_bytes()
for relative,pin in PINS.items():
    if hashlib.sha256((HERE/relative).read_bytes()).hexdigest()!=pin:
        raise ValueError('frozen independent dependency hash mismatch')
spec=importlib.util.spec_from_file_location('ym15_independent_point',HERE/'vendor/verify_certificate.py')
point=importlib.util.module_from_spec(spec);spec.loader.exec_module(point)
spec=importlib.util.spec_from_file_location('ym15_independent_derivative',HERE/'derivative_check.py')
derivative=importlib.util.module_from_spec(spec);spec.loader.exec_module(derivative)


def canonical(value):
    if type(value) is not str or len(value)>20000:
        raise ValueError('canonical rational string required')
    try:
        result=Q(value)
    except (ValueError,ZeroDivisionError,OverflowError) as exc:
        raise ValueError('invalid rational') from exc
    if str(result)!=value:
        raise ValueError('noncanonical rational')
    return result


def same(actual,expected):
    try:
        return json.dumps(actual,sort_keys=True,allow_nan=False,separators=(',',':'))==json.dumps(expected,sort_keys=True,allow_nan=False,separators=(',',':'))
    except (ValueError,TypeError):
        return False


class Review:
    def __init__(self,producer_dir):
        self.base=Path(producer_dir)
        self.paths={name:self.base/name for name in ('cover.py','derivation.md','vendor/point_certificate.py')}
        self.paths.update({'independent/'+name:HERE/name for name in PINS})
        self.paths.update({'independent/verify_cover.py':Path(__file__),
                           'independent/derivative_check.py':HERE/'derivative_check.py',
                           'independent/derivative-proof.md':HERE/'derivative-proof.md'})
        self.snapshot={name:self.read(path) for name,path in self.paths.items()}
        self.hashes={name:hashlib.sha256(data).hexdigest() for name,data in self.snapshot.items()}
        if self.hashes['vendor/point_certificate.py']!=POINT_PIN or self.hashes['derivation.md']!=THEOREM_PIN:
            raise ValueError('unreviewed point producer or derivative theorem')
        if self.snapshot['independent/verify_cover.py']!=SOURCE_BYTES:
            raise ValueError('independent verifier changed before snapshot')
        derivative.run()

    @staticmethod
    def read(path):
        if path.is_symlink() or not path.is_file():
            raise ValueError('required input must be a regular nonsymlink file')
        return path.read_bytes()

    def unchanged(self):
        if set(self.snapshot)!=set(self.paths) or any(self.read(path)!=self.snapshot[name] for name,path in self.paths.items()):
            raise ValueError('required source changed after review')

    def verify(self,cover):
        self.unchanged()
        if type(cover) is not dict or type(cover.get('cells')) is not list:
            raise ValueError('cover object and cells required')
        cells=cover['cells'];n=cover.get('cell_count');degree=cover.get('degree')
        if type(n) is not int or not 1<=n<=4096 or n!=len(cells):
            raise ValueError('nonempty bounded integer cell count required')
        if type(degree) is not int or not 0<=degree<=48:
            raise ValueError('integer Taylor degree required')
        reconstructed=[];edge=Q(1,8)
        for index,cell in enumerate(cells):
            if type(cell) is not dict:
                raise ValueError('invalid cell')
            left=canonical(cell.get('left'));right=canonical(cell.get('right'))
            if left!=edge or not left<right<=Q(1,4):
                raise ValueError('cover has a gap, overlap, boundary error or reversed cell')
            center=(left+right)/2;radius=max(center-left,right-center)
            certificate=cell.get('certificate')
            if type(certificate) is not dict or certificate.get('parameters')!={'k1':'1','k2':'1','eta':str(center)}:
                raise ValueError('point parameters do not match this center and fixed action')
            if type(certificate.get('degree')) is not int or certificate['degree']!=degree:
                raise ValueError('point degree mismatch')
            point.verify(certificate,producer_source_sha256=POINT_PIN)
            low,high=map(canonical,certificate['enclosures']['covariance'])
            transported=(low-Q(2)*radius,high+Q(2)*radius)
            expected_cell={'left':str(left),'right':str(right),'center':str(center),'radius':str(radius),
              'certificate':certificate,'transported_lower':str(transported[0]),
              'transported_upper':str(transported[1]),'status':'positive' if transported[0]>0 else 'insufficient'}
            if not same(cell,expected_cell):
                raise ValueError('cell arithmetic or semantics mismatch')
            reconstructed.append(expected_cell);edge=right
        if edge!=Q(1,4):
            raise ValueError('right endpoint omitted')
        minimum=min(canonical(c['transported_lower']) for c in reconstructed)
        insufficient=[i for i,c in enumerate(reconstructed) if canonical(c['transported_lower'])<=0]
        expected={'schema':'ym15-covariance-cover-v1','source_sha256':self.hashes['cover.py'],
          'point_source_sha256':POINT_PIN,'derivative_source_sha256':THEOREM_PIN,
          'scope':point.SCOPE,'fixed_parameters':{'k1':'1','k2':'1'},'target':['1/8','1/4'],
          'lipschitz':'2','degree':degree,'cell_count':n,'cells':reconstructed,'minimum_lower':str(minimum),
          'insufficient_indices':insufficient,'status':'insufficient-cover' if insufficient else 'certified-positive-cover'}
        if not same(cover,expected):
            raise ValueError('complete cover source/scope/arithmetic/status replay failed')
        self.unchanged()
        return {'status':expected['status'],'cell_count':n,'minimum_lower':str(minimum),
                'insufficient_indices':insufficient}


def audit(cover_path,producer_dir,output_dir):
    cover_path=Path(cover_path);cover_bytes=cover_path.read_bytes();cover=json.loads(cover_bytes)
    review=Review(producer_dir);result=review.verify(cover);checks=[]
    def gate(name,passed=True):
        if not passed:
            raise ValueError(name)
        checks.append({'name':name,'passed':True})
    gate('independent derivative identity and two wrong-formula controls',derivative.run()['checks']==3)
    gate('all exact character point certificates and full cover replayed')
    gate('A1 exactly eight degree24 cells',cover['cell_count']==8 and cover['degree']==24)
    gate('A1 retained as insufficient rather than false positivity',result['status']=='insufficient-cover' and bool(result['insufficient_indices']))
    def reject(name,changed):
        try: review.verify(changed)
        except ValueError: gate(name);return
        raise ValueError('accepted invalid cover: '+name)
    for path,value in [
      ('schema','bad'),('source_sha256','0'*64),('point_source_sha256','0'*64),
      ('derivative_source_sha256','0'*64),('fixed_parameters',{'k1':'2','k2':'1'}),
      ('target',['1/8','15/64']),('lipschitz','1'),('degree',True),('cell_count',True),
      ('minimum_lower','1'),('insufficient_indices',[]),('status','certified-positive-cover'),
      ('scope',{'group':'SU(2)','limit':'physical mass gap'}),
    ]:
        mutation=copy.deepcopy(cover);mutation[path]=value;reject('mutation '+path,mutation)
    for field,value in [
      ('left','0'),('right','1/8'),('center','1/8'),('radius','0'),
      ('transported_lower','1'),('transported_upper','0'),('status','positive'),
    ]:
        mutation=copy.deepcopy(cover);mutation['cells'][0][field]=value;reject('first cell mutation '+field,mutation)
    mutation=copy.deepcopy(cover);mutation['cells'][0]['certificate']['parameters']['eta']='1/8';reject('wrong point eta',mutation)
    mutation=copy.deepcopy(cover);mutation['cells'][0]['certificate']['parameters']['k1']=True;reject('Boolean point parameter',mutation)
    mutation=copy.deepcopy(cover);mutation['cells'][0]['certificate']['tail']['first_omitted_degree']=True;reject('nested Boolean tail metadata',mutation)
    mutation=copy.deepcopy(cover);mutation['cells'][0]['certificate']['status']='certified-positive';mutation['cells'][0]['certificate']['width']='0';reject('forged point passed metadata',mutation)
    for index,name in [(0,'left endpoint'),(3,'interior cell'),(-1,'right endpoint')]:
        mutation=copy.deepcopy(cover);del mutation['cells'][index];mutation['cell_count']-=1;reject('missing '+name,mutation)
    mutation=copy.deepcopy(cover);mutation['cells'][4]=copy.deepcopy(mutation['cells'][3]);reject('duplicated cell hides missing interval',mutation)
    mutation=copy.deepcopy(cover);mutation['cells']=[];mutation['cell_count']=0;reject('empty cover vacuous pass',mutation)
    mutation=copy.deepcopy(cover);mutation['extra']='mass gap';reject('unproved metadata insertion',mutation)
    mutation=copy.deepcopy(cover);del mutation['derivative_source_sha256'];reject('missing theorem provenance',mutation)
    for filename,operation in [('cover.py','change'),('derivation.md','change'),('vendor/point_certificate.py','change'),('derivation.md','delete'),('derivation.md','symlink')]:
        with tempfile.TemporaryDirectory() as temp:
            target=Path(temp)/'producer';shutil.copytree(producer_dir,target)
            local=Review(target);local.verify(cover);path=target/filename
            if operation=='change': path.write_bytes(path.read_bytes()+b'\n')
            elif operation=='delete': path.unlink()
            else:
                backup=target/'backup.md';backup.write_bytes(path.read_bytes());path.unlink();path.symlink_to(backup)
            try: local.verify(cover)
            except ValueError: gate('warm source '+operation+' '+filename)
            else: raise ValueError('changed source accepted')
    gate('input collection unchanged',cover_path.read_bytes()==cover_bytes)
    output={'schema':'ym15-A1-independent-review-v1','status':'passed','scientific_outcome':result['status'],
      'checks_count':len(checks),'checks':checks,'result':result,'derivative_check':derivative.run(),
      'source_sha256':hashlib.sha256(SOURCE_BYTES).hexdigest(),'reviewed_inputs':review.hashes,
      'cover_sha256':hashlib.sha256(cover_bytes).hexdigest(),
      'limits':['Finite normalized round14 Euclidean action only.',
                'Insufficient transported lower margins are not negative covariance findings.',
                'Conventional mathematical proof plus independent rational replay, not a formal proof-assistant kernel.']}
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
    (out/'independent_review.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':'passed','checks':len(checks),'scientific_outcome':result}))
    return output


if __name__=='__main__':
    if len(sys.argv)!=4: raise SystemExit('usage: verify_cover.py COVER PRODUCER_DIR OUTPUT_DIR')
    audit(*sys.argv[1:])
