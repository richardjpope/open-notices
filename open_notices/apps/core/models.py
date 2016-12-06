from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from core.managers import UserManager
from django.db.models.signals import pre_save

class User(AbstractBaseUser):
    USERNAME_FIELD = 'email'

    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_superuser  = models.BooleanField(default=False)

    objects = UserManager()

def lowercase_email(sender, instance, *args, **kwargs):
    if instance.email:
        instance.email = instance.email.lower()

pre_save.connect(lowercase_email, sender=User)