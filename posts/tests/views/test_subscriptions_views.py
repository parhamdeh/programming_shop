import pytest

from django.urls import reverse

from posts.models import Subscription
from posts.tests.factory.subscription import SubscriptionFactory
from users.tests.factories.users import BaseUserFactory


pytestmark = pytest.mark.django_db


class TestCreateSubscriptionView:

    def test_anonymous_redirects_to_login(self, client):
        response = client.get(reverse("posts:create-subscription"))

        assert response.status_code == 302
        assert response.url == reverse("users:login")

    def test_normal_user_redirects_home(self, client):
        user = BaseUserFactory()

        client.force_login(user)

        response = client.get(reverse("posts:create-subscription"))

        assert response.status_code == 302
        assert response.url == reverse("home:home")

    def test_staff_can_open_page(self, client):
        staff = BaseUserFactory(is_staff=True)

        client.force_login(staff)

        response = client.get(reverse("posts:create-subscription"))

        assert response.status_code == 200
        assert "form" in response.context

    def test_staff_can_create_subscription(self, client):
        staff = BaseUserFactory(is_staff=True)

        client.force_login(staff)

        response = client.post(
            reverse("posts:create-subscription"),
            {
                "name": "Gold",
                "price": 50000,
                "limit_days": 30,
            },
        )

        assert response.status_code == 302

        assert Subscription.objects.filter(
            name="Gold"
        ).exists()

    def test_invalid_form_returns_template(self, client):
        staff = BaseUserFactory(is_staff=True)

        client.force_login(staff)

        response = client.post(
            reverse("posts:create-subscription"),
            {}
        )

        assert response.status_code == 200
        assert "form" in response.context


class TestSubscriptionDetailView:

    def test_login_required(self, client):
        subscription = SubscriptionFactory()

        response = client.get(
            reverse(
                "posts:subscription-detail",
                kwargs={
                    "subscription_id": subscription.id,
                },
            )
        )

        assert response.status_code == 302

    def test_detail_page(self, client):
        user = BaseUserFactory()

        subscription = SubscriptionFactory()

        client.force_login(user)

        response = client.get(
            reverse(
                "posts:subscription-detail",
                kwargs={
                    "subscription_id": subscription.id,
                },
            )
        )

        assert response.status_code == 200
        assert response.context["category"] == subscription

    def test_invalid_subscription(self, client):
        user = BaseUserFactory()

        client.force_login(user)

        with pytest.raises(Exception):
            client.get(
                reverse(
                    "posts:subscription-detail",
                    kwargs={
                        "subscription_id": 99999,
                    },
                )
            )