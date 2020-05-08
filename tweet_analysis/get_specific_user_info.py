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
TWEET_CSV_HEADER = ['id_str', 'tweet_text', 'favorite', 'RT', 'tweet_date', 'in_reply_to_status_id_str',
                    'media_id',
                    'media_url']

# not used path
MEDIA_DIR = '/appl/scripts/media/'


# todo replyを排除
# todo ログを吐く場所
class GetSpecificUserInfo():
    """
    get user's tweets info from twitter and output to csv file.
    If to_csv is False, return tweets list.
    """

    def __init__(self, account, to_csv=True):
        """
        :param account: tweeter account name
        :param to_csv:  output to csv flag
        """
        # 取得するツイートを計算する
        self.num = 0
        # 全ツイートを入れる空のリストを用意
        self.all_tweets = []
        # twitter user account id
        self.account = account
        # 出力用のリスト
        self.output_list = []
        # output to csv flag
        self.to_csv = to_csv

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

    def set_tweet(self, tweets):
        """
        tweetの情報を取捨選択、整形し、リストにセットする。
        :param tweets: tweet200件の情報
        :return:
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

                # escape ' because syntax error occur when using pandas
                if "'" in output_text:
                    output_text = output_text.replace("'", "''")

                try:
                    # output to tweets csv file
                    media_url = tweet.entities['media'][0]['media_url_https']

                    # 画像のDLは重い処理のため省略
                    # self.download_media(media_url)
                    self.output_list.append(
                        [tweet.id_str, output_text, tweet.favorite_count, tweet.retweet_count,
                         str(tweet.created_at), tweet.in_reply_to_status_id_str,
                         tweet.entities['media'][0]['id_str'],
                         str(media_url)])

                except KeyError:
                    # if a tweet doesn't have media , output tweet info except media
                    self.output_list.append(
                        [tweet.id_str, output_text, tweet.favorite_count, tweet.retweet_count,
                         str(tweet.created_at), tweet.in_reply_to_status_id_str, '', ''])
                self.num += 1

    def output_csv(self):
        """
        output tweets list to csv file
        :return:
        """
        tweets_file_path = 'tweet_analysis/csv/' + self.account + CSV_EXTENSION
        # ファイルにツイートを出力。エクセルでの文字化け防止のためBOM付utf8で作成
        with open(tweets_file_path, mode='w', encoding='utf_8_sig')as f:
            tweets_writer = csv.writer(f)
            for tweet_row in self.output_list:
                tweets_writer.writerow(tweet_row)

    def main(self):
        """
        get user's tweets from Twitter and output header to csv.
        If to_csv is False, return tweets list.
        :return: normal end: True
                 abnormal end: False
        """

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth)

        # tweet_mode='extended'を設定することで、tweetが切れないかつ、画像も取得できる。
        try:
            tweets = api.user_timeline(self.account, count=200, tweet_mode='extended')
        except tweepy.error.TweepError as e:
            print(e)
            # abnormal end
            return False

        # header
        self.output_list.append(TWEET_CSV_HEADER)

        # 直近200ツイートの情報をリストにセット
        self.set_tweet(tweets)

        # get every 200 tweets
        while len(tweets) > 0:
            # tweet_mode='extended'を設定することで、tweetが切れないかつ、画像も取得できる。
            tweets = api.user_timeline(self.account, count=200, max_id=self.all_tweets[-1].id - 1,
                                       tweet_mode='extended')
            self.set_tweet(tweets)
            print(self.num, 'ツイート表示しました。')

        # csv出力フラグがあれば、ファイルにツイートを出力。それ以外はtweetリストを返す。
        if self.to_csv:
            self.output_csv()
            # normal end
            return True
        else:
            return self.output_list
