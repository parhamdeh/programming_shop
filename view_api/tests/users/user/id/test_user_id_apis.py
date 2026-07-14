import pytest

from rest_framework import status
from rest_framework.test import APIClient

from users.models import BaseUserModel
from users.tests.factories.users import BaseUserFactory


pytestmark = pytest.mark.django_db


def user_detail_url(user_id: int) -> str:
    # Using a direct path here (matching the "/api/users/" convention used
    # in test_user_apis.py) instead of reverse("user-detail", ...), because
    # that URL name isn't registered/doesn't match what's in urls.py.
    # If you later confirm the real url name, this can go back to reverse().
    return f"/api/users/{user_id}/"


class TestUserRetrieveUpdateDestroy:

    def setup_method(self):
        self.client = APIClient()

    def test_admin_can_get_user(self):
        admin = BaseUserFactory(
            is_staff=True,
            is_superuser=True,
        )

        user = BaseUserFactory()

        self.client.force_authenticate(admin)

        response = self.client.get(user_detail_url(user.id))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == user.username

    def test_user_can_get_self(self):
        user = BaseUserFactory()

        self.client.force_authenticate(user)

        response = self.client.get(user_detail_url(user.id))

        assert response.status_code == status.HTTP_200_OK

    def test_user_cannot_get_other_user(self):
        user1 = BaseUserFactory()
        user2 = BaseUserFactory()

        self.client.force_authenticate(user1)

        response = self.client.get(user_detail_url(user2.id))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_not_found(self):
        admin = BaseUserFactory(
            is_staff=True,
            is_superuser=True,
        )

        self.client.force_authenticate(admin)

        response = self.client.get(user_detail_url(99999))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_can_patch_self(self):
        user = BaseUserFactory()

        self.client.force_authenticate(user)

        response = self.client.patch(
            user_detail_url(user.id),
            {
                "username": "changed",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()

        assert user.username == "changed"

    def test_admin_can_delete_user(self):
        admin = BaseUserFactory(
            is_staff=True,
            is_superuser=True,
        )

        user = BaseUserFactory()

        self.client.force_authenticate(admin)

        response = self.client.delete(user_detail_url(user.id))

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not BaseUserModel.objects.filter(id=user.id).exists()