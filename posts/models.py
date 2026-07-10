from django.db import models
from django.conf import settings
from django.utils import timezone

from mptt.models import MPTTModel, TreeForeignKey

from utils.models import BaseModel
from ckeditor_uploader.fields import RichTextUploadingField



class Subscription(BaseModel):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    limit_days = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class UserSubscription(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )

    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name="users",
    )

    start_date = models.DateTimeField(auto_now_add=True)

    end_date = models.DateTimeField()

    is_active = models.BooleanField(default=True)

    @property
    def remaining_days(self):
        remaining = (self.end_date - timezone.now()).days
        return max(remaining, 0)


class Category(MPTTModel, BaseModel):
    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    

class Post(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="author")
    title = models.CharField(max_length=50)
    content = RichTextUploadingField()
    image = models.ImageField(upload_to="posts/images/",
        blank=True,
        null=True)
    
    video = models.FileField( upload_to="posts/videos/",
        blank=True,
        null=True)
    
    is_premium = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title


class Comments(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_comment")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
    content = models.CharField()



class FavoritPost(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_favorits")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="favorits")

    class Meta:
        unique_together = ("user", "post")


