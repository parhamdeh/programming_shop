from django.db.models import QuerySet
from posts.models import Category


def get_all_categories() -> QuerySet[Category]:
    return Category.objects.all()

def get_category_by_id(*, category_id: int) -> Category:
    return Category.objects.filter(id=category_id)
