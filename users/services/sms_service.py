# Local Apps
from config import settings

# Third Party Packages
from kavenegar import KavenegarAPI


def send_otp(phone: str, code: str):
    api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
    print(phone)
    params = {
        "sender" : settings.KAVENEGAR_SENDER,
        "receptor": phone,
        "message": f"Your verification code is: {code}",
    }

    return api.sms_send(params)