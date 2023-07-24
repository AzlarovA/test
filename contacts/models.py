from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Contact(models.Model):
    company = models.CharField(verbose_name=_('Компания'), default="AIWIKS", max_length=200)
    telephone_1 = models.CharField(verbose_name=_('Телефон'), default="+998 12 345-67-89", max_length=200)
    telephone_2 = models.CharField(verbose_name=_('Телефон'), default="+998 00 000-00-00", blank=True, max_length=200)
    address = models.CharField(verbose_name=_('Адрес'), blank=True, max_length=200)
    email = models.EmailField(verbose_name=_('Почта'))
    social = models.ManyToManyField(verbose_name=_('Соци'), to="Social")
    about = models.TextField(verbose_name=_('Соци'))

    class Meta:
        verbose_name = _("Контакт")
        verbose_name_plural = _("Контакты")
        ordering = ("company", "address", 'telephone_1')

    def __str__(self) -> str:
        return f"{self.company}"


class FAQ(models.Model):
    que = models.CharField(verbose_name=_('Вопрос'), max_length=200)
    ans = models.CharField(verbose_name=_('Ответ'), max_length=200)

    class Meta:
        verbose_name = _("ВопросОтвет")
        verbose_name_plural = _("ВопросОтветы")

    def __str__(self) -> str:
        return f"{self.que}-{self.ans}"


class Social(models.Model):
    soci = models.CharField(verbose_name=_('Сеть'), max_length=200)
    text = models.CharField(verbose_name=_('Текст'), blank=True, max_length=200)
    css_field = models.CharField(verbose_name=_('Поля для css'), blank=True, max_length=200)
    link = models.URLField(verbose_name=_('Ссылка'), blank=True)

    class Meta:
        verbose_name = _("Соц. сеть")
        verbose_name_plural = _("Соц. сети")
        ordering = ("soci", "text")

    def __str__(self) -> str:
        return f"{self.soci}"


class ContactPageForm(models.Model):
    first_name = models.CharField(verbose_name='Имя', max_length=150)
    last_name = models.CharField(verbose_name='Фамилия', max_length=150)
    email = models.EmailField(verbose_name='e-mail')
    phone = models.CharField(verbose_name='Телефон', max_length=14)
    subject = models.CharField(verbose_name='Тема', max_length=100)
    message = models.TextField(verbose_name='Текст сообщения')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self) -> str:
        return f'{self.subject}'
