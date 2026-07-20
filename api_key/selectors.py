


from api_key.models import APIKeyModel


def get_api_key(*, key: str) -> APIKeyModel:
    return APIKeyModel.objects.filter(key=key)