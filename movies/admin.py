from django.contrib import admin
from .models import Movie, Genre, ToShowMainpage
# Register your models here.


class MovieAdmin(admin.ModelAdmin):
    list_display = ("name", "release_date", 'rating', 'genre_list')
    list_display_links = ("name", "release_date", 'rating', 'genre_list')

    def genre_list(self, obj):
        return ", ".join([str(genre) for genre in obj.genre.all()])
    genre_list.short_description = 'Genre'


class GenreAdmin(admin.ModelAdmin):
    list_display = ["genre"]


admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(ToShowMainpage)