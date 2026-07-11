import pytest

from users.models import BaseUserModel, UserProfileModel
from users.services.user_services import (
    create_user,
    create_profile,
    register,
)

from users.tests.factories.users import (
    BaseUserFactory,
)
from posts.tests.factory.subscription import SubscriptionFactory

pytestmark = pytest.mark.django_db


class TestCreateUser:

    def test_create_user_success(self):

        user = create_user(
            username="parham",
            phone="09123456789",
            password="Admin12345",
        )

        assert isinstance(user, BaseUserModel)
        assert user.username == "parham"
        assert str(user.phone) == "+989123456789"
        assert user.check_password("Admin12345")


class TestCreateProfile:

    def test_create_profile_without_subscription(self):

        user = BaseUserFactory()

        profile = create_profile(
            user=user,
            subscription=None,
        )

        assert isinstance(profile, UserProfileModel)
        assert profile.user == user
        assert profile.subscription is None


    def test_create_profile_with_subscription(self):

        user = BaseUserFactory()
        subscription = SubscriptionFactory()

        profile = create_profile(
            user=user,
            subscription=subscription,
        )

        assert profile.subscription == subscription


class TestRegister:

    def test_register_success(self):

        subscription = SubscriptionFactory()

        user = register(
            username="parham",
            phone="09123456789",
            password="Admin12345",
            subscription=subscription,
            user=None,
        )

        assert BaseUserModel.objects.count() == 1

        assert UserProfileModel.objects.count() == 1

        profile = UserProfileModel.objects.get()

        assert profile.user == user
        assert profile.subscription == subscription