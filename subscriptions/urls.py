from django.urls import path
from .views import subs_page, payment_view, payment_processing_view

app_name = 'subscription'

urlpatterns = [
    path('', subs_page, name='subs_page'),
    path('subscription/payment/<str:subscription_type>/<str:subscription_description>/<str:price>/', payment_view, name='payment_view'),
    path('payment/', payment_processing_view, name='payment_processing_view'),
]
