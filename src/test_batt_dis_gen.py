import unittest
import numpy as np
from batt_dis_gen import BattDisGen

class TestBattDisGen(unittest.TestCase):
    def test_generate(self):
        batt = BattDisGen()
        batt.generate(timestep=1, exponent=0.01, chargedbattvolt=12, dischargecurve=3, timeoffset=100)
        self.assertIsInstance(batt.time, np.ndarray)
        self.assertIsInstance(batt.discurve, np.ndarray)
        self.assertEqual(len(batt.time), 100)
        self.assertEqual(len(batt.discurve), 100)
        # Further assertions could be added to check the values in discurve
        # For example, checking the start and end values of the discharge curve
        self.assertAlmostEqual(batt.discurve[0], 12 - 3 * np.exp(0.01 * (0 - 100)))
        self.assertAlmostEqual(batt.discurve[-1], 12 - 3 * np.exp(0.01 * (99 - 100)))

if __name__ == '__main__':
    unittest.main()