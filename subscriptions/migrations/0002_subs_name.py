# Generated by Django 4.2.2 on 2023-06-20 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subs',
            name='name',
            field=models.CharField(default='subscriptions', max_length=100),
        ),
    ]
