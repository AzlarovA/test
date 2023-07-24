from django.db.models import Count, Q
from QandA.models import Question
from .models import Notification


def notifications(request):
    if request.user.is_authenticated:
        unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()
        questions_with_unread_answer_count = Question.objects.filter(
            Q(notification__user=request.user) & Q(notification__is_read=False)
        ).annotate(answer_count=Count('notification'))
    else:
        unread_notifications_count = 0
        questions_with_unread_answer_count = []

    return {
        'unread_notifications_count': unread_notifications_count,
        'questions_with_unread_answer_count': questions_with_unread_answer_count,
    }
