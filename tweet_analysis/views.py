from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from tweet_analysis.manipulate_csv import ManipulateCsv

# Create your views here.
def index(request):
    csv_name = 'muni_gurume.csv'
    instance = ManipulateCsv(csv_name)
    descr = instance.get_df_describe()
    df = instance.get_data_frame()
    template = loader.get_template('tweet_analysis/index.html')
    context = {
        'mean': str(descr.at['mean','favorite']),
        'max' : df[df['favorite'] == descr.at['max', 'favorite']].loc[:,'tweet_text'],
    }
    return render(request, 'tweet_analysis/index.html', context)

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)
