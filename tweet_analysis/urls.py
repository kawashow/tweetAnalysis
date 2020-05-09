from django.urls import path
from . import views

app_name = 'tweet_analysis'
urlpatterns = [
    path('', views.index, name='index'),
    path('tweets_detail/', views.detail, name='detail'),
    path('tweetinfo/', views.tweet_info, name='tweetinfo'),
    path('<str:tweet_usr_id>/register_result/', views.register_result, name='register_result'),
    path('analysis/', views.analysis, name='analysis'),
    # グラフ描画
    path('tweet_analysis/plot/<str:usr_id>/<str:column1>/<str:column2>', views.get_svg, name='plot'),

]
