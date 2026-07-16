# Local Apps
from users.models import BaseUserModel

# Django Built-in modules
from django.db.models import QuerySet



def get_users_list() ->QuerySet[BaseUserModel]:
    """
    this func returns all users in db -> queryset of BaseUserModel
    """
    return BaseUserModel.objects.all()

def get_user_by_id(*, user_id:int) -> BaseUserModel:
    return BaseUserModel.objects.filter(id=user_id)

