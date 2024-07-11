from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError
from uuid6 import uuid7
from core.models import UUIDBaseModel


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, full_name, password, **extra_fields):
        if not all([email, full_name, password]):
            raise ValueError("Email, full name, and password must be provided.")
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            full_name=full_name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, full_name, password, **extra_fields)
    
    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self._create_user(email, full_name, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, default=uuid7)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=200)
    is_staff = models.BooleanField(default=False)

    ROLE_CHOICES = (
        ('regular_user', 'Regular User'),
        ('law_expert', 'Law Expert'),
    )

    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='regular_user')
    law_certificate = models.URLField(max_length=100, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']


