from django.urls import path
from .views import music_page, music_detail, search, genre_detail, detail_search

app_name = 'music'

urlpatterns = [
    path('', music_page, name='music_page'),
    path('music/<slug:slug>/', music_detail, name='movie_detail'),
    path('search/', search, name='search'),
    path('genre/', genre_detail, name='genre_detail'),
    path('detail-search/', detail_search, name='detail_search'),
]