# Generated by Django 4.2.2 on 2023-06-23 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0029_genre_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
