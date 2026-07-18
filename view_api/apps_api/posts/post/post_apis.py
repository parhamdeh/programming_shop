# Third Party Packages
import logging
from rest_framework.serializers import Serializer
from rest_framework.request import Request
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

# Local Apps
from posts.selectors.list_posts import get_all_posts
from posts.services.post import create_post
from users.models import BaseUserModel
from view_api.apps_api.posts.post.post_serializers import PostOutputModelSerializer, PostsInputModelSerializer
from view_api.permissions import PremiumPostPermission
from view_api.renderers import CustomResponseRenderer
from view_api.throttle import AdminRequestThrottle



logger = logging.getLogger(__name__)


class PostListCreateAPIView(ListCreateAPIView):
    renderer_classes = (CustomResponseRenderer,)
    parser_classes = (MultiPartParser, FormParser)
    throttle_classes = (AdminRequestThrottle,)
    permission_classes = (PremiumPostPermission,)
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get_queryset(self):
        return get_all_posts()
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return PostsInputModelSerializer
        return PostOutputModelSerializer
    
    @extend_schema(
        summary="List Posts",
        description="Returns a paginated list of all posts.",
        responses={
            200: PostOutputModelSerializer(many=True),
        },
    )

    def get(self, request: Request) -> Response:
        page = self.paginate_queryset(self.get_queryset())

        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Create Post",
        description="Creates a new post. Admin users only.",
        request={
            "multipart/form-data": PostsInputModelSerializer,
        },
        responses={
            201: PostOutputModelSerializer,
            400: OpenApiResponse(description="Validation Error"),
            403: OpenApiResponse(description="Permission Denied"),
        },
    )
    def post(self, request: Request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def perform_create(self, user: BaseUserModel, serializer: Serializer) -> Response:
        try:
            # author:BaseUserModel, title:str, content, image, video, is_premium, category
            post = create_post(author=user,
                               title=serializer.validated_data["title"],
                               content=serializer.validated_data["content"],
                               image=serializer.validated_data.get("image"),
                               video=serializer.validated_data.get("video"),
                               is_premium=serializer.validated_data["is_premium"],
                               category=serializer.validated_data["category"])
        except Exception as e:
            logger.exception(f"database error {e}")
            raise
        
        self.instance = post

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer=serializer, user=user)

        output = PostOutputModelSerializer(self.instance)

        return Response(output.data, status=status.HTTP_201_CREATED)
    

