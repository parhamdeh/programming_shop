from unittest.mock import patch

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import BaseUserModel
from posts.models import Subscription, UserSubscription


class SubscriptionVerifyAPIViewTest(APITestCase):

    def setUp(self):

        self.user = BaseUserModel.objects.create_user(
            phone="09111111111",
            username="user",
            password="12345678",
        )

        self.subscription = Subscription.objects.create(
            name="VIP",
            price=50000,
            limit_days=30,
        )

        self.url = reverse(
            "api:subscription-verify",
        )

    @patch(
        "view_api.apps_api.posts.pay.pay_apis.requests.post"
    )
    def test_verify_success(self, mock_post):

        self.client.force_authenticate(self.user)

        session = self.client.session
        session["subscription"] = {
            "subscription_id": self.subscription.id,
        }
        session.save()

        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "data": {
                "code": 100,
                "ref_id": 987654321,
            }
        }

        response = self.client.get(
            self.url,
            {
                "Status": "OK",
                "Authority": "AUTH123",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"],
        )

        self.assertEqual(
            response.data["ref_id"],
            987654321,
        )

        self.assertTrue(
            UserSubscription.objects.filter(
                user=self.user,
            ).exists()
        )

    @patch(
        "view_api.apps_api.posts.pay.pay_apis.requests.post"
    )
    def test_verify_failed(self, mock_post):

        self.client.force_authenticate(self.user)

        session = self.client.session
        session["subscription"] = {
            "subscription_id": self.subscription.id,
        }
        session.save()

        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "data": {
                "code": 101,
            }
        }

        response = self.client.get(
            self.url,
            {
                "Status": "OK",
                "Authority": "AUTH123",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(
            response.data["success"],
        )

    def test_session_expired(self):

        self.client.force_authenticate(self.user)

        response = self.client.get(
            self.url,
            {
                "Status": "OK",
                "Authority": "AUTH123",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_guest_cannot_verify(self):

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )