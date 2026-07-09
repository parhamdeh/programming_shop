

from django.db.models import QuerySet
from posts.models import Subscription, UserSubscription


def get_all_subscriptions() -> QuerySet[Subscription]:
    return Subscription.objects.all()

def get_subscription_by_id(*, sub_id: int) -> Subscription:
    return Subscription.objects.filter(id=sub_id) #.first() in view

def get_user_subscription_with_user(*, user_id: int):
    return UserSubscription.objects.filter(user=user_id)

