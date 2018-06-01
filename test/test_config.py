import unittest
import pandas
import config

class Test_test_config(unittest.TestCase):
    def test_getTransFee(self):
        self.assertIsInstance(config.getTransFee(), pandas.DataFrame)

    def test_getBuySellMultipler(self):
        self.assertIsInstance(config.getBuySellMultipler(), pandas.DataFrame)

if __name__ == '__main__':
    unittest.main()
