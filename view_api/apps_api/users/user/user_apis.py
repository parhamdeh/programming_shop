from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from view_api.pagination import UsersPagination
from view_api.renderers import CustomResponseRenderer
from view_api.throttle import AdminRequestThrottle
from view_api.apps_api.users.user.users_serializer import UserInputSerializer, UserOutputModelSerializer

from users.services.user_services import register
from users.selectors.user_selector import get_users_list

import logging

logger = logging.getLogger(__name__)



class UserListCreate(APIView):
    renderer_classes = (CustomResponseRenderer,)
    permission_classes = (IsAdminUser,)
    throttle_classes = (AdminRequestThrottle,)
    pagination_class = UsersPagination

    @extend_schema(
        tags=["account"],
        summary="List Users",
        description="Retrieve a paginated list of all users.",
        responses={
            200: UserOutputModelSerializer(many=True),
            403: OpenApiResponse(description="Permission denied"),
        },
    )
    def get(self, request: Request) -> Response:
        users = get_users_list()
        pagination = UsersPagination()
        page = pagination.paginate_queryset(users, request)

        serializer = UserOutputModelSerializer(page, many=True)

        return pagination.get_paginated_response(data=serializer.data)

    @extend_schema(
        tags=["account"],
        summary="Create User",
        description="Create a new user.",
        request=UserInputSerializer,
        responses={
            201: UserOutputModelSerializer,
            400: OpenApiResponse(description="Validation error"),
            403: OpenApiResponse(description="Permission denied"),
        },
    )
    def post(self, request: Request) -> Response:
        serializer = UserInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:

            user = register(
                username=serializer.validated_data.get("username"),
                phone=serializer.validated_data.get("phone"),
                password=serializer.validated_data.get("password"),
                subscription=None,
                )
        except Exception as e:
            logger.exception(f"database error! {e}")
            raise

        return Response(
            data=UserOutputModelSerializer(instance=user).data,
            status=status.HTTP_201_CREATED,
        )



