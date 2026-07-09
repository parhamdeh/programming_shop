from django.http import HttpRequest
from django.db.models import QuerySet

from posts.models import Post
from posts.models import UserSubscription


def get_user_subscription_detail(*, request: HttpRequest) -> UserSubscription:
    subscription = UserSubscription.objects.filter(
                user=request.user,
                is_active=True,
            ).select_related("subscription").last()
    return subscription


def get_user_favorite_posts(*, request: HttpRequest) -> QuerySet[Post]:
    return Post.objects.filter(
        favorits__user=request.user
    ).select_related("author", "category")