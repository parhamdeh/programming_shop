from users.models import BaseUserModel
from utils.models import BaseModel


from django.db import models
from django.utils.translation import gettext_lazy as _


class APIKeyModel(BaseModel):
    user = models.ForeignKey(BaseUserModel, on_delete=models.CASCADE, related_name="user_api_key", verbose_name=_("کاربر"))
    key = models.CharField()
    last_use = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    expires_at = models.PositiveIntegerField()

    def __str__(self):
        return self.user.username + f"has a api key {self.key}"
    




