import sys, types, json, unittest, importlib.util
from pathlib import Path
class E(Exception): pass
class Contract:
 def __new__(cls):
  x=super().__new__(cls);x.cases={};return x
sender=types.SimpleNamespace(as_hex='owner');answer={}
gl=types.ModuleType('genlayer');gl.contract=types.SimpleNamespace(Contract=Contract);gl.storage=types.SimpleNamespace(TreeMap=dict)
gl.message=types.SimpleNamespace(sender_address=sender);gl.vm=types.SimpleNamespace(UserError=E);gl.public=types.SimpleNamespace(write=lambda f:f,view=lambda f:f)
gl.nondet=types.SimpleNamespace(exec_prompt=lambda *a,**k:answer);gl.eq_principle=types.SimpleNamespace(prompt_comparative=lambda f,p:f())
gt=types.ModuleType('genlayer.types');gt.u256=int;sys.modules['genlayer']=gl;sys.modules['genlayer.types']=gt
spec=importlib.util.spec_from_file_location('range_contract',Path(__file__).parent/'contract.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def bounded(i,lo,hi,q):return dict(id=i,status='bounded',lower=lo,upper=hi,quote=q,reason='Exact range for the committed metric and unit')
class Tests(unittest.TestCase):
 def setUp(self):
  global answer
  sender.as_hex='owner';self.c=m.RangeWitness();self.c.commit('Parcel transit time for route A','hours',json.dumps(['Route A parcel transit takes 12 to 24 hours.','Route A parcel transit takes 18 to 30 hours.','The parcel packaging weighs 200 grams.']))
  answer={'readings':[bounded(1,12,24,'12 to 24 hours'),bounded(2,18,30,'18 to 30 hours'),dict(id=3,status='irrelevant',lower=None,upper=None,quote='',reason='Packaging weight is not transit time')]}
 def result(self):
  self.c.resolve('1');return json.loads(self.c.get_case('1'))['result']
 def test_overlap(self):self.assertEqual(self.result()['intersection'],dict(status='overlap',bounded_ids=[1,2],excluded_ids=[3],lower=18,upper=24,lower_witness=2,upper_witness=1))
 def test_conflict_witness(self):
  rows=[bounded(1,12,24,'unused'),bounded(2,30,40,'unused')];r=self.c._aggregate(rows);self.assertEqual((r['status'],r['lower_witness'],r['upper_witness']),('conflict',2,1));self.assertGreater(r['lower'],r['upper'])
 def test_touching_endpoints(self):self.assertEqual(self.c._aggregate([bounded(1,12,24,''),bounded(2,24,30,'')])['status'],'overlap')
 def test_ties_lowest_id(self):
  r=self.c._aggregate([bounded(2,12,24,''),bounded(1,12,24,'')]);self.assertEqual((r['lower_witness'],r['upper_witness']),(1,1))
 def test_insufficient(self):
  answer['readings'][1]=dict(id=2,status='uncertain',lower=None,upper=None,quote='',reason='Ambiguous unit');self.assertEqual(self.result()['intersection']['status'],'insufficient')
 def test_quote_not_fabricated(self):
  answer['readings'][0]['quote']='A made-up quote'
  with self.assertRaises(E):self.c.resolve('1')
 def test_complete_coverage(self):
  answer['readings'].pop()
  with self.assertRaises(E):self.c.resolve('1')
 def test_duplicate_id(self):
  answer['readings'][1]['id']=1
  with self.assertRaises(E):self.c.resolve('1')
 def test_boolean_id(self):
  answer['readings'][0]['id']=True
  with self.assertRaises(E):self.c.resolve('1')
 def test_boolean_bound(self):
  answer['readings'][0]['lower']=True
  with self.assertRaises(E):self.c.resolve('1')
 def test_reversed_interval(self):
  answer['readings'][0]['lower']=25
  with self.assertRaises(E):self.c.resolve('1')
 def test_negative_bound(self):
  answer['readings'][0]['lower']=-1
  with self.assertRaises(E):self.c.resolve('1')
 def test_decimal_bound(self):
  answer['readings'][0]['lower']=12.1
  with self.assertRaises(E):self.c.resolve('1')
 def test_excluded_no_bounds(self):
  answer['readings'][2]['lower']=0
  with self.assertRaises(E):self.c.resolve('1')
 def test_owner(self):
  sender.as_hex='attacker'
  with self.assertRaises(E):self.c.resolve('1')
 def test_final_immutable(self):
  self.result()
  with self.assertRaises(E):self.c.resolve('1')
 def test_snapshot_preserved(self):
  old=json.loads(self.c.get_case('1'));self.result();new=json.loads(self.c.get_case('1'));self.assertEqual(old['snapshot_sha256'],new['snapshot_sha256']);self.assertEqual(old['excerpts'],new['excerpts']);self.assertEqual(len(new['result']['readings'][0]['excerpt_sha256']),64)
 def test_duplicate_inputs(self):
  with self.assertRaises(E):self.c.commit('Transit time','hours',json.dumps(['Duplicate sentence.']*2))
 def test_atomic_failure(self):
  answer['readings'][0]['upper']=10
  with self.assertRaises(E):self.c.resolve('1')
  self.assertEqual(json.loads(self.c.get_case('1'))['status'],'committed')
if __name__=='__main__':unittest.main()
