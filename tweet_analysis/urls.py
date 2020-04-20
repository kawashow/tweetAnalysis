from django.urls import path
from . import views

app_name = 'tweet_analysis'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:csv_name>/', views.detail, name='detail'),
    path('<str:csv_name>/register_result/', views.register_result, name='register_result'),
]
