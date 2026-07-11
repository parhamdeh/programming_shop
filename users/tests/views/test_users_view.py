import pytest

from unittest.mock import patch

from django.urls import reverse

from users.models import OtpCode
from users.tests.factories.users import BaseUserFactory


pytestmark = pytest.mark.django_db

class TestRegisterView:

    def test_get_register_page(self, client):

        response = client.get(
            reverse("users:register")
        )

        assert response.status_code == 200


    @patch("users.views.user_view.send_otp_task.delay")
    @patch("users.views.user_view.delete_otp_task.apply_async")
    def test_register_user(
        self,
        delete_task,
        send_task,
        client,
    ):

        data = {
            "username": "parham",
            "phone": "09123456789",
            "password": "Admin12345#",
            "confirm_password": "Admin12345#",
        }

        response = client.post(
            reverse("users:register"),
            data=data,
        )
        # print(response.context["form"].errors)  
        assert response.status_code == 302

        assert BaseUserFactory._meta.model.objects.filter(
            username="parham"
        ).exists()

        otp = OtpCode.objects.get(
            user__username="parham"
        )

        send_task.assert_called_once()

        delete_task.assert_called_once()

        assert otp.code


class TestLoginView:

    def test_get_login(self, client):

        response = client.get(
            reverse("users:login")
        )

        assert response.status_code == 200


    def test_login_success(
        self,
        client,
    ):

        user = BaseUserFactory(
            password="Admin12345"
        )

        response = client.post(
            reverse("users:login"),
            {
                "username": user.username,
                "password": "Admin12345",
            },
        )

        assert response.status_code == 302


    def test_login_invalid_password(
        self,
        client,
    ):

        user = BaseUserFactory(
            password="Admin12345"
        )

        response = client.post(
            reverse("users:login"),
            {
                "username": user.username,
                "password": "wrong",
            },
        )

        assert response.status_code == 200


class TestLogoutView:

    def test_logout(
        self,
        client,
    ):

        user = BaseUserFactory()

        client.force_login(user)

        response = client.get(
            reverse("users:logout")
        )

        assert response.status_code == 302