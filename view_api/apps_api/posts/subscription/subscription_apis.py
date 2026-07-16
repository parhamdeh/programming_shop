# Third Party Packages
import logging
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

# Local Apps
from posts.selectors.subscription import get_all_subscriptions
from posts.services.subscription import create_subscription
from view_api.apps_api.posts.subscription.subscription_serializers import SubscriptionInputSerializer, SubscriptionOutputModelSerializer
from view_api.permissions import BuySubscriptionPermission, IsAdminOrReadOnly
from view_api.renderers import CustomResponseRenderer
from view_api.throttle import AdminRequestThrottle


logger = logging.getLogger(__name__)


class SubscriptionListCreateAPIView(generics.ListCreateAPIView):
    renderer_classes = (CustomResponseRenderer,)
    throttle_classes = (AdminRequestThrottle,)
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated)

    def get_queryset(self):
        try:
            return get_all_subscriptions()
        except Exception as e:
            logger.exception(f"database error{e}")
            raise

    def get_serializer_class(self):
        if self.request.method == "POST":
            return SubscriptionInputSerializer
        return SubscriptionOutputModelSerializer

    def perform_create(self, serializer) -> None:
        try:
            subscription = create_subscription(data=serializer.validated_data)
        except Exception as e:
            logger.exception(f"database error {e}")
            raise
        serializer.instance = subscription

    @extend_schema(
    summary="List Subscriptions",
    description="Retrieve all subscriptions.",
    responses={
        200: SubscriptionOutputModelSerializer(many=True),
    },
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

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
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = self.create(request, *args, **kwargs)
        response.status_code = status.HTTP_201_CREATED
        return response