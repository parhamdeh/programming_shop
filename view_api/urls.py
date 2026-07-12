from django.urls import path, include

from view_api.apps_api.users.user.id.user_id_apis import UserRetrieveUpdatadeDestroy
from view_api.apps_api.users.user.user_apis import UserListCreate



urlpatterns = [
    path(route="users/", view=UserListCreate.as_view(), name="user-list-create"),
    path(route="users/<int:user_id>", view=UserRetrieveUpdatadeDestroy.as_view(), name="user-detail"),
]