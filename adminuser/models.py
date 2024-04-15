from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import AdminUserManager


class AdminUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    hiredate = models.DateField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["firstname", "lastname", "dob", "gender", "hiredate"]

    objects = AdminUserManager()

    def __str__(self):
        return self.email
