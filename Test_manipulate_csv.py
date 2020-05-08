import unittest
from tweet_analysis.manipulate_csv import ManipulateCsv


class TestManipulateCsv(unittest.TestCase):
    def test_convert_list_to_df(self):
        tweet_list = [['favorite', 1, 2], ['3', '4', '5']]
        instance = ManipulateCsv()
        df = instance.convert_list_to_df(tweet_list)
        print(df)

    def test_get_data_frame(self):
        instance = ManipulateCsv('muni_gurume.csv')
        df = instance.get_data_frame()
        print(df)


if __name__ == '__main__':
    unittest.main()
