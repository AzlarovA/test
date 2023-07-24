from django.urls import path
from .views import user_page, user_profile, user_edit, update_image, confirm_email, rate_user

app_name = 'user'

urlpatterns = [
    path('', user_page, name='user_page'),
    path('confirm_email/', confirm_email, name="confirm_email"),
    path('<str:username>/', user_profile, name='user_profile'),
    path('edit/<str:username>/', user_edit, name='user_edit'),
    path('update-image/<str:username>/', update_image, name='update_image'),
    path('rate/<str:username>/', rate_user, name='rate_user'),
]
