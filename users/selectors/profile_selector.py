# Django Built-in modules
from django.http import HttpRequest
from django.db.models import QuerySet

# Local Apps
from posts.models import Post
from posts.models import UserSubscription
from view_api.exceptions import SubscriptionExpiredError


def get_user_subscription_detail(*, request: HttpRequest) -> UserSubscription | None:
    subscription = UserSubscription.objects.filter(
                user=request.user,
                is_active=True,
            ).select_related("subscription").last()
    if not subscription:
        return None
    if subscription.remaining_days == 0:
        subscription.delete()
        raise SubscriptionExpiredError()
    return subscription


def get_user_favorite_posts(*, request: HttpRequest) -> QuerySet[Post]:
    return Post.objects.filter(
        favorits__user=request.user
    ).select_related("author", "category")