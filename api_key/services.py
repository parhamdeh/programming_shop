import secrets


from api_key.models import APIKeyModel
from users.models import BaseUserModel
from utils.exceptions import ApplicationError


def create_api_key(*, user: BaseUserModel) -> APIKeyModel:
    expire = 30
    
    api_key = secrets.token_urlsafe(32)
    try:
        api_key = APIKeyModel.objects.create(user=user, key=api_key, expires_at=expire, is_active=True)
    except Exception:
        raise ApplicationError()
    
    return api_key
    
