import pytest

from posts.models import Category
from posts.services.category import create_category

from posts.tests.factory.category import CategoryFactory


pytestmark = pytest.mark.django_db


class TestCreateCategory:

    def test_create_root_category(self):
        data = {
            "name": "Python",
            "parent": None,
        }

        category = create_category(data=data)

        assert isinstance(category, Category)

        assert category.name == "Python"

        assert category.parent is None

        assert Category.objects.count() == 1

    def test_create_child_category(self):
        parent = CategoryFactory(name="Backend")

        data = {
            "name": "Django",
            "parent": parent,
        }

        child = create_category(data=data)

        assert child.name == "Django"

        assert child.parent == parent

        assert Category.objects.count() == 2

    def test_create_multiple_categories(self):
        create_category(
            data={
                "name": "Python",
                "parent": None,
            }
        )

        create_category(
            data={
                "name": "Django",
                "parent": None,
            }
        )

        create_category(
            data={
                "name": "FastAPI",
                "parent": None,
            }
        )

        assert Category.objects.count() == 3

    def test_create_nested_categories(self):
        root = CategoryFactory(name="Programming")

        backend = create_category(
            data={
                "name": "Backend",
                "parent": root,
            }
        )

        django = create_category(
            data={
                "name": "Django",
                "parent": backend,
            }
        )

        assert django.parent == backend

        assert backend.parent == root

        assert Category.objects.count() == 3