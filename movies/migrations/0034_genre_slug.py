# Generated by Django 4.2.2 on 2023-06-24 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0033_remove_genre_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='slug',
            field=models.SlugField(default='asd'),
        ),
    ]
