from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import BaseUserModel
from posts.models import Category


class CategoryRetrieveUpdateDestroyAPIViewTest(APITestCase):

    def setUp(self):
        self.admin = BaseUserModel.objects.create_superuser(
            phone="09111111111",
            username="admin",
            password="12345678",
        )

        self.user = BaseUserModel.objects.create_user(
            phone="09999999999",
            username="user",
            password="12345678",
        )

        self.category = Category.objects.create(
            name="Python",
        )

    def test_guest_cannot_get_category(self):
        response = self.client.get(
            reverse(
                "api:category-detail",
                kwargs={"category_id": self.category.id},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_get_category(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(
            reverse(
                "api:category-detail",
                kwargs={"category_id": self.category.id},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            self.category.id,
        )

        self.assertEqual(
            response.data["name"],
            "Python",
        )

    def test_get_not_found(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(
            reverse(
                "api:category-detail",
                kwargs={"category_id": 999},
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
                "api:category-detail",
                kwargs={"category_id": self.category.id},
            ),
            {
                "name": "Django",
                "parent": None,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.category.refresh_from_db()

        self.assertEqual(
            self.category.name,
            "Django",
        )

    def test_admin_can_patch(self):
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            reverse(
                "api:category-detail",
                kwargs={"category_id": self.category.id},
            ),
            {
                "name": "DRF",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.category.refresh_from_db()

        self.assertEqual(
            self.category.name,
            "DRF",
        )

    def test_admin_can_delete(self):
        self.client.force_authenticate(self.admin)

        response = self.client.delete(
            reverse(
                "api:category-detail",
                kwargs={"category_id": self.category.id},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Category.objects.filter(id=self.category.id).exists()
        )

    def test_normal_user_cannot_put(self):
        self.client.force_authenticate(self.user)

        response = self.client.put(
            reverse(
                "api:category-detail",
                kwargs={"category_id": self.category.id},
            ),
            {
                "name": "Hack",
                "parent": None,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_normal_user_cannot_patch(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(
            reverse(
                "api:category-detail",
                kwargs={"category_id": self.category.id},
            ),
            {
                "name": "Hack",
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
                "api:category-detail",
                kwargs={"category_id": self.category.id},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )