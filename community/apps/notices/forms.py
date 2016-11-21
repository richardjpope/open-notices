from django.contrib.gis import forms
from django.contrib.postgres.forms import HStoreField
from notices.widgets import DataWidget
from notices import models

class CreateNotice(forms.ModelForm):
    class Meta:
        model = models.Notice
        fields = ['location', 'title', 'details', 'data']
        widgets = {
            'location': forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500}),
            'details': forms.Textarea,
            'data': DataWidget
        }
