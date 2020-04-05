import pandas as pd
'''
this class gets information from csv data with using pandas
'''
def test_a():
    pass

class ManipulateCsv():
    def __init__(self, csv_name):
        self.csv_name = csv_name
        self.CSV_FILE_PATH = 'csv/' + self.csv_name

    def get_data_set(self):
        df = pd.read_csv(self.CSV_FILE_PATH)
        data_list = [df.info(), df.shape, df.describe]
        return data_list


if __name__ == '__main__':
    pass
