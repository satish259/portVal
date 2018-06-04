import unittest
from pricer import pricer

class Test_test_pricer(unittest.TestCase):
    def test_fetchPrice(self):
        p1=pricer('', '')
        test1=p1.fetchPrice()
        test2=p1.fetchPrice()
        self.assertTrue(test1,1)
        self.assertTrue(test2,1)

if __name__ == '__main__':
    unittest.main()
