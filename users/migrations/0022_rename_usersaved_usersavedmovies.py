# Generated by Django 4.2.2 on 2023-07-12 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0053_delete_userrating'),
        ('users', '0021_alter_usersaved_options_usersaved_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserSaved',
            new_name='UserSavedMovies',
        ),
    ]
