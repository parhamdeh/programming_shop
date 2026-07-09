from django import forms

from posts.models import Subscription


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ("name", "price", "limit_days")