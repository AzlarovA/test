from django.urls import path
from .views import contacts_page

app_name = 'contacts'

urlpatterns = [
    path('', contacts_page, name='contacts_page'),
]