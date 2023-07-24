from django.db import models
from django.urls import reverse_lazy
from transliterate.exceptions import LanguagePackNotFound
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from transliterate import translit
from langdetect import detect
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Movie(models.Model):
    name = models.CharField(verbose_name=_('Наименование'), max_length=100)
    director = models.CharField(verbose_name=_('Режиссер'), max_length=100)
    description = models.TextField(verbose_name=_('Описание'))
    rating = models.DecimalField(verbose_name=_('Рейтинг'), max_digits=5, decimal_places=2, default=False, validators=[MinValueValidator(0), MaxValueValidator(10)])
    budget = models.IntegerField(verbose_name=_('Бюджет'), default=False)
    release_date = models.DateField(verbose_name=_('Дата релиза'))
    genre = models.ManyToManyField('Genre', verbose_name=_('Жанры'))
    on_screens = models.BooleanField(verbose_name=_('На экранах '), default=False)
    image = models.ImageField(verbose_name='Постер', upload_to='static/posters')
    video_file = models.FileField(verbose_name='Видеофайл', upload_to='static/videos', blank=True)
    active = models.BooleanField(verbose_name=_('Показать'), default=False, blank=True)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        lang = detect(self.name)
        try:
            self.slug = slugify(translit(self.name, lang, reversed=True))
        except LanguagePackNotFound:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Фильм")
        verbose_name_plural = _("Фильмы")
        ordering = ("name", "release_date", 'rating')

    def __str__(self) -> str:
        return f"{self.name}"


class Genre(models.Model):
    genre = models.CharField(verbose_name=_('Жанр'), max_length=50)
    slug = models.SlugField(blank=True)

    def validate_unique(self, *args, **kwargs):
        if Genre.objects.filter(genre=self.genre).exists():
            raise ValidationError('Такое объект уже существует')

    def save(self, *args, **kwargs):
        self.genre = self.genre.lower()
        lang = detect(self.genre)
        try:
            self.slug = slugify(translit(self.genre, lang, reversed=True))
        except LanguagePackNotFound:
            self.slug = slugify(self.genre)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Жанр")
        verbose_name_plural = _("Жанры")
        ordering = ["genre"]

    def __str__(self) -> str:
        return f"{self.genre}"


class ToShowMainpage(models.Model):
    title = models.ForeignKey(Movie, verbose_name='Название', on_delete=models.CASCADE, related_name="title")
    short_description = models.CharField(verbose_name='Короткое описание', max_length=200, blank=True)
    image = models.ForeignKey(Movie, verbose_name='Фото', on_delete=models.CASCADE, related_name="images")
    video = models.FileField(verbose_name='Видеофайл', upload_to='movies/videos/main', blank=True)
    popular = models.BooleanField(verbose_name='Что смотрят')
    slug = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Для глав. страницы")
        verbose_name_plural = _("Для глав. страницы")

    def __str__(self) -> str:
        return f"{self.title}"
