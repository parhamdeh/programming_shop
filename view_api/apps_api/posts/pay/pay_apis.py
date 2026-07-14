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
from view_api.permissions import BuySubscriptionPermission

logger = logging.getLogger(__name__)

ZP_API_REQUEST = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://sandbox.zarinpal.com/pg/StartPay/"

CALLBACK_URL = "http://127.0.0.1:8000/api/subscriptions/verify/"

class SubscriptionPaymentAPIView(APIView):

    permission_classes = (BuySubscriptionPermission,)

    @extend_schema(
        summary="Create payment",
        description="Create zarinpal payment request.",
        responses={
            200: SubscriptionPaymentOutputSerializer,
            404: OpenApiResponse(description="Subscription not found"),
        },
    )
    def post(self, request: Request, subscription_id: int):

        subscription = get_subscription_by_id(sub_id=subscription_id).first()

        if not subscription:
            raise NotFound("subscription not found")

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
            result = response.json()

        except requests.RequestException:
            logger.exception("payment gateway unavailable")

            return Response(
                {"message": "payment gateway unavailable"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        logger.info(result)

        data = result.get("data", {})
        errors = result.get("errors", {})

        if data.get("code") != 100:

            return Response(
                {
                    "success": False,
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        authority = data["authority"]

        request.session["subscription"] = {
            "subscription_id": subscription.id,
            "authority": authority,
        }

        return Response(
            {
                "success": True,
                "authority": authority,
                "payment_url": f"{ZP_API_STARTPAY}{authority}",
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

        payment = request.session.get("subscription")

        if not payment:
            return Response(
                {
                    "success": False,
                    "message": "session expired",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        status_param = request.GET.get("Status")
        authority = request.GET.get("Authority")
        print(request.GET)
        print(request.GET.get("Status"))
        print(request.GET.get("Authority"))
        if status_param != "OK":
            return Response(
                {
                    "success": False,
                    "message": "payment cancelled",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if authority != payment["authority"]:
            return Response(
                {
                    "success": False,
                    "message": "invalid authority",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        subscription = get_subscription_by_id(
            sub_id=payment["subscription_id"]
        ).first()

        payload = {
            "merchant_id": settings.MERCHANT,
            "amount": subscription.price,
            "authority": authority,
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        try:
            response = requests.post(
                ZP_API_VERIFY,
                json=payload,
                headers=headers,
                timeout=10,
            )
            print(response.status_code)
            print(response.text)

            result = response.json()

        except requests.RequestException:
            return Response(
                {
                    "success": False,
                    "message": "gateway unavailable",
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        logger.info(result)

        data = result.get("data", {})
        errors = result.get("errors", {})

        if data.get("code") != 100:

            return Response(
                {
                    "success": False,
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        create_user_subscription(
            user=request.user,
            subscription=subscription,
        )

        request.session.pop("subscription", None)

        return Response(
            {
                "success": True,
                "ref_id": data.get("ref_id"),
                "message": "payment successful",
            }
        )