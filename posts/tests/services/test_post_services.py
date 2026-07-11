import pytest

from posts.models import (
    Comments,
    FavoritPost,
    Post,
)

from posts.services.post import (
    create_comment,
    create_post,
    create_favorit_post,
    delete_comment_post,
    delete_favorit_post,
)

from posts.tests.factory.posts import (
    CommentFactory,
    FavoritePostFactory,
    PostFactory,
)
from posts.tests.factory.category import CategoryFactory

from users.tests.factories.users import BaseUserFactory


pytestmark = pytest.mark.django_db


class TestCreateComment:

    def test_create_comment_success(self):

        user = BaseUserFactory()

        post = PostFactory()

        comment = create_comment(
            user=user,
            post_id=post.id,
            content="hello world",
        )

        assert isinstance(comment, Comments)

        assert comment.author == user

        assert comment.post == post

        assert comment.content == "hello world"

        assert Comments.objects.count() == 1


class TestCreatePost:

    def test_create_post_success(self):

        author = BaseUserFactory()

        category = CategoryFactory()

        post = create_post(
            author=author,
            title="django",
            content="django content",
            image=None,
            video=None,
            is_premium=False,
            category=category,
        )

        assert isinstance(post, Post)

        assert post.author == author

        assert post.category == category

        assert post.title == "django"

        assert post.content == "django content"

        assert post.is_premium is False


class TestCreateFavoritePost:

    def test_create_favorite_success(self):

        user = BaseUserFactory()

        post = PostFactory()

        favorite = create_favorit_post(
            user=user,
            post_id=post.id,
        )

        assert isinstance(favorite, FavoritPost)

        assert favorite.user == user

        assert favorite.post == post

        assert FavoritPost.objects.count() == 1


class TestDeleteComment:

    def test_delete_comment(self):

        comment = CommentFactory()

        assert Comments.objects.count() == 1

        delete_comment_post(
            user=comment.author,
            post_id=comment.post.id,
        )

        assert Comments.objects.count() == 0


    def test_delete_only_user_comment(self):

        post = PostFactory()

        user1 = BaseUserFactory()

        user2 = BaseUserFactory()

        CommentFactory(
            author=user1,
            post=post,
        )

        CommentFactory(
            author=user2,
            post=post,
        )

        delete_comment_post(
            user=user1,
            post_id=post.id,
        )

        assert Comments.objects.count() == 1

        assert Comments.objects.first().author == user2


class TestDeleteFavorite:

    def test_delete_favorite(self):

        favorite = FavoritePostFactory()

        assert FavoritPost.objects.count() == 1

        delete_favorit_post(
            user=favorite.user,
            post_id=favorite.post.id,
        )

        assert FavoritPost.objects.count() == 0


    def test_delete_only_user_favorite(self):

        post = PostFactory()

        user1 = BaseUserFactory()

        user2 = BaseUserFactory()

        FavoritePostFactory(
            user=user1,
            post=post,
        )

        FavoritePostFactory(
            user=user2,
            post=post,
        )

        delete_favorit_post(
            user=user1,
            post_id=post.id,
        )

        assert FavoritPost.objects.count() == 1

        assert FavoritPost.objects.first().user == user2