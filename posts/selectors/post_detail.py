# Local Apps
from posts.models import Comments, Post
from posts.models import FavoritPost
from posts.selectors.subscription import get_user_subscription_with_user
from users.models import BaseUserModel
from users.selectors.user_selector import get_user_by_id

# Django Built-in modules
from django.db.models import QuerySet

# Third Party Packages
from rest_framework.exceptions import NotFound



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
    return Post.objects.filter(id=post_id)

def check_favorit(user:BaseUserModel, post:Post) -> bool:

    favorit = FavoritPost.objects.filter(
        user=user,
        post=post
    ).first()
    if not favorit:
        return False
    return True

def check_post_is_premium(*, post_id: int, user_id: int) -> bool:
    post = get_post_by_id(post_id=post_id).first()
    if post.author.id == user_id:
        return True
    is_premium = Post.objects.filter(is_premium=True, id=post_id).exists()
    if not is_premium:
        return True
    
    has_subscription = get_user_subscription_with_user(user_id=user_id).exists()
    return has_subscription

def get_list_post_liks(*, post_id: int) -> QuerySet[FavoritPost]:
    post = get_post_by_id(post_id=post_id).first()
    if not post:
        raise NotFound("post not found")
    return FavoritPost.objects.filter(
        post=post
    ).all()

def get_post_comments_list(*, post_id: int) -> QuerySet[Comments]:
    post = get_post_by_id(post_id=post_id).first()
    if not post:
        raise NotFound("post not found")
    return Comments.objects.filter(
        post=post
    ).all()