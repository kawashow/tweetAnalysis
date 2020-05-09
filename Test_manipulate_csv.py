import unittest
from tweet_analysis.manipulate_csv import ManipulateCsv


class TestManipulateCsv(unittest.TestCase):
    def test_convert_list_to_df(self):
        tweet_list = [['favorite', 'RT', 2], [3, 4, '5']]
        instance = ManipulateCsv()
        df, desc = instance.convert_list_to_df(tweet_list)
        print(df.favorite)
        analysis_context = instance.set_analysis_result(df, desc)
        print(analysis_context)

    def test_get_data_frame(self):
        instance = ManipulateCsv('muni_gurume.csv')
        df = instance.get_data_frame()
        print(df)


if __name__ == '__main__':
    unittest.main()
