# Third Party Packages
import logging
from typing import Any
from rest_framework.request import Request
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

# Django Built-in modules
from django.db import transaction

# Local Apps
from users.models import OtpCode
from users.services.otp_services import create_otp_code
from users.tasks import delete_otp_task, send_otp_task
from view_api.apps_api.users.authentication.authentication_serializers import RefreshTokenOutputSerializer, RegisterInputSerializer, VerifyOtpSerializer
from view_api.apps_api.users.user.users_serializer import UserInputSerializer
from view_api.exceptions import OTPExpiredError
from view_api.renderers import CustomResponseRenderer
from view_api.throttle import UserRequestThrottle
from users.services.user_services import create_user, register, register_request, verify_before_register
from users.selectors.user_selector import get_users_list


logger = logging.getLogger(__name__)



class UserRegisterAPIView(GenericAPIView):
    throttle_classes = [UserRequestThrottle]
    renderer_classes = [CustomResponseRenderer]
    serializer_class = UserInputSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        try:
            register_request(phone=serializer.validated_data["phone"])
        except Exception as ex:
            logger.exception(f"error in create otp")
            raise
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer=serializer)
        
        request.session["register_data"] = {
            "username": serializer.validated_data["username"],
            "password": serializer.validated_data["password"],
            "phone": str(serializer.validated_data["phone"]),
        }
        logger.info(
        "Verification code sent successfully. phone=%s",
        serializer.validated_data["phone"],)

        return Response({
            "msg" : "Verification code sent successfully."
        },
        status=status.HTTP_200_OK
        )
    
    @extend_schema(
    tags=["account"],
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
    def post(self, request: Request):
        return self.create(request)
    
    
class VerifyOtpAPIView(CreateAPIView):
    renderer_classes = (CustomResponseRenderer,)
    permission_classes = (AllowAny,)
    throttle_classes = (UserRequestThrottle,)
    serializer_class = VerifyOtpSerializer


    def perform_create(self, serializer):
        register_data = self.request.session.get("register_data")
        if register_data is None:
            raise OTPExpiredError()
        return verify_before_register(
            register_data=register_data,
            code=serializer.validated_data['code']
        )
    
    @extend_schema(
    tags=["account"],
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
    def create(self, request: Request, *args: Any, **kwargs: Any):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.perform_create(serializer=serializer)
        logger.info(
            "%s verified successfully.",
            user.username,
        )
        token = RefreshToken.for_user(user)
        output_data = {
                "refresh": str(token),
                "access": str(token.access_token),
                "username" : user.username,
                "phone" : user.phone,

            }
        del request.session["register_data"]


        return Response(
            data = RefreshTokenOutputSerializer(instance=output_data).data,
            status=status.HTTP_201_CREATED,
            )