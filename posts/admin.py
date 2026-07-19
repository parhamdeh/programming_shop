# Django Built-in modules
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Third Party Packages
from mptt.admin import DraggableMPTTAdmin
from unfold.paginator import InfinitePaginator
from unfold.admin import ModelAdmin


# Local Apps
from posts.admin_folder.forms import PostAdminForm
from .models import (
    Post,
    Category,
    Comments,
    Subscription,
    UserSubscription,
    FavoritPost,
)

@admin.register(Post)
class PostAdmin(ModelAdmin):
   
    form = PostAdminForm
    paginator = InfinitePaginator
    show_full_result_count = False
    list_display = (
        "id",
        "title",
        "author",
        "category",
        "is_premium",
        "image",
        "video",
        "created_at",
    )
    

    list_filter = (
        "category",
        "is_premium",
    )

    search_fields = (
        "title",
        "content",
    )

    autocomplete_fields = (
        "author",
        "category",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = ("-created_at",)

    list_select_related = (
        "author",
        "category",
    )

    save_on_top = True

    list_per_page = 30
    fieldsets = (
        (_("نویسنده "), {
            "fields": ("author", )
        }),
        (_("محتوا"), {
            "fields": ("title", "content", "image", "video", "is_premium", "category"),
            "classes": ("collapse",),  
        }),
        (_("تاریخ‌ها"), {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )


@admin.register(Category)
class CategoryAdmin(ModelAdmin, DraggableMPTTAdmin):
    paginator = InfinitePaginator
    show_full_result_count = False
    mptt_indent_field = "name"
    
    list_display_links = (
        "indented_title",
    )
    list_display = (
        "id",
        "name",
        "parent",
        "created_at",
        "tree_actions",
        "indented_title",
    )


    search_fields = (
        "parent",
        "name",
    )

    ordering = (
        "-created_at",
    )
    list_select_related = ["parent"] 
    
    fieldsets = (
        (_(" دسته بندی اصلی"), {
            "fields": ("parent", )
        }),
        (_("محتوا"), {
            "fields": ("name",),
            "classes": ("collapse",),  
        }),
        (_("تاریخ‌ها"), {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )

@admin.register(Comments)
class CommentAdmin(ModelAdmin):
    paginator = InfinitePaginator
    show_full_result_count = False
    
    list_display = (
        "id",
        "content",
        "author",
        "post",
        "created_at",
    )
    search_fields = (
        "post",
        "author",
    )

    ordering = (
        "-created_at",
    )
    list_select_related = ["author", "post"] 
    
    # فیلدها
    fieldsets = (
        (_("نویسنده"), {
            "fields": ("author", )
        }),
        (_("محتوا"), {
            "fields": ("post", "content"),
            "classes": ("collapse",),  
        }),
        (_("تاریخ‌ها"), {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )


@admin.register(Subscription)
class SubscriptionAdmin(ModelAdmin):
    paginator = InfinitePaginator
    show_full_result_count = False
    list_display = (
        "id",
        "price",
        "name",
        "limit_days",
        "created_at",
    )
    fieldsets = (
        (_("نام"), {
            "fields": ("name",)
        }),
        (_("محتوا"), {
            "fields": ("price", "limit_days",),
            "classes": ("collapse",), 
        }),
        (_("تاریخ‌ها"), {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )


@admin.register(UserSubscription)
class UserSubscriptionAdmin(ModelAdmin):
    paginator = InfinitePaginator
    show_full_result_count = False
    list_display = (
        "id",
        "user",
        "subscription",
        "created_at",
    )
    list_select_related = ["user", "subscription"]
    fieldsets = (
        (_("محتوا"), {
            "fields": ("user", "subscription")
        }),
        (_("تاریخ‌ها"), {
            "fields": ("created_at", "start_date", "end_date"),
            "classes": ("collapse",),
        }),
    )


@admin.register(FavoritPost)
class FavoritPostAdmin(ModelAdmin):
    paginator = InfinitePaginator
    show_full_result_count = False
    list_display = (
        "id",
        "user",
        "post",
        "created_at",
    )
    search_fields = (
        "post",
        "user",
    )
    ordering = (
        "-created_at",
    )

    fieldsets = (
        (_("نام"), {
            "fields": ("user",)
        }),
        (_("محتوا"), {
            "fields": ("post", ),
            "classes": ("collapse",),  
        }),
        (_("تاریخ‌ها"), {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )