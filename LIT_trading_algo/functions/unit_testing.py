from LIT_trading_algo.functions.basic_functions import *

import pandas as pd
import unittest


class TestTradingFunctions(unittest.TestCase):

    def test_bear(self):
        self.assertTrue(bear(pd.Series([1, 2, 3, 4, 1])))
        self.assertFalse(bear(pd.Series([1, 2, 3, 1, 4])))

    def test_bull(self):
        self.assertTrue(bull(pd.Series([1, 2, 3, 4, 4])))
        self.assertFalse(bull(pd.Series([1, 2, 3, 1, 1])))

    def test_last_low(self):
        df = pd.DataFrame({
            'time': [1 ,1 ,1 ,1],
            'Open': [1, 2, 3, 4],
            'High': [5, 6, 7, 8],
            'Low': [0, 5, 1, 3],
            'Close': [4, 3, 2, 1]
        })
        self.assertEqual(last_low(df, 3), 1)

    def test_last_high(self):
        df = pd.DataFrame({
            'time': [1 ,1 ,1 ,1],
            'Open': [1, 2, 3, 4],
            'High': [5, 6, 7, 3],
            'Low': [0, 1, 2, 3],
            'Close': [4, 3, 2, 1]
        })
        self.assertEqual(last_high(df, 3), 7)

    def test_speed(self):
        df = pd.DataFrame({
            'time': [1 ,1 ,1 ,1 ,1],
            'Open': [1, 2, 3, 4, 5],
            'High': [5, 2, 3, 5, 4],
            'Low': [0, 1, 2, 3, 2],
            'Close': [4, 3, 2, 1, 2] })

        self.assertTrue(speed(df, 2, 2, 2))
        self.assertFalse(speed(df, 2, 2, 4))


if __name__ == '__main__':
    unittest.main()
