from unittest.mock import patch

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import BaseUserModel
from posts.models import Subscription


class SubscriptionPaymentAPIViewTest(APITestCase):

    def setUp(self):
        self.user = BaseUserModel.objects.create_user(
            phone="09123456789",
            username="parham",
            password="12345678",
        )

        self.subscription = Subscription.objects.create(
            name="VIP",
            price=100000,
            limit_days=30,
        )

        self.url = reverse(
            "api:subscription-pay",
            kwargs={
                "subscription_id": self.subscription.id,
            },
        )

    @patch(
        "view_api.apps_api.posts.pay.pay_apis.requests.post"
    )
    def test_create_payment_success(self, mock_post):

        self.client.force_authenticate(self.user)

        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "data": {
                "code": 100,
                "authority": "TESTAUTHORITY",
            }
        }

        response = self.client.post(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            "payment_url",
            response.data,
        )

        self.assertIn(
            "TESTAUTHORITY",
            response.data["payment_url"],
        )

    def test_subscription_not_found(self):

        self.client.force_authenticate(self.user)

        response = self.client.post(
            reverse(
                "api:subscription-pay",
                kwargs={
                    "subscription_id": 999,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    @patch(
        "view_api.apps_api.posts.pay.pay_apis.requests.post"
    )
    def test_gateway_timeout(self, mock_post):

        import requests

        self.client.force_authenticate(self.user)

        mock_post.side_effect = requests.exceptions.Timeout()

        response = self.client.post(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    def test_guest_cannot_create_payment(self):

        response = self.client.post(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )