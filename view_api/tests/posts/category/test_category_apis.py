from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.tests.factories.users import BaseUserFactory
from posts.tests.factory.category import CategoryFactory


class CategoryListCreateAPIViewTest(APITestCase):

    def setUp(self):
        self.admin = BaseUserFactory(is_staff=True)
        self.user = BaseUserFactory()

    def test_get_categories(self):
        CategoryFactory.create_batch(3)

        self.client.force_authenticate(self.user)

        response = self.client.get(
            reverse("api:category-list-create"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            3,
        )

    def test_admin_can_create_category(self):
        self.client.force_authenticate(self.admin)

        response = self.client.post(
            reverse("api:category-list-create"),
            {
                "name": "Python",
                "parent": None,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["name"],
            "Python",
        )

    def test_normal_user_cannot_create_category(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            reverse("api:category-list-create"),
            {
                "name": "Python",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_guest_cannot_create_category(self):
        response = self.client.post(
            reverse("api:category-list-create"),
            {
                "name": "Python",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )