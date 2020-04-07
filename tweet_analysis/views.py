from django.shortcuts import render
from django.http import HttpResponse
from tweet_analysis.manipulate_csv import ManipulateCsv

# Create your views here.
def index(request):
    csv_name = 'muni_gurume.csv'
    instance = ManipulateCsv(csv_name)
    descr = instance.get_df_describe()
    df = instance.get_data_frame()
    result_text = 'あHello. Tweet analysis result below.<br>' \
                  'favorite mean:{0}<br>' \
                  'favorite max:{1}'.format(descr.at['mean','favorite'],df[df['favorite'] == descr.at['max', 'favorite']].loc[:,'tweet_text'])

    return HttpResponse(result_text)
