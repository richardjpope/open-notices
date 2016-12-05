import pytz
from django.utils import timezone
from django.contrib.gis import forms
from django.contrib.postgres.forms import HStoreField
from notices.widgets import DataWidget, NoticeAreaWidget
from notices import models
from django.conf import settings

def localize_timezone(value, timezone_string):
    value = value.replace(tzinfo=None)
    return pytz.timezone(timezone_string).localize(value)

def get_timezones():
    result = []
    for timezone in pytz.common_timezones:
        result.append((timezone, timezone))
    return result

class CreateNotice(forms.ModelForm):

    class Meta:
        model = models.Notice
        fields = ['title', 'description', 'tags']        
        widgets = {
            'description': forms.Textarea,
            'tags': DataWidget,
        }

class CreateNoticeLocation(forms.ModelForm):

    class Meta:
        model = models.Notice
        fields = ['location']
        widgets = {
            'location': NoticeAreaWidget,
        }

class CreateNoticeDatetime(forms.ModelForm):

    class Meta:
        model = models.Notice
        fields = ['starts_at', 'ends_at', 'timezone']        
        widgets = {
            'starts_at': forms.TextInput(attrs={'type': 'datetime'}),
            'ends_at': forms.TextInput(attrs={'type': 'datetime'}),
        }

    def clean(self):
        cleaned_data = super(CreateNoticeDatetime, self).clean()
        notice_timezone = cleaned_data.get('timezone', False)
        if notice_timezone:
            if cleaned_data.get('starts_at', False):
                cleaned_data['starts_at'] = localize_timezone(cleaned_data['starts_at'], notice_timezone)

            if cleaned_data.get('ends_at', False):
                cleaned_data['ends_at'] = localize_timezone(cleaned_data['ends_at'], notice_timezone)
        return cleaned_data