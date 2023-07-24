from django.db import models
from slugify import slugify
from transliterate import translit
from django.utils.translation import gettext_lazy as _
from transliterate.exceptions import LanguagePackNotFound
from langdetect import detect
from decimal import Decimal
# Create your models here.


class Subs(models.Model):
    name = models.CharField(default="subscriptions", max_length=100)
    subscription_1 = models.DecimalField(verbose_name=_('Подписка на 1 месяц'), max_digits=10, decimal_places=2)
    subscription_2 = models.DecimalField(verbose_name=_('Подписка на 3 месяц'), blank=True, max_digits=10, decimal_places=2)
    subscription_3 = models.DecimalField(verbose_name=_('Подписка на 6 месяц'), blank=True, max_digits=10, decimal_places=2)
    subscription_4 = models.DecimalField(verbose_name=_('Подписка на 12 месяц'), blank=True, max_digits=10, decimal_places=2)

    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.subscription_2 = self.subscription_1 * Decimal(3) - self.subscription_1 * Decimal(0.19639278557114228456913827655311)
        self.subscription_3 = self.subscription_1 * Decimal(6) - self.subscription_1 * Decimal(0.99198396793587174348697394789579)
        self.subscription_4 = self.subscription_1 * Decimal(12) - self.subscription_1 * Decimal(1.9819639278557114228456913827655)
        lang = detect(self.name)
        try:
            self.slug = slugify(translit(self.name, lang, reversed=True))
        except LanguagePackNotFound:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Подписка")
        verbose_name_plural = _("Подписки")
        ordering = ("subscription_1", "subscription_2", 'subscription_3', 'subscription_4')

    def __str__(self) -> str:
        return f"Подписки"


class MainPage(models.Model):
    image = models.ImageField(verbose_name=_('Фото'), blank=True, upload_to="subscriptions/")


#допол привелегии
class Subs_priv(models.Model):
    pass