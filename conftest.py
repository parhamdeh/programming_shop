import logging
import pytest


@pytest.fixture(autouse=True)
def disable_django_request_logging():
    logger = logging.getLogger("django.request")
    previous_level = logger.getEffectiveLevel()
    logger.setLevel(logging.CRITICAL)
    yield
    logger.setLevel(previous_level)