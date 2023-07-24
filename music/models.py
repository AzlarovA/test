from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from transliterate import translit
from langdetect import detect
# Create your models here.


class Music(models.Model):
    title = models.CharField(verbose_name=_('Наименование'), max_length=100, blank=False)
    author = models.ForeignKey("Author",on_delete=models.CASCADE, verbose_name=_('Певец'), max_length=100)
    created_at = models.DateTimeField(verbose_name=_('Дата выпуска'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Дата обновления'), auto_now=True)
    content = models.TextField(verbose_name=_('Тема'))
    genre = models.ManyToManyField('Genre', verbose_name=_('Жанры'))
    slug = models.SlugField(unique=True, blank=True)
    active = models.BooleanField(verbose_name=_('Показать'))
    image = models.ImageField(verbose_name=_('Изображение'), upload_to='music/album/')
    files = models.FileField(verbose_name=_('Файл'), upload_to='music/music/', blank=True)

    def save(self, *args, **kwargs):
        self.title = self.title.capitalize()
        self.content = self.content.capitalize()
        lang = detect(self.title)
        self.slug = slugify(translit(self.title, lang, reversed=True))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Музыка")
        verbose_name_plural = _("Музыки")
        ordering = ("title", "author", 'content')

    def __str__(self) -> str:
        return f"{self.title}"


class Genre(models.Model):
    genre = models.CharField(verbose_name=_('Жанр'), max_length=50)
    slug = models.SlugField(unique=True, blank=True)

    def validate_unique(self, *args, **kwargs):
        if Genre.objects.filter(genre=self.genre).exists():
            raise ValidationError('Такое объект уже существует')

    def save(self, *args, **kwargs):
        self.genre = self.genre.lower()
        lang = detect(self.genre)
        self.slug = slugify(translit(self.genre, lang, reversed=True))
        super(Genre, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Жанр")
        verbose_name_plural = _("Жанры")
        ordering = ["genre"]

    def __str__(self) -> str:
        return f"{self.genre}"


class ToShowMainpage(models.Model):
    title = models.ForeignKey(Music, verbose_name=_('Название'), on_delete=models.CASCADE, related_name="name")
    short_description = models.CharField(verbose_name=_('Короткое описание'), max_length=200, blank=True)
    image = models.ForeignKey(Music, verbose_name=_('Фото'), on_delete=models.CASCADE, related_name="images")
    video = models.FileField(verbose_name=_('Видеофайл'), upload_to='movies/videos/main', blank=True)
    popular = models.BooleanField(verbose_name=_('Что смотрят'))
    slug = models.ForeignKey(Music, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Для глав. страницы")
        verbose_name_plural = _("Для глав. страницы")

    def __str__(self) -> str:
        return f"{self.title}"


class Author(models.Model):
    name = models.CharField(verbose_name=_('Испольнитель'), max_length=100)
    birth_date = models.DateField(verbose_name=_('Дата рождения'), null=True, blank=True)
    bio = models.TextField(verbose_name=_('Биография'), blank=True)
    group = models.CharField(verbose_name=_('Группа'), blank=True, max_length=100)
    image = models.ImageField(verbose_name=_('Изображение'), upload_to='music/author/')

    class Meta:
        verbose_name = _("Испольнитель")
        verbose_name_plural = _("Испольнители")

    def __str__(self):
        return self.name