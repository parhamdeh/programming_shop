from posts.models import Subscription, UserSubscription
from users.models import BaseUserModel

from datetime import timedelta

from django.utils import timezone



def create_subscription(*, data:dict) -> Subscription:
    return Subscription.objects.create(
        name=data.get("name"),
        price=data.get("price"),
        limit_days=data.get("limit_days")
    )

def create_user_subscription(*, user: BaseUserModel, subscription: Subscription) -> UserSubscription:
    start_day = timezone.now()
    end_day = start_day + timedelta(days=subscription.limit_days)
    
    return UserSubscription.objects.create(user=user, subscription=subscription, end_date=end_day)