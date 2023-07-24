from django.shortcuts import render
from .models import News
# Create your views here.


def news_list(request):
    articles = News.objects.all().order_by('-created_at')
    template_ = 'articles\mainpage.html'
    context = {
        "articles": articles
    }
    return render(request, template_name=template_, context=context)