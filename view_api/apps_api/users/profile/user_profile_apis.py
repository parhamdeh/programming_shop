

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
from users.selectors.profile_selector import get_user_favorite_posts, get_user_subscription_detail
from users.services.otp_services import create_otp_code
from users.tasks import delete_otp_task, send_otp_task
from view_api.apps_api.users.authentication.authentication_serializers import RefreshTokenOutputSerializer, RegisterInputSerializer, VerifyOtpSerializer
from view_api.apps_api.users.profile.user_profile_serializer import ProfileOutputSerializer
from view_api.permissions import ProfilePermission
from view_api.renderers import CustomResponseRenderer
from view_api.throttle import AdminRequestThrottle, UserRequestThrottle
from view_api.apps_api.users.user.users_serializer import UserInputSerializer, UserOutputModelSerializer

from users.services.user_services import register
from users.selectors.user_selector import get_users_list

import logging

logger = logging.getLogger(__name__)



class ProfileAPIView(APIView):
    renderer_classes = (CustomResponseRenderer,)
    permission_classes = (ProfilePermission,)
    throttle_classes = (UserRequestThrottle,)

    @extend_schema(
    summary="User profile",
    description="Returns the authenticated user's profile information, active subscription, and favorite posts.",
    responses={
        200: ProfileOutputSerializer,
        403: OpenApiResponse(description="Permission denied"),
        404: OpenApiResponse(description="User not found"),
    },
    )
    def get(self, request: Request, user_id: int) -> Response:
        subscription = get_user_subscription_detail(request=request)
        favorits = get_user_favorite_posts(request=request)

        
        data = {
                "user": request.user,
                "subscription": subscription,
                "favorits": favorits,
            }

        serializer = ProfileOutputSerializer(instance=data)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            )
    
    