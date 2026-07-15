from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from posts.selectors.list_posts import get_all_posts
from posts.services.post import create_post

from view_api.apps_api.posts.post.post_serializers import PostOutputModelSerializer, PostsInputModelSerializer
from view_api.permissions import PremiumPostPermission
from view_api.renderers import CustomResponseRenderer
from view_api.throttle import AdminRequestThrottle

from rest_framework.settings import api_settings

import logging

logger = logging.getLogger(__name__)


class PostListCreateAPIView(APIView):
    renderer_classes = (CustomResponseRenderer,)
    parser_classes = (MultiPartParser, FormParser)
    throttle_classes = (AdminRequestThrottle,)
    permission_classes = (PremiumPostPermission,)
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    
    @extend_schema(
        summary="List Posts",
        description="Returns a paginated list of all posts.",
        responses={
            200: PostOutputModelSerializer(many=True),
        },
    )
    def get(self, request: Request) -> Response:
        posts = get_all_posts()
        pagination = self.pagination_class()
        page = pagination.paginate_queryset(posts, request)

        serializer = PostOutputModelSerializer(page, many=True)

        return pagination.get_paginated_response(data=serializer.data)

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
    def post(self, request: Request) -> Response:
        serilizer = PostsInputModelSerializer(data=request.data)
        serilizer.is_valid(raise_exception=True)

        try:
            # author:BaseUserModel, title:str, content, image, video, is_premium, category
            post = create_post(author=request.user,
                               title=serilizer.validated_data["title"],
                               content=serilizer.validated_data["content"],
                               image=serilizer.validated_data.get("image"),
                               video=serilizer.validated_data.get("video"),
                               is_premium=serilizer.validated_data["is_premium"],
                               category=serilizer.validated_data["category"])
        except Exception as e:
            logger.exception(f"database error {e}")
            raise

        return Response(
            data=PostOutputModelSerializer(instance=post).data,
            status=status.HTTP_201_CREATED
        )
    

