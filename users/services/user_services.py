# Local Apps
from posts.models import Subscription
from users.models import BaseUserModel, UserProfileModel
from users.selectors.otp_selector import get_not_used_otp
from users.services.otp_services import create_otp_code
from users.tasks import delete_otp_task, send_otp_task
from users.selectors.user_selector import get_user_by_id

# Django Built-in modules
from django.db import transaction

# Third Party Packages
from rest_framework.exceptions import NotFound
import logging

from view_api.exceptions import OTPExpiredError

logger = logging.getLogger(__name__)


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

@transaction.atomic
def register_request(*, phone):
    otp = create_otp_code(phone=phone)

    transaction.on_commit(
        lambda: send_otp_task.delay(
            phone=str(phone),
            code=otp.code,
        )
    )

    transaction.on_commit(
        lambda: delete_otp_task.apply_async(
            args=[otp.id],
            countdown=120,
        )
    )

    return otp

@transaction.atomic
def verify_before_register(*, register_data: dict, code):
    phone = register_data["phone"]
    otp = get_not_used_otp(phone=phone, code=code)

    if otp is None:
        logger.warning(
        "Invalid OTP for phone %s",
        phone,
        )
        raise OTPExpiredError()

    if otp.is_expired():
        logger.warning(
        "Invalid OTP for phone %s",
        otp.phone,
        )
        otp.delete()
        raise OTPExpiredError()
    
    otp.is_used = True
    otp.save(update_fields=["is_used"])
    user = register(
        username=register_data["username"],
        password=register_data["password"],
        phone=register_data["phone"],
        subscription=None,
    )
    otp.delete()

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