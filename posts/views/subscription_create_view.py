from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
import logging

from posts.forms.subscription_form import SubscriptionForm
from posts.services.subscription import create_subscription

logger = logging.getLogger(__name__)


class CreateSubscription(View):
    """
    Handle creation of new subscriptions.

    Only authenticated staff users are allowed to access
    this view.
    """

    form_class = SubscriptionForm
    template_name = "subscription/create_subscription.html"

    def dispatch(
        self,
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> HttpResponse:
        """
        Check authentication and staff permissions before
        processing the request.
        """

        if not request.user.is_authenticated:
            logger.warning(
                "Anonymous user attempted to access CreateSubscription."
            )
            return redirect("users:login")

        if not request.user.is_staff:
            logger.warning(
                "User '%s' attempted to access CreateSubscription without permission.",
                request.user.username,
            )

            messages.error(
                request,
                "You don't have permission to access this page.",
            )

            return redirect("home:home")

        return super().dispatch(
            request,
            *args,
            **kwargs,
        )

    def get(
        self,
        request: HttpRequest,
    ) -> HttpResponse:
        """
        Display an empty subscription creation form.
        """

        logger.info(
            "User '%s' opened CreateSubscription page.",
            request.user.username,
        )

        form = self.form_class()

        return render(
            request=request,
            template_name=self.template_name,
            context={
                "form": form,
            },
        )

    def post(
        self,
        request: HttpRequest,
    ) -> HttpResponse:
        """
        Validate the submitted form and create
        a new subscription.
        """

        form = self.form_class(request.POST)

        if form.is_valid():

            subscription = create_subscription(
                data=form.cleaned_data,
            )

            logger.info(
                "Subscription '%s' created by '%s'.",
                subscription.name,
                request.user.username,
            )

            messages.success(
                request,
                "Subscription created successfully.",
            )

            return redirect("home:home")

        logger.warning(
            "Invalid subscription creation form submitted by '%s'. Errors: %s",
            request.user.username,
            form.errors.as_json(),
        )

        messages.error(
            request,
            "Form is not valid. Try again.",
        )

        return render(
            request=request,
            template_name=self.template_name,
            context={
                "form": form,
            },
        )