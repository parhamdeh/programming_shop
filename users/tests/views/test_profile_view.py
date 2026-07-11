import pytest

from django.urls import reverse

from users.tests.factories.users import BaseUserFactory
from posts.tests.factory.posts import (

    PostFactory,
    FavoritePostFactory,
)
from posts.tests.factory.subscription import (

        SubscriptionFactory,
    UserSubscriptionFactory,
    )


pytestmark = pytest.mark.django_db


class TestProfileView:

    def test_redirect_if_user_is_not_logged_in(self, client):
        response = client.get(
            reverse("users:profile")
        )

        assert response.status_code == 302

    def test_profile_page_returns_200(self, client):
        user = BaseUserFactory()

        client.force_login(user)

        response = client.get(
            reverse("users:profile")
        )

        assert response.status_code == 200
        assert "subscription" in response.context
        assert "favorits" in response.context

    def test_profile_shows_active_subscription(self, client):
        user = BaseUserFactory()

        subscription = SubscriptionFactory()

        user_subscription = UserSubscriptionFactory(
            user=user,
            subscription=subscription,
        )

        client.force_login(user)

        response = client.get(
            reverse("users:profile")
        )

        assert response.context["subscription"] == user_subscription

    def test_profile_shows_favorite_posts(self, client):
        user = BaseUserFactory()

        post = PostFactory()

        FavoritePostFactory(
            user=user,
            post=post,
        )

        client.force_login(user)

        response = client.get(
            reverse("users:profile")
        )

        favorites = response.context["favorits"]

        assert post in favorites