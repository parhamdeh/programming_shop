from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect

from posts.selectors.subscription import get_user_subscription_with_user


class NoActiveSubscriptionRequiredMixin:
    """
    Redirects users who already have an active subscription
    back to the home page, preventing them from purchasing again.
    """
    redirect_url = "home:home"
    warning_message = "you have a subscription!"

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if get_user_subscription_with_user(user_id=request.user.id).exists():
            messages.warning(request, self.warning_message)
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)