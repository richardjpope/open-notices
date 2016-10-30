from django.contrib.gis.db import models
from django.conf import settings

class Alert(models.Model):

    location = models.PolygonField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)