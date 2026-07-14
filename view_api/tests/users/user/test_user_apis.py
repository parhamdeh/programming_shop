import pytest

from rest_framework import status
from rest_framework.test import APIClient

from users.tests.factories.users import BaseUserFactory


pytestmark = pytest.mark.django_db


class TestUserListCreateAPIView:

    def setup_method(self):
        self.client = APIClient()

    # -----------------------------
    # GET
    # -----------------------------

    def test_admin_can_get_users(self):
        admin = BaseUserFactory(
            is_staff=True,
            is_superuser=True,
        )

        BaseUserFactory.create_batch(5)

        self.client.force_authenticate(admin)

        response = self.client.get("/api/users/")

        assert response.status_code == status.HTTP_200_OK

        assert "results" in response.data
        assert response.data["count"] == 6

    def test_anonymous_cannot_get_users(self):
        response = self.client.get("/api/users/")

        # DRF returns 401 (not 403) for genuinely unauthenticated requests
        # whenever authentication classes are configured on the view -
        # this is standard DRF behavior (see APIView.permission_denied),
        # not a bug. Only *authenticated-but-unauthorized* requests get 403
        # (see test_normal_user_cannot_get_users below).
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_normal_user_cannot_get_users(self):
        user = BaseUserFactory()

        self.client.force_authenticate(user)

        response = self.client.get("/api/users/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    # -----------------------------
    # POST
    # -----------------------------

    def test_admin_can_create_user(self):
        admin = BaseUserFactory(
            is_staff=True,
            is_superuser=True,
        )

        self.client.force_authenticate(admin)

        response = self.client.post(
            "/api/users/",
            {
                "username": "parham",
                "phone": "+989111111111",
                "password": "Admin123456",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        assert response.data["username"] == "parham"

    def test_normal_user_cannot_create_user(self):
        user = BaseUserFactory()

        self.client.force_authenticate(user)

        response = self.client.post(
            "/api/users/",
            {
                "username": "test",
                "phone": "+989222222222",
                "password": "12345678",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_invalid_data_returns_400(self):
        admin = BaseUserFactory(
            is_staff=True,
            is_superuser=True,
        )

        self.client.force_authenticate(admin)

        response = self.client.post(
            "/api/users/",
            {},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST