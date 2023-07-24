from django.shortcuts import render, redirect, resolve_url
from .forms import SearchFormDB
from .models import Movie, Genre, ToShowMainpage
from django.shortcuts import render, get_object_or_404
from django.db.models import Func, Q, Value
from users.models import UserSavedMovies, Users
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.paginator import Paginator
from fuzzywuzzy import fuzz
# Create your views here.


class Replace(Func):
    function = 'REPLACE'


def movie_page(request):
    mainp = ToShowMainpage.objects.filter(popular=False)
    popular = ToShowMainpage.objects.filter(popular=True)
    template_ = 'movies/mainpage.html'
    context={
        "mains": mainp,
        "popular": popular,
    }
    return render(request=request, template_name=template_, context=context)


def movie_detail(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    if request.user.is_authenticated:
        users_object = Users.objects.get(user=request.user)
        user_saved_movies = UserSavedMovies.objects.filter(user=users_object).first()
        premium = users_object.premium
    else:
        user_saved_movies = None
        premium = False
    context = {
        'movie': movie,
        'user_saved_movies': user_saved_movies,
        'premium': premium,
    }
    return render(request, 'movies/movie_detail.html', context)


def save_movie(request, slug):
    if request.method == "POST":
        if request.user.is_authenticated:
            users_object = Users.objects.get(user=request.user)
            movie = get_object_or_404(Movie, slug=slug)
            status = request.POST.get("status")
            user_saved_movies, created = UserSavedMovies.objects.get_or_create(user=users_object)
            #
            user_saved_movies.saved_movies.remove(movie)
            user_saved_movies.watched_movies.remove(movie)
            user_saved_movies.dropped_movies.remove(movie)
            user_saved_movies.favorite_movies.remove(movie)
            #
            if status == "saved":
                user_saved_movies.saved_movies.add(movie)
            elif status == "watched":
                user_saved_movies.watched_movies.add(movie)
            elif status == "dropped":
                user_saved_movies.dropped_movies.add(movie)
            elif status == "favorite":
                user_saved_movies.favorite_movies.add(movie)
            return redirect("movies:movie_detail", slug=slug)
        else:
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url('/accounts/login/')
            return redirect_to_login(path, resolved_login_url, REDIRECT_FIELD_NAME)


def genre_list(request):
    genres = Genre.objects.all()
    context = {
        'genres': genres,
    }
    return render(request, 'movies/category_page.html', context)


def genre_detail(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    movies = genre.movie_set.all()
    paginator = Paginator(movies, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'genre': genre,
        'page_obj': page_obj,
    }
    return render(request, 'movies/genre_detail.html', context)


def search(request):
    query = request.GET.get('search')
    form = SearchFormDB()
    results = search_movies(query)
    context = {
        'form': form,
        'results': results
    }
    return render(request, 'movies/search_results.html', context=context)


def detail_search(request):
    template_name = 'movies/search_results.html'
    form = SearchFormDB(request.GET or None)
    context = {
        'form': form
    }
    if form.is_valid():
        name = form.cleaned_data.get('name')
        director = form.cleaned_data.get('director')
        genre = form.cleaned_data.get('genre')
        rating_from = request.GET.get('rating_from')
        rating_to = request.GET.get('rating_to')
        release_date_from = request.GET.get('release_year_from')
        release_date_to = request.GET.get('release_year_to')
        query = request.session.get('query')
        print(name, director, genre)
        print(query)
        print(f"rating_from: {rating_from}, rating_to: {rating_to}, release_date_from: {release_date_from}, release_date_to: {release_date_to}")

        if query:
            print(f"rating_from: {rating_from}, rating_to: {rating_to}, release_date_from: {release_date_from}, release_date_to: {release_date_to}")
            results = search_movies(query, rating_from, rating_to, release_date_from, release_date_to)
        else:
            results = Movie.objects.all()
        if name:
            print("nameeee")
            results = results.filter(name__icontains=name)
        if director:
            results = results.filter(director__icontains=director)
        if genre:
            results = results.filter(genre__in=genre)
        print(results)
        paginator = Paginator(results, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

    return render(request, template_name=template_name, context=context)


def search_movies(query, rating_from=None, rating_to=None, release_date_from=None, release_date_to=None):
    results = []
    threshold = 50
    query = query.lower()
    for movie in Movie.objects.all():
        name_similarity = fuzz.partial_ratio(query, movie.name.lower())
        director_similarity = fuzz.partial_ratio(query, movie.director.lower())
        if name_similarity > threshold or director_similarity > threshold:
            results.append(movie)

    if rating_from:
        print(f"Filtering by rating_from: {rating_from}")
        results = [movie for movie in results if movie.rating >= rating_from]
    if rating_to:
        results = [movie for movie in results if movie.rating <= rating_to]
    if release_date_from:
        results = [movie for movie in results if movie.release_date.year >= release_date_from]
    if release_date_to:
        results = [movie for movie in results if movie.release_date.year <= release_date_to]

    return results



