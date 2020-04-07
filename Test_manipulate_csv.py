import unittest
from tweet_analysis.manipulate_csv import ManipulateCsv

instance = ManipulateCsv('muni_gurume.csv')

descr = instance.get_df_describe()
print(descr.at['mean','favorite'])
print(descr.at['mean','retweet_count'])
print(descr.at['max', 'favorite'])
print(type(descr))

df =instance.get_data_frame()

print(df.info())
print(df[df['favorite'] == descr.at['max', 'favorite']].loc[:,'tweet_text'])


