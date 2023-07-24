from django.db.models import Count
from QandA.models import Question
from .models import Notification


class NotificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
            request.unread_notifications_count = unread_notifications.count()
            request.unread_notifications = unread_notifications[:3]

            questions_with_answer_count = Question.objects.filter(notification__user=request.user).annotate(answer_count=Count('comments'))
            request.questions_with_answer_count = questions_with_answer_count
        print(response)
        return response
