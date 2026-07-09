from users.models import BaseUserModel
from django.db.models import QuerySet



def get_users_list() ->QuerySet[BaseUserModel]:
    """
    this func returns all users in db -> queryset of BaseUserModel
    """
    return BaseUserModel.objects.all()

