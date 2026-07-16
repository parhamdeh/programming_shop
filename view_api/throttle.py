# Third Party Packages
from rest_framework.throttling import AnonRateThrottle


class AdminRequestThrottle(AnonRateThrottle):
    rate = "7/min"

class UserRequestThrottle(AnonRateThrottle):
    rate = "4/min"