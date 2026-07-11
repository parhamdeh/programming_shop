from datetime import timedelta
from django.utils import timezone
import factory
import pytest

from django.test import RequestFactory

from users.selectors.profile_selector import (
    get_user_subscription_detail,
    get_user_favorite_posts,
)
from posts.models import UserSubscription
from users.tests.factories.users import BaseUserFactory
from posts.tests.factory.subscription import (
    SubscriptionFactory,
    UserSubscriptionFactory,
)
from posts.tests.factory.posts import (
    PostFactory,
    FavoritePostFactory,
)

pytestmark = pytest.mark.django_db


class TestGetUserSubscriptionDetail:

    def setup_method(self):
        self.factory = RequestFactory()

    def test_return_active_subscription(self):

        user = BaseUserFactory()

        subscription = SubscriptionFactory()

        user_subscription = UserSubscriptionFactory(
            user=user,
            subscription=subscription,
            is_active=True,
            end_date=factory.LazyAttribute(lambda o: timezone.now() + timedelta(days=30)),
        )

        request = self.factory.get("/")
        request.user = user

        result = get_user_subscription_detail(
            request=request,
        )

        assert result == user_subscription

    def test_return_none_when_user_has_no_subscription(self):

        user = BaseUserFactory()

        request = self.factory.get("/")
        request.user = user

        result = get_user_subscription_detail(
            request=request,
        )

        assert result is None

    def test_delete_subscription_when_remaining_days_is_zero(self):

        user = BaseUserFactory()

        subscription = SubscriptionFactory()

        user_subscription = UserSubscriptionFactory(
            user=user,
            subscription=subscription,
            is_active=True,
            end_date=timezone.now(),
        )

        request = self.factory.get("/")
        request.user = user

        result = get_user_subscription_detail(
            request=request,
        )

        assert result is None

        assert not UserSubscription.objects.filter(
            id=user_subscription.id
        ).exists()


class TestGetUserFavoritePosts:

    def setup_method(self):
        self.factory = RequestFactory()

    def test_return_user_favorite_posts(self):

        user = BaseUserFactory()

        post1 = PostFactory()

        post2 = PostFactory()

        FavoritePostFactory(
            user=user,
            post=post1,
        )

        FavoritePostFactory(
            user=user,
            post=post2,
        )

        request = self.factory.get("/")
        request.user = user

        posts = get_user_favorite_posts(
            request=request,
        )

        assert posts.count() == 2

        assert post1 in posts

        assert post2 in posts

    def test_return_empty_queryset(self):

        user = BaseUserFactory()

        request = self.factory.get("/")
        request.user = user

        posts = get_user_favorite_posts(
            request=request,
        )

        assert posts.count() == 0