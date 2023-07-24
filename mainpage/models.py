from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class MainPage(models.Model):
    movies = models.ImageField(verbose_name=_('Фильмы'), upload_to='photo_for_templates/')
    music = models.ImageField(verbose_name=_('Музыка'), upload_to='photo_for_templates/')
    queue = models.ImageField(verbose_name=_('В_О'), upload_to='photo_for_templates/')

    class Meta:
        verbose_name = _("Фото для страницы")
        verbose_name_plural = _("Фото для страницы")

    def __str__(self) -> str:
        return f"Глав стр."


class Banner(models.Model):
    slide_1 = models.ImageField(verbose_name=_('Фильмы'), upload_to='photo_for_templates/')
    slide_2 = models.ImageField(verbose_name=_('Музыка'), upload_to='photo_for_templates/')
    slide_3 = models.ImageField(verbose_name=_('В_О'), upload_to='photo_for_templates/')

    class Meta:
        verbose_name = _("Фото для баннера")
        verbose_name_plural = _("Фото для баннера")

    def __str__(self) -> str:
        return f"Глав стр."