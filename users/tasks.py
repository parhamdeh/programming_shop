# Third Party Packages
from celery import shared_task

# Local Apps
from users.services.sms_service import send_otp
from users.models import OtpCode



@shared_task
def send_otp_task(phone, code):
    print(1)
    send_otp(phone, code)

@shared_task
def delete_otp_task(otp_id: int):
    OtpCode.objects.filter(id=otp_id, is_used=False).delete()