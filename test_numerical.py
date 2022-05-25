import unittest
from numerical import Numerical


class NumericalTestCase(unittest.TestCase):
    def testIntRaisesException(self):
        numerical = Numerical()
        with self.assertRaises(Exception) as e:
            int(numerical)


if __name__ == '__main__':
    unittest.main()
