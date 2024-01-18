import _add_path
import unittest
from wolfhece.pyshields import get_d_cr, get_Shields_2D_Manning

class TestShields(unittest.TestCase):

    def test_shields(self):

        q = 1.
        h = 1.
        K = 25.

        d = 0.1

        rhom = 2650
        s   = rhom/1000.

        Shields1 = get_Shields_2D_Manning(s, d, q, h, K)

        d_cr_shields, d_cr_Itzbach = get_d_cr(q, h, K, rhom)
        Shields3 = get_Shields_2D_Manning(s, d_cr_shields, q, h, K)

        q = 1.
        h = 1.
        K = 1.

        d = 1.

        rhom = 2000.
        s   = rhom/1000.

        Shields4 = get_Shields_2D_Manning(s, d, q, h, K)


        self.assertEqual(Shields1, 0.009696969696969697)
        self.assertAlmostEqual(d_cr_shields, 0.02154882154882155, 8)
        self.assertAlmostEqual(Shields3, 0.045, 4)
        self.assertEqual(Shields4, 1.)