from django.urls import path

from users.views.profile_views import ChangePasswordView, ProfileView
from users.views.user_view import LoginView, RegisterUser, LogoutView, VerifyOtpView


app_name = "users"

urlpatterns = [
    path(route="register/", view=RegisterUser.as_view(), name="register"),
    path(route="login/", view=LoginView.as_view(), name="login"),
    path(route="logout/", view=LogoutView.as_view(), name="logout"),
    path(route="verify/", view=VerifyOtpView.as_view(), name="code"),
    path(route="profile/", view=ProfileView.as_view(), name="profile"),
    path(route="change_password/", view=ChangePasswordView.as_view(), name="change-password"),
]