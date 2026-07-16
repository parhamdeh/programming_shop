# Third Party Packages
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
import logging
from rest_framework import generics, mixins
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

# Local Apps
from posts.selectors.post_detail import get_list_post_liks
from posts.services.post import create_favorit_post, create_post, delete_favorit_post
from view_api.apps_api.posts.likes.like_serilizers import PostLiksOutputModelSerializer
from view_api.renderers import CustomResponseRenderer
from view_api.throttle import AdminRequestThrottle



logger = logging.getLogger(__name__)


class PostLikeListCreateAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    renderer_classes = (CustomResponseRenderer,)
    throttle_classes = (AdminRequestThrottle,)
    permission_classes = (IsAuthenticated,)
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    serializer_class = PostLiksOutputModelSerializer

    def get_queryset(self):
        return get_list_post_liks(post_id=self.kwargs["post_id"])

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
        return self.list(request, post_id=post_id)

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
            data=self.get_serializer(instance=post).data,
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