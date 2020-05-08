from django.urls import path
from . import views

app_name = 'tweet_analysis'
urlpatterns = [
    path('', views.index, name='index'),
    path('tweets_detail/', views.detail, name='detail'),
    path('tweetinfo/', views.tweetinfo, name='tweetinfo'),
    path('<str:tweet_usr_id>/register_result/', views.register_result, name='register_result'),
    path('analysis/', views.analysis, name='analysis'),
]
