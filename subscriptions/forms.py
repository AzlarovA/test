from django import forms

SUBSCRIPTION_DESCRIPTIONS = {
    'monthly': 'Ежемесячная подписка на наши услуги',
    '3-months': 'Подписка на 3 месяцев на наши услуги',
    '6-months': 'Подписка на 6 месяцев на наши услуги',
    'yearly': 'Годовая подписка на наши услуги',
}


class SubscriptionForm(forms.Form):
    SUBSCRIPTION_CHOICES = [
        ('monthly', SUBSCRIPTION_DESCRIPTIONS['monthly']),
        ('3-months', SUBSCRIPTION_DESCRIPTIONS['3-months']),
        ('6-months', SUBSCRIPTION_DESCRIPTIONS['6-months']),
        ('yearly', SUBSCRIPTION_DESCRIPTIONS['yearly']),
    ]

    subscription_type = forms.ChoiceField(choices=SUBSCRIPTION_CHOICES)