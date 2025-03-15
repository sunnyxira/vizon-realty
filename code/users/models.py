from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import random

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("The Phone number is required")
        extra_fields.setdefault("is_active", True)
        user = self.model(phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('agent', 'Agent'),
        ('admin', 'Admin'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    pin = models.CharField(max_length=6, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)

    username = None  # Remove username

    USERNAME_FIELD = 'phone'  # Use phone for authentication
    REQUIRED_FIELDS = []  # No extra required fields

    objects = UserManager()  # Use the custom manager

    def generate_temp_pin(self):
        """Generate and store a temporary 6-digit PIN."""
        self.pin = str(random.randint(100000, 999999))
        self.save()
        return self.pin
