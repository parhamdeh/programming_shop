# Local Apps
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _



class BaseModel(models.Model):
    created_at = models.DateTimeField(
        db_index=True,
        default=timezone.now,
        verbose_name=_("ساخته شده در تاریخ")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("آخرین بروز رسانی")
    )

    class Meta:
        abstract = True