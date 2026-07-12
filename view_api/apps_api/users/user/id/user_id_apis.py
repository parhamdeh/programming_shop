from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import NotFound

from view_api.throttle import AdminRequestThrottle
from view_api.apps_api.users.user.users_serializer import UserInputSerializer, UserOutputModelSerializer

from users.services.user_services import delete_user, full_update, partial_update, register
from users.selectors.user_selector import get_user_by_id, get_users_list

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

import logging

logger = logging.getLogger(__name__)


class UserRetrieveUpdatadeDestroy(APIView):
    """
    Retrieve, update or delete a user.
    """

    permission_classes = (IsAdminUser,)
    throttle_classes = (AdminRequestThrottle,)

    @extend_schema(
        summary="Retrieve User",
        description="""
Retrieve a single user by its unique identifier.

Only administrators are allowed to access this endpoint.
        """,
        tags=["Users"],
        responses={
            200: UserOutputModelSerializer,
            404: OpenApiResponse(description="User not found"),
            403: OpenApiResponse(description="Permission denied"),
        },
    )
    def get(self, request: Request, user_id: int) -> Response:
        user = get_user_by_id(user_id=user_id).first()

        if not user:
            logger.info("user not found")
            raise NotFound("user not found!")

        return Response(
            UserOutputModelSerializer(user).data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Full Update User",
        description="""
Replace all editable fields of a user.

All required fields must be provided.
        """,
        tags=["Users"],
        request=UserInputSerializer,
        responses={
            200: UserOutputModelSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: OpenApiResponse(description="User not found"),
            403: OpenApiResponse(description="Permission denied"),
        },
    )
    def put(self, request: Request, user_id: int) -> Response:

        serializer = UserInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = full_update(
                data=serializer.validated_data,
                user_id=user_id,
            )
        except Exception as e:
            logger.exception(f"database error {e}")
            raise

        logger.info("user updated! -> full update")

        return Response(
            UserOutputModelSerializer(user).data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Partial Update User",
        description="""
Update one or more fields of a user.

Only the supplied fields will be modified.
        """,
        tags=["Users"],
        request=UserInputSerializer,
        responses={
            200: UserOutputModelSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: OpenApiResponse(description="User not found"),
            403: OpenApiResponse(description="Permission denied"),
        },
    )
    def patch(self, request: Request, user_id: int) -> Response:

        serializer = UserInputSerializer(
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        try:
            user = partial_update(
                data=serializer.validated_data,
                user_id=user_id,
            )
        except Exception as e:
            logger.exception(f"database error {e}")
            raise

        logger.info("user updated! -> partial update")

        return Response(
            UserOutputModelSerializer(user).data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Delete User",
        description="""
Delete a user permanently.

This operation cannot be undone.
        """,
        tags=["Users"],
        responses={
            204: OpenApiResponse(description="User deleted successfully"),
            404: OpenApiResponse(description="User not found"),
            403: OpenApiResponse(description="Permission denied"),
        },
    )
    def delete(self, request: Request, user_id: int) -> Response:

        try:
            delete_user(user_id=user_id)
        except Exception:
            logger.exception("database error")
            raise

        logger.info("user deleted!")

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )