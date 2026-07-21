# Django Built-in modules
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager as BUM
from django.db import models
from django.conf import settings
from django.apps import apps
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import (
    acheck_password,
    check_password,
    is_password_usable,
    make_password,
)
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Third Party Packages
from phonenumber_field.modelfields import PhoneNumberField
from datetime import timedelta

# Local Apps
from posts.models import Subscription
from utils.models import BaseModel



class BaseUserManager(BUM):
    use_in_migrations = True

    def _create_user_object(self, username, password, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        return user

    def _create_user(self, username, password, **extra_fields):
        user = self._create_user_object(username, password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        
        return self._create_user(username, password, **extra_fields)

    create_user.alters_data = True
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self._create_user(username, password, **extra_fields)

    create_superuser.alters_data = True


class BaseUserModel(BaseModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, unique=True, verbose_name=_("نام کاربری "))
    
    phone = PhoneNumberField(
        unique=True,
        region="IR",
        verbose_name=_("شماره تلفن ")
    )
    password = models.CharField(max_length=128, verbose_name=_("رمز ورود"))
    last_login = models.DateTimeField(blank=True, null=True, verbose_name=_("آخرین ورود"))
    is_staff = models.BooleanField(default=False, verbose_name=_("ادمین است"))
    is_active = models.BooleanField(default=True, verbose_name=_("فعال است"))

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phone"]


    _password = None
    objects = BaseUserManager()
    class Meta:
        ordering = ('-created_at',)
        verbose_name = _("کاربر")
        verbose_name_plural = _("کاربر")


    def __str__(self):
        return self.username

    def save(self, **kwargs):
        super().save(**kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def clean(self):
        setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Set a value that will never be a valid hash
        self.password = make_password(None)


class UserProfileModel(BaseModel):

    user = models.ForeignKey(BaseUserModel, on_delete=models.CASCADE, related_name="user_profile", verbose_name=_("کاربر"))
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="subscription", null=True, blank=True, verbose_name=_("اشتراک کاربر"))

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _("پروفایل کاربر")
        verbose_name_plural = _("پروفایل کاربر")

    def __str__(self):
        return self.user.username 

class OtpCode(BaseModel):
    phone = models.CharField(max_length=11, verbose_name=_("شماره تلفن"))
    code = models.CharField(max_length=6, verbose_name=_(" کد تایید"))
    is_used = models.BooleanField(default=False, verbose_name=_("استفاده شده"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("ساخته شده در تاریخ"))

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _("کد تایید ")
        verbose_name_plural = _("کد تایید ")

    def __str__(self):
        return self.phone + ">>>>" + self.code

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=2)

    def __str__(self):
        return f"{self.user.username} - {self.code}"
    
