import logging
import requests

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
)

from posts.selectors.subscription import get_subscription_by_id
from posts.services.subscription import create_user_subscription

from view_api.apps_api.posts.pay.pay_serializers import (
    SubscriptionPaymentOutputSerializer,
    SubscriptionVerifyOutputSerializer,
)

logger = logging.getLogger(__name__)

ZP_API_REQUEST = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://sandbox.zarinpal.com/pg/StartPay/"

CALLBACK_URL = "http://127.0.0.1:8000/api/subscriptions/verify/"

class SubscriptionPaymentAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    @extend_schema(
        summary="Create payment",
        description="Create zarinpal payment request.",
        responses={
            200: SubscriptionPaymentOutputSerializer,
            404: OpenApiResponse(description="Subscription not found"),
        },
    )
    def post(self, request: Request, subscription_id: int):

        subscription = get_subscription_by_id(
            sub_id=subscription_id
        ).first()

        if not subscription:
            logger.warning("subscription not found")
            raise NotFound("subscription not found")

        request.session["subscription"] = {
            "subscription_id": subscription.id,
        }

        payload = {
            "merchant_id": settings.MERCHANT,
            "amount": subscription.price,
            "description": "Subscription Payment",
            "callback_url": CALLBACK_URL,
            "metadata": {
                "mobile": str(request.user.phone),
            },
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        try:

            response = requests.post(
                ZP_API_REQUEST,
                json=payload,
                headers=headers,
                timeout=10,
            )

            logger.info("payment request sent")

        except requests.RequestException:

            logger.exception("connection error")

            return Response(
                {
                    "message": "payment gateway unavailable",
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        result = response.json()

        if result["data"]["code"] != 100:

            logger.warning("payment request failed")

            return Response(
                {
                    "message": "payment failed",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        authority = result["data"]["authority"]

        logger.info("payment created")

        return Response(
            {
                "payment_url":
                    f"{ZP_API_STARTPAY}{authority}"
            }
        )
    
class SubscriptionVerifyAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    @extend_schema(
        summary="Verify payment",
        parameters=[
            OpenApiParameter("Status", str),
            OpenApiParameter("Authority", str),
        ],
        responses={
            200: SubscriptionVerifyOutputSerializer,
        },
    )
    def get(self, request: Request):

        sub_id = request.session.get(
            "subscription",
            {}
        ).get("subscription_id")

        if not sub_id:

            return Response(
                {
                    "success": False,
                    "message": "session expired",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        subscription = get_subscription_by_id(
            sub_id=sub_id
        ).first()

        payload = {
            "merchant_id": settings.MERCHANT,
            "amount": subscription.price,
            "authority": request.GET.get("Authority"),
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        response = requests.post(
            ZP_API_VERIFY,
            json=payload,
            headers=headers,
            timeout=10,
        )

        result = response.json()

        if result["data"]["code"] == 100:

            create_user_subscription(
                user=request.user,
                subscription=subscription,
            )

            ref_id = result["data"]["ref_id"]

            logger.info(
                f"payment success ref={ref_id}"
            )

            del request.session["subscription"]

            return Response(
                {
                    "success": True,
                    "ref_id": ref_id,
                    "message": "payment successful",
                }
            )

        logger.warning("payment verify failed")

        return Response(
            {
                "success": False,
                "message": "payment failed",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )