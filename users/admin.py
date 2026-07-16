# Django Built-in modules   
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Local Apps
from .models import BaseUserModel, OtpCode, UserProfileModel

# Third Party Packages
from unfold.admin import ModelAdmin



@admin.register(BaseUserModel)
class BaseUserAdmin(ModelAdmin, UserAdmin):
    list_display = (
        "id",
        "username",
        "phone",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "username",
        "phone",
    )

    ordering = (
        "id",
    )



admin.site.register(OtpCode)
admin.site.register(UserProfileModel)