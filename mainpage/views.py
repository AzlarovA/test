from django.shortcuts import render
from .models import MainPage, Banner
from subscriptions.models import Subs
from django.http import HttpResponseNotFound
from django.template import loader
# Create your views here.


def passs(request):
    main = MainPage.objects.filter(pk=1).first()
    subs = Subs.objects.filter(pk=1).first()
    banner = Banner.objects.filter(pk=1).first()
    user = request.user
    template_ = 'mainpage\mainpage.html'
    context = {
        "main": main,
        "subs": subs,
        "banner": banner,
        "user":user
    }
    return render(request, template_name=template_, context=context)
