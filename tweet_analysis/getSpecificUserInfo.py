# coding:utf-8

import tweepy
from datetime import timedelta
import sys
from conf import twitterApi
import csv
import traceback
import urllib.request
import urllib.error

CONSUMER_KEY = twitterApi.CONSUMER_KEY
CONSUMER_SECRET = twitterApi.CONSUMER_SECRET
ACCESS_KEY = twitterApi.ACCESS_KEY
ACCESS_SECRET = twitterApi.ACCESS_SECRET

CSV_EXTENSION = '.csv'
MEDIA_DIR = '/appl/scripts/media/'

class GetUserInfo():
    '''
    get user's tweets from twitter and output to csv file
    '''
    
    def __init__(self):
        self.num = 0  # 取得するツイートを計算する
        # 全ツイートを入れる空のリストを用意
        self.all_tweets = []

    def get_tweets(self):
        '''
        get user's tweets from Twitter and output header to csv
        '''

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth)
        if len(sys.argv) < 2:
            print('need one parameter')
            return False
        account = sys.argv[1]
        # account = '@muni_gurume'
        tweets_file_name = account + CSV_EXTENSION
        # reply_file_name = account + '_reply' + CSV_EXTENSION
        # media_file_name = account + '_media' + CSV_EXTENSION
        print(account)
        # tweet_mode='extended'を設定することで、tweetが切れないかつ、画像も取得できる。
        tweets = api.user_timeline(account, count=200, tweet_mode='extended')

        # ファイルにツイートを出力。エクセルでの文字化け防止のためBOM付utf8で作成
        with open(tweets_file_name, mode='w', encoding='utf_8_sig')as f:
            tweets_writer = csv.writer(f)
            # header
            tweets_writer.writerow(
                ['id_str', 'tweet_text', 'favorite', 'retweet_count', 'Data', 'in_reply_to_status_id_str', 'media_id',
                 'media_url'])
            self.output_tweet(tweets, tweets_writer)

            # get every 200 tweets
            while len(tweets) > 0:
                # tweet_mode='extended'を設定することで、tweetが切れないかつ、画像も取得できる。
                tweets = api.user_timeline(account, count=200, max_id=self.all_tweets[-1].id - 1,
                                           tweet_mode='extended')
                self.output_tweet(tweets, tweets_writer)
                print(self.num, 'ツイート表示しました。')



    def output_tweet(self, tweets, tweets_writer):
        '''
        output tweets to csv file
        '''


        self.all_tweets.extend(tweets)
        for tweet in tweets:
            tweet.created_at += timedelta(hours=9)

            # replyを判別
            # if tweet.in_reply_to_status_id is not None:
            # print('this tweet is a reply')

            # RTは除去
            if tweet.full_text.startswith('RT'):
                continue
            else:

                # 改行を除去
                s = tweet.full_text.splitlines()
                output_text = ''
                for text_data in s:
                    if text_data != '':
                        output_text += text_data

                # escape ' because syntax error occur when insert into DB
                if "'" in output_text:
                    print(output_text)
                    output_text = output_text.replace("'", "''")
                    print(output_text)

                try:
                    # output to tweets csv file
                    media_url = tweet.entities['media'][0]['media_url_https']

                    self.download_media(media_url)
                    tweets_writer.writerow([tweet.id_str, output_text, str(tweet.favorite_count), str(tweet.retweet_count),
                                           str(tweet.created_at), tweet.in_reply_to_status_id_str,
                                           tweet.entities['media'][0]['id_str'],
                                           str(media_url)])
                except KeyError:
                    # if a tweet doesn't have media , output tweet info except media
                    tweets_writer.writerow(
                        [tweet.id_str, output_text, str(tweet.favorite_count), str(tweet.retweet_count),
                         str(tweet.created_at), tweet.in_reply_to_status_id_str])
                self.num += 1


    def download_media(self, media_url):
        pic_name = media_url.split('/')[-1]
        dst_path = MEDIA_DIR + pic_name
        try:
            with urllib.request.urlopen(media_url) as web_file:
                data = web_file.read()
                with open(dst_path, mode='wb') as local_file:
                    local_file.write(data)
        except urllib.error.URLError as e:
            print(e)
            print(media_url)


# execute
if __name__ == '__main__':
    GetUserInfo().get_tweets()
