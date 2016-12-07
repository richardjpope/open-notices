from django.contrib.gis.db import models
from django.conf import settings

class Alert(models.Model):

    location = models.PolygonField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_checked_at = models.DateTimeField(auto_now_add=True)