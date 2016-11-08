from django.contrib.gis import forms
from django.core.exceptions import ValidationError
from alerts.widgets import AlertAreaWidget
import geojson
from django.contrib.auth import get_user_model

def validate_email_unique(value):
    UserModel = get_user_model()
    if UserModel.objects.filter(email=value):
        raise ValidationError("This email already exists")

class CreateAlert(forms.Form):
    location = forms.PolygonField(widget=
        AlertAreaWidget(attrs={'map_width': 800, 'map_height': 500}))

class CreateUser(forms.Form):
    email = forms.EmailField(label='Email address',validators=[validate_email_unique])
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

