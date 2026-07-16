# Third Party Packages
import logging
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

# Local Apps
from posts.selectors.subscription import get_subscription_by_id
from posts.services.post import delete_sub, full_update_sub, partial_update_sub
from view_api.apps_api.posts.subscription.subscription_serializers import SubscriptionInputSerializer, SubscriptionOutputModelSerializer
from view_api.permissions import BuySubscriptionPermission, IsAdminOrReadOnly
from view_api.renderers import CustomResponseRenderer
from view_api.throttle import AdminRequestThrottle



logger = logging.getLogger(__name__)



class SubscriptionRetrieveUpdateDstroyAPIView(APIView):
    renderer_classes = (CustomResponseRenderer,)
    throttle_classes = (AdminRequestThrottle,)
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated)

    @extend_schema(
    summary="Retrieve Subscription",
    description="Retrieve a subscription by id.",
    responses={
        200: SubscriptionOutputModelSerializer,
        404: OpenApiResponse(description="Subscription not found"),
    },
)
    def get(self, requesta: Request, subscription_id: int) -> Response:
        subscription = get_subscription_by_id(sub_id=subscription_id).first()
        if not subscription:
            raise NotFound("subscription not found")
        
        return Response(
            data=SubscriptionOutputModelSerializer(instance=subscription).data,
            status=status.HTTP_200_OK,
        )
    
    @extend_schema(
    summary="Update Subscription",
    description="Fully update a subscription. Admin only.",
    request=SubscriptionInputSerializer,
    responses={
        200: SubscriptionOutputModelSerializer,
        400: OpenApiResponse(description="Validation error"),
        403: OpenApiResponse(description="Permission denied"),
        404: OpenApiResponse(description="Subscription not found"),
    },
    )
    def put(self, requesta: Request, subscription_id: int) -> Response:
        serializer = SubscriptionInputSerializer(data=requesta.data)
        serializer.is_valid(raise_exception=True)
        try:
            subscription = full_update_sub(subscription_id=subscription_id, data=serializer.validated_data)
        except Exception as e:
            logger.exception(f"database error {e}")
            raise

        return Response(
            data=SubscriptionOutputModelSerializer(instance=subscription).data,
            status=status.HTTP_200_OK,
        )
    
    @extend_schema(
    summary="Partial Update Subscription",
    description="Partially update a subscription. Admin only.",
    request=SubscriptionInputSerializer,
    responses={
        200: SubscriptionOutputModelSerializer,
        400: OpenApiResponse(description="Validation error"),
        403: OpenApiResponse(description="Permission denied"),
        404: OpenApiResponse(description="Subscription not found"),
    },
    )
    def patch(self, requesta: Request, subscription_id: int) -> Response:
        serializer = SubscriptionInputSerializer(data=requesta.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            subscription = partial_update_sub(subscription_id=subscription_id, data=serializer.validated_data)
        except Exception as e:
            logger.exception(f"database error {e}")

        return Response(
            data=SubscriptionOutputModelSerializer(instance=subscription).data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
    summary="Delete Subscription",
    description="Delete a subscription. Admin only.",
    responses={
        204: OpenApiResponse(description="Subscription deleted successfully"),
        403: OpenApiResponse(description="Permission denied"),
        404: OpenApiResponse(description="Subscription not found"),
    },
    )
    def delete(self, requesta: Request, subscription_id: int) -> Response:
        delete_sub(subscription_id=subscription_id)
        return Response(status=status.HTTP_204_NO_CONTENT)