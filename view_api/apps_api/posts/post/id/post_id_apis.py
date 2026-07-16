# Third Party Packages
import logging
from rest_framework.request import Request
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiRequest
)

# Local Apps
from posts.selectors.post_detail import get_post_by_id
from posts.services.post import delete_post, full_update, partial_update
from view_api.apps_api.posts.post.post_serializers import PostOutputModelSerializer, PostsInputModelSerializer
from view_api.permissions import PremiumPostPermission
from view_api.renderers import CustomResponseRenderer
from view_api.throttle import UserRequestThrottle


logger = logging.getLogger(__name__)


class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    renderer_classes = (CustomResponseRenderer,)
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (PremiumPostPermission,)
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
        
        self.check_object_permissions(request, post)
        
        return Response(
            data=PostOutputModelSerializer(instance=post).data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
    summary="Update Post",
    description="Fully update a post. Admin only.",
    
    request=OpenApiRequest(
        request=PostsInputModelSerializer,
        encoding={
            "image": {"contentType": "image/*"},
            "video": {"contentType": "video/*"},
        },
    ),
    responses={
        200: PostOutputModelSerializer,
        400: OpenApiResponse(description="Validation Error"),
        403: OpenApiResponse(description="Permission Denied"),
        404: OpenApiResponse(description="Post not found"),
    },
    )   
    def put(self, request: Request, post_id: int) -> Response:
        print(request.content_type)
        print(request.FILES)
        print(request.data)
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
    request={
        "multipart/form-data": PostsInputModelSerializer,
    },
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
    

    