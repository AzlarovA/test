# Generated by Django 4.2.2 on 2023-07-08 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0045_alter_genre_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(default='a'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='slug',
            field=models.SlugField(default='a'),
        ),
    ]
