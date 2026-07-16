# Django Built-in modules
from django.urls import path, include

# Local Apps
from view_api.apps_api.home.home_apis import HomeAPIview
from view_api.apps_api.posts.category.post_categoy_apis import CategoryListCreateAPIView
from view_api.apps_api.posts.comments.post_comment_apis import PostCommentListCreateAPIView
from view_api.apps_api.posts.likes.like_apis import PostLikeListCreateAPIView
from view_api.apps_api.posts.pay.pay_apis import SubscriptionPaymentAPIView, SubscriptionVerifyAPIView
from view_api.apps_api.posts.post.id.post_id_apis import PostRetrieveUpdateDestroyAPIView
from view_api.apps_api.posts.post.post_apis import PostListCreateAPIView
from view_api.apps_api.posts.subscription.id.subscription_id_apis import SubscriptionRetrieveUpdateDstroyAPIView
from view_api.apps_api.posts.subscription.subscription_apis import SubscriptionListCreateAPIView
from view_api.apps_api.users.authentication.login_api import CustomTokenObtainPairView
from view_api.apps_api.users.authentication.register_user_apis import RegisterUserAPIView, VerifyOtpAPIView
from view_api.apps_api.users.profile.user_profile_apis import ProfileAPIView
from view_api.apps_api.users.user.id.user_id_apis import UserRetrieveUpdatadeDestroy
from view_api.apps_api.users.user.user_apis import UserListCreate
from view_api.apps_api.posts.category.id.category_id_apis import CategoryRetrieveUpdateDstroyAPIView

# Third Party Packages
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView



app_name = "api"
urlpatterns = [
    path("account/jwt/", include(([
        path("login/", CustomTokenObtainPairView.as_view(), name="login"),
        path("refresh/", TokenRefreshView.as_view(), name="refresh"),

    ])), name="jwt"),
    path(route="users/", view=UserListCreate.as_view(), name="user-list-create"),
    path(route="users/<int:user_id>/", view=UserRetrieveUpdatadeDestroy.as_view(), name="user-detail"),
    path(route="register/", view=RegisterUserAPIView.as_view(), name="register"),
    path(route="register/verify/", view=VerifyOtpAPIView.as_view(), name="verify-code"),
    path(route="profile/<int:user_id>/", view=ProfileAPIView.as_view(), name="profile"),
    path(route="posts/", view=PostListCreateAPIView.as_view(), name="post-list-create"),
    path(route="posts/<int:post_id>/", view=PostRetrieveUpdateDestroyAPIView.as_view(), name="post-detail"),
    path(route="likes/<int:post_id>/", view=PostLikeListCreateAPIView.as_view(), name="post-likes"),
    path(route="comments/<int:post_id>/", view=PostCommentListCreateAPIView.as_view(), name="post-comments"),
    path(route="categories/", view=CategoryListCreateAPIView.as_view(), name="category-list-create"),
    path(route="categories/<int:category_id>/", view=CategoryRetrieveUpdateDstroyAPIView.as_view(), name="category-detail"),
    path(route="subscriptions/", view=SubscriptionListCreateAPIView.as_view(), name="subscription-list-create"),
    path(route="subscriptions/<int:subscription_id>/", view=SubscriptionRetrieveUpdateDstroyAPIView.as_view(), name="subscription-detail"),
    path(
    "subscriptions/<int:subscription_id>/pay/",
    SubscriptionPaymentAPIView.as_view(),
    name="subscription-pay",
),
    path(
        "subscriptions/verify/",
        SubscriptionVerifyAPIView.as_view(),
        name="subscription-verify",
    ),
    path(route="", view=HomeAPIview.as_view(), name="home")
]