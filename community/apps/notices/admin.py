from django.contrib import admin
from notices import models

class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(models.Notice, NoticeAdmin)