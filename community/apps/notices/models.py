from django.contrib.gis.db import models
from django.core.urlresolvers import reverse
from django.contrib.postgres.fields import HStoreField

class Notice(models.Model):
    title = models.CharField(max_length=50)
    details = models.TextField(blank=True)
    location = models.GeometryField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data = HStoreField(null=True)

    objects = models.GeoManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('notice-detail', args=[str(self.id)])