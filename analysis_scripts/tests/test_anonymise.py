import unittest
from analytics import anonymise

class TestAnonymise(unittest.TestCase):

    def test_anon_dr(self):
        self.assertEqual('\nDetails: HI', anonymise('Patient Name:  Brian\nDetails: HI\n\nDr David Barney\nRadiologist'))

    def test_anon_non_doc(self):
        self.assertEqual('\nDetails: HI\n', anonymise('Patient Name:  Brian\nDetails: HI\n\n AN other\nSonographer'))

    def test_anon_radiographer(self):
        reptest = 'Clinical Information: Pneumothorax? \nI note a CTPA has been requested.\nAlfred Hitchcock\nReporting Radiographer\nRA67676'
        self.assertEqual( anonymise(reptest),'\nClinical Information: Pneumothorax? \nI note a CTPA has been requested.')

if __name__ == '__main__':
    unittest.main()
