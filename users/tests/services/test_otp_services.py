import pytest

from users.models import OtpCode

from users.services.otp_services import create_otp_code

from users.tests.factories.users import BaseUserFactory


pytestmark = pytest.mark.django_db


class TestCreateOtp:

    def test_create_otp(self):

        user = BaseUserFactory()

        otp = create_otp_code(
            user=user,
        )

        assert isinstance(otp, OtpCode)

        assert otp.user == user

        assert len(otp.code) == 6

        assert otp.code.isdigit()


    def test_every_call_creates_new_otp(self):

        user = BaseUserFactory()

        otp1 = create_otp_code(user=user)

        otp2 = create_otp_code(user=user)

        assert otp1.id != otp2.id

        assert OtpCode.objects.count() == 2