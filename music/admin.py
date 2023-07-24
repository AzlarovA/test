from django.contrib import admin
from .models import Music, Genre, ToShowMainpage, Author
# Register your models here.


class MusicAdmin(admin.ModelAdmin):
    list_display = ("title", "author", 'content', 'genre_list')
    list_display_links = ("title", "author", 'content', 'genre_list')

    def genre_list(self, obj):
        return ", ".join([str(genre) for genre in obj.genre.all()])
    genre_list.short_description = 'Genre'


class GenreAdmin(admin.ModelAdmin):
    list_display = ["genre"]


admin.site.register(Music, MusicAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(ToShowMainpage)
admin.site.register(Author)