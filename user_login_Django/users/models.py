# users/models.py
import uuid
import random
import string
from datetime import timedelta
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

def _random_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)

GENDER_CHOICES = (('Male','Male'),('Female','Female'),('Other','Other'))

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    nid_number = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.name or self.email

    def __str__(self):
        return self.email


class OTP(models.Model):
    """
    OTP stored with timezone-aware expiry.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='otps')
    code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    @classmethod
    def create_otp(cls, user, valid_seconds=None, length=6):
        if valid_seconds is None:
            valid_seconds = getattr(settings, "OTP_VALID_SECONDS", 60)
        code = _random_otp(length)
        now = timezone.now()
        expires = now + timedelta(seconds=valid_seconds)
        return cls.objects.create(user=user, code=code, expires_at=expires)

    def is_valid(self):
        return (not self.is_used) and (timezone.now() <= self.expires_at)

    def mark_used(self):
        self.is_used = True
        self.save(update_fields=['is_used'])

    def time_left(self):
        left = (self.expires_at - timezone.now()).total_seconds()
        return int(left) if left > 0 else 0

    def __str__(self):
        return f"{self.user.email} - {self.code}"


class AdminNotification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.created_at}: {self.message[:60]}"
