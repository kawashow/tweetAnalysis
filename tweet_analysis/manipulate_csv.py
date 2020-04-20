import pandas as pd


class ManipulateCsv():
    """
    this class gets information from csv data with using pandas
    needed arg 1 : csv_name
    """
    CSV_DIR = 'tweet_analysis/csv/'

    def __init__(self, csv_name):
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


if __name__ == '__main__':
    pass
