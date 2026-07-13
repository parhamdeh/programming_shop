from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from users.tests.factories.users import BaseUserFactory
from posts.tests.factory.posts import PostFactory
from posts.tests.factory.subscription import (
    SubscriptionFactory,
    UserSubscriptionFactory,
)
from posts.tests.factory.posts import FavoritePostFactory


class ProfileAPIViewTest(APITestCase):

    def setUp(self):
        self.user = BaseUserFactory()
        self.client.force_authenticate(self.user)

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

    def test_get_profile(self):
        response = self.client.get(
            reverse(
                "api:profile",
                kwargs={"user_id": self.user.id},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        print(response.data)
        self.assertIn("subscription", response.data)
        self.assertIn("favorits", response.data)

    def test_other_user_cannot_access_profile(self):
        other = BaseUserFactory()

        response = self.client.get(
            reverse(
                "api:profile",
                kwargs={"user_id": other.id},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )