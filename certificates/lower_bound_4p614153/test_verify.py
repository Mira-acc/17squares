#!/usr/bin/env python3
"""Boundary, exact cross-implementation, and deliberate-rejection controls."""
from fractions import Fraction as F
from pathlib import Path
import copy,json,os,subprocess,sys,tempfile,unittest
import verify
sys.path.insert(0,str(verify.ROOT/'upstream'))
from sweep import coverage,direct_mass

class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory();cls.out=Path(cls.temp.name)
        cls.tree=verify.compile_kernel(cls.out)
        cls.direct=verify.compile_kernel(cls.out,True)
        cls.case=verify.read(verify.ROOT/'certificate.json')
    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()
    def cpp(self,aa,jobs,binary=None,raw=None):
        path=self.out/'test.txt'
        if raw is None:verify.write_input(path,aa,jobs)
        else:path.write_text(raw)
        p=subprocess.run([str(binary or self.tree),str(path)],text=True,capture_output=True,env=dict(os.environ,OMP_NUM_THREADS='1'))
        return p
    def test_01_new_arithmetic(self):
        aa,jobs,margin=verify.validate(self.case)
        self.assertGreater(margin,0);self.assertGreater(len(jobs),1000)
    def test_02_upstream_identity(self):
        c=verify.upstream_certificate();aa,jobs,_=verify.validate(c)
        self.assertEqual(len(aa),1616);self.assertEqual(len(jobs),2925)
    def test_21_sharpening(self):
        import sharpening
        result=sharpening.check(self.case)
        self.assertEqual(result['target'],'46129999999859/9997499999900')
        self.assertEqual(result['minimum_scalar_slack'],'3156837929188515937426608335639966497291/2009206832324365552240070870206040941943769650000000000')
        self.assertEqual(result['fixed_library_axis_cap'],'783497431270959447209451212282201903/169803068915384203003727378193801903')
    def test_22_sharpening_rejects_insufficient_margin(self):
        import sharpening
        from unittest.mock import patch
        with patch.object(sharpening,'EPSILON',F(1,1000)):
            with self.assertRaisesRegex(ValueError,'containment inequality'):
                sharpening.check(self.case)
    def test_03_angle_gap(self):
        c=copy.deepcopy(self.case);c['entries'][1][0]=c['entries'][0][0]
        with self.assertRaises(ValueError):verify.validate(c)
    def test_04_incomplete_angles(self):
        c=copy.deepcopy(self.case);c['entries']=c['entries'][:-1]
        with self.assertRaises(ValueError):verify.validate(c)
    def test_05_nonstrict_core(self):
        c=copy.deepcopy(self.case);c['entries'][0][3]=c['A']
        with self.assertRaises(ValueError):verify.validate(c)
    def test_06_wrong_target(self):
        c=copy.deepcopy(self.case);c['target']='5'
        with self.assertRaises(ValueError):verify.validate(c)
    def test_07_wrong_outer_side(self):
        c=copy.deepcopy(self.case);c['L']='5'
        with self.assertRaises(ValueError):verify.validate(c)
    def test_08_negative_orbit_weight(self):
        c=copy.deepcopy(self.case);c['orbits'][0][2]=-1
        with self.assertRaises(ValueError):verify.validate(c)
    def test_09_duplicate_orbit(self):
        c=copy.deepcopy(self.case);c['orbits'].append(c['orbits'][0])
        with self.assertRaises(ValueError):verify.validate(c)
    def test_10_nonintegral_atom(self):
        c=copy.deepcopy(self.case);c['orbits'][0][0]=0.1
        with self.assertRaises(ValueError):verify.validate(c)
    def test_11_mass_gap(self):
        c=copy.deepcopy(self.case);c['minimum_units']=0
        with self.assertRaises(ValueError):verify.validate(c)
    def test_12_mass_mismatch(self):
        c=copy.deepcopy(self.case);c['mass_units']+=1
        with self.assertRaises(ValueError):verify.validate(c)
    def test_13_duplicate_json(self):
        p=self.out/'bad.json';p.write_text('{"a":1,"a":2}')
        with self.assertRaises(ValueError):verify.read(p)
    def test_14_nonfinite_json(self):
        p=self.out/'bad.json';p.write_text('{"a":NaN}')
        with self.assertRaises(ValueError):verify.read(p)
    def test_15_closed_boundary(self):
        aa=[(230650,230650,7)];jobs=[(F(0),F(1613,1000),F(3,2))]
        for binary in (self.tree,self.direct):
            p=self.cpp(aa,jobs,binary);self.assertEqual(p.returncode,0,p.stderr)
            self.assertEqual(json.loads(p.stdout)['minimum_units'],7)
    def test_16_axis_and_oblique_known(self):
        aa=[(230650,230650,7)]
        jobs=[(t,F(2),F(2)) for t in (F(0),F(1,3),F(3,5))]
        for binary in (self.tree,self.direct):
            p=self.cpp(aa,jobs,binary);self.assertEqual(p.returncode,0,p.stderr)
            self.assertEqual([json.loads(s)['minimum_units'] for s in p.stdout.splitlines()],[7]*3)
    def test_17_zero_weight(self):
        p=self.cpp([(230650,230650,0)],[(F(0),F(1),F(1))]);self.assertEqual(p.returncode,0,p.stderr)
        self.assertEqual(json.loads(p.stdout)['minimum_units'],0)
    def test_18_geometric_python_crosschecks(self):
        aa=verify.expand([[100000,190000,3],[180000,210000,5],[230650,230650,2]])
        jobs=[(t,B,max(B*sum(verify.trig(t))/2,F(3,4))) for t in (F(0),F(1,20),F(1,5),F(207107,500000),F(3,5)) for B in (F(7,8),F(3,2))]
        expected=[]
        for t,B,r in jobs:
            expected.append(int(F(coverage(verify.L,B,[(F(x,100000),F(y,100000),F(w)) for x,y,w in aa],t,r)['minimum'])))
        for binary in (self.tree,self.direct):
            p=self.cpp(aa,jobs,binary);self.assertEqual(p.returncode,0,p.stderr)
            self.assertEqual([json.loads(s)['minimum_units'] for s in p.stdout.splitlines()],expected)
    def test_19_cpp_malformed_controls(self):
        good='1 1\n230650 230650 7\n0 1 2 1 2 1\n'
        cases=[good+'extra\n',good.replace('0 1 2 1 2 1','0 0 2 1 2 1'),good.replace('0 1 2 1 2 1','0 1 2 1 4613 2000'),
          good.replace('0 1 2 1 2 1','0 1 2 1 1 2'),good.replace('230650 230650 7','230650 230650 -1'),
          good.replace('230650 230650 7','230649 230650 7'),good.replace('230650 230650 7','230650 230650 1000000000001'),
          '1 1\n230650 230650 7\n','2 1\n230650 230650 7\n230650 230650 7\n0 1 2 1 2 1\n']
        for raw in cases:
            with self.subTest(raw=raw):self.assertNotEqual(self.cpp(None,None,raw=raw).returncode,0)
    def test_20_upstream_counterexamples(self):
        c=verify.upstream_certificate();aa=verify.expand(c['orbits']);aa=[(F(x,100000),F(y,100000),F(w,10**6)) for x,y,w in aa];A=F(c['A'])
        for e in verify.read(verify.ROOT/'upstream/counterexamples.json'):
            t,B=F(e['t']),F(e['B']);xy=tuple(map(F,e['centre']));u=min(map(F,e['parent_interval']),key=lambda v:sum(verify.trig(v)))
            cp,sp=verify.trig(u);ct,st=verify.trig(t);r=A*(cp+sp)/2
            self.assertTrue(all(r<=z<=verify.L-r for z in xy));self.assertLess(B*(ct*cp+st*sp+abs(st*cp-ct*sp)),A)
            mass,ids=direct_mass(aa,B,t,xy);self.assertEqual(mass,F(e['mass']));self.assertEqual(len(ids),e['atom_count'])

if __name__=='__main__':unittest.main(verbosity=2)
