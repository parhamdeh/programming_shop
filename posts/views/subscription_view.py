from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

from posts.mixins import NoActiveSubscriptionRequiredMixin
from posts.selectors.subscription import get_subscription_by_id, get_user_subscription_with_user

from config import settings
import requests
import logging

from posts.services.subscription import create_user_subscription

logger = logging.getLogger(__name__)

ZP_API_REQUEST = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://sandbox.zarinpal.com/pg/StartPay/"

CallbackURL = 'http://127.0.0.1:8000/posts/verify/'


class SubscriptionDetailView(LoginRequiredMixin, NoActiveSubscriptionRequiredMixin, View):
    template_name = "subscription/detail.html"

    def get(self, request: HttpRequest, subscription_id: int) -> HttpResponse:
        try:
            subscription = get_subscription_by_id(sub_id=subscription_id).first()
        except Exception as e:
            logger.exception(f"database error: {e}")
            subscription = None

        if not subscription:
            raise ObjectDoesNotExist("not found!")

        return render(
            request=request,
            template_name=self.template_name,
            context={'category': subscription},
        )


class SubscriptionPaymentView(LoginRequiredMixin, NoActiveSubscriptionRequiredMixin, View):

    def get(self, request: HttpRequest, subscription_id: int) -> HttpResponse:
        try:
            subscription = get_subscription_by_id(sub_id=subscription_id).first()
        except Exception as e:
            logger.exception(f"database error: {e}")
            subscription = None

        if not subscription:
            raise ObjectDoesNotExist("not found!")

        request.session["subscription"] = {
            'subscription_id': subscription_id,
        }

        payload = {
            "merchant_id": settings.MERCHANT,
            "amount": subscription.price,
            "description": "خرید اشتراک",
            "callback_url": CallbackURL,
            "metadata": {
                "mobile": str(request.user.phone),
            },
        }

        headers = {'content-type': 'application/json', 'accept': 'application/json'}

        try:
            response = requests.post(ZP_API_REQUEST, json=payload, headers=headers, timeout=10)
            logger.info("sent post request to zarinpal")

            if response.status_code == 200:
                result = response.json()

                if result.get("data", {}).get("code") == 100:
                    authority = result["data"]["authority"]
                    logger.info("zarinpal payment request successful")
                    return redirect(ZP_API_STARTPAY + authority)
                else:
                    errors = result.get("errors", {})
                    logger.warning(f"zarinpal request failed: {errors}")
                    messages.error(request, "خطا در ایجاد تراکنش. لطفاً دوباره تلاش کنید.")
                    return redirect("posts:subscription-detail", subscription_id=subscription_id)

            logger.warning(f"zarinpal returned non-200 status: {response.status_code}")
            messages.error(request, "خطا در ارتباط با درگاه پرداخت.")
            return redirect("posts:subscription-detail", subscription_id=subscription_id)

        except requests.exceptions.Timeout:
            logger.warning("zarinpal request timed out")
            messages.error(request, "درگاه پرداخت پاسخ نداد. دوباره تلاش کنید.")
            return redirect("posts:subscription-detail", subscription_id=subscription_id)

        except requests.exceptions.ConnectionError:
            logger.warning("zarinpal connection error")
            messages.error(request, "مشکل در اتصال به درگاه پرداخت.")
            return redirect("posts:subscription-detail", subscription_id=subscription_id)


class VerifyPay(LoginRequiredMixin, NoActiveSubscriptionRequiredMixin, View):

    def get(self, request: HttpRequest) -> HttpResponse:
        sub_id = request.session.get("subscription", {}).get("subscription_id")
        if not sub_id:
            messages.error(request, "نشست پرداخت یافت نشد.")
            return redirect("home:home")

        subscription = get_subscription_by_id(sub_id=int(sub_id)).first()

        t_status = request.GET.get("Status")
        t_authority = request.GET.get("Authority")

        if t_status == "OK" and t_authority:
            payload = {
                "merchant_id": settings.MERCHANT,
                "amount": subscription.price,
                "authority": t_authority,
            }
            headers = {'content-type': 'application/json', 'accept': 'application/json'}

            response = requests.post(ZP_API_VERIFY, json=payload, headers=headers, timeout=10)

            if response.status_code == 200:
                result = response.json()

                if result.get("data", {}).get("code") == 100:
                    create_user_subscription(user=request.user, subscription=subscription)
                    ref_id = result["data"]["ref_id"]
                    logger.info(f"payment successful! ref_id={ref_id}")
                    messages.success(request, f"پرداخت با موفقیت انجام شد. کد پیگیری: {ref_id}")
                    del request.session["subscription"]
                    return redirect("home:home")
                else:
                    logger.error(f"payment verification failed: {result.get('errors')}")
                    messages.error(request, "تأیید پرداخت ناموفق بود.")
                    return redirect("home:home")

            messages.error(request, "خطا در ارتباط با درگاه پرداخت.")
            return redirect("home:home")

        else:
            logger.warning(f"Transaction failed or canceled by {request.user.username}")
            messages.error(request, "تراکنش توسط شما لغو شد یا ناموفق بود.")
            return redirect("home:home")