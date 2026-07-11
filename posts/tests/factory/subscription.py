import factory

from datetime import timedelta
from django.utils import timezone

from users.tests.factories.users import BaseUserFactory
from posts.models import UserSubscription
from posts.models import Subscription

class SubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subscription

    name = factory.Sequence(lambda n: f"Subscription {n}")
    price = factory.Faker("random_int", min=10000, max=500000)
    limit_days = factory.Faker("random_int", min=5, max=90)


class UserSubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserSubscription

    user = factory.SubFactory(BaseUserFactory)

    subscription = factory.SubFactory(
        SubscriptionFactory
    )

    end_date = factory.LazyAttribute(lambda o: timezone.now() + timedelta(days=30))

    is_active = True