from django.urls import path
from .views import news_list

app_name = 'articles'

urlpatterns = [
    path('', news_list, name='news_list'),
    # path('news/<slug:slug>/', article_detail, name='movie_detail'),
    # path('search/', search, name='search'),
]