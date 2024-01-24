import unittest, os.path
from analytics import process_csv

class TestProcessCsv(unittest.TestCase):

    def test_process_csv(self):
        csv_path='../data/semisynthetic_reports.csv'
        assets_folder='./tests/output/'
        md_file='./tests/output/test_out.markdown'
        process_csv(csv_path, assets_folder, md_file)
        expected_files = [
            f'{assets_folder}IPCT_imaging_24h.png',
            f'{assets_folder}IPMRI_imaging_24h.png',
            f'{assets_folder}IPUS_imaging_24h.png',
            f'{assets_folder}IPCT_reporting_4h.png',
            f'{assets_folder}IPMRI_reporting_4h.png',
            f'{assets_folder}IPUS_reporting_4h.png',
            md_file,
        ]
        for f in expected_files:   
            self.assertTrue( os.path.exists(f) )

        # Tidy-up
        #for f in expected_files:
        #    os.remove(f)

if __name__ == '__main__':
    unittest.main()
