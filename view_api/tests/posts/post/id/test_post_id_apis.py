from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from posts.models import Post
from posts.tests.factory.posts import PostFactory
from posts.tests.factory.category import CategoryFactory
from users.tests.factories.users import BaseUserFactory


class PostRetrieveUpdateDestroyAPIViewTest(APITestCase):

    def setUp(self):
        self.admin = BaseUserFactory(is_staff=True)
        self.user = BaseUserFactory()
        self.category = CategoryFactory()

        self.post = PostFactory(
            author=self.admin,
            category=self.category,
        )

    def test_get_post(self):
        response = self.client.get(
            reverse(
                "api:post-detail",
                kwargs={"post_id": self.post.id},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            self.post.id,
        )

    def test_get_not_found(self):
        response = self.client.get(
            reverse(
                "api:post-detail",
                kwargs={"post_id": 99999},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_admin_can_put(self):
        self.client.force_authenticate(self.admin)

        response = self.client.put(
            reverse(
                "api:post-detail",
                kwargs={"post_id": self.post.id},
            ),
            {
                "title": "Updated",
                "content": "Updated Content",
                "category": self.category.id,
                "is_premium": False,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.post.refresh_from_db()

        self.assertEqual(
            self.post.title,
            "Updated",
        )

    def test_admin_can_patch(self):
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            reverse(
                "api:post-detail",
                kwargs={"post_id": self.post.id},
            ),
            {
                "title": "Patched",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.post.refresh_from_db()

        self.assertEqual(
            self.post.title,
            "Patched",
        )

    def test_admin_can_delete(self):
        self.client.force_authenticate(self.admin)

        response = self.client.delete(
            reverse(
                "api:post-detail",
                kwargs={"post_id": self.post.id},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Post.objects.filter(id=self.post.id).exists()
        )

    def test_normal_user_cannot_update(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(
            reverse(
                "api:post-detail",
                kwargs={"post_id": self.post.id},
            ),
            {
                "title": "Hack",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_normal_user_cannot_delete(self):
        self.client.force_authenticate(self.user)

        response = self.client.delete(
            reverse(
                "api:post-detail",
                kwargs={"post_id": self.post.id},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )