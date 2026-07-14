from unittest.mock import patch, MagicMock

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


class RegisterUserAPIViewTest(APITestCase):


    @patch(
        "view_api.apps_api.users.authentication.register_user_apis.delete_otp_task.apply_async"
    )
    @patch(
        "view_api.apps_api.users.authentication.register_user_apis.send_otp_task.delay"
    )
    @patch(
        "view_api.apps_api.users.authentication.register_user_apis.create_otp_code"
    )
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
                "username":"parham22",
                "phone":"09913698103",
                "password":"12345678pP#",
                "confirm_password":"12345678pP#"
            },
            format="json",
        )


        assert response.status_code == status.HTTP_200_OK

        print(response.data)
        assert response.data["detail"] == (
            "Verification code sent successfully."
        )


        mock_create_otp.assert_called_once_with(
            phone="09913698103"
        )


        mock_send_task.assert_called_once_with(
            phone="09913698103",
            code="123456",
        )


        mock_delete_task.assert_called_once_with(
            args=[1],
            countdown=120,
        )


        assert "register_data" in self.client.session