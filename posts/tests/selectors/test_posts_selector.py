import pytest

from posts.models import FavoritPost

from posts.selectors.post_detail import (
    get_post_detail,
    get_related_posts,
    get_post_by_id,
    check_favorit,
    check_post_is_premium,
)
from posts.tests.factory.category import CategoryFactory
from posts.tests.factory.subscription import SubscriptionFactory, UserSubscriptionFactory
from posts.tests.factory.posts import (
    FavoritePostFactory,
    PostFactory,
)

from users.tests.factories.users import BaseUserFactory


pytestmark = pytest.mark.django_db


class TestGetPostDetail:

    def test_get_post_detail_returns_post(self):
        post = PostFactory()

        result = get_post_detail(post.id)

        assert result == post

    def test_get_post_by_id(self):
        post = PostFactory()

        result = get_post_by_id(post.id).first()

        assert result == post


class TestGetRelatedPosts:

    def test_returns_related_posts(self):
        category = CategoryFactory()

        post = PostFactory(category=category)

        related1 = PostFactory(category=category)

        related2 = PostFactory(category=category)

        PostFactory()

        result = get_related_posts(post)

        assert related1 in result
        assert related2 in result
        assert post not in result

    def test_returns_max_five_posts(self):
        category = CategoryFactory()

        post = PostFactory(category=category)

        for _ in range(10):
            PostFactory(category=category)

        result = get_related_posts(post)

        assert len(result) == 5


class TestCheckFavorit:

    def test_returns_true_when_post_is_favorite(self):
        user = BaseUserFactory()

        post = PostFactory()

        FavoritePostFactory(
            user=user,
            post=post,
        )

        assert check_favorit(
            user=user,
            post=post,
        ) is True

    def test_returns_false_when_post_is_not_favorite(self):
        user = BaseUserFactory()

        post = PostFactory()

        assert check_favorit(
            user=user,
            post=post,
        ) is False


class TestPremiumPosts:

    def test_author_can_access_premium_post(self):
        author = BaseUserFactory()

        post = PostFactory(
            author=author,
            is_premium=True,
        )

        assert check_post_is_premium(
            post_id=post.id,
            user_id=author.id,
        ) is True

    def test_free_post_is_accessible(self):
        user = BaseUserFactory()

        post = PostFactory(
            is_premium=False,
        )

        assert check_post_is_premium(
            post_id=post.id,
            user_id=user.id,
        ) is True

    def test_premium_post_with_subscription(self):
        user = BaseUserFactory()

        subscription = SubscriptionFactory()

        UserSubscriptionFactory(
            user=user,
            subscription=subscription,
        )

        post = PostFactory(
            is_premium=True,
        )

        assert check_post_is_premium(
            post_id=post.id,
            user_id=user.id,
        ) is True

    def test_premium_post_without_subscription(self):
        user = BaseUserFactory()

        post = PostFactory(
            is_premium=True,
        )

        assert check_post_is_premium(
            post_id=post.id,
            user_id=user.id,
        ) is False