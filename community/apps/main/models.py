from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    alerts_checked_at = models.DateTimeField(auto_now_add=True)
