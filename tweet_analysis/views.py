from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from tweet_analysis.manipulate_csv import ManipulateCsv
from tweet_analysis.models import AnalysisResult
from django.utils import timezone

INDEX_TWEET_TEXT = 1


# Create your views here.
def index(request):
    template = loader.get_template('tweet_analysis/index.html')
    context = {}
    return render(request, 'tweet_analysis/index.html', context)


def detail(request, csv_name):
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


def register_result(request, csv_name):
    csv_name = csv_name + '.csv'
    instance = ManipulateCsv(csv_name)
    descr = instance.get_df_describe()
    df = instance.get_data_frame()
    max_row = df[df['favorite'] == descr.at['max', 'favorite']]
    register_data = AnalysisResult(id_str=max_row.iloc[0, 0], fv_max_count=descr.at['max', 'favorite'],
                                   fv_max_text=max_row.iloc[0, INDEX_TWEET_TEXT], fv_avg=descr.at['mean', 'favorite'],
                                   create_date=timezone.now())
    register_data.save()

    template = loader.get_template('tweet_analysis/register_result.html')
    context = {}
    return render(request, 'tweet_analysis/register_result.html', context)
