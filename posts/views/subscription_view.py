from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

from posts.selectors.subscription import get_subscription_by_id



class SubscriptionDetailView(LoginRequiredMixin, View):
    template_name = "subscription/detail.html"
    def get(self, request: HttpRequest, subscription_id: int) -> HttpResponse:
        subscription = get_subscription_by_id(sub_id=subscription_id).first()
        if not subscription:
            raise ObjectDoesNotExist("category not found")

        return render(request=request,
                      template_name=self.template_name,
                      context={
                          'category' : subscription,
                      })
    
class SubscriptionPaymentView(LoginRequiredMixin, View):
    ...