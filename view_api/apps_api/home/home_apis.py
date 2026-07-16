# Third Party Packages# Local Apps
import logging
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

# Local Apps
from posts.selectors.category import get_all_categories
from posts.selectors.list_posts import get_all_posts
from posts.selectors.subscription import get_all_subscriptions
from view_api.apps_api.home.home_serializer import HomeOutputSerializer
from view_api.renderers import CustomResponseRenderer
from view_api.throttle import UserRequestThrottle

logger = logging.getLogger(__name__)


class HomeAPIview(APIView):
    renderer_classes = (CustomResponseRenderer,)
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