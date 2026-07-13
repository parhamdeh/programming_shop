from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import BaseUserModel
from posts.models import Subscription


class SubscriptionRetrieveUpdateDestroyAPIViewTest(APITestCase):

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
            reverse(
                "api:subscription-detail",
                kwargs={"subscription_id": self.subscription.id},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_get_subscription(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(
            reverse(
                "api:subscription-detail",
                kwargs={"subscription_id": self.subscription.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.subscription.id)
        self.assertEqual(response.data["name"], "VIP")

    def test_get_not_found(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(
            reverse(
                "api:subscription-detail",
                kwargs={"subscription_id": 999},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_admin_can_put(self):
        self.client.force_authenticate(self.admin)

        response = self.client.put(
            reverse(
                "api:subscription-detail",
                kwargs={"subscription_id": self.subscription.id},
            ),
            {
                "name": "Premium",
                "price": 250000,
                "limit_days": 90,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.subscription.refresh_from_db()

        self.assertEqual(self.subscription.name, "Premium")
        self.assertEqual(self.subscription.price, 250000)
        self.assertEqual(self.subscription.limit_days, 90)

    def test_admin_can_patch(self):
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            reverse(
                "api:subscription-detail",
                kwargs={"subscription_id": self.subscription.id},
            ),
            {
                "price": 500000,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.subscription.refresh_from_db()

        self.assertEqual(self.subscription.price, 500000)

    def test_admin_can_delete(self):
        self.client.force_authenticate(self.admin)

        response = self.client.delete(
            reverse(
                "api:subscription-detail",
                kwargs={"subscription_id": self.subscription.id},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Subscription.objects.filter(
                id=self.subscription.id,
            ).exists()
        )

    def test_normal_user_cannot_put(self):
        self.client.force_authenticate(self.user)

        response = self.client.put(
            reverse(
                "api:subscription-detail",
                kwargs={"subscription_id": self.subscription.id},
            ),
            {
                "name": "Hack",
                "price": 1,
                "limit_days": 1,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_normal_user_cannot_patch(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(
            reverse(
                "api:subscription-detail",
                kwargs={"subscription_id": self.subscription.id},
            ),
            {
                "price": 1,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_normal_user_cannot_delete(self):
        self.client.force_authenticate(self.user)

        response = self.client.delete(
            reverse(
                "api:subscription-detail",
                kwargs={"subscription_id": self.subscription.id},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )