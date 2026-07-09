from django.db import models
from django.conf import settings

from posts.models import Subscription


class Payment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
    )

    amount = models.PositiveIntegerField()

    authority = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    ref_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    is_paid = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.user} - {self.subscription}"