# Third Party Packages
from rest_framework.request import Request
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
import logging
from typing import Any
from rest_framework.serializers import BaseSerializer
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

# Local Apps
from posts.models import Category
from posts.selectors.category import get_all_categories, get_category_by_id
from posts.services.category import create_category
from posts.services.post import delete_category, full_update_category, partial_update_category
from view_api.apps_api.posts.category.category_serializer import CategoryInputSerializer, CategoryOutputSerializer
from view_api.permissions import IsAdminOrReadOnly
from view_api.renderers import CustomResponseRenderer
from view_api.throttle import AdminRequestThrottle


logger = logging.getLogger(__name__)



class CategoryRetrieveUpdateDstroyAPIView(RetrieveUpdateDestroyAPIView):
    renderer_classes = (CustomResponseRenderer,)
    throttle_classes = (AdminRequestThrottle,)
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated)

    def get_object(self) -> Category:
        category = get_category_by_id(
            category_id=self.kwargs["category_id"]
        ).first()

        if not category:
            raise NotFound("category not found")

        return category
    
    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.request.method == "GET":
            return CategoryOutputSerializer
        return CategoryInputSerializer
    
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
            data=CategoryOutputSerializer(instance=serializer.instance).data,
            status=status.HTTP_200_OK,
        )
    
    def perform_update(self, serializer: BaseSerializer) -> None:
        category_id = self.kwargs["category_id"]

        if serializer.partial:
            category = partial_update_category(
                category_id=category_id,
                data=serializer.validated_data,
            )
        else:
            category = full_update_category(
                category_id=category_id,
                data=serializer.validated_data,
            )

        serializer.instance = category

    def perform_destroy(self, instance: Category) -> None:
        delete_category(category_id=self.kwargs["category_id"])

    @extend_schema(
    summary="Retrieve Category",
    description="Retrieve a category by id.",
    responses={
        200: CategoryOutputSerializer,
        404: OpenApiResponse(description="Category not found"),
    },
    )
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return self.retrieve(request, *args, **kwargs)


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
    def put(self, requesta: Request, *args: Any, **kwargs: Any) -> Response:
        return self.update(requesta, *args, **kwargs)
    
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
    def patch(self, requesta: Request, *args: Any, **kwargs: Any) -> Response:
        return self.partial_update(requesta, *args, **kwargs)

    @extend_schema(
    summary="Delete Category",
    description="Delete a category.",
    responses={
        204: OpenApiResponse(description="Category deleted"),
        404: OpenApiResponse(description="Category not found"),
    },
    )
    def delete(self, requesta: Request, *args: Any, **kwargs: Any) -> Response:
        return self.destroy(requesta, *args, **kwargs)