from django.urls import path
from posts.views.category_create_view import CreateCategory
from posts.views.post_create_view import CreatePost
from posts.views.posts_view import DeleteCommetntView, DeleteFavorit, PostDetailView, PostFavoritView
from posts.views.subscription_create_view import CreateSubscription
from posts.views.category_view import CategoryDetailView
from posts.views.subscription_view import SubscriptionDetailView, SubscriptionPaymentView, VerifyPay

app_name = "posts"
urlpatterns = [
    path(route="detail/<int:post_id>/", view=PostDetailView.as_view(), name="detail"),
    path(route="favorit/<int:post_id>/", view=PostFavoritView.as_view(), name="favorit"),
    path(route="unlike/<int:post_id>/", view=DeleteFavorit.as_view(), name="unlike"),
    path(route="delete-comment/<int:post_id>/", view=DeleteCommetntView.as_view(), name="delete-comment"),
    path(route="create/", view=CreatePost.as_view(), name="create-post"),
    path(route="create_sub/", view=CreateSubscription.as_view(), name="create-subscription"),
    path(route="create_cat/", view=CreateCategory.as_view(), name="create-category"),
    path(route="detail_cat/<int:category_id>/", view=CategoryDetailView.as_view(), name="category-detail"),
    path(route="detail_sub/<int:subscription_id>/", view=SubscriptionDetailView.as_view(), name="subscription-detail"),
    path(route="payment/<int:subscription_id>/", view=SubscriptionPaymentView.as_view(), name="payment"),
    # path(route="payment/<int:subscription_id>/", view=VerifyPay.as_view(), name="payment"),
    path(route="verify/", view=VerifyPay.as_view(), name="verify"),
]