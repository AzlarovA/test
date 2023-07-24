from django.db import models
from slugify import slugify
from transliterate import translit, get_available_language_codes
from transliterate.exceptions import LanguagePackNotFound
from django.utils.translation import gettext_lazy as _
from langdetect import detect
from movies.models import Movie
from music.models import Music
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Users(models.Model):
    user = models.OneToOneField(User, verbose_name=_('Юзернейм'),blank=False, unique=True, on_delete=models.CASCADE)
    nickname = models.CharField(verbose_name=_('Никнейм'), max_length=100, blank=False)
    image = models.ImageField(verbose_name=_('Изображение'), blank=True, upload_to='users/user_photo',
                              default="users/user_photo.png")
    email = models.EmailField(verbose_name=_('Имейл'))
    email_confirmed = models.BooleanField(default=False)
    email_confirmation_code = models.CharField(max_length=6, blank=True)
    premium = models.BooleanField(default=False)
    premium_expiry_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    rating = models.DecimalField(verbose_name=_('Рейтинг'), max_digits=7, decimal_places=5, default=False, blank=True, validators=[MinValueValidator(0), MaxValueValidator(10)])
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        lang = detect(self.user.username)
        try:
            self.slug = slugify(translit(self.user.username, lang, reversed=True))
        except LanguagePackNotFound:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
        ordering = ("nickname", "email",)

    def __str__(self) -> str:
        return f"{self.user}"


class UserSavedMovies(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, blank=True, null=True)
    saved_movies = models.ManyToManyField(Movie, verbose_name=_('Вы хотели посмотреть потом'), related_name='saved_by_user', blank=True)
    watched_movies = models.ManyToManyField(Movie, verbose_name=_('Эти фильмы вы уже смотрели'), related_name='watched_by_user', blank=True)
    dropped_movies = models.ManyToManyField(Movie, verbose_name=_('Эти фильмы вы бросили'), related_name='dropped_by_user', blank=True)
    favorite_movies = models.ManyToManyField(Movie, verbose_name=_('Ваши любимые фильмы'), related_name='favorited_by_user', blank=True)

    class Meta:
        verbose_name = _("Фильм пользователя")
        verbose_name_plural = _("Фильмы пользователя")
        ordering = ("user",)

    def __str__(self) -> str:
        return f"{self.user}"


class UserAskedQnA(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, blank=True, null=True)
    ur_ques = models.ManyToManyField('QandA.Question', verbose_name=_('Ваши вопросы'), related_name='saved_by_user',
                                     blank=True)
    ur_ans = models.ManyToManyField('QandA.Answer', verbose_name=_('Ваши ответы'), related_name='saved_by_user',
                                    blank=True)

    class Meta:
        verbose_name = _("Вопрос и Ответ")
        verbose_name_plural = _("Вопрос и Ответ")
        ordering = ("user",)

    def __str__(self) -> str:
        return f"{self.user}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey('QandA.Question', on_delete=models.CASCADE)
    answer = models.ForeignKey('QandA.Answer', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Уведомление")
        verbose_name_plural = _("Уведомления")
        ordering = ("user",)

    def __str__(self) -> str:
        return f"{self.user}"