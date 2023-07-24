from django.utils import timezone
from users.models import Users


class SubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user_profile = Users.objects.filter(user=request.user).first()
            if user_profile and user_profile.premium and timezone.now() > user_profile.premium_expiry_date:
                user_profile.premium = False
                user_profile.save()

        response = self.get_response(request)
        return response

