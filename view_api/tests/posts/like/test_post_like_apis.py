from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.tests.factories.users import BaseUserFactory
from posts.tests.factory.posts import PostFactory
from posts.models import FavoritPost


class PostLikeListCreateAPIViewTest(APITestCase):

    def setUp(self):
        self.user = BaseUserFactory()
        self.client.force_authenticate(self.user)

        self.post = PostFactory()

    def test_get_likes(self):
        FavoritPost.objects.create(
            user=self.user,
            post=self.post,
        )

        response = self.client.get(
            reverse(
                "api:post-likes",
                kwargs={"post_id": self.post.id},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

    def test_like_post(self):
        response = self.client.post(
            reverse(
                "api:post-likes",
                kwargs={"post_id": self.post.id},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            FavoritPost.objects.filter(
                user=self.user,
                post=self.post,
            ).exists()
        )

    def test_delete_like(self):
        FavoritPost.objects.create(
            user=self.user,
            post=self.post,
        )

        response = self.client.delete(
            reverse(
                "api:post-likes",
                kwargs={"post_id": self.post.id},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            FavoritPost.objects.filter(
                user=self.user,
                post=self.post,
            ).exists()
        )

    def test_anonymous_cannot_like(self):
        self.client.force_authenticate(None)

        response = self.client.post(
            reverse(
                "api:post-likes",
                kwargs={"post_id": self.post.id},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )