from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from posts.selectors.category import get_all_categories, get_category_by_id
from posts.services.category import create_category
from posts.services.post import delete_category, full_update_category, partial_update_category
from view_api.apps_api.posts.category.category_serializer import CategoryInputSerializer, CategoryOutputSerializer
from view_api.permissions import IsAdminOrReadOnly
from view_api.throttle import AdminRequestThrottle

import logging

logger = logging.getLogger(__name__)



class CategoryRetrieveUpdateDstroyAPIView(APIView):
    throttle_classes = (AdminRequestThrottle,)
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated)

    @extend_schema(
    summary="Retrieve Category",
    description="Retrieve a category by id.",
    responses={
        200: CategoryOutputSerializer,
        404: OpenApiResponse(description="Category not found"),
    },
    )
    def get(self, requesta: Request, category_id: int) -> Response:
        category = get_category_by_id(category_id=category_id).first()
        if not category:
            raise NotFound("post not found")
        
        return Response(
            data=CategoryOutputSerializer(instance=category).data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
    summary="Update Category",
    description="Replace a category.",
    request=CategoryInputSerializer,
    responses={
        200: CategoryOutputSerializer,
        400: OpenApiResponse(description="Validation error"),
        404: OpenApiResponse(description="Category not found"),
    },
)
    def put(self, requesta: Request, category_id: int) -> Response:
        serializer = CategoryInputSerializer(data=requesta.data)
        serializer.is_valid(raise_exception=True)
        try:
            category = full_update_category(category_id=category_id, data=serializer.validated_data)
        except Exception as e:
            logger.exception(f"database error {e}")

        return Response(
            data=CategoryOutputSerializer(instance=category).data,
            status=status.HTTP_200_OK,
        )
    
    @extend_schema(
    summary="Partial Update Category",
    description="Partially update a category.",
    request=CategoryInputSerializer,
    responses={
        200: CategoryOutputSerializer,
        400: OpenApiResponse(description="Validation error"),
        404: OpenApiResponse(description="Category not found"),
    },
    )
    def patch(self, requesta: Request, category_id: int) -> Response:
        serializer = CategoryInputSerializer(data=requesta.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            category = partial_update_category(category_id=category_id, data=serializer.validated_data)
        except Exception as e:
            logger.exception(f"database error {e}")

        return Response(
            data=CategoryOutputSerializer(instance=category).data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
    summary="Delete Category",
    description="Delete a category.",
    responses={
        204: OpenApiResponse(description="Category deleted"),
        404: OpenApiResponse(description="Category not found"),
    },
    )
    def delete(self, requesta: Request, category_id: int) -> Response:
        delete_category(category_id=category_id)
        return Response(status=status.HTTP_204_NO_CONTENT)