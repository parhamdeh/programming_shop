from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import BaseUserModel
from posts.models import Subscription


class SubscriptionListCreateAPIViewTest(APITestCase):

    def setUp(self):
        self.admin = BaseUserModel.objects.create_superuser(
            username="admin",
            phone="09111111111",
            password="12345678",
        )

        self.user = BaseUserModel.objects.create_user(
            username="user",
            phone="09999999999",
            password="12345678",
        )

        self.subscription = Subscription.objects.create(
            name="VIP",
            price=100000,
            limit_days=30,
        )

    def test_guest_cannot_get(self):
        response = self.client.get(
            reverse("api:subscription-list-create")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_user_can_get(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(
            reverse("api:subscription-list-create")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(len(response.data), 1)

    def test_admin_can_create(self):
        self.client.force_authenticate(self.admin)

        response = self.client.post(
            reverse("api:subscription-list-create"),
            {
                "name": "Premium",
                "price": 250000,
                "limit_days": 90,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Subscription.objects.filter(name="Premium").exists()
        )

    def test_normal_user_cannot_create(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            reverse("api:subscription-list-create"),
            {
                "name": "Premium",
                "price": 250000,
                "limit_days": 90,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )