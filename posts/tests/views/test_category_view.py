import pytest

from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from posts.models import Category
from posts.tests.factory.posts import PostFactory
from posts.tests.factory.category import CategoryFactory
from users.tests.factories.users import BaseUserFactory


pytestmark = pytest.mark.django_db


class TestCreateCategoryView:

    def test_get_anonymous_redirects_to_login(self, client):
        response = client.get(reverse("posts:create-category"))

        assert response.status_code == 302
        assert response.url == reverse("users:login")

    def test_get_normal_user_redirects_home(self, client):
        user = BaseUserFactory()

        client.force_login(user)

        response = client.get(reverse("posts:create-category"))

        assert response.status_code == 302
        assert response.url == reverse("home:home")

    def test_get_staff_returns_page(self, client):
        staff = BaseUserFactory(is_staff=True)

        client.force_login(staff)

        response = client.get(reverse("posts:create-category"))

        assert response.status_code == 200
        assert "form" in response.context

    def test_post_valid_data_creates_category(self, client):
        staff = BaseUserFactory(is_staff=True)

        client.force_login(staff)

        response = client.post(
            reverse("posts:create-category"),
            {
                "name": "Python",
                "parent": "",
            },
        )

        assert response.status_code == 302
        assert Category.objects.filter(name="Python").exists()

    def test_post_with_parent_creates_category(self, client):
        staff = BaseUserFactory(is_staff=True)
        parent = CategoryFactory()

        client.force_login(staff)

        client.post(
            reverse("posts:create-category"),
            {
                "name": "Django",
                "parent": parent.id,
            },
        )

        category = Category.objects.get(name="Django")

        assert category.parent == parent

    def test_post_invalid_form(self, client):
        staff = BaseUserFactory(is_staff=True)

        client.force_login(staff)

        response = client.post(
            reverse("posts:create-category"),
            {
                "name": "",
            },
        )

        assert response.status_code == 200
        assert "form" in response.context

class TestCategoryDetailView:

    def test_login_required(self, client):
        category = CategoryFactory()

        response = client.get(
            reverse(
                "posts:category-detail",
                kwargs={"category_id": category.id},
            )
        )

        assert response.status_code == 302

    def test_parent_category_returns_parent_and_children_posts(self, client):
        user = BaseUserFactory()
        client.force_login(user)

        parent = CategoryFactory()
        child = CategoryFactory(parent=parent)

        parent_post = PostFactory(category=parent)
        child_post = PostFactory(category=child)

        response = client.get(
            reverse(
                "posts:category-detail",
                kwargs={"category_id": parent.id},
            )
        )

        posts = response.context["posts"]

        assert response.status_code == 200
        assert parent_post in posts
        assert child_post in posts

    def test_child_category_returns_only_its_posts(self, client):
        user = BaseUserFactory()
        client.force_login(user)

        parent = CategoryFactory()
        child = CategoryFactory(parent=parent)

        child_post = PostFactory(category=child)
        parent_post = PostFactory(category=parent)

        response = client.get(
            reverse(
                "posts:category-detail",
                kwargs={"category_id": child.id},
            )
        )

        posts = response.context["posts"]

        assert response.status_code == 200
        assert child_post in posts
        assert parent_post not in posts

    def test_non_existing_category_raises_exception(self, client):
        user = BaseUserFactory()
        client.force_login(user)

        with pytest.raises(Exception):
            client.get(
                reverse(
                    "posts:category-detail",
                    kwargs={"category_id": 999999},
                )
            )

    def test_template_used(self, client):
        user = BaseUserFactory()
        client.force_login(user)

        category = CategoryFactory()

        response = client.get(
            reverse(
                "posts:category-detail",
                kwargs={"category_id": category.id},
            )
        )

        assert response.status_code == 200
        assert response.templates[0].name == "category/detail.html"
        assert response.context["category"] == category