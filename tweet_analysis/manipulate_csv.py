import pandas as pd
import logging

INDEX_TWEET_TEXT = 1
# todo バグ調査用のロギングのため後で消す
LOGFILE = 'man_debug.log'
logging.basicConfig(filename=LOGFILE,level=logging.DEBUG)


class ManipulateCsv():
    """
    this class gets information from csv data with using pandas
    needed arg 1 : csv_name
    """
    CSV_DIR = 'tweet_analysis/csv/'

    def __init__(self, csv_name=''):
        self.csv_name = csv_name
        self.CSV_FILE_PATH = self.CSV_DIR + self.csv_name

    def get_data_frame(self):
        # tweetの最大文字数が200文字のため
        pd.set_option("display.max_colwidth", 250)
        df = pd.read_csv(self.CSV_FILE_PATH)
        return df

    def get_df_describe(self):
        df = pd.read_csv(self.CSV_FILE_PATH)
        return df.describe()

    def set_analysis_result(self, df, desc):
        """
　　　　　データフレームから分析結果を作成
        :param df:
        :param desc:
        :return: 辞書型の分析結果

        """
        context = {
            'fv_mean': str(desc.at['mean', 'favorite']),
            'fv_max': int(desc.at['max', 'favorite']),
            'fv_max_text': df[df['favorite'] == desc.at['max', 'favorite']].iloc[0, INDEX_TWEET_TEXT],
            'rt_mean': str(desc.at['mean', 'RT']),
            'rt_max': int(desc.at['max', 'RT']),
            'rt_max_text': df[df['RT'] == desc.at['max', 'RT']].iloc[0, INDEX_TWEET_TEXT],
        }
        return context

    def convert_list_to_df(self, all_tweets_list):
        """
        1行目はヘッダを想定。リストをデータフレームに変換し分析結果を返す
        :param all_tweets_list:
        :return:1 データフレーム,2 データフレーム情報
        """
        context = {'all_tweets_list': all_tweets_list}
        if len(all_tweets_list) == 0:
            return context

        df = pd.DataFrame(all_tweets_list[1:],
                          columns=all_tweets_list[0])
        desc = df.describe()
        return df, desc


if __name__ == '__main__':
    pass
