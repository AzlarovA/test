from django.contrib import admin
from .models import Subs, MainPage
# Register your models here.


class SubsAdmin(admin.ModelAdmin):
    list_display = ("subscription_1", "subscription_2", 'subscription_3', 'subscription_4')
    list_display_links = ("subscription_1", "subscription_2", 'subscription_3', 'subscription_4')


admin.site.register(Subs, SubsAdmin)
admin.site.register(MainPage)