from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import random

class UserManager(BaseUserManager):
    def create_user(self, email, **extra_fields):
        if not email:
            raise ValueError("Email kiritilishi kerak")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_unusable_password()
        user.save()
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='users/', blank=True, null=True)
    phone = models.CharField(max_length=20, unique=True)  # yangi qo‘shildi
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class VerificationCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=5, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(random.randint(10000, 99999))
        super().save(*args, **kwargs)