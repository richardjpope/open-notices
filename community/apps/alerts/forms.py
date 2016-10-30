from django.contrib.gis import forms
from django.core.exceptions import ValidationError
from alerts.widgets import AlertAreaWidget
import geojson

class CreateAlert(forms.Form):
    location = forms.PolygonField(widget=
        AlertAreaWidget(attrs={'map_width': 800, 'map_height': 500}))
