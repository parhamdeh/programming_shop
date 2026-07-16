# Third Party Packages
import logging
from typing import Any
from rest_framework.request import Request
from rest_framework.serializers import BaseSerializer
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
from posts.models import Post
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

    lookup_url_kwarg = "post_id"

    def get_object(self):
        post = get_post_by_id(
            post_id=self.kwargs["post_id"]
        ).first()

        if not post:
            raise NotFound("post not found")
        return post
    
    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.request.method == "GET":
            return PostOutputModelSerializer
        return PostsInputModelSerializer
    
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer)
        except Exception as e:
            logger.exception(f"database error {e}")
            raise

        return Response(
            data=PostOutputModelSerializer(instance=serializer.instance).data,
            status=status.HTTP_200_OK
        )
    
    def perform_update(self, serializer: BaseSerializer) -> None:
        post_id = self.kwargs["post_id"]
        if serializer.partial:
            post = partial_update(
                post_id=post_id,
                data=serializer.validated_data,
            )
        else:
            post = full_update(
                post_id=post_id,
                data=serializer.validated_data
            )
            serializer.instance = post
        
    def perform_destroy(self, instance: Post) -> None:
        delete_post(post_id=self.kwargs["post_id"])

    
        
    @extend_schema(
    summary="Retrieve Post",
    description="Retrieve a post by id.",
    responses={
        200: PostOutputModelSerializer,
        404: OpenApiResponse(description="Post not found"),
    },
    )
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return self.retrieve(request=request, *args, **kwargs)

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
    def put(self, requesta: Request, *args: Any, **kwargs: Any) -> Response:
        return self.update(requesta, *args, **kwargs)
    
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
    def patch(self, requesta: Request, *args: Any, **kwargs: Any) -> Response:
        return self.partial_update(requesta, *args, **kwargs)
    
    @extend_schema(
    summary="Delete Post",
    description="Delete a post. Admin only.",
    responses={
        204: OpenApiResponse(description="Deleted"),
        403: OpenApiResponse(description="Permission Denied"),
        404: OpenApiResponse(description="Post not found"),
    },
    )
    def delete(self, requesta: Request, *args: Any, **kwargs: Any) -> Response:
        return self.destroy(requesta, *args, **kwargs)
    

    