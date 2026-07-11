import pytest

from datetime import timedelta

from django.utils import timezone

from posts.models import (
    Subscription,
    UserSubscription,
)

from posts.services.subscription import (
    create_subscription,
    create_user_subscription,
)

from posts.tests.factory.subscription import (
    SubscriptionFactory,
)

from users.tests.factories.users import (
    BaseUserFactory,
)


pytestmark = pytest.mark.django_db


class TestCreateSubscription:

    def test_create_subscription(self):

        data = {
            "name": "Gold",
            "price": 150000,
            "limit_days": 30,
        }

        subscription = create_subscription(data=data)

        assert isinstance(subscription, Subscription)

        assert subscription.name == "Gold"

        assert subscription.price == 150000

        assert subscription.limit_days == 30

        assert Subscription.objects.count() == 1


class TestCreateUserSubscription:

    def test_create_user_subscription(self):

        user = BaseUserFactory()

        subscription = SubscriptionFactory(limit_days=30)

        user_subscription = create_user_subscription(
            user=user,
            subscription=subscription,
        )

        assert isinstance(
            user_subscription,
            UserSubscription,
        )

        assert user_subscription.user == user

        assert user_subscription.subscription == subscription

        assert user_subscription.is_active is True

        assert (
            user_subscription.end_date.date()
            == (timezone.now() + timedelta(days=30)).date()
        )

    def test_remaining_days_property(self):

        user = BaseUserFactory()

        subscription = SubscriptionFactory(limit_days=15)

        user_subscription = create_user_subscription(
            user=user,
            subscription=subscription,
        )

        assert user_subscription.remaining_days >= 14

    def test_create_multiple_subscriptions(self):

        subscription = SubscriptionFactory()

        user1 = BaseUserFactory()

        user2 = BaseUserFactory()

        create_user_subscription(
            user=user1,
            subscription=subscription,
        )

        create_user_subscription(
            user=user2,
            subscription=subscription,
        )

        assert UserSubscription.objects.count() == 2