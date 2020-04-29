# coding:utf-8

import tweepy
from datetime import timedelta
from .tweet_conf import twitterApi
import csv
import traceback
import urllib.request
import urllib.error

CONSUMER_KEY = twitterApi.CONSUMER_KEY
CONSUMER_SECRET = twitterApi.CONSUMER_SECRET
ACCESS_KEY = twitterApi.ACCESS_KEY
ACCESS_SECRET = twitterApi.ACCESS_SECRET

CSV_EXTENSION = '.csv'

# not used path
MEDIA_DIR = '/appl/scripts/media/'


# todo replyを排除
# todo ログを吐く場所
class GetSpecificUserInfo():
    """
    get user's tweets info from twitter and output to csv file
    """
    
    def __init__(self, account):
        self.num = 0  # 取得するツイートを計算する
        # 全ツイートを入れる空のリストを用意
        self.all_tweets = []
        # twitter user account id
        self.account = account

    def main(self):
        """
        get user's tweets from Twitter and output header to csv
        """

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth)

        tweets_file_path = 'tweet_analysis/csv/' + self.account + CSV_EXTENSION
        # tweet_mode='extended'を設定することで、tweetが切れないかつ、画像も取得できる。
        try:
            tweets = api.user_timeline(self.account, count=200, tweet_mode='extended')
        except tweepy.error.TweepError as e:
            print(e)
            # abnormal end
            return False

        # ファイルにツイートを出力。エクセルでの文字化け防止のためBOM付utf8で作成
        with open(tweets_file_path, mode='w', encoding='utf_8_sig')as f:
            tweets_writer = csv.writer(f)
            # header
            tweets_writer.writerow(
                ['id_str', 'tweet_text', 'favorite', 'retweet_count', 'Data', 'in_reply_to_status_id_str', 'media_id',
                 'media_url'])
            self.output_tweet(tweets, tweets_writer)

            # get every 200 tweets
            while len(tweets) > 0:
                # tweet_mode='extended'を設定することで、tweetが切れないかつ、画像も取得できる。
                tweets = api.user_timeline(self.account, count=200, max_id=self.all_tweets[-1].id - 1,
                                           tweet_mode='extended')
                self.output_tweet(tweets, tweets_writer)
                print(self.num, 'ツイート表示しました。')

        # normal end
        return True

    def output_tweet(self, tweets, tweets_writer):
        """
        output tweets to csv file
        """

        self.all_tweets.extend(tweets)
        for tweet in tweets:
            tweet.created_at += timedelta(hours=9)

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
                    output_text = output_text.replace("'", "''")

                try:
                    # output to tweets csv file
                    media_url = tweet.entities['media'][0]['media_url_https']

                    # 画像のDLは重い処理のため省略
                    # self.download_media(media_url)
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
        """
        画像DL処理は重いため採用を保留
        :param media_url:
        :return:
        """
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

