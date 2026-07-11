
import pytest

from posts.selectors.subscription import (
    get_all_subscriptions,
    get_subscription_by_id,
    get_user_subscription_with_user,
)

from posts.tests.factory.subscription import (
    SubscriptionFactory,
    UserSubscriptionFactory,
)

from users.tests.factories.users import BaseUserFactory


pytestmark = pytest.mark.django_db


class TestGetAllSubscriptions:

    def test_returns_all_subscriptions(self):
        SubscriptionFactory.create_batch(3)

        subscriptions = get_all_subscriptions()

        assert subscriptions.count() == 3

    def test_returns_queryset(self):
        SubscriptionFactory()

        subscriptions = get_all_subscriptions()

        assert hasattr(subscriptions, "filter")


class TestGetSubscriptionById:

    def test_returns_subscription_queryset(self):
        subscription = SubscriptionFactory()

        result = get_subscription_by_id(
            sub_id=subscription.id,
        )

        assert result.exists()
        assert result.first() == subscription

    def test_returns_empty_queryset(self):
        result = get_subscription_by_id(
            sub_id=99999,
        )

        assert not result.exists()


class TestGetUserSubscriptionWithUser:

    def test_returns_user_subscription(self):
        user = BaseUserFactory()

        user_subscription = UserSubscriptionFactory(
            user=user,
        )

        result = get_user_subscription_with_user(
            user_id=user.id,
        )

        assert result.exists()
        assert result.first() == user_subscription

    def test_returns_empty_queryset_when_user_has_no_subscription(self):
        user = BaseUserFactory()

        result = get_user_subscription_with_user(
            user_id=user.id,
        )

        assert not result.exists()

    def test_does_not_return_other_users_subscription(self):
        user1 = BaseUserFactory()
        user2 = BaseUserFactory()

        UserSubscriptionFactory(user=user1)

        result = get_user_subscription_with_user(
            user_id=user2.id,
        )

        assert not result.exists()