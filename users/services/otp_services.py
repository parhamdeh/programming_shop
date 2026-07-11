from users.models import BaseUserModel, OtpCode
from random import randint


def create_otp_code(*, phone):
    otp = str(randint(100000, 999999))
    return OtpCode.objects.create(phone=phone, code=otp)