# Django Built-in modules   
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.text import Truncator
from django.core.validators import EMPTY_VALUES


# Local Apps
from users.selectors.user_selector import get_users_list
from .models import BaseUserModel, OtpCode, UserProfileModel

# Third Party Packages
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.paginator import InfinitePaginator
from unfold.contrib.filters.admin import TextFilter, FieldTextFilter




class CustomTextFilter(TextFilter):
    title = _("Custom filter")
    parameter_name = "query_param_in_uri"

    def queryset(self, request, queryset):
        if self.value() not in EMPTY_VALUES:
            queryset = get_users_list()
            return queryset.filter(phone=self.value())

        return queryset




@admin.register(BaseUserModel)
class BaseUserAdmin(ModelAdmin, UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    paginator = InfinitePaginator
    show_full_result_count = False

    list_display = (
        "id",
        "phone",
        "username",
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
    list_select_related = [] 
    
    # فیلدها
    fieldsets = (
        (_("اطلاعات شخصی"), {
            "fields": ("username", "phone",)
        }),
        (_("مجوزات"), {
            "fields": ("is_staff", "is_superuser", "is_active", "user_permissions"),
            "classes": ("collapse",),  
        }),
        (_("تاریخ‌ها"), {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )
    
    @admin.display(description='', empty_value='_')
    def display_truncate_user(self, obj):
        return Truncator(obj.username).chars(50)



@admin.register(UserProfileModel)
class BaseUserAdmin(ModelAdmin):
    change_password_form = AdminPasswordChangeForm
    list_display = (
        "id",
        "user",
        "subscription",
    )

    search_fields = (
        "user.id",
        "subscription",
    )

    ordering = (
        "id",
    )
    


admin.site.register(OtpCode)
