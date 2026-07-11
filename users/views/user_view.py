from datetime import timedelta

import logging

logger = logging.getLogger(__name__)

from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout

from users.selectors.user_selector import get_users_list
from users.forms.user_form import LoginForm, RegisterForm, VerifyOtpForm
from users.models import OtpCode, BaseUserModel
from users.tasks import send_otp_task, delete_otp_task
from users.services.otp_services import create_otp_code
from users.services.user_services import create_user


class RegisterUser(View):
    """
    Display and process the user registration form.

    GET:
        Render an empty registration form.

    POST:
        Validate form data, create a new user account,
        log the user in automatically, and redirect
        to the home page.
    """

    form_class = RegisterForm
    template_name = "users/user_register.html"

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        """
        Initialize common attributes used by the view.

        This method is called before dispatch() and can be
        used to prepare objects needed by multiple handlers.
        """
        super().setup(request, *args, **kwargs)

        self.request = request
        self.form = self.form_class()

    def dispatch(
        self,
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> HttpResponse:
        """
        Route the request to the appropriate handler.

        This method executes before get(), post(), etc.
        It is commonly used for authentication, permissions,
        logging, throttling, and other cross-cutting concerns.
        """

        if request.user.is_authenticated:
            messages.info(
                request,
                "You are already logged in."
            )
            return redirect("home:home")

        return super().dispatch(
            request,
            *args,
            **kwargs,
        )

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Render the registration form.
        """

        return render(
            request,
            self.template_name,
            {
                "form": self.form,
            },
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Process registration form submission.
        """

        form = self.form_class(request.POST)

        if form.is_valid():
            request.session["username"] = form.cleaned_data["username"]
            request.session["phone"] = form.cleaned_data["phone"]
            request.session["password"] = make_password(form.cleaned_data["password"])
            
            otp = create_otp_code(phone=form.cleaned_data["phone"])
            
            send_otp_task.delay(
                phone=str(form.cleaned_data["phone"]),
                code=otp.code,
            )
            print(otp.code)
            delete_otp_task.apply_async(
                args=[otp.id],
                countdown=120,
            )

            return redirect("users:code")

        messages.error(
            request,
            "Please correct the errors below."
        )

        return render(
            request,
            self.template_name,
            {
                "form": form,
            },
        )


class LoginView(View):
    """
    Handle user authentication.
    """

    form_class = LoginForm
    template_name = "users/user_login.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Display login form.
        """

        if request.user.is_authenticated:
            return redirect("home:home")

        form = self.form_class()

        return render(
            request=request,
            template_name=self.template_name,
            context={
                "form": form,
            },
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Authenticate and log in the user.
        """

        form = self.form_class(request.POST)

        if form.is_valid():
            login(
                request,
                form.user,
            )
            logger.info(
                f"{form.user.username} logged in."
            )

            messages.success(
                request,
                f"Welcome back {form.user.username}!",
            )

            return redirect("home:home")
        submitted_username = request.POST.get("username", "unknown")
        logger.warning(f"Invalid credentials for user {submitted_username}")

        messages.error(
            request,
            "Invalid credentials.",
        )

        return render(
            request,
            self.template_name,
            {
                "form": form,
            },
        )
    

class LogoutView(View):
    """
    Log out the current user.
    """
    
    def get(self, request:HttpRequest) -> HttpResponse:
        logout(request)
        logger.info(
            f"{request.user.username} logged out."
        )

        messages.success(
            request,
            "You have been logged out."
        )

        return redirect("users:login")
    


class VerifyOtpView(View):
    form_class = VerifyOtpForm
    template_name = "users/validation_code.html"

    def get(self, request):
        if not request.session.get("phone"):
            messages.error(request, "please register first.")
            return redirect("users:register")
        return render(
            request,
            self.template_name,
            {
                "form": self.form_class()
            }
        )

    def post(self, request):

        form = self.form_class(request.POST)

        if form.is_valid():

            code = form.cleaned_data["code"]

            otp = OtpCode.objects.filter(
                phone=request.session["phone"],
                code=code,
                is_used=False,
            ).last()

            if otp is None:
                logger.warning(
                    f"Invalid OTP for user "
                )

                messages.error(
                    request,
                    "Invalid verification code."
                )

                return redirect(
                    "users:code"
                )

            if otp.is_expired():
                logger.warning(
                    f"OTP is expired for user"
                )
                messages.error(
                    request,
                    "Verification code has expired."
                )
                otp.delete()

                return redirect(
                    "users:code"
                )

            otp.is_used = True
            otp.save(update_fields=["is_used"])

            try:
                user = create_user(username=request.session["username"],
                                                phone=request.session["phone"],
                                                password=request.session["password"])
            except Exception as e:
                logger.exception(f"Error while creating user -> {e}")
                return render(
                request,
                self.template_name,
                {
                    "form": self.form,
                },
                )
            del request.session["username"]
            del request.session["phone"]
            del request.session["password"]
            logger.info(f"New user registered: {user.username}")

            messages.success(
                request,
                "Account created successfully."
            )
            login(
                request,
                user
            )
            logger.info(
                f"{user.username} logged in."
            )
            otp.delete()

            messages.success(
                request,
                "Your account has been verified successfully."
            )

            return redirect("home:home")

        return render(
            request,
            self.template_name,
            {
                "form": form
            }
        )

    