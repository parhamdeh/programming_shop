# Django Built-in modules
from django.db.models import QuerySet

# Local Apps
from posts.models import Post


def get_all_posts() -> QuerySet[Post]:
    return Post.objects.all().order_by("-created_at")