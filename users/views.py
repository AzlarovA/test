import random
import string
from PIL import Image
from io import BytesIO
from .forms import UsersForm, LoginForm, UpdateUserForm, EmailConfirmationForm
from .models import Users, UserSavedMovies, UserAskedQnA
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from decimal import Decimal, ROUND_HALF_UP
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models import Avg, Count
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
# Create your views here.


def generate_random_code(length=6):
    return ''.join(random.choices(string.digits, k=length))


def users_form_view(request):
    if request.method == 'POST':
        form = UsersForm(request.POST, request.FILES)
        if form.is_valid():
            request.session['user_data'] = form.cleaned_data

            code = generate_random_code()
            request.session['email_confirmation_code'] = code


            current_site = get_current_site(request)


            mail_subject = 'Activate your account.'
            message = render_to_string('authentication/activation_email.html', {
                'user': form.cleaned_data['username'],
                'domain': current_site.domain,
                'code': code,
            })


            send_mail(mail_subject, message, 'webmaster@mydomain.com', [form.cleaned_data['email']])

            confirmation_form = EmailConfirmationForm(request.POST)

            return render(request, 'authentication/registration.html',
                          {'confirmation_form': confirmation_form, 'code_sent': True})
    else:
        form = UsersForm()

    return render(request, 'authentication/registration.html', {'form': form})


def confirm_email(request):
    if request.method == 'POST':
        form = EmailConfirmationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if code == request.session.get('email_confirmation_code'):
                user_data = request.session.get('user_data')
                if user_data:
                    user = User.objects.create_user(
                        username=user_data['username'],
                        email=user_data['email'],
                        password=user_data['password1']
                    )
                    user.save()
                    user_profile = Users(
                        user=user,
                        nickname=user_data['nickname'],
                        email=user_data['email'],
                        email_confirmed = True
                    )
                    user_profile.save()
                    return redirect('login')
            else:
                return render(request, 'authentication/registration.html', {'confirmation_form': EmailConfirmationForm(), 'code_sent': True, 'invalid_code': True})
    else:
        form = EmailConfirmationForm()

    return render(request, 'authentication/registration.html', {'confirmation_form': form})


def users_login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['user_id'] = user.id
                return redirect('user:user_page')
    else:
        form = LoginForm()
    return render(request, 'authentication/login.html', {'form': form})


def users_logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'authentication/logout.html')


def user_page(request):
    if request.user.is_authenticated:
        user = get_object_or_404(Users, user=request.user)
        context = {
            'user': user,
        }
        user_saved_movies = UserSavedMovies.objects.filter(user=user).first()
        if user_saved_movies:
            saved_movies_verbose_name = UserSavedMovies._meta.get_field('saved_movies').verbose_name
            watched_movies_verbose_name = UserSavedMovies._meta.get_field('watched_movies').verbose_name
            dropped_movies_verbose_name = UserSavedMovies._meta.get_field('dropped_movies').verbose_name
            favorite_movies_verbose_name = UserSavedMovies._meta.get_field('favorite_movies').verbose_name
            movie_lists = [
                (saved_movies_verbose_name, user_saved_movies.saved_movies.all()),
                (watched_movies_verbose_name, user_saved_movies.watched_movies.all()),
                (dropped_movies_verbose_name, user_saved_movies.dropped_movies.all()),
                (favorite_movies_verbose_name, user_saved_movies.favorite_movies.all()),
            ]
            context['movie_lists'] = movie_lists

        user_asked_qna = UserAskedQnA.objects.filter(user=user).first()
        if user_asked_qna:
            qna_lists = {
                'questions': user_asked_qna.ur_ques.all(),
                'answers': user_asked_qna.ur_ans.all(),
            }
            context['qna_lists'] = qna_lists

        return render(request, 'user_profile/mainpage.html', context)
    else:
        return redirect('login')


def user_profile(request, username):
    user = get_object_or_404(Users, user__username=username)
    context = {
        'user': user,
    }

    user_saved_movies = UserSavedMovies.objects.filter(user=user).first()
    if user_saved_movies:
        saved_movies_verbose_name = UserSavedMovies._meta.get_field('saved_movies').verbose_name
        watched_movies_verbose_name = UserSavedMovies._meta.get_field('watched_movies').verbose_name
        dropped_movies_verbose_name = UserSavedMovies._meta.get_field('dropped_movies').verbose_name
        favorite_movies_verbose_name = UserSavedMovies._meta.get_field('favorite_movies').verbose_name
        movie_lists = [
            (saved_movies_verbose_name, user_saved_movies.saved_movies.all()),
            (watched_movies_verbose_name, user_saved_movies.watched_movies.all()),
            (dropped_movies_verbose_name, user_saved_movies.dropped_movies.all()),
            (favorite_movies_verbose_name, user_saved_movies.favorite_movies.all()),
        ]
        context['movie_lists'] = movie_lists

    user_asked_qna = UserAskedQnA.objects.filter(user=user).first()
    if user_asked_qna:
        qna_lists = {
            'questions': user_asked_qna.ur_ques.all(),
            'answers': user_asked_qna.ur_ans.all(),
        }
        context['qna_lists'] = qna_lists

    return render(request, 'user_profile/mainpage.html', context)


def user_edit(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(Users, user=user)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            login(request, user)
            return redirect('user:user_page')
    else:
        form = UpdateUserForm(instance=user_profile)
    context = {
        'form': form,
        "user": user_profile
    }
    return render(request, 'user_profile/user_redactor.html', context)


def update_image(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(Users, user=user)
    if request.method == 'POST':
        image = request.FILES.get('image')
        image = Image.open(image)
        crop_x = round(float(request.POST.get('crop_x')))
        crop_y = round(float(request.POST.get('crop_y')))
        crop_width = round(float(request.POST.get('crop_width')))
        crop_height = round(float(request.POST.get('crop_height')))
        cropped_image = image.crop((crop_x, crop_y, crop_x + crop_width, crop_y + crop_height))
        image_io = BytesIO()
        cropped_image.save(image_io, format='JPEG')
        user_profile.image.delete(save=False)
        user_profile.image.save(f'{username}.jpeg', ContentFile(image_io.getvalue()))
        return redirect('user:user_profile', username=username)
    else:
        return render(request, 'update_image.html', {'user': user_profile})


@require_POST
@login_required
def rate_user(request, username):
    # Get rating from POST data
    rating = request.POST.get('rating')
    if not rating:
        return JsonResponse({'error': 'Invalid rating'})

    rating = Decimal(rating).quantize(Decimal('0.00001'), rounding=ROUND_HALF_UP)

    rated_user = Users.objects.filter(user__username=username).first()
    if not rated_user:
        return JsonResponse({'error': 'User not found'})

    rated_user.rating = rating
    rated_user.save()

    average_rating = Users.objects.filter(user__username=username).aggregate(Avg('rating'))['rating__avg']
    rating_count = Users.objects.filter(user__username=username).aggregate(Count('rating'))['rating__count']

    return JsonResponse({'average_rating': average_rating, 'rating_count': rating_count})
