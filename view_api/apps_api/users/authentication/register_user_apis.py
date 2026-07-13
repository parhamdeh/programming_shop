from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from users.models import OtpCode
from users.services.otp_services import create_otp_code
from users.tasks import delete_otp_task, send_otp_task
from view_api.apps_api.users.authentication.authentication_serializers import RefreshTokenOutputSerializer, RegisterInputSerializer, VerifyOtpSerializer
from view_api.pagination import UsersPagination
from view_api.throttle import AdminRequestThrottle, UserRequestThrottle
from view_api.apps_api.users.user.users_serializer import UserInputSerializer, UserOutputModelSerializer

from users.services.user_services import register
from users.selectors.user_selector import get_users_list

import logging

logger = logging.getLogger(__name__)



@extend_schema(
    summary="Register user",
    description="Send OTP to the user's phone number before creating the account.",
    request=RegisterInputSerializer,
    responses={
        200: OpenApiResponse(
            description="Verification code sent successfully."
        ),
        400: OpenApiResponse(
            description="Invalid request."
        ),
    },
)
class RegisterUserAPIView(APIView):
    permission_classes = (AllowAny,)
    throttle_classes = (UserRequestThrottle,)

    def post(self, request: Request) -> Response:
        serializer = RegisterInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = create_otp_code(phone=serializer.validated_data["phone"])
        send_otp_task.delay(phone=str(serializer.validated_data["phone"]),
                      code=otp.code)
        delete_otp_task.apply_async(
            args=[otp.id],
            countdown=120,
        )
        request.session["register_data"] = {
            "username": serializer.validated_data["username"],
            "password": serializer.validated_data["password"],
            "phone": str(serializer.validated_data["phone"]),
        }
        logger.info(
        "Verification code sent successfully. phone=%s",
        serializer.validated_data["phone"],
)

        return Response(
            {
                "detail": "Verification code sent successfully."
            },
            status=status.HTTP_200_OK,
        )
    
@extend_schema(
    summary="Verify OTP",
    description="Verify OTP code and create the user account.",
    request=VerifyOtpSerializer,
    responses={
        200: RefreshTokenOutputSerializer,
        400: OpenApiResponse(
            description="Invalid or expired verification code."
        ),
    },
)
class VerifyOtpAPIView(APIView):
    permission_classes = (AllowAny,)
    throttle_classes = (UserRequestThrottle,)

    def post(self, request: Request):

        serializer = VerifyOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        register_data = request.session.get("register_data")
        if register_data is None:
            return Response(
                {"detail": "Registration session expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        phone = register_data["phone"]
        code = serializer.validated_data["code"]

        otp = (
            OtpCode.objects.filter(
                phone=phone,
                code=code,
                is_used=False,
            )
            .order_by("-created_at")
            .first()
        )

        if otp is None:
            logger.warning(
            "Invalid OTP for phone %s",
            phone,
            )
            return Response(
                {"detail": "Invalid verification code."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if otp.is_expired():
            logger.warning(
            "Invalid OTP for phone %s",
            otp.phone,
            )
            otp.delete()

            return Response(
                {"detail": "Verification code has expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if register_data is None:
            return Response(
                {"detail": "Registration session expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        with transaction.atomic():
            otp.is_used = True
            otp.save(update_fields=["is_used"])

            user = register(
            username=register_data["username"],
            password=register_data["password"],
            phone=register_data["phone"],
            subscription=None,
            )

            otp.delete()
        logger.info(
            "%s verified successfully.",
            user.username,
        )
        del request.session["register_data"]

        token = RefreshToken.for_user(user)
        return Response(
            data = RefreshTokenOutputSerializer(
            {
                "refresh": str(token),
                "access": str(token.access_token),
            }
            ).data,

            status=status.HTTP_201_CREATED,
            )