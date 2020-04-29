import unittest
from tweet_analysis.manipulate_csv import ManipulateCsv

instance = ManipulateCsv('muni_gurume_old.csv')

descr = instance.get_df_describe()
print(descr.at['mean','favorite'])
print(descr.at['mean','retweet_count'])
print(descr.at['max', 'favorite'])
print(descr)

df =instance.get_data_frame()


#print(df[df['favorite'] == descr.at['max', 'favorite']].loc[:,'tweet_text'])
print('------------------------')
print(df[df['favorite'] == descr.at['max', 'favorite']])
print(df[df['favorite'] == descr.at['max', 'favorite']]['tweet_text'])
print(type(df.loc[df['favorite'] == descr.at['max', 'favorite'],'tweet_text']))
print(df.loc[df['favorite'] == descr.at['max', 'favorite']].iloc[0,1])

