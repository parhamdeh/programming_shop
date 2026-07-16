# Third Party Packages
from drf_error_handler.formatter import ExceptionFormatter


class StatusExceptionFormatter(ExceptionFormatter):

    def format_error_response(self, error_response):
        data = super().format_error_response(error_response)
        data["status"] = getattr(self.exc, "status_code", 500)
        return data