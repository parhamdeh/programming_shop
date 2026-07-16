# Local Apps
from posts.models import Category


def create_category(*, data:dict) -> Category:
    return Category.objects.create(name=data.get("name"), parent=data.get("parent"))