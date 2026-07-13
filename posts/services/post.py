from rest_framework.exceptions import NotFound


from posts.models import Comments, FavoritPost, Post
from users.models import BaseUserModel
from posts.selectors.post_detail import get_post_by_id


def create_comment(*, user: BaseUserModel, post_id: int, content: str) -> Comments:
    post = get_post_by_id(post_id=post_id)

    return Comments.objects.create(author=user,
        post=post,
        content=content,)

def create_post(*, author:BaseUserModel, title:str, content, image, video, is_premium, category) -> Post:
    return Post.objects.create(author=author, title=title, content=content, image=image, video=video, is_premium=is_premium, category=category)


def create_favorit_post(*, user: BaseUserModel, post_id: int) -> FavoritPost:
    post = get_post_by_id(post_id=post_id).first()
    return FavoritPost.objects.create(user=user, post=post)


def delete_comment_post(*, user:BaseUserModel, post_id:int):
    post = get_post_by_id(post_id=post_id)
    Comments.objects.filter(
    author=user,
    post=post,
).delete()

def delete_favorit_post(*, user:BaseUserModel, post_id:int):
    post = get_post_by_id(post_id=post_id).first()
    
    FavoritPost.objects.filter(
    user=user,
    post=post,
).delete()

def update_post(*, data: dict, post:Post) -> Post:
    for key, value in data.items():
        setattr(post, key, value)

    post.save(update_fields=data.keys())

def full_update(*, data:dict, post_id: int):
    post = get_post_by_id(post_id=post_id).first()
    if not post:
        raise NotFound("post not found")
    
    return update_post(data=data, post=post)

def partial_update(*, data:dict, post_id: int):
    post = get_post_by_id(post_id=post_id).first()
    if not post:
        raise NotFound("post not found")
    
    return update_post(data=data, post=post)

def delete_post(*, post_id: int):
    post = get_post_by_id(post_id=post_id).first()
    if not post:
        raise NotFound("post not found")
    
    post.delete()

