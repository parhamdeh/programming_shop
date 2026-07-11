import pytest

from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from users.models import OtpCode
from users.tests.factories.users import BaseUserFactory


pytestmark = pytest.mark.django_db


class TestVerifyOtpView:

    def test_get_returns_page(self, client):
        user = BaseUserFactory()

        response = client.get(
            reverse(
                "users:code",
                kwargs={"user_id": user.id},
            )
        )

        assert response.status_code == 200
        assert "form" in response.context

    def test_verify_valid_code(self, client):
        user = BaseUserFactory()

        otp = OtpCode.objects.create(
            user=user,
            code="123456",
        )

        response = client.post(
            reverse(
                "users:code",
                kwargs={"user_id": user.id},
            ),
            {
                "code": "123456",
            },
            follow=True,
        )

        assert response.status_code == 200
        assert "_auth_user_id" in client.session
        assert not OtpCode.objects.filter(id=otp.id).exists()

    def test_invalid_code(self, client):
        user = BaseUserFactory()

        OtpCode.objects.create(
            user=user,
            code="123456",
        )

        response = client.post(
            reverse(
                "users:code",
                kwargs={"user_id": user.id},
            ),
            {
                "code": "999999",
            },
            follow=True,
        )

        assert response.status_code == 200
        assert "_auth_user_id" not in client.session

    def test_expired_code(self, client):
        user = BaseUserFactory()

        otp = OtpCode.objects.create(
            user=user,
            code="123456",
        )

        otp.created_at = timezone.now() - timedelta(minutes=3)
        otp.save(update_fields=["created_at"])

        response = client.post(
            reverse(
                "users:code",
                kwargs={"user_id": user.id},
            ),
            {
                "code": "123456",
            },
            follow=True,
        )

        assert response.status_code == 200
        assert not OtpCode.objects.filter(id=otp.id).exists()
        assert "_auth_user_id" not in client.session

    def test_used_code_is_invalid(self, client):
        user = BaseUserFactory()

        OtpCode.objects.create(
            user=user,
            code="123456",
            is_used=True,
        )

        response = client.post(
            reverse(
                "users:code",
                kwargs={"user_id": user.id},
            ),
            {
                "code": "123456",
            },
            follow=True,
        )

        assert response.status_code == 200
        assert "_auth_user_id" not in client.session

    def test_invalid_form(self, client):
        user = BaseUserFactory()

        response = client.post(
            reverse(
                "users:code",
                kwargs={"user_id": user.id},
            ),
            {
                "code": "",
            },
        )

        assert response.status_code == 200
        assert "form" in response.context

    def test_invalid_user_returns_404(self, client):
        response = client.post(
            reverse(
                "users:code",
                kwargs={"user_id": 999999},
            ),
            {
                "code": "123456",
            },
        )

        assert response.status_code == 404