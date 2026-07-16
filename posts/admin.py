# Django Built-in modules
from django.contrib import admin

# Third Party Packages
from mptt.admin import DraggableMPTTAdmin
from unfold.admin import ModelAdmin

# Local Apps
from .models import (
    Post,
    Category,
    Comments,
    Subscription,
    UserSubscription,
    FavoritPost,
)

@admin.register(Post)
class PostAdmin(ModelAdmin, admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "category",
        "is_premium",
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


@admin.register(Category)
class CategoryAdmin(ModelAdmin, DraggableMPTTAdmin):
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
        "name",
    )

    list_filter = (
        "parent",
    )

admin.site.register(Comments)
admin.site.register(Subscription)
admin.site.register(UserSubscription)
admin.site.register(FavoritPost)