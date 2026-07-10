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
import json
import logging

from posts.services.subscription import create_user_subscription

logger = logging.getLogger(__name__)

if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'


ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"


CallbackURL = 'http://127.0.0.1:8080/posts/verify/'



class SubscriptionDetailView(LoginRequiredMixin, NoActiveSubscriptionRequiredMixin, View):
    template_name = "subscription/detail.html"
    def get(self, request: HttpRequest, subscription_id: int) -> HttpResponse:
        try:
            subscription = get_subscription_by_id(sub_id=subscription_id).first()
        except Exception as e:
                logger.exception(
                f"database error: {e}"
                )
        
        if not subscription:
            raise ObjectDoesNotExist("not found!")

        return render(request=request,
                      template_name=self.template_name,
                      context={
                          'category' : subscription,
                      })
    

class SubscriptionPaymentView(LoginRequiredMixin, NoActiveSubscriptionRequiredMixin, View):
    
    def get(self, request: HttpRequest, subscription_id: int) -> HttpResponse:
        try:
            subscription = get_subscription_by_id(sub_id=subscription_id).first()
        except Exception as e:
                logger.exception(
                f"database error: {e}"
                )
        
        if not subscription:
            raise ObjectDoesNotExist("not found!")
        
        request.session["subscription"] = {
            'subscription_id' : subscription_id,
        }

        data = {
        "MerchantID": settings.MERCHANT,
        "Amount": subscription.price,
        "Description": "توضیحات مربوط به تراکنش را در این قسمت وارد کنید",
        "Phone": str(request.user.phone),
        "CallbackURL": CallbackURL,
    }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }

        try:
            response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)
            logger.info("sent post request to zarinpal")

            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    logger.info("sent a success post request to zarinpal")
                    payment_url = ZP_API_STARTPAY + str(data['Authority'])
                    return redirect(payment_url)
                    # return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']}
                else:
                    logger.info("sent a faild post request to zarinpal")
                    messages.error(request, f"{data['Status']}")
                    return redirect("posts:subscription-detail", subscription_id=subscription_id)
                    # return {'status': False, 'code': str(response['Status'])}
            # return response
            # messages.error(request, f"خطا در ایجاد تراکنش: کد {data['Status']}")
            return redirect("posts:subscription-detail", subscription_id=subscription_id)
    
        except requests.exceptions.Timeout:
            # messages.error(request,f"خطا در ایجاد تراکنش: کد  f"خطا در ایجاد تراکنش: کد {data['Status']}")
            return redirect("posts:subscription-detail", subscription_id=subscription_id)
            # return {'status': False, 'code': 'timeout'}
        except requests.exceptions.ConnectionError:
            # messages.error(request, f"خطا در ایجاد تراکنش: کد {data['Status']}")
            return redirect("posts:subscription-detail", subscription_id=subscription_id)
            # return {'status': False, 'code': 'connection error'}
    

class VerifyPay(LoginRequiredMixin, NoActiveSubscriptionRequiredMixin, View):

    def get(self, request: HttpRequest) -> HttpResponse:
        
        sub_id = request.session["subscription"]["subscription_id"]
        subscription = get_subscription_by_id(sub_id=int(sub_id)).first()

        t_status = request.GET.get("Status")
        t_authority = request.GET["Authority"]
        
        if t_status == "OK":
            data = {
            "MerchantID": settings.MERCHANT,
            "Amount": subscription.price,
            "Authority": t_authority,
        }
            data = json.dumps(data)
    
            headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
            response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    create_user_subscription(user=request.user, subscription=subscription)
                    logger.info("payment successfully!")
                    messages.info(request, "payment successfully!")
                    return {'status': True, 'RefID': response['RefID']}
                else:
                    logger.error("payment faild!!")
                    return {'status': False, 'code': str(response['Status'])}
            return response

        else:
            logger.warning(f"Transaction faild or canceled by {request.user.username}")
            return HttpResponse("Transaction faild or canceled by user!")
        
