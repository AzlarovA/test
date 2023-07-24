# Generated by Django 4.2.2 on 2023-06-21 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_alter_news_created_at_alter_news_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='files',
            field=models.FileField(blank=True, upload_to='QandA/files/', verbose_name='Файл'),
        ),
        migrations.AddField(
            model_name='news',
            name='image',
            field=models.ImageField(blank=True, upload_to='QandA/images/', verbose_name='Изображжение'),
        ),
    ]
