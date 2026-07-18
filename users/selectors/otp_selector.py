from users.models import OtpCode


def get_not_used_otp(*, phone, code) -> OtpCode:
    return OtpCode.objects.filter(
                phone=phone,
                code=code,
                is_used=False,
            ).order_by("-created_at").first()