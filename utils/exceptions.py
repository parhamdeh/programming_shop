from rest_framework.exceptions import APIException
from rest_framework import status


class ApplicationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Application error"
    default_code = "application_error"

    def __init__(self, detail=None, *, extra=None):
        self.extra = extra or {}
        super().__init__(detail or self.default_detail)