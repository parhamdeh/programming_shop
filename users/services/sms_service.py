from django.conf import settings
from kavenegar import KavenegarAPI


def send_otp(phone: str, code: str):
    api = KavenegarAPI(settings.KAVENEGAR_API_KEY)

    params = {
        "receptor": phone,
        "message": f"Your verification code is: {code}",
    }

    api.sms_send(params)