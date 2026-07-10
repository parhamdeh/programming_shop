
from posts.models import Post
from posts.models import FavoritPost
from posts.selectors.subscription import get_user_subscription_with_user
from users.models import BaseUserModel
from django.core.exceptions import ObjectDoesNotExist

from users.selectors.user_selector import get_user_by_id



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


def check_favorit(user:BaseUserModel, post:Post) -> bool:

    favorit = FavoritPost.objects.filter(
        user=user,
        post=post
    ).first()
    if not favorit:
        return False
    return True

def check_post_is_premium(*, post_id: int, user_id: int) -> bool:
    post = get_post_by_id(post_id=post_id)
    if post.author.id == user_id:
        return True
    is_premium = Post.objects.filter(is_premium=True, id=post_id).exists()
    if not is_premium:
        return True
    
    has_subscription = get_user_subscription_with_user(user_id=user_id).exists()
    return has_subscription
        