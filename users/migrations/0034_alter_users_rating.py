# Generated by Django 4.2.3 on 2023-07-23 20:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0033_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=5, default=False, max_digits=6, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(11)], verbose_name='Рейтинг'),
        ),
    ]
