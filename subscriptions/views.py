from .models import Subs, MainPage
from movies.models import ToShowMainpage
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect, resolve_url
from .forms import SubscriptionForm, SUBSCRIPTION_DESCRIPTIONS
from users.models import Users
import stripe
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY


def subs_page(request):
    photo = MainPage.objects.all()
    popular = ToShowMainpage.objects.filter(popular=True)
    subs = Subs.objects.first()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url('/accounts/login/')
            return redirect_to_login(path, resolved_login_url, REDIRECT_FIELD_NAME)

        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription_type = form.cleaned_data['subscription_type']
            subscription_description = SUBSCRIPTION_DESCRIPTIONS[subscription_type]
            if subscription_type == 'monthly':
                price = subs.subscription_1
            elif subscription_type == '3-months':
                price = subs.subscription_2
            elif subscription_type == '6-months':
                price = subs.subscription_3
            elif subscription_type == 'yearly':
                price = subs.subscription_4
            return redirect('subscription:payment_view', subscription_type=subscription_type, subscription_description=subscription_description, price=price)
    else:
        form = SubscriptionForm()

    context = {
        'form': form,
        "photo": photo,
        "popular": popular,
        "subs": subs,
    }
    return render(request, 'purchase/subscription_page.html', context)


def payment_view(request, subscription_type, subscription_description, price):
    user_profile = Users.objects.get(user=request.user)
    context = {
        'subscription_type': subscription_type,
        'subscription_description': subscription_description,
        'price': price,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'username': request.user.username,
        'email': request.user.email,
        'SUBSCRIPTION_DESCRIPTIONS': SUBSCRIPTION_DESCRIPTIONS,
        'user_profile': user_profile,
    }
    return render(request, 'purchase/payment_page.html', context)


def payment_processing_view(request):
    if request.method == 'POST':
        subscription_type = request.POST.get('subscription_type')
        user_profile = Users.objects.get(user=request.user)
        user_profile.premium = True
        print(subscription_type)
        if subscription_type == 'monthly':
            user_profile.premium_expiry_date = timezone.now() + timedelta(seconds=5)
            print("5")
        elif subscription_type == '3-months':
            user_profile.premium_expiry_date = timezone.now() + timedelta(seconds=7)
            print("7")
        elif subscription_type == '6-months':
            user_profile.premium_expiry_date = timezone.now() + timedelta(seconds=9)
            print("9")
        elif subscription_type == 'yearly':
            user_profile.premium_expiry_date = timezone.now() + timedelta(seconds=11)
            print("11")
        print("ya tut")
        user_profile.save()

        return redirect('main:mainpage_view')
    else:
        return redirect('subscription:payment_view')

