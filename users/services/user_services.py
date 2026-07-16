# Local Apps
from posts.models import Subscription
from users.models import BaseUserModel, UserProfileModel
from users.selectors.user_selector import get_user_by_id

# Django Built-in modules
from django.db import transaction

# Third Party Packages
from rest_framework.exceptions import NotFound


def create_user(*, username:str, password:str, phone:str) -> BaseUserModel:
    user =  BaseUserModel.objects.create_user(username=username, phone=phone)
    user.password = password
    user.save()
    return user 

def create_profile(*, user:BaseUserModel, subscription:Subscription | None) -> UserProfileModel:
    return UserProfileModel.objects.create(user=user, subscription=subscription)

@transaction.atomic
def register(*, username:str, password:str, phone:str, subscription:Subscription | None) -> BaseUserModel:
    user = create_user(username=username, phone=phone, password=password)
    create_profile(user=user, subscription=subscription)

    return user

def update_user(*, data: dict, user=BaseUserModel) -> BaseUserModel:
    for key, value in data.items():
        setattr(user, key, value)

    user.save(update_fields=data.keys())

def full_update(*, data:dict, user_id: int):
    user = get_user_by_id(user_id=user_id).first()
    if not user:
        raise NotFound
    
    return update_user(data=data, user=user)

def partial_update(*, data:dict, user_id: int):
    user = get_user_by_id(user_id=user_id).first()
    if not user:
        raise NotFound
    
    return update_user(data=data, user=user)

def delete_user(*, user_id: int):
    user = get_user_by_id(user_id=user_id).first()
    if not user:
        raise NotFound("user not found")
    
    user.delete()