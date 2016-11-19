from django.contrib.gis import forms
from django.contrib.postgres.forms import HStoreField
from notices.widgets import DataWidget

class CreateNotice(forms.Form):
    location = forms.GeometryField(widget=
        forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500}))
    title = forms.CharField(max_length=50)
    details = forms.CharField(widget=forms.Textarea)
    data = HStoreField(widget=DataWidget)