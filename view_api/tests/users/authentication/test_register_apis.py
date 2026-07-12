from unittest.mock import patch, MagicMock

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


class RegisterUserAPIViewTest(APITestCase):

    @patch("view_api.apps_api.users.authentication.register_user_apis.delete_otp_task.apply_async")
    @patch("view_api.apps_api.users.authentication.register_user_apis.send_otp_task.delay")
    @patch("view_api.apps_api.users.authentication.register_user_apis.create_otp_code")
    def test_register_send_otp(
        self,
        mock_create_otp,
        mock_send_task,
        mock_delete_task,
    ):
        otp = MagicMock()
        otp.id = 1
        otp.code = "123456"
        mock_create_otp.return_value = otp

        response = self.client.post(
            reverse("api:register"),
            {
                "username": "parham",
                "phone": "09123456789",
                "password": "12345678",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        mock_create_otp.assert_called_once()
        mock_send_task.assert_called_once_with(
            phone="09123456789",
            code="123456",
        )
        mock_delete_task.assert_called_once()

        self.assertIn("register_data", self.client.session)