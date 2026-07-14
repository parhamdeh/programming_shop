from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from posts.selectors.subscription import get_all_subscriptions
from posts.services.subscription import create_subscription
from view_api.apps_api.posts.subscription.subscription_serializers import SubscriptionInputSerializer, SubscriptionOutputModelSerializer
from view_api.permissions import BuySubscriptionPermission
from view_api.throttle import AdminRequestThrottle

import logging

logger = logging.getLogger(__name__)


class SubscriptionListCreateAPIView(APIView):
    throttle_classes = (AdminRequestThrottle,)
    permission_classes = (BuySubscriptionPermission, IsAuthenticated)

    @extend_schema(
    summary="List Subscriptions",
    description="Retrieve all subscriptions.",
    responses={
        200: SubscriptionOutputModelSerializer(many=True),
    },
    )
    def get(self, request: Request) -> Response:
        try:
            subscription = get_all_subscriptions()
        except Exception as e:
            logger.exception(f"database error{e}")
            raise
        return Response(
            data=SubscriptionOutputModelSerializer(instance=subscription, many=True).data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
    summary="Create Subscription",
    description="Create a new subscription. Admin only.",
    request=SubscriptionInputSerializer,
    responses={
        201: SubscriptionOutputModelSerializer,
        400: OpenApiResponse(description="Validation error"),
        403: OpenApiResponse(description="Permission denied"),
    },
    )
    def post(self, request: Request) -> Response:
        serializer = SubscriptionInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            subscription = create_subscription(data=serializer.validated_data)
        except Exception as e:
            logger.exception(f"database error {e}")
            raise

        return Response(
            data=SubscriptionOutputModelSerializer(instance=subscription).data,
            status=status.HTTP_201_CREATED,
        )