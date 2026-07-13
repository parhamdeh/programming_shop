from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from users.tests.factories.users import BaseUserFactory
from posts.tests.factory.posts import PostFactory
from posts.tests.factory.category import CategoryFactory


class PostListCreateAPIViewTest(APITestCase):

    def setUp(self):
        self.admin = BaseUserFactory(is_staff=True)
        self.user = BaseUserFactory()
        self.category = CategoryFactory()

    def test_get_posts(self):
        PostFactory.create_batch(3)

        response = self.client.get(
            reverse("api:post-list-create")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            3,
        )

    def test_admin_can_create_post(self):
        self.client.force_authenticate(self.admin)

        response = self.client.post(
            reverse("api:post-list-create"),
            {
                "title": "Test Post",
                "content": "Test Content",
                "category": self.category.id,
                "is_premium": False,
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["title"],
            "Test Post",
        )

    def test_normal_user_cannot_create_post(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            reverse("api:post-list-create"),
            {
                "title": "Test",
                "content": "Test",
                "category": self.category.id,
                "is_premium": False,
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )