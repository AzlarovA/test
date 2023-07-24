# Generated by Django 4.2.2 on 2023-07-12 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QandA', '0008_alter_question_active'),
        ('users', '0026_alter_useraskedqna_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraskedqna',
            name='ur_ans',
            field=models.ManyToManyField(blank=True, related_name='saved_by_user', to='QandA.answer', verbose_name='Ваши ответы'),
        ),
        migrations.AlterField(
            model_name='useraskedqna',
            name='ur_ques',
            field=models.ManyToManyField(blank=True, related_name='saved_by_user', to='QandA.question', verbose_name='Ваши вопросы'),
        ),
    ]
