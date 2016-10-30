from django.contrib.gis import forms

class CreateNotice(forms.Form):
    title = forms.CharField(max_length=50)
    details = forms.CharField(widget=forms.Textarea)
    location = forms.GeometryField(widget=
        forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500}))