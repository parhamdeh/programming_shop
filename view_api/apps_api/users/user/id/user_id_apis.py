from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework import generics, mixins

from view_api.permissions import UserChangeIfAdminOrSelfUser
from view_api.renderers import CustomResponseRenderer
from view_api.throttle import AdminRequestThrottle
from view_api.apps_api.users.user.users_serializer import UserInputSerializer, UserOutputModelSerializer

from users.services.user_services import delete_user, full_update, partial_update
from users.selectors.user_selector import get_user_by_id

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

import logging

logger = logging.getLogger(__name__)


class UserRetrieveUpdatadeDestroy(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    Retrieve, update or delete a user.
    """
    renderer_classes = (CustomResponseRenderer,)
    permission_classes = (UserChangeIfAdminOrSelfUser,)
    throttle_classes = (AdminRequestThrottle,)
    serializer_class = UserOutputModelSerializer

    def get_object(self):
        user = get_user_by_id(user_id=self.kwargs["user_id"]).first()

        if not user:
            logger.info("user not found")
            raise NotFound("user not found!")

        return user

    @extend_schema(
        summary="Retrieve User",
        description="""
Retrieve a single user by its unique identifier.

Only administrators are allowed to access this endpoint.
        """,
        tags=["account"],
        responses={
            200: UserOutputModelSerializer,
            404: OpenApiResponse(description="User not found"),
            403: OpenApiResponse(description="Permission denied"),
        },
    )
    def get(self, request: Request, user_id: int) -> Response:
        return self.retrieve(request, user_id=user_id)

    @extend_schema(
        summary="Full Update User",
        description="""
Replace all editable fields of a user.

All required fields must be provided.
        """,
        tags=["account"],
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
            self.get_serializer(user).data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Partial Update User",
        description="""
Update one or more fields of a user.

Only the supplied fields will be modified.
        """,
        tags=["account"],
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
            self.get_serializer(user).data,
            status=status.HTTP_200_OK,
        )

    def perform_destroy(self, instance) -> None:
        try:
            delete_user(user_id=instance.id)
        except Exception:
            logger.exception("database error")
            raise

        logger.info("user deleted!")

    @extend_schema(
        summary="Delete User",
        description="""
Delete a user permanently.

This operation cannot be undone.
        """,
        tags=["account"],
        responses={
            204: OpenApiResponse(description="User deleted successfully"),
            404: OpenApiResponse(description="User not found"),
            403: OpenApiResponse(description="Permission denied"),
        },
    )
    def delete(self, request: Request, user_id: int) -> Response:
        return self.destroy(request, user_id=user_id)