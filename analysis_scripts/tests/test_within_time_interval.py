import unittest
import pandas as pd
from analytics import within_time_interval

class TestWithinTimeInterval(unittest.TestCase):
    def test_within(self):
        self.assertEqual("xx","xx")

    def test_32_forwards(self):
        self.assertTrue( within_time_interval(pd.to_datetime('2/1/2018'), pd.to_datetime('1/1/2018'), 32.0, direction='forwards') )
        
    def test_30_forwards(self):
        self.assertFalse( within_time_interval(pd.to_datetime('2/1/2018'), pd.to_datetime('1/1/2018'), 30.0, direction='forwards') )

    def test_32_backwards(self):
        self.assertTrue( within_time_interval(pd.to_datetime('1/1/2018'), pd.to_datetime('2/1/2018'), 32.0, direction='backwards') )

    def test_30_backwards(self):
        self.assertFalse( within_time_interval(pd.to_datetime('1/1/2018'), pd.to_datetime('2/1/2018'), 30.0, direction='backwards') )

    def test_64_centred(self):
        self.assertTrue( within_time_interval(pd.to_datetime('2/1/2018'), pd.to_datetime('1/1/2018'), 64.0, direction='centred') )

    def test_60_centred(self):
        self.assertFalse( within_time_interval(pd.to_datetime('2/1/2018'), pd.to_datetime('1/1/2018'), 60.0, direction='centred') )

if __name__ == '__main__':
    unittest.main()
