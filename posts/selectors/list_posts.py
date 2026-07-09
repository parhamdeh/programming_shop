from django.db.models import QuerySet

from posts.models import Post


def get_all_posts() -> QuerySet[Post]:
    return Post.objects.all().order_by("-created_at")