import pytest

from users.selectors.user_selector import (
    get_users_list,
    get_user_by_id,
)

from users.tests.factories.users import BaseUserFactory


pytestmark = pytest.mark.django_db


class TestGetUsersList:

    def test_return_all_users(self):

        BaseUserFactory.create_batch(5)

        users = get_users_list()

        assert users.count() == 5


    def test_return_queryset(self):

        users = get_users_list()

        assert hasattr(users, "filter")


class TestGetUserById:

    def test_get_existing_user(self):

        user = BaseUserFactory()

        result = get_user_by_id(
            user_id=user.id,
        )

        assert result.exists()

        assert result.first() == user


    def test_non_existing_user(self):

        result = get_user_by_id(
            user_id=9999,
        )

        assert result.count() == 0