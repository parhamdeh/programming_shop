import pytest

from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

from users.models import BaseUserModel
from users.tests.factories.users import BaseUserFactory


pytestmark = pytest.mark.django_db


class TestUserRetrieveUpdateDestroy:

    def setup_method(self):
        self.client = APIClient()

        self.admin = BaseUserFactory(
            is_staff=True,
            is_superuser=True,
        )

        self.client.force_authenticate(self.admin)

    def test_get_user(self):

        user = BaseUserFactory()

        response = self.client.get(
            reverse(
                "user-detail",
                kwargs={
                    "user_id": user.id,
                },
            )
        )

        assert response.status_code == status.HTTP_200_OK

        assert response.data["username"] == user.username

    def test_get_not_found(self):

        response = self.client.get(
            reverse(
                "user-detail",
                kwargs={
                    "user_id": 99999,
                },
            )
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_put_user(self):

        user = BaseUserFactory()

        response = self.client.put(
            reverse(
                "user-detail",
                kwargs={
                    "user_id": user.id,
                },
            ),
            {
                "username": "new_username",
                "phone": "+989111111111",
                "password": "Admin123456",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()

        assert user.username == "new_username"

    def test_patch_user(self):

        user = BaseUserFactory()

        response = self.client.patch(
            reverse(
                "user-detail",
                kwargs={
                    "user_id": user.id,
                },
            ),
            {
                "username": "patched",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()

        assert user.username == "patched"

    def test_delete_user(self):

        user = BaseUserFactory()

        response = self.client.delete(
            reverse(
                "user-detail",
                kwargs={
                    "user_id": user.id,
                },
            )
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not BaseUserModel.objects.filter(
            id=user.id
        ).exists()