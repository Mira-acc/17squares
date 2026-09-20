import unittest
from fractions import Fraction as F
from verify import maximum_load, polygon, margin, check


def pose(x=0,y=0,c=1,s=0,w=1):
    return tuple(map(F,(x,y,c,s,w)))


class Tests(unittest.TestCase):
    def test_single_square(self):
        self.assertEqual(maximum_load([pose(w=F(2,3))])[0],F(2,3))

    def test_coincident_squares(self):
        self.assertEqual(maximum_load([pose(),pose(w=2)])[0],3)

    def test_touching_open_squares(self):
        self.assertEqual(maximum_load([pose(),pose(x=1)])[0],1)

    def test_oblique_overlap(self):
        self.assertEqual(maximum_load([pose(),pose(c=F(3,5),s=F(4,5),w=2)])[0],3)

    def test_oblique_disjoint(self):
        self.assertEqual(maximum_load([pose(),pose(x=3,c=F(3,5),s=F(4,5),w=2)])[0],2)

    def test_vertex_boundary(self):
        p=pose(c=F(3,5),s=F(4,5))
        self.assertTrue(all(margin(p,v)==0 for v in polygon(p)))

    def test_supplied_certificate(self):
        result=check()
        self.assertEqual(result['maximum_pointwise_load'],'59431493389/79999999999')
        self.assertEqual(result['fractional_mass'],'81407286808/79999999999')
        self.assertEqual(result['arrangement_slabs'],1475)
        extra=result['additional_activations']
        self.assertEqual(extra['unit_weight_sum'],'99656162199/79999999999')
        self.assertEqual(extra['small_core_weight_sum'],'96836866527/79999999999')
        self.assertEqual(extra['maximum_pointwise_load'],'73959042636/79999999999')
        self.assertEqual(extra['arrangement_slabs'],8405)


if __name__=='__main__':
    unittest.main(verbosity=2)
