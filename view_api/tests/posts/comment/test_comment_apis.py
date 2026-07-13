from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.tests.factories.users import BaseUserFactory
from posts.tests.factory.posts import PostFactory
from posts.models import Comments


class PostCommentAPIViewTest(APITestCase):

    def setUp(self):
        self.user = BaseUserFactory()
        self.client.force_authenticate(self.user)

        self.post = PostFactory()

    def test_get_comments(self):
        Comments.objects.create(
            author=self.user,
            post=self.post,
            content="first comment",
        )

        response = self.client.get(
            reverse(
                "api:post-comments",
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

    def test_create_comment(self):
        response = self.client.post(
            reverse(
                "api:post-comments",
                kwargs={"post_id": self.post.id},
            ),
            {
                "content": "Nice post",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Comments.objects.filter(
                author=self.user,
                post=self.post,
                content="Nice post",
            ).exists()
        )

    def test_delete_comment(self):
        Comments.objects.create(
            author=self.user,
            post=self.post,
            content="comment",
        )

        response = self.client.delete(
            reverse(
                "api:post-comments",
                kwargs={"post_id": self.post.id},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Comments.objects.filter(
                author=self.user,
                post=self.post,
            ).exists()
        )

    def test_anonymous_user_cannot_comment(self):
        self.client.force_authenticate(None)

        response = self.client.post(
            reverse(
                "api:post-comments",
                kwargs={"post_id": self.post.id},
            ),
            {
                "content": "hello",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )