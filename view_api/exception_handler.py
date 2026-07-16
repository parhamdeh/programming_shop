# Django Built-in modules
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.exceptions import PermissionDenied
from django.http import Http404

# Third Party Packages
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler

# Local Apps
from utils.exceptions import ApplicationError


def custom_exception_handler(exc, context):
    # Django -> DRF
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    if isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    # Business exceptions
    if isinstance(exc, ApplicationError):
        return Response(
            {
                "success": False,
                "status": getattr(exc, "status_code", status.HTTP_400_BAD_REQUEST),
                "message": exc.message,
                "errors": {},
                "extra": getattr(exc, "extra", {}),
            },
            status=getattr(exc, "status_code", status.HTTP_400_BAD_REQUEST),
        )

    response = exception_handler(exc, context)

    if response is None:
        return response

    # Validation Errors
    if isinstance(exc, exceptions.ValidationError):
        response.data = {
            "success": False,
            "status": response.status_code,
            "message": "Validation error.",
            "errors": response.data,
            "extra": {},
        }
        return response

    # Other DRF Exceptions
    message = response.data.get("detail", "An error occurred.")

    response.data = {
        "success": False,
        "status": response.status_code,
        "message": message,
        "errors": {},
        "extra": {},
    }

    return response

def hacksoft_proposed_exception_handler(exc, ctx):
    """
    {
        "message": "Error message",
        "extra": {}
    }
    """
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    if isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    response = exception_handler(exc, ctx)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        if isinstance(exc, ApplicationError):
            data = {
                "message": exc.message,
                "extra": exc.extra
            }
            return Response(data, status=400)

        return response

    if isinstance(exc.detail, (list, dict)):
        response.data = {
            "detail": response.data
        }

    if isinstance(exc, exceptions.ValidationError):
        response.data["message"] = "Validation error"
        response.data["extra"] = {
            "fields": response.data["detail"]
        }
    else:
        response.data["message"] = response.data["detail"]
        response.data["extra"] = {}

    del response.data["detail"]

    return response