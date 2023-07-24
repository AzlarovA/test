from django.urls import path
from .views import movie_page, movie_detail, genre_detail, search, detail_search, save_movie, genre_list

app_name = 'movies'

urlpatterns = [
    path('', movie_page, name='movie_page'),
    path('movie/<slug:slug>/', movie_detail, name='movie_detail'),
    path('safe/<slug:slug>/', save_movie, name='save_movie'),

    path('search/', search, name='search'),

    path('genres/', genre_list, name='genre_list'),
    path('genre/<slug:slug>/', genre_detail, name='genre_detail'),
    path('detail-search/', detail_search, name='detail_search'),
]
