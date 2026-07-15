from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from posts.selectors.category import get_all_categories
from posts.services.category import create_category
from view_api.apps_api.posts.category.category_serializer import CategoryInputSerializer, CategoryOutputSerializer
from view_api.permissions import IsAdminOrReadOnly
from view_api.renderers import CustomResponseRenderer
from view_api.throttle import AdminRequestThrottle

import logging

logger = logging.getLogger(__name__)


class CategoryListCreateAPIView(APIView):
    renderer_classes = (CustomResponseRenderer,)
    throttle_classes = (AdminRequestThrottle,)
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated)

    @extend_schema(
    summary="List Categories",
    description="Retrieve all categories.",
    responses={
        200: CategoryOutputSerializer(many=True),
    },
    )
    def get(self, request: Request) -> Response:
        try:
            categories = get_all_categories()
        except Exception as e:
            logger.exception(f"database error{e}")
            raise
        return Response(
            data=CategoryOutputSerializer(instance=categories, many=True).data,
            status=status.HTTP_200_OK,
        )

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
    def post(self, request: Request) -> Response:
        serializer = CategoryInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            category = create_category(data=serializer.validated_data)
        except Exception as e:
            logger.exception(f"database error {e}")
            raise

        return Response(
            data=CategoryOutputSerializer(instance=category).data,
            status=status.HTTP_201_CREATED,
        )