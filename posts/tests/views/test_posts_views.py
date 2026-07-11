import pytest

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from posts.models import (
    Post,
    Comments,
    FavoritPost,
)

from posts.tests.factory.posts import PostFactory
from posts.tests.factory.category import CategoryFactory
from users.tests.factories.users import BaseUserFactory

import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


def generate_test_image(name="image.jpg", size=(100, 100), color="red"):
    file = io.BytesIO()
    image = Image.new("RGB", size, color=color)
    image.save(file, "JPEG")
    file.seek(0)
    return SimpleUploadedFile(name, file.read(), content_type="image/jpeg")


pytestmark = pytest.mark.django_db


# ------------------------------------------------------------------
# CreatePostView
# ------------------------------------------------------------------

class TestCreatePostView:

    def test_get_anonymous_redirects_login(self, client):
        response = client.get(reverse("posts:create-post"))

        assert response.status_code == 302
        assert response.url == reverse("users:login")

    def test_get_normal_user_redirects_home(self, client):
        user = BaseUserFactory()

        client.force_login(user)

        response = client.get(reverse("posts:create-post"))

        assert response.status_code == 302
        assert response.url == reverse("home:home")

    def test_get_staff_returns_template(self, client):
        staff = BaseUserFactory(is_staff=True)

        client.force_login(staff)

        response = client.get(reverse("posts:create-post"))

        assert response.status_code == 200
        assert "form" in response.context

    def test_post_valid_data_creates_post(self, client):
        staff = BaseUserFactory(is_staff=True)
        category = CategoryFactory()

        client.force_login(staff)

        image = generate_test_image()  
        response = client.post(
            reverse("posts:create-post"),
            {
                "title": "Test Post",
                "content": "Lorem ipsum",
                "category": category.id,
                "image": image,
                "video": "",
                "is_premium": False,
            },
        )

        assert response.status_code == 302
        assert Post.objects.filter(title="Test Post").exists()

    def test_invalid_form_returns_page(self, client):
        staff = BaseUserFactory(is_staff=True)

        client.force_login(staff)

        response = client.post(
            reverse("posts:create-post"),
            {}
        )

        assert response.status_code == 200
        assert "form" in response.context


# ------------------------------------------------------------------
# PostDetailView
# ------------------------------------------------------------------

class TestPostDetailView:

    def test_get_detail(self, client):
        user = BaseUserFactory()

        category = CategoryFactory()

        post = PostFactory(
            author=user,
            category=category,
            is_premium=False,
        )

        client.force_login(user)

        response = client.get(
            reverse(
                "posts:detail",
                kwargs={"post_id": post.id},
            )
        )

        assert response.status_code == 200
        assert response.context["post"] == post

    def test_comment_created(self, client):
        user = BaseUserFactory()

        post = PostFactory(author=user)

        client.force_login(user)

        response = client.post(
            reverse(
                "posts:detail",
                kwargs={"post_id": post.id},
            ),
            {
                "content": "Nice Post",
            },
        )

        assert response.status_code == 302
        assert Comments.objects.filter(
            author=user,
            post=post,
        ).exists()

    def test_premium_post_without_subscription_redirects(self, client):
        author = BaseUserFactory()

        user = BaseUserFactory()

        post = PostFactory(
            author=author,
            is_premium=True,
        )

        client.force_login(user)

        response = client.get(
            reverse(
                "posts:detail",
                kwargs={"post_id": post.id},
            )
        )

        assert response.status_code == 302
        assert response.url == reverse("home:home")


# ------------------------------------------------------------------
# Favorite View
# ------------------------------------------------------------------

class TestFavoriteView:

    def test_add_to_favorite(self, client):
        user = BaseUserFactory()

        post = PostFactory()

        client.force_login(user)

        response = client.get(
            reverse(
                "posts:favorit",
                kwargs={"post_id": post.id},
            )
        )

        assert response.status_code == 302

        assert FavoritPost.objects.filter(
            user=user,
            post=post,
        ).exists()


# ------------------------------------------------------------------
# Delete Favorite
# ------------------------------------------------------------------

class TestDeleteFavoriteView:

    def test_delete_favorite(self, client):
        user = BaseUserFactory()

        post = PostFactory()

        FavoritPost.objects.create(
            user=user,
            post=post,
        )

        client.force_login(user)

        response = client.get(
            reverse(
                "posts:unlike",
                kwargs={"post_id": post.id},
            )
        )

        assert response.status_code == 302

        assert not FavoritPost.objects.filter(
            user=user,
            post=post,
        ).exists()


# ------------------------------------------------------------------
# Delete Comment
# ------------------------------------------------------------------

class TestDeleteCommentView:

    def test_delete_comment(self, client):
        user = BaseUserFactory()

        post = PostFactory(author=user)

        comment = Comments.objects.create(
            author=user,
            post=post,
            content="hello",
        )

        client.force_login(user)

        response = client.get(
            reverse(
                "posts:delete-comment",
                kwargs={"post_id": post.id},
            )
        )

        assert response.status_code == 302

        assert not Comments.objects.filter(
            id=comment.id,
        ).exists()