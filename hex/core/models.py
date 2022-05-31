"""
Database models.
"""
from django.db import models
import os
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
# from django.contrib.auth.models import User


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    BASIC = 'bp'
    PREMIUM = 'pp'
    ENTERPRISE = 'ep'
    ADMIN = 'aa'
    PLAN_CHOICE = [
        (BASIC, 'BASIC PLAN'),
        (PREMIUM, 'PREMIUM PLAN'),
        (ENTERPRISE, 'ENTERPRISE PLAN'),
        (ADMIN, 'ADMIN PLAN'),
    ]
    account_plan = models.CharField(max_length=2, choices=PLAN_CHOICE, default=BASIC)

    objects = UserManager()

    USERNAME_FIELD = 'email'



