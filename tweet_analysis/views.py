from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from tweet_analysis.manipulate_csv import ManipulateCsv
from tweet_analysis.models import AnalysisResult
from django.utils import timezone
from tweet_analysis.get_specific_user_info import GetSpecificUserInfo
from tweet_analysis.set_graph import SetGraph
import matplotlib.pyplot as plt
import pandas as pd

import logging

# todo バグ調査用のロギングのため後で消す
LOGFILE = 'man_debug.log'
logging.basicConfig(filename=LOGFILE,level=logging.DEBUG)

# todo create csv conf py file
INDEX_TWEET_TEXT = 1


# Create your views here.
def index(request):
    context = {}
    return render(request, 'tweet_analysis/index.html', context)


def detail(request):
    """
    csv データをブラウザに表示させる
    :param request:
    :return:
    """
    twitter_usr_id = request.POST['csv_name']

    # twitter apiを使用しcsv出力
    instance = GetSpecificUserInfo(twitter_usr_id)
    ret = instance.main()
    if ret:
        api_result = 'api success'
    else:
        api_result = '存在しないユーザです。'
        context = {
            'api_result': api_result
        }
        return render(request, 'tweet_analysis/detail.html', context)

    # csv_name = csv_name + '.csv'
    csv_name = twitter_usr_id + '.csv'
    instance = ManipulateCsv(csv_name)
    descr = instance.get_df_describe()
    df = instance.get_data_frame()

    context = {
        'mean': str(descr.at['mean', 'favorite']),
        'max': int(descr.at['max', 'favorite']),
        'max_text': df[df['favorite'] == descr.at['max', 'favorite']].iloc[0, INDEX_TWEET_TEXT],
        'api_result': api_result
    }
    return render(request, 'tweet_analysis/detail.html', context)


def tweet_info(request):
    """
    csv データをブラウザに表示させる
    :param request:
    :return:
    """
    twitter_usr_id = request.POST['usr_id']

    # twitter apiを使用しcsv出力
    instance = GetSpecificUserInfo(twitter_usr_id, to_csv=False)
    tweets_list = instance.main()
    if tweets_list:
        api_result = 'api success'
    else:
        api_result = '存在しないユーザまたは、ツイート情報を取得できないユーザです。'
        context = {
            'api_result': api_result,
            'all_tweets_list': tweets_list,
        }
        return render(request, 'tweet_analysis/tweetinfo.html', context)

    instance.output_csv()
    context = {
        # headerの表示に必要なものだけ指定
        'tweet_header': tweets_list[0][1:5],
        'tweets_list': tweets_list[1:],
        'api_result': api_result,
        'usr_id': twitter_usr_id,
        'all_tweets_list': tweets_list,
    }

    # 分析結果を追加
    instance = ManipulateCsv()
    df, desc = instance.convert_list_to_df(tweets_list)
    analysis_context = instance.set_analysis_result(df, desc)
    context.update(analysis_context)

    return render(request, 'tweet_analysis/tweetinfo.html', context)


def register_result(request, tweet_usr_id):
    """
    csvデータをDBに登録する
    :param request:
    :param tweet_usr_id:
    :return:
    """
    csv_name = tweet_usr_id + '.csv'
    instance = ManipulateCsv(csv_name)
    descr = instance.get_df_describe()
    df = instance.get_data_frame()
    max_row = df[df['favorite'] == descr.at['max', 'favorite']]

    value_id_str = max_row.iloc[0, 0]
    value_fv_max_count = descr.at['max', 'favorite']
    value_fv_max_text = max_row.iloc[0, INDEX_TWEET_TEXT]
    value_fv_avg = descr.at['mean', 'favorite']
    value_create_date = timezone.now()

    register_data = AnalysisResult(id_str=value_id_str, fv_max_count=value_fv_max_count,
                                   fv_max_text=value_fv_max_text, fv_avg=value_fv_avg,
                                   create_date=value_create_date, tweet_usr=tweet_usr_id)
    register_data.save()
    analysis_list = AnalysisResult.objects.all()
    context = {
        'id_str': value_id_str,
        'fv_max_count': value_fv_max_count,
        'fv_max_text': value_fv_max_text,
        'fv_avg': value_fv_avg,
        'create_date': value_create_date,
        'analysis_list': analysis_list,
    }

    return render(request, 'tweet_analysis/register_result.html', context)


def analysis(request):
    """
    tweetの情報分析ページを表示する。
    :param request:
    :return:
    """
    all_tweets_list = request.POST['all_tweets_list']

    instance = ManipulateCsv()
    context = instance.convert_list_to_df(all_tweets_list)

    return render(request, 'tweet_analysis/analysis.html', context)


def get_svg(request, usr_id, column1, column2):
    df = pd.read_csv('tweet_analysis/csv/{0}.csv'.format(usr_id))
    graph_data1 = df[column1]
    graph_data2 = df[column2]
    sg_instance = SetGraph(graph_data1, column1, graph_data2, column2)
    svg = sg_instance.main()
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response  # convert plot to SVG

