from django.urls import path, include

from view_api.apps_api.users.authentication.register_user_apis import RegisterUserAPIView, VerifyOtpAPIView
from view_api.apps_api.users.user.id.user_id_apis import UserRetrieveUpdatadeDestroy
from view_api.apps_api.users.user.user_apis import UserListCreate
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


app_name = "api"
urlpatterns = [
    path("jwt/", include(([
        path("login/", TokenObtainPairView.as_view(), name="login"),
        path("refresh/", TokenRefreshView.as_view(), name="refresh"),
        path("verify/", TokenVerifyView.as_view(), name="verify"),

    ])), name="jwt"),
    path(route="users/", view=UserListCreate.as_view(), name="user-list-create"),
    path(route="users/<int:user_id>/", view=UserRetrieveUpdatadeDestroy.as_view(), name="user-detail"),
    path(route="register/", view=RegisterUserAPIView.as_view(), name="register"),
    path(route="register/verify/", view=VerifyOtpAPIView.as_view(), name="verify"),
]