import pytz
from django.contrib.gis.db import models
from django.core.urlresolvers import reverse
from django.contrib.postgres.fields import HStoreField
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.contrib.sessions.models import Session
from django.conf import settings

def _get_timezones_as_tuple():
    result = []
    for timezone in pytz.common_timezones:
        result.append((timezone, timezone))
    return result

class Notice(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    details = models.TextField(blank=True, null=True)
    location = models.GeometryField()
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data = HStoreField(blank=True, null=True)
    timezone = models.CharField(max_length=40, choices=_get_timezones_as_tuple(), blank=False)

    objects = models.GeoManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('notice-detail', args=[str(self.id)])

    def clean(self):
        if self.starts_at and self.ends_at:
            if self.starts_at > self.ends_at:
                raise ValidationError("Start date/time must be before the end date/time")

@receiver(pre_save)
def pre_save_handler(sender, instance, *args, **kwargs):
    if sender != Session:
        instance.full_clean()