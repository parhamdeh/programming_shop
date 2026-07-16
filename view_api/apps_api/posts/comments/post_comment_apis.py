# Third Party Packages
from rest_framework.request import Request
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
import logging
from rest_framework.settings import api_settings
from rest_framework import status, mixins
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

# Local Apps
from posts.selectors.post_detail import get_list_post_liks, get_post_comments_list
from posts.services.post import create_comment, create_favorit_post, create_post, delete_comment_post, delete_favorit_post
from view_api.apps_api.posts.comments.comment_serializers import PostCommentInputSerializer, PostCommentsOutputModelSerializer
from view_api.renderers import CustomResponseRenderer
from view_api.throttle import UserRequestThrottle



logger = logging.getLogger(__name__)


class PostCommentListCreateAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    renderer_classes = (CustomResponseRenderer,)
    permission_classes = (IsAuthenticated,)
    throttle_classes = (UserRequestThrottle,)
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    serializer_class = PostCommentsOutputModelSerializer

    def get_queryset(self):
        return get_post_comments_list(post_id=self.kwargs["post_id"])

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
        logger.info(
            "Comments retrieved for post %s by user %s",
            post_id,
            request.user.username,
        )

        return self.list(request, post_id=post_id)

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
        input_serializer = PostCommentInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            comment = create_comment(
                user=request.user,
                post_id=post_id,
                content=input_serializer.validated_data["content"],
            )
        except Exception as ex:
            logger.exception("Database error: %s", ex)
            raise

        logger.info(
            "User %s commented on post %s",
            request.user.username,
            post_id,
        )

        output_serializer = self.get_serializer(comment)

        return Response(
            output_serializer.data,
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