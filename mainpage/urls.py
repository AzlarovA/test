from django.urls import path
from .views import passs

app_name = 'main'

urlpatterns = [
    path("", passs, name="mainpage_view"),
]