from django.db import models

class Notice(models.Model):
    title = models.CharField(max_length=50)
    details = models.TextField(blank=True)

    def __str__(self):
        return self.title