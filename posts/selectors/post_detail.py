from xmlrpc.client import Boolean

from posts.models import Post
from posts.models import FavoritPost
from users.models import BaseUserModel



def get_post_detail(post_id:int) -> Post:

    return (
        Post.objects
        .select_related("category")
        .prefetch_related("comment__author")
        .get(id=post_id)
    )

def get_related_posts(post:Post) -> Post:

    return (
        Post.objects
        .filter(category=post.category)
        .exclude(id=post.id)[:5]
    )

def get_post_by_id(post_id:int) -> Post:
    return Post.objects.get(id=post_id)


def check_favorit(user:BaseUserModel, post:Post) -> Boolean:

    favorit = FavoritPost.objects.filter(
        user=user,
        post=post
    ).first()
    if not favorit:
        return False
    return True
