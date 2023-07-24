from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from slugify import slugify
from transliterate import translit
from langdetect import detect
# Create your models here.


class News(models.Model):
    title = models.CharField(verbose_name=_('Заголовок'), max_length=100, blank=False)
    author = models.CharField(verbose_name=_('Автор'), max_length=100)
    created_at = models.DateTimeField(verbose_name=_('Дата выпуска'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Дата обновления'), auto_now=True)
    content = models.TextField(verbose_name=_('Тема'))
    image = models.ImageField(verbose_name=_('Изображжение'), upload_to='QandA/images/', blank=True)
    files = models.FileField(verbose_name=_('Файл'), upload_to='QandA/files/', blank=True)
    link = models.URLField(verbose_name=_('Ссылка'))
    slug = models.SlugField(unique=True, blank=True)
    active = models.BooleanField(verbose_name=_('Показать'))

    def save(self, *args, **kwargs):
        self.title = self.title.capitalize()
        self.author = self.author.capitalize()
        self.content = self.content.capitalize()
        lang = detect(self.title)
        self.slug = slugify(translit(self.title, lang, reversed=True))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Новость")
        verbose_name_plural = _("Новости")
        ordering = ("title", "author", 'content')

    def __str__(self) -> str:
        return f"{self.title}"

