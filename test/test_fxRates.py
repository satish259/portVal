import unittest
from fxRates import fxRates

class Test_test_fxRates(unittest.TestCase):
    def test_fxRates(self):
        f1=fxRates('2018-6-1','GBP','USD')
        test1=f1.fetchFxRates()
        test2=f1.fetchFxRates()
        self.assertTrue(test1,1)
        self.assertTrue(test2,1)        

if __name__ == '__main__':
    unittest.main()
