import pytest

from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

from users.tests.factories.users import BaseUserFactory

from posts.tests.factory.posts import PostFactory
from posts.tests.factory.subscription import (
    SubscriptionFactory,
    UserSubscriptionFactory,
)

from posts.tests.factory.posts import FavoritePostFactory


pytestmark = pytest.mark.django_db


class TestProfileAPIView:


    def setup_method(self):

        self.client = APIClient()

        self.user = BaseUserFactory()

        self.client.force_authenticate(
            self.user
        )


        self.subscription = SubscriptionFactory()


        UserSubscriptionFactory(
            user=self.user,
            subscription=self.subscription,
        )


        self.post = PostFactory()


        FavoritePostFactory(
            user=self.user,
            post=self.post,
        )


    def test_user_can_get_own_profile(self):

        response = self.client.get(
            reverse(
                "api:profile",
                kwargs={
                    "user_id": self.user.id,
                },
            )
        )


        assert response.status_code == status.HTTP_200_OK


        assert "username" in response.data
        assert "subscription" in response.data
        assert "favorits" in response.data



    def test_user_cannot_get_other_profile(self):

        other_user = BaseUserFactory()


        response = self.client.get(
            reverse(
                "api:profile",
                kwargs={
                    "user_id": other_user.id,
                },
            )
        )


        assert response.status_code == status.HTTP_403_FORBIDDEN



    def test_anonymous_cannot_get_profile(self):

        self.client.logout()


        response = self.client.get(
            reverse(
                "api:profile",
                kwargs={
                    "user_id": self.user.id,
                },
            )
        )


        assert response.status_code == status.HTTP_401_UNAUTHORIZED