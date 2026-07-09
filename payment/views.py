from django.shortcuts import get_object_or_404
from django.views import View

from posts.models import Subscription



class SubscriptionPaymentView(View):

    def get(self, request, subscription_id):

        subscription = get_object_or_404(
            Subscription,
            id=subscription_id,
        )
        ...

     
