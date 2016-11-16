from django.core.serializers import serialize
from rest_framework import renderers

class GEOJSONRenderer(renderers.JSONRenderer):
    format = 'geojson'