# Generated by Django 4.2.2 on 2023-07-08 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_users_password_1_users_password_2_users_user_movies'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='user_movies',
        ),
    ]
