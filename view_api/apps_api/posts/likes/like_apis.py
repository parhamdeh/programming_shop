from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from posts.selectors.list_posts import get_all_posts
from posts.selectors.post_detail import get_list_post_liks
from posts.services.post import create_favorit_post, create_post, delete_favorit_post
from view_api.apps_api.posts.likes.like_serilizers import PostLiksOutputModelSerializer
from view_api.apps_api.posts.post.post_serializers import PostOutputModelSerializer, PostsInputModelSerializer
from view_api.pagination import ProductsPagination
from view_api.permissions import PremiumPostPermission
from view_api.renderers import CustomResponseRenderer
from view_api.throttle import AdminRequestThrottle
from view_api.apps_api.users.user.users_serializer import UserInputSerializer, UserOutputModelSerializer

from users.services.user_services import register
from users.selectors.user_selector import get_users_list

import logging

logger = logging.getLogger(__name__)


class PostLikeListCreateAPIView(APIView):
    renderer_classes = (CustomResponseRenderer,)
    throttle_classes = (AdminRequestThrottle,)
    permission_classes = (IsAuthenticated,)
    
    @extend_schema(
    summary="List post likes",
    description="Return all users who liked the specified post.",
    responses={
        200: PostLiksOutputModelSerializer(many=True),
        401: OpenApiResponse(description="Authentication required"),
        404: OpenApiResponse(description="Post not found"),
    },
    )
    def get(self, request: Request, post_id: int) -> Response:
        likes = get_list_post_liks(post_id=post_id)
        pagination = ProductsPagination()
        page = pagination.paginate_queryset(likes, request)

        serializer = PostLiksOutputModelSerializer(page, many=True)

        return pagination.get_paginated_response(data=serializer.data)

    @extend_schema(
    summary="Like a post",
    description="Like the specified post.",
    responses={
        201: PostLiksOutputModelSerializer,
        401: OpenApiResponse(description="Authentication required"),
        404: OpenApiResponse(description="Post not found"),
    },
    )    
    def post(self, request: Request, post_id: int) -> Response:
        try:
            post = create_favorit_post(user=request.user, post_id=post_id)
        except Exception as e:
            logger.exception(f"database error {e}")
            raise

        return Response(
            data=PostLiksOutputModelSerializer(instance=post).data,
            status=status.HTTP_201_CREATED
        )
    
    @extend_schema(
    summary="Remove like",
    description="Remove authenticated user's like from the post.",
    responses={
        204: OpenApiResponse(description="Like removed"),
        401: OpenApiResponse(description="Authentication required"),
        404: OpenApiResponse(description="Post not found"),
    },
    )
    def delete(self, request: Request, post_id: int) -> Response:
        delete_favorit_post(user=request.user, post_id=post_id)

        return Response(status=status.HTTP_204_NO_CONTENT)
    
