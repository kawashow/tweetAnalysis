from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from tweet_analysis.manipulate_csv import ManipulateCsv
from tweet_analysis.models import AnalysisResult
from django.utils import timezone

# todo create csv conf py file
INDEX_TWEET_TEXT = 1


# Create your views here.
def index(request):
    template = loader.get_template('tweet_analysis/index.html')
    context = {}
    return render(request, 'tweet_analysis/index.html', context)


def detail(request, csv_name):
    """
    csv データをブラウザに表示させる
    :param request:
    :param csv_name:
    :return:
    """
    csv_name = csv_name + '.csv'
    instance = ManipulateCsv(csv_name)
    descr = instance.get_df_describe()
    df = instance.get_data_frame()
    template = loader.get_template('tweet_analysis/detail.html')
    context = {
        'mean': str(descr.at['mean', 'favorite']),
        'max': int(descr.at['max', 'favorite']),
        'max_text': df[df['favorite'] == descr.at['max', 'favorite']].iloc[0, INDEX_TWEET_TEXT],
    }
    return render(request, 'tweet_analysis/detail.html', context)


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
