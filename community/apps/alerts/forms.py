from django.contrib.gis import forms
from alerts.widgets import AlertAreaWidget

class CreateAlert(forms.Form):
    location = forms.GeometryField(widget=
        AlertAreaWidget(attrs={'map_width': 800, 'map_height': 500}))