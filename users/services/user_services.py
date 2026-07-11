from posts.models import Subscription
from users.models import BaseUserModel, UserProfileModel

from django.db import transaction


def create_user(*, username:str, password:str, phone:str) -> BaseUserModel:
    user =  BaseUserModel.objects.create_user(username=username, phone=phone)
    user.password = password
    user.save()
    return user 

def create_profile(*, user:BaseUserModel, subscription:Subscription | None) -> UserProfileModel:
    return UserProfileModel.objects.create(user=user, subscription=subscription)

@transaction.atomic
def register(*, username:str, password:str, phone:str, user:BaseUserModel, subscription:Subscription | None) -> BaseUserModel:
    user = create_user(username=username, phone=phone, password=password)
    create_profile(user=user, subscription=subscription)

    return user