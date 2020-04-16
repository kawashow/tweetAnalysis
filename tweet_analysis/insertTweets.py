# coding:utf-8
import psycopg2
import csv
import sys
import re
import traceback
import logging
import dbconf

'''
  from csv file to db
'''

HOST = conf.HOST
PORT = conf.PORT
DB_NAME = conf.DB_NAME
USER_NAME = conf.USER_NAME
DB_PASS = conf.DB_PASS

# db name and sql
INSERT_QUERY = 'insert into {0} values ({1})'
TWEETS_TABLE_NAME = 'tweets (id,tweet_text,favorite,retweeted,tweet_created_date)'
TWEETS_REPLY_TABLE = 'reply_tweets (id,in_reply_to_status_id,TWEET_TEXT,tweet_created_date)'
MEDIA_TABLE_NAME = 'tweet_media(media_id,tweet_id,media_path,media_link)'

# grume_db column number information
ID_COLUMN_NUM = 0
TEXT_COLUMN_NUM = 1
FAVORITE_COLUMN_NUM = 2
RETWEET_COLUMN_NUM = 3
CREATEDATE_COLUMN_NUM = 4
REPLY_STATUS_COLUMN_NUM = 5
MEDIA_ID_COLUMN_NUM = 6
MEDIA_LINK_COLUMN_NUM = 7

MEDIA_DST_PATH = '/appl/scripts/media/'

TWEETS_INSERT_QUERY = INSERT_QUERY.format(TWEETS_TABLE_NAME, 'id')
print(TWEETS_INSERT_QUERY)


class InsertTweets():
    def __init__(self):
        pass

    def main(self):
        # connect to db
        connection = psycopg2.connect(
            'host=' + HOST + ' port=' + PORT + ' dbname=' + DB_NAME + ' user=' + USER_NAME + ' password=' + DB_PASS)
        cur = connection.cursor()

        input_file_name = sys.argv[1] + '.csv'
        # from csv file, create insert query
        with open(input_file_name, 'r', encoding='utf-8')as f:
            reader = csv.reader(f)
            for index, line in enumerate(reader):
                if index == 0:
                    continue

                if line[REPLY_STATUS_COLUMN_NUM] != '':
                    print('reply')
                    insert_value = line[ID_COLUMN_NUM] + ',\'' + line[5] + '\',\'' + line[TEXT_COLUMN_NUM] + '\',\'' + line[
                        CREATEDATE_COLUMN_NUM] +'\''
                    print(INSERT_QUERY.format(TWEETS_REPLY_TABLE, insert_value))
                    reply_insert_query = INSERT_QUERY.format(TWEETS_REPLY_TABLE, insert_value)
                    cur.execute(reply_insert_query)
                else:
                    insert_value = line[ID_COLUMN_NUM] + ',\'' + line[TEXT_COLUMN_NUM] + '\',' + line[RETWEET_COLUMN_NUM] + ',' + \
                                   line[FAVORITE_COLUMN_NUM] + ',\'' + line[CREATEDATE_COLUMN_NUM]+'\''
                    print(line[TEXT_COLUMN_NUM])
                    print(INSERT_QUERY.format(TWEETS_TABLE_NAME, insert_value))
                    tweets_insert_query = INSERT_QUERY.format(TWEETS_TABLE_NAME, insert_value)
                    cur.execute(tweets_insert_query)

                # insert into media. if line doesn't have media info, skip this insert query
                try:
                    pic_name = line[MEDIA_LINK_COLUMN_NUM].split('/')[-1]
                    local_media_path = MEDIA_DST_PATH + pic_name
                    insert_value = line[MEDIA_ID_COLUMN_NUM] + ',' + line[ID_COLUMN_NUM] + ',\'' + local_media_path + '\',\'' + line[
                        MEDIA_LINK_COLUMN_NUM] + '\''
                    print(INSERT_QUERY.format(MEDIA_TABLE_NAME,insert_value))
                    media_insert_query = INSERT_QUERY.format(MEDIA_TABLE_NAME,insert_value)
                    cur.execute(media_insert_query)
                except IndexError:
                    continue
        connection.commit()


# execute
if __name__ == '__main__':
    InsertTweets().main()
