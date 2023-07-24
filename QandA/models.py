from django.db import models
from slugify import slugify
from transliterate import translit
from langdetect import detect
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from users.models import Users
from transliterate.exceptions import LanguagePackNotFound
# Create your models here.


class Question(models.Model):
    title = models.CharField(verbose_name=_('Вопрос'), max_length=100, blank=False)
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(verbose_name=_('Содержанеие'))
    genre = models.ManyToManyField('Tag', verbose_name=_('тег'))
    active = models.BooleanField(verbose_name=_('Показать'), default=True)
    image = models.ImageField(verbose_name = _('Изображжение'), upload_to='QandA/images/', blank=True)
    files = models.FileField(verbose_name = _('Файл'), upload_to='QandA/files/', blank=True)

    def save(self, *args, **kwargs):
        self.title = self.title.capitalize()
        self.content = self.content.capitalize()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Вопрос")
        verbose_name_plural = _("Вопроы")
        ordering = ("title", "author", 'content')

    def __str__(self) -> str:
        return f"{self.title}"


class Answer(models.Model):
    topic = models.ManyToManyField(Question, related_name='comments')
    commentator = models.ManyToManyField(Users, related_name='qanda_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(verbose_name=_('Комментарий'))
    active = models.BooleanField(verbose_name=_('Показать'), default=True)
    image = models.ImageField(verbose_name=_('Изображжение'), upload_to='QandA/images/', blank=True)
    files = models.FileField(verbose_name=_('Файл'), upload_to='QandA/files/', blank=True)
    rating = models.IntegerField(default=0)
    voters = models.JSONField(default=dict)

    class Meta:
        verbose_name = _("Коммент")
        verbose_name_plural = _("Комментарии")
        ordering = ('content',)

    def __str__(self) -> str:
        return f"{self.commentator}"


class Tag(models.Model):
    genre = models.CharField(verbose_name=_('Теги'), max_length=50)
    slug = models.SlugField(unique=True, blank=True)

    def validate_unique(self, *args, **kwargs):
        if Tag.objects.filter(genre=self.genre).exists():
            raise ValidationError('Такое объект уже существует')

    def save(self, *args, **kwargs):
        lang = detect(self.genre)
        try:
            self.slug = slugify(translit(self.genre, lang, reversed=True))
        except LanguagePackNotFound:
            self.slug = slugify(self.genre)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Тег")
        verbose_name_plural = _("Теги")
        ordering = ["genre"]

    def __str__(self) -> str:
        return f"{self.genre}"
