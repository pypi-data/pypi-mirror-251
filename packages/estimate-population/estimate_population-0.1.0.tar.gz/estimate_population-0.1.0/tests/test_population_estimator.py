# tests/test_population_estimator.py

import unittest
from estimate_population.population_estimator import auto_estimate_population_size

class TestPopulationEstimator(unittest.TestCase):

    def test_auto_estimate_population_size(self):
        # テスト用のCSVファイルを作成し、行数を取得する
        test_csv_file = 'test_data.csv'
        with open(test_csv_file, 'w') as file:
            file.writelines(['1,2,3\n', '4,5,6\n', '7,8,9\n'])

        sample_size = auto_estimate_population_size(test_csv_file)

        # 期待される結果と比較する
        self.assertEqual(sample_size, 3)

if __name__ == '__main__':
    unittest.main()
