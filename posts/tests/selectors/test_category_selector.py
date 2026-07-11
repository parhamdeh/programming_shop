import pytest

from posts.selectors.category import (
    get_all_categories,
    get_category_by_id,
)

from posts.tests.factory.category import (
    CategoryFactory,
)


pytestmark = pytest.mark.django_db


class TestGetAllCategories:

    def test_returns_all_categories(self):

        CategoryFactory.create_batch(5)

        categories = get_all_categories()

        assert categories.count() == 5

    def test_returns_queryset(self):

        CategoryFactory()

        categories = get_all_categories()

        assert hasattr(categories, "filter")


class TestGetCategoryById:

    def test_returns_category(self):

        category = CategoryFactory()

        result = get_category_by_id(
            category_id=category.id,
        )

        assert result.exists()

        assert result.first() == category

    def test_returns_empty_queryset(self):

        result = get_category_by_id(
            category_id=99999,
        )

        assert result.exists() is False