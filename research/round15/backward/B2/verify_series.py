"""Independent exact replay of the cube total-action Taylor certificates."""
from fractions import Fraction as Q
from pathlib import Path
from math import factorial
import copy
import hashlib
import json
import shutil
import sys
import tempfile
import series_oracle as oracle

HERE=Path(__file__).resolve().parent
SOURCE_BYTES=Path(__file__).read_bytes()
GRAPH_PIN='4e85817855a880ce5f48e6b3995adca6852557d55103623bb0d686295f334f65'
B1_PIN='d0df83cd06d062ae525f91bfc2c53eb4beacfdb8d467fe2000449e2e20a38107'
INDEPENDENT_PINS={
 'independent_oracle':'5b4af669d5013a90812ceed5f875a1aae0ec9a8dfc716415bc4bffe6b0764eab',
 'independent_derivation':'0987af03af76bebd92676d738d1adf7e4cf63d71f73ac7fa15b6e339f6b57c85',
 'B1_independent_derivation':'b1b44e8950316ab3d3c87bb2eb9def4ffd77eaa8adf5540fb71dba4b362cd864',
 'B1_independent_source':'b7774bf45d5db7eddfbf080a2637e1a7f3e39022386596c6bc63b13a92c63a1b',
 'B1_independent_index_algebra':'88ed912040d5cc988513c5d081465cdb08a6a29f11066c9ff05405f4b55a3dcf'}
SCOPE={'graph':'closed oriented cube boundary','measure':'normalized product Haar on12 links',
       'action':'k*sum_f Tr(U_face_f)/2','observable':'product_f Tr(U_face_f)/2',
       'generator':'none; finite Euclidean measure'}


def canonical(value):
    if type(value) is not str or len(value)>20000:raise ValueError('canonical rational string required')
    try:result=Q(value)
    except (ValueError,ZeroDivisionError):raise ValueError('invalid rational')
    if str(result)!=value:raise ValueError('noncanonical rational')
    return result


def same(a,b):
    try:return json.dumps(a,sort_keys=True,allow_nan=False,separators=(',',':'))==json.dumps(b,sort_keys=True,allow_nan=False,separators=(',',':'))
    except (TypeError,ValueError):return False


class Review:
    def __init__(self,forward_root):
        self.root=Path(forward_root)
        self.paths={'graph':self.root/'B1/graph.json','B1_source':self.root/'B1/cube.py',
          'B2_source':self.root/'B2/series.py','self':Path(__file__),
          'independent_oracle':HERE/'series_oracle.py','independent_derivation':HERE/'derivation.md',
          'B1_independent_derivation':HERE.parent/'B1/derivation.md',
          'B1_independent_source':HERE.parent/'B1/verify_cube.py',
          'B1_independent_index_algebra':HERE.parent/'B1/exact_algebra.py'}
        self.snapshot={name:self.read(path) for name,path in self.paths.items()}
        self.hashes={name:hashlib.sha256(data).hexdigest() for name,data in self.snapshot.items()}
        if self.hashes['graph']!=GRAPH_PIN or self.hashes['B1_source']!=B1_PIN:
            raise ValueError('accepted B1 source/graph changed')
        if any(self.hashes[name]!=pin for name,pin in INDEPENDENT_PINS.items()):
            raise ValueError('reviewed independent oracle/derivation changed')
        if self.snapshot['self']!=SOURCE_BYTES:raise ValueError('verifier source changed')

    @staticmethod
    def read(path):
        if path.is_symlink() or not path.is_file():raise ValueError('regular nonsymlink required source missing')
        return path.read_bytes()

    def unchanged(self):
        if any(self.read(path)!=self.snapshot[name] for name,path in self.paths.items()):
            raise ValueError('source changed after replay context creation')

    def verify(self,certificate):
        self.unchanged()
        if type(certificate) is not dict:raise ValueError('certificate object required')
        k=canonical(certificate.get('k'));precision=canonical(certificate.get('precision'))
        n=certificate.get('degree')
        if type(n) is not int or not 0<=n<=30 or precision<=0:raise ValueError('review implementation degree0..30 and positive precision required')
        value=oracle.calculate(k,n)
        coefficients={'Z':oracle.action_coefficients(n,False),'Aproduct':oracle.action_coefficients(n,True),'Zindependent':oracle._six_series(0,n,0)}
        expected={'schema':'ym15-cube-taylor-certificate-v1','source_sha256':self.hashes['B2_source'],
          'graph_file_sha256':GRAPH_PIN,'b1_source_sha256':B1_PIN,'scope':SCOPE,
          'k':str(k),'degree':n,'precision':str(precision),'absolute_exponent_bound':str(value['M']),
          'tail':{'remainder':str(value['tail']),'ratio':str(value['M']/Q(n+2)),'first_omitted_degree':n+1},
          'polynomial_coefficients':{name:list(map(str,values)) for name,values in coefficients.items()},
          'polynomial_values':{'Z':str(value['Z_poly']),'Aproduct':str(value['A_poly']),'Zindependent':str(value['Z_ind_poly'])},
          'enclosures':{name:list(map(str,value[key])) for name,key in [('Z','Z'),('Aproduct','A'),('Zindependent','Z_ind'),('expectation','observable'),('partition_excess','excess')]},
          'expectation_width':str(value['observable_width']),
          'expectation_status':'target-certified' if value['observable_width']<precision else 'insufficient-width',
          'partition_excess_status':'certified-positive' if value['excess'][0]>0 else 'inconclusive',
          'derivative_convention':'one derivative per distinct face coefficient, then all k_f=k'}
        if not same(certificate,expected):raise ValueError('independent cube coefficient/remainder/normalization replay failed')
        self.unchanged()
        return value

    def collection(self,collection):
        if type(collection) is not dict or set(collection)!={'schema','certificates','zero','negative'} or collection['schema']!='ym15-cube-series-collection-v1':
            raise ValueError('strict collection envelope required')
        rows=collection['certificates']
        if type(rows) is not list or len(rows)!=5 or [c.get('degree') if type(c) is dict else None for c in rows]!=[0,6,12,18,24]:
            raise ValueError('complete ordered declared degree sequence required')
        for certificate in rows:
            self.verify(certificate)
            if certificate['k']!='1/4' or certificate['precision']!='1/1000000000000':raise ValueError('target fixture mismatch')
        self.verify(collection['zero']);self.verify(collection['negative'])
        if collection['zero']['k']!='0' or collection['zero']['degree']!=0 or collection['negative']['k']!='-1/4' or collection['negative']['degree']!=24:
            raise ValueError('zero/signed fixture mismatch')
        return rows[-1]


def audit(forward_root,output_dir):
    root=Path(forward_root);review=Review(root);path=root/'B2/output/certificates.json';data=path.read_bytes();collection=json.loads(data)
    final=review.collection(collection);checks=[]
    def gate(name,test=True):
        if not test:raise ValueError(name)
        checks.append({'name':name,'passed':True})
    gate('all seven requested certificates independently replayed')
    gate('final expectation width and sign',Q(final['expectation_width'])<Q(1,10**12) and Q(final['enclosures']['expectation'][0])>0)
    gate('final two-tail partition excess strictly positive',Q(final['enclosures']['partition_excess'][0])>0)
    gate('coarse degrees0 and6 remain insufficient',all(c['expectation_status']=='insufficient-width' and Q(c['enclosures']['expectation'][0])<0 for c in collection['certificates'][:2]))
    gate('zero action returns exact cube Haar product',collection['zero']['enclosures']['expectation']==['1/1024','1/1024'])
    gate('common signed coupling symmetry is exact',collection['negative']['enclosures']==final['enclosures'])
    prediction=json.loads((HERE/'prediction.json').read_bytes())
    gate('pre-replay independent predictions agree exactly',all(row['exact']['observable']==cert['enclosures']['expectation'] and row['exact']['excess']==cert['enclosures']['partition_excess'] for row,cert in zip(prediction['rows'],collection['certificates'])))
    gate('six common derivatives differ from six distinct insertions atzero',factorial(6)*oracle.action_coefficients(6,False)[6]==Q(2775,64) and Q(2775,64)!=Q(1,1024))
    gate('signed numerator quotient includes all corners',oracle.quotient((Q(-3),Q(1)),(Q(2),Q(4)))==(Q(-3,2),Q(1,2)))
    def reject(name,mutation):
        try:review.verify(mutation)
        except ValueError:gate(name);return
        raise ValueError('accepted invalid certificate '+name)
    changes=[('schema','bad'),('source_sha256','0'*64),('graph_file_sha256','0'*64),('b1_source_sha256','0'*64),
      ('k','1.0'),('k',True),('k','2'),('degree',True),('degree',-1),('degree',31),
      ('precision','0'),('precision','-1'),('absolute_exponent_bound','0'),('expectation_width','0'),
      ('expectation_status','insufficient-width'),('partition_excess_status','inconclusive'),
      ('derivative_convention','sixth derivative along common coupling')]
    for field,value in changes:
        mutation=copy.deepcopy(final);mutation[field]=value;reject('metadata '+field+' '+str(value),mutation)
    for field,value in [('remainder','0'),('ratio','0'),('first_omitted_degree',True)]:
        mutation=copy.deepcopy(final);mutation['tail'][field]=value;reject('tail '+field,mutation)
    mutation=copy.deepcopy(collection['zero']);mutation['tail']['first_omitted_degree']=True;reject('nested bool alias at expectedone',mutation)
    mutation=copy.deepcopy(final);mutation['polynomial_coefficients']['Z']=mutation['polynomial_coefficients']['Zindependent'];mutation['polynomial_values']['Z']=mutation['polynomial_values']['Zindependent'];reject('plausible six independent faces model',mutation)
    mutation=copy.deepcopy(final);mutation['polynomial_coefficients']['Aproduct'][0]='2775/64';reject('common-diagonal derivative substituted for insertion',mutation)
    mutation=copy.deepcopy(final);mutation['enclosures']['Z']=['0','1'];reject('nonpositive denominator',mutation)
    mutation=copy.deepcopy(final);mutation['enclosures']['partition_excess']=[str(Q(final['polynomial_values']['Z'])-Q(final['polynomial_values']['Zindependent']))]*2;reject('baseline and cube tails omitted in excess',mutation)
    mutation=copy.deepcopy(final);mutation['scope']['generator']='physical Hamiltonian';reject('state-generator substitution',mutation)
    mutation=copy.deepcopy(final);mutation['extra']='mass gap';reject('extra physical metadata',mutation)
    for label,mutator in [('missing fixture',lambda c:c['certificates'].pop()),('empty list',lambda c:c.update(certificates=[])),('extra envelope',lambda c:c.update(extra=True)),('duplicate final fixture',lambda c:c['certificates'].__setitem__(0,copy.deepcopy(c['certificates'][-1])))]:
        mutation=copy.deepcopy(collection);mutator(mutation)
        try:review.collection(mutation)
        except ValueError:gate('collection '+label)
        else:raise ValueError('invalid collection accepted '+label)
    for filename in ('B2/series.py','B1/graph.json','B1/cube.py'):
        with tempfile.TemporaryDirectory() as temp:
            target=Path(temp)/'forward';shutil.copytree(root/'B1',target/'B1');shutil.copytree(root/'B2',target/'B2')
            local=Review(target);local.verify(final);p=target/filename;p.write_bytes(p.read_bytes()+b'\n')
            try:local.verify(final)
            except ValueError:gate('warmed source mutation '+filename)
            else:raise ValueError('source mutation accepted')
    gate('collection and sources unchanged',path.read_bytes()==data);review.unchanged()
    result={'schema':'ym15-B2-independent-review-v1','status':'passed','checks_count':len(checks),'checks':checks,
      'source_sha256':hashlib.sha256(SOURCE_BYTES).hexdigest(),'reviewed_inputs':review.hashes,
      'collection_sha256':hashlib.sha256(data).hexdigest(),'certificates_replayed':7,
      'final':{'k':final['k'],'degree':final['degree'],'expectation':final['enclosures']['expectation'],
               'width':final['expectation_width'],'partition_excess':final['enclosures']['partition_excess']},
      'limits':['Finite sphere-topology cube Wilson graph only; no physical mass-gap inference.',
                'Independent evaluator supports degrees0..30; requested evidence uses0..24. Producer API extends to48 but those extra degrees are not claimed independently reviewed.',
                'Exact Taylor certificates do not require rounded floating values to lie inside ultranarrow intervals.']}
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True);(out/'independent_review.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'passed','checks':len(checks),'width_display':float(Q(final['expectation_width'])),
                      'partition_excess_lower_display':float(Q(final['enclosures']['partition_excess'][0]))}))
    return result


if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('usage: verify_series.py FORWARD_ROOT OUTPUT_DIR')
    audit(*sys.argv[1:])
