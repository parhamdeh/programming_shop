from unittest.mock import patch, MagicMock

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from config import settings
from django.test import override_settings


@override_settings(REST_FRAMEWORK={
    **settings.REST_FRAMEWORK,
    "DEFAULT_THROTTLE_CLASSES": [],
})
class VerifyOtpAPIViewTest(APITestCase):


    @patch(
        "view_api.apps_api.users.authentication.register_user_apis.RefreshToken"
    )
    @patch(
        "view_api.apps_api.users.authentication.register_user_apis.register"
    )
    @patch(
        "view_api.apps_api.users.authentication.register_user_apis.OtpCode.objects"
    )
    def test_verify_success(
        self,
        mock_otp_objects,
        mock_register,
        mock_refresh,
    ):


        session = self.client.session

        session["register_data"] = {
            "username":"parham",
            "phone":"09123456789",
            "password":"12345678",
        }

        session.save()


        otp = MagicMock()
        otp.is_expired.return_value = False


        mock_otp_objects.filter.return_value.order_by.return_value.first.return_value = otp



        user = MagicMock()

        mock_register.return_value = user



        token = MagicMock()

        token.access_token = "access-token"


        mock_refresh.for_user.return_value = token



        response = self.client.post(
            reverse("api:verify-code"),
            {
                "code":"123456"
            },
            format="json",
        )


        assert response.status_code == status.HTTP_201_CREATED


        mock_register.assert_called_once()


        assert "refresh" in response.data
        assert "access" in response.data



    def test_verify_without_session(self):


        response = self.client.post(
            reverse("api:verify-code"),
            {
                "code":"123456"
            },
            format="json",
        )


        assert response.status_code == status.HTTP_400_BAD_REQUEST



    @patch(
        "view_api.apps_api.users.authentication.register_user_apis.OtpCode.objects"
    )
    def test_verify_invalid_code(
        self,
        mock_otp_objects,
    ):


        session = self.client.session

        session["register_data"] = {
            "username":"parham",
            "phone":"09123456789",
            "password":"12345678",
        }

        session.save()



        mock_otp_objects.filter.return_value.order_by.return_value.first.return_value = None



        response = self.client.post(
            reverse("api:verify"),
            {
                "code":"999999"
            },
            format="json",
        )


        assert response.status_code == status.HTTP_400_BAD_REQUEST



    @patch(
        "view_api.apps_api.users.authentication.register_user_apis.OtpCode.objects"
    )
    def test_verify_expired_code(
        self,
        mock_otp_objects,
    ):


        session = self.client.session

        session["register_data"] = {
            "username":"parham",
            "phone":"09123456789",
            "password":"12345678",
        }

        session.save()



        otp = MagicMock()

        otp.is_expired.return_value = True


        mock_otp_objects.filter.return_value.order_by.return_value.first.return_value = otp



        response = self.client.post(
            reverse("api:verify-code"),
            {
                "code":"123456"
            },
            format="json",
        )


        assert response.status_code == status.HTTP_400_BAD_REQUEST