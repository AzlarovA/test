from django.contrib import admin
from .models import News
# Register your models here.


class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "author", 'content')
    list_display_links = ("title", "author", 'content')


admin.site.register(News, NewsAdmin
)