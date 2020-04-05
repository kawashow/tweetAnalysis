from django.shortcuts import render
from django.http import HttpResponse
from tweet_analysis.manipulate_csv import ManipulateCsv

# Create your views here.
def index(request):
    csv_name = 'muni_gurume'
    instance = ManipulateCsv(csv_name)
    data_set = instance.get_data_set()
    return HttpResponse("Hello, world. You're at the polls index."
                        "<br>"+
                        str(*data_set))
