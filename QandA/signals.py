from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Question, Answer
from users.models import User, UserAskedQnA


@receiver(post_save, sender=Question)
def save_question(sender, instance, **kwargs):
    user, created = UserAskedQnA.objects.get_or_create(user=instance.author)
    user.ur_ques.add(instance)


@receiver(post_save, sender=Answer)
def save_answer(sender, instance, **kwargs):
    for user in instance.commentator.all():
        user_profile, created = UserAskedQnA.objects.get_or_create(user=user)
        user_profile.ur_ans.add(instance)




