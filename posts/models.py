# Django Built-in modules
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Third Party Packages
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField

# Local Apps
from utils.models import BaseModel



class Subscription(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("کاربر"))
    price = models.PositiveIntegerField(verbose_name=_("قیمت"))
    limit_days = models.PositiveIntegerField(verbose_name=_("تعداد روز ها"))

    class Meta:
        ordering = ('-created_at',)
        verbose_name=_("اشتراک")
        verbose_name_plural = _("اشتراک")


    def __str__(self):
        return self.name


class UserSubscription(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name=_("کاربر",)
    )

    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name="users",
        verbose_name=_("اشتراک")
    )

    start_date = models.DateTimeField(auto_now_add=True, verbose_name=_("روز شروع"))

    end_date = models.DateTimeField(verbose_name=_("روز پایان"))

    is_active = models.BooleanField(default=True, verbose_name=_("فعال است"))

    class Meta:
        ordering = ('-created_at',)
        verbose_name=_("اشتراک کاربر")
        verbose_name_plural = _("اشتراک کاربر")

    def __str__(self):
        return self.subscription + " for " + self.user.name


    @property
    def remaining_days(self):
        remaining = (self.end_date - timezone.now()).days
        return max(remaining, 0)


class Category(MPTTModel, BaseModel):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("نام دسته بندی"))
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_("دسته بندی اصلی")
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _( 'دسته بندی')
        verbose_name_plural = _('دسته بندی')

    def __str__(self):
        return self.name
    

class Post(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts", verbose_name=_("دسته بندی"))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="author", verbose_name=_("نویسنده"))
    title = models.CharField(max_length=50, verbose_name=_("تیتر پست"))
    content = RichTextUploadingField(verbose_name=_("محتوا"))
    image = models.ImageField(upload_to="posts/images/",
        blank=True,
        null=True, verbose_name=_("عکس"))
    
    video = models.FileField( upload_to="posts/videos/",
        blank=True,
        null=True, verbose_name=_("ویدئو"))
    
    is_premium = models.BooleanField(default=False, verbose_name=_("ویژه است"))

    class Meta:
        ordering = ('-created_at',)
        verbose_name=_("پست ")
        verbose_name_plural = _("پست ")
    
    def __str__(self):
        return self.title


class Comments(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_comment", verbose_name=_("نویسنده"))
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment", verbose_name=_("پست"))
    content = models.CharField(verbose_name=_("محتوا"))

    class Meta:
        ordering = ('-created_at',)
        verbose_name=_("کامنت ها")
        verbose_name_plural = _("کامنت ها")

    def __str__(self):
        return self.author.username + "  added a comment for " + self.post.title 



class FavoritPost(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_favorits", verbose_name=_("کاربر"))
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="favorits", verbose_name=_("پست"))

    class Meta:
        ordering = ('-created_at',)
        unique_together = ("user", "post")
        verbose_name=_(" لایک ها")
        verbose_name_plural =_(" لایک ها")

    def __str__(self):
        return self.user.username + "  added a like for " + self.post.title


