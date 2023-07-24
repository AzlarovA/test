# Generated by Django 4.2.2 on 2023-06-21 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movies', models.ImageField(upload_to='photo_for_templates/', verbose_name='Фильмы')),
                ('music', models.ImageField(upload_to='photo_for_templates/', verbose_name='Музыка')),
                ('queue', models.ImageField(upload_to='photo_for_templates/', verbose_name='В_О')),
            ],
            options={
                'verbose_name': 'Фото для страницы',
                'verbose_name_plural': 'Фото для страницы',
            },
        ),
    ]
