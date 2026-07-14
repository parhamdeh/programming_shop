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
from posts.selectors.post_detail import get_list_post_liks, get_post_comments_list
from posts.services.post import create_comment, create_favorit_post, create_post, delete_comment_post, delete_favorit_post
from view_api.apps_api.posts.comments.comment_serializers import PostCommentInputSerializer, PostCommentsOutputModelSerializer
from view_api.apps_api.posts.likes.like_serilizers import PostLiksOutputModelSerializer
from view_api.apps_api.posts.post.post_serializers import PostOutputModelSerializer, PostsInputModelSerializer
from view_api.pagination import ProductsPagination
from view_api.permissions import PremiumPostPermission
from view_api.throttle import UserRequestThrottle
from view_api.apps_api.users.user.users_serializer import UserInputSerializer, UserOutputModelSerializer

from users.services.user_services import register
from users.selectors.user_selector import get_users_list

import logging

logger = logging.getLogger(__name__)


class PostCommentListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    throttle_classes = (UserRequestThrottle,)

    @extend_schema(
        summary="List post comments",
        description="Retrieve all comments for a specific post.",
        responses={
            200: PostCommentsOutputModelSerializer(many=True),
            401: OpenApiResponse(description="Authentication required"),
            404: OpenApiResponse(description="Post not found"),
        },
    )
    def get(self, request: Request, post_id: int) -> Response:
        comments = get_post_comments_list(post_id=post_id)

        logger.info(
            "Comments retrieved for post %s by user %s",
            post_id,
            request.user.username,
        )

        pagination = ProductsPagination()
        page = pagination.paginate_queryset(comments, request)

        serializer = PostCommentsOutputModelSerializer(
            page,
            many=True,
        )

        return pagination.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Create comment",
        description="Create a new comment for a post.",
        request=PostCommentInputSerializer,
        responses={
            201: PostCommentsOutputModelSerializer,
            400: OpenApiResponse(description="Validation error"),
            401: OpenApiResponse(description="Authentication required"),
            404: OpenApiResponse(description="Post not found"),
        },
    )
    def post(self, request: Request, post_id: int) -> Response:
        serializer = PostCommentInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            comment = create_comment(
                user=request.user,
                post_id=post_id,
                content=serializer.validated_data["content"],
            )
        except Exception as ex:
            logger.exception("Database error: %s", ex)
            raise

        logger.info(
            "User %s commented on post %s",
            request.user.username,
            post_id,
        )

        return Response(
            PostCommentsOutputModelSerializer(comment).data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        summary="Delete my comment",
        description="Delete authenticated user's comment from the post.",
        responses={
            204: OpenApiResponse(description="Comment deleted"),
            401: OpenApiResponse(description="Authentication required"),
            404: OpenApiResponse(description="Post not found"),
        },
    )
    def delete(self, request: Request, post_id: int) -> Response:
        delete_comment_post(
            user=request.user,
            post_id=post_id,
        )

        logger.info(
            "User %s deleted comment from post %s",
            request.user.username,
            post_id,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)