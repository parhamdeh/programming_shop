# Local Apps
from utils.exceptions import ApplicationError

# Third Party Packages
from rest_framework import status


class UserAlreadyExistsError(ApplicationError):
    default_detail = "User already exists"


class SubscriptionExpiredError(ApplicationError):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Subscription has expired"


class OTPExpiredError(ApplicationError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "OTP has expired"