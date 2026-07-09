import logging

logger = logging.getLogger(__name__)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth import update_session_auth_hash

from users.selectors.profile_selector import get_user_subscription_detail, get_user_favorite_posts
from posts.models import UserSubscription
from users.forms.edit_profile_form import ChangePasswordForm


class ProfileView(LoginRequiredMixin, View):
    """
    Display the authenticated user's profile.
    """
    template_name = "profile/profile.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        
        subscription = get_user_subscription_detail(request=request)
        favorits = get_user_favorite_posts(request=request)
      

        return render(
            request,
            self.template_name,
            {
                "subscription": subscription,
                "favorits" : favorits,
            },
        )
        


class ChangePasswordView(LoginRequiredMixin, View):
    """
    Allow authenticated users to change their password.
    """

    form_class = ChangePasswordForm
    template_name = "profile/change_password.html"

    def get(self, request):

        return render(
            request,
            self.template_name,
            {
                "form": self.form_class(),
            },
        )

    def post(self, request):

        form = self.form_class(request.POST)

        if form.is_valid():

            if not request.user.check_password(
                form.cleaned_data["old_password"]
            ):

                messages.error(
                    request,
                    "Current password is incorrect."
                )

                return render(
                    request,
                    self.template_name,
                    {
                        "form": form,
                    },
                )

            request.user.set_password(
                form.cleaned_data["new_password"]
            )

            request.user.save()

            update_session_auth_hash(
                request,
                request.user,
            )
            logger.info(
                f"{request.user.username} Password changed successfully."
            )
            messages.success(
                request,
                "Password changed successfully."
            )

            return redirect("users:profile")

        return render(
            request,
            self.template_name,
            {
                "form": form,
            },
        )


