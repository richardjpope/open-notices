from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from core.managers import UserManager

class User(AbstractBaseUser):
    USERNAME_FIELD = 'email'

    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_superuser  = models.BooleanField(default=False)

    objects = UserManager()