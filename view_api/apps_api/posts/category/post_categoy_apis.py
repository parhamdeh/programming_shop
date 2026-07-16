# Third Party Packages
from typing import Any
from rest_framework.request import Request
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import BaseSerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)
import logging

# Local Apps
from posts.selectors.category import get_all_categories
from posts.services.category import create_category
from view_api.apps_api.posts.category.category_serializer import CategoryInputSerializer, CategoryOutputSerializer
from view_api.permissions import IsAdminOrReadOnly
from view_api.renderers import CustomResponseRenderer
from view_api.throttle import AdminRequestThrottle


logger = logging.getLogger(__name__)


class CategoryListCreateAPIView(ListCreateAPIView):
    renderer_classes = (CustomResponseRenderer,)
    throttle_classes = (AdminRequestThrottle,)
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated)

    def get_queryset(self):
        try:
            return get_all_categories()
        except Exception as e:
            logger.exception(f"database error{e}")
            raise

    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.request.method == "POST":
            return CategoryInputSerializer
        return CategoryOutputSerializer
    
    def perform_create(self, serializer: BaseSerializer) -> None:
        try:
            category = create_category(data=serializer.validated_data)
        except Exception as e:
            logger.exception(f"database error {e}")
            raise
        serializer.instance = category

    @extend_schema(
    summary="List Categories",
    description="Retrieve all categories.",
    responses={
        200: CategoryOutputSerializer(many=True),
    },
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

    @extend_schema(
    summary="Create Category",
    description="Create a new category (Admin only).",
    request=CategoryInputSerializer,
    responses={
        201: CategoryOutputSerializer,
        400: OpenApiResponse(description="Validation Error"),
        401: OpenApiResponse(description="Authentication required"),
        403: OpenApiResponse(description="Permission denied"),
    },
    )   
    def post(self, request: Request, *args, **kwargs) -> Response:
        
        response = self.create(request, *args, **kwargs)
        response.status_code = status.HTTP_201_CREATED
        return response