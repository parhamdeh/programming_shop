from posts.models import Subscription


def create_subscription(*, data:dict) -> Subscription:
    return Subscription.objects.create(
        name=data.get("name"),
        price=data.get("price"),
        limit_days=data.get("limit_days")
    )