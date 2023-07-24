from django.contrib import admin
from .models import Users, UserSavedMovies, UserAskedQnA, Notification
# Register your models here.


class UsersAdmin(admin.ModelAdmin):
    list_display = ("user", "email",)
    list_display_links = ("user", "email",)


admin.site.register(Users, UsersAdmin)
admin.site.register(UserSavedMovies)
admin.site.register(UserAskedQnA)
admin.site.register(Notification)