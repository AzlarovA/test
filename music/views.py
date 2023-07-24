from django.shortcuts import render
from .forms import SearchFormDB
from .models import Music, Genre, ToShowMainpage
from django.shortcuts import render, get_object_or_404
from django.db.models import Func, Q, Value
# Create your views here.


class Replace(Func):
    function = 'REPLACE'


def music_page(request):
    mainp = ToShowMainpage.objects.filter(popular=False)
    popular = ToShowMainpage.objects.filter(popular=True)
    template_ = 'music/mainpage.html'
    context = {
        "mains": mainp,
        "popular": popular,
    }
    return render(request=request, template_name=template_, context=context)


def music_detail(request, slug):
    music = get_object_or_404(Music, slug=slug)
    context = {
        'music': music
    }
    return render(request, 'music/music_detail.html', context)


def genre_detail(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    context = {
        'genre': genre
    }
    return render(request, 'music/genre_detail.html', context)


def search(request):
    query = request.GET.get('search')
    form = SearchFormDB()
    results = search_music(query)
    context = {
        'form': form,
        'results': results
    }
    return render(request, 'music/search_results.html', context=context)


def detail_search(request):
    template_name = 'music/search_results.html'
    form = SearchFormDB(request.GET or None)
    context = {
        'form': form
    }
    if form.is_valid():
        title = form.cleaned_data.get('title')
        author = form.cleaned_data.get('author')
        genre = form.cleaned_data.get('genre')
        release_date_from = request.GET.get('release-date-from')
        release_date_to = request.GET.get('release-date-to')

        results = Music.objects.all()

        query = request.session.get('query')
        if title:
            results = search_music(query)
        if title:
            results = results.filter(name__icontains=title)
        if author:
            results = results.filter(author__icontains=author)
        if genre:
            results = results.filter(genre__in=genre)
        if release_date_from:
            results = results.filter(release_date__year__gte=release_date_from)
        if release_date_to:
            results = results.filter(release_date__year__lte=release_date_to)

        context['results'] = results

    return render(request, template_name=template_name, context=context)


def search_music(query):
    query = query.replace(' ', '').replace('.', '').replace(',', '')
    title_query = Replace('title', Value(' '), Value(''))
    title_query = Replace(title_query, Value('.'), Value(''))
    title_query = Replace(title_query, Value(','), Value(''))
    author_query = Replace('author', Value(' '), Value(''))
    author_query = Replace(author_query, Value('.'), Value(''))
    author_query = Replace(author_query, Value(','), Value(''))
    results = Music.objects.annotate(
        title_query=title_query,
        author_query=author_query
    ).filter(
        Q(title_query__icontains=query) | Q(author_query__icontains=query)
    )
    return results