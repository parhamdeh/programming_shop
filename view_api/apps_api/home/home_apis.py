from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from posts.selectors.category import get_all_categories
from posts.selectors.list_posts import get_all_posts
from posts.selectors.subscription import get_all_subscriptions
from view_api.apps_api.home.home_serializer import HomeOutputSerializer
from view_api.apps_api.users.profile.user_profile_serializer import ProfileOutputSerializer

from users.services.user_services import register
from users.selectors.user_selector import get_users_list

import logging

from view_api.throttle import UserRequestThrottle

logger = logging.getLogger(__name__)


class HomeAPIview(APIView):
    throttle_classes = (UserRequestThrottle,)

    @extend_schema(
    summary="Home",
    description="""
Retrieve data required for the home page.

Returns:
- List of posts
- List of categories
- List of available subscriptions
""",
    tags=["Home"],
    responses={
        200: HomeOutputSerializer,
        500: OpenApiResponse(description="Internal server error"),
    },
)
    def get(self, request: Request) -> Response:
        posts = get_all_posts()
        categories = get_all_categories()
        subscriptions = get_all_subscriptions()

        
        data = {
                "subscription": subscriptions,
                "post": posts,
                "category" : categories,
            }

        serializer = HomeOutputSerializer(instance=data)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            )