from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from posts.selectors.list_posts import get_all_posts
from posts.selectors.post_detail import get_post_by_id
from posts.services.post import create_post, delete_post, full_update, partial_update
from view_api.apps_api.posts.post.post_serializers import PostOutputModelSerializer, PostsInputModelSerializer
from view_api.pagination import ProductsPagination, UsersPagination
from view_api.permissions import IsAdminOrReadOnly
from view_api.throttle import AdminRequestThrottle, UserRequestThrottle
from view_api.apps_api.users.user.users_serializer import UserInputSerializer, UserOutputModelSerializer

from users.services.user_services import register
from users.selectors.user_selector import get_users_list

import logging

logger = logging.getLogger(__name__)


class PostRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    throttle_classes = (UserRequestThrottle,)

    @extend_schema(
    summary="Retrieve Post",
    description="Retrieve a post by id.",
    responses={
        200: PostOutputModelSerializer,
        404: OpenApiResponse(description="Post not found"),
    },
    )
    def get(self, request: Request, post_id: int) -> Response:
        try:
            post = get_post_by_id(post_id=post_id).first()
        except Exception as e:
            logger.exception(f'database error{e}')
            raise

        if not post:
            logger.info(f"there is not post with {post_id}")
            raise NotFound("post not found")
        
        return Response(
            data=PostOutputModelSerializer(instance=post).data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
    summary="Update Post",
    description="Fully update a post. Admin only.",
    request=PostsInputModelSerializer,
    responses={
        200: PostOutputModelSerializer,
        400: OpenApiResponse(description="Validation Error"),
        403: OpenApiResponse(description="Permission Denied"),
        404: OpenApiResponse(description="Post not found"),
    },
    )   
    def put(self, request: Request, post_id: int) -> Response:
        serializer = PostsInputModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            post = full_update(post_id=post_id, data=serializer.validated_data)

        except Exception as e:
            logger.exception(f"database error{e}")
            raise

        return Response(
            data=PostOutputModelSerializer(instance=post).data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
    summary="Partial Update Post",
    description="Partially update a post. Admin only.",
    request=PostsInputModelSerializer,
    responses={
        200: PostOutputModelSerializer,
        400: OpenApiResponse(description="Validation Error"),
        403: OpenApiResponse(description="Permission Denied"),
        404: OpenApiResponse(description="Post not found"),
    },
    )
    def patch(self, request: Request, post_id: int) -> Response:
        serializer = PostsInputModelSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            post = partial_update(post_id=post_id, data=serializer.validated_data)

        except Exception as e:
            logger.exception(f"database error{e}")
            raise

        return Response(
            data=PostOutputModelSerializer(instance=post).data,
            status=status.HTTP_200_OK,
        )
    
    @extend_schema(
    summary="Delete Post",
    description="Delete a post. Admin only.",
    responses={
        204: OpenApiResponse(description="Deleted"),
        403: OpenApiResponse(description="Permission Denied"),
        404: OpenApiResponse(description="Post not found"),
    },
    )
    def delete(self, request: Request, post_id: int) -> Response:
        try:
            delete_post(post_id=post_id)
        except Exception as e:
            logger.exception(f"database error {e}")
            raise

        return Response(status=status.HTTP_204_NO_CONTENT)
    

    