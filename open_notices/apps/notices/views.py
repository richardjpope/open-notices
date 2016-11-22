from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from rest_framework import generics 
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_hstore.fields import HStoreField
from rest_framework.exceptions import MethodNotAllowed
from notices import models, forms
from django.conf import settings

class NoticeGeojsonSerializer(GeoFeatureModelSerializer):
    data = HStoreField()

    class Meta:
        model = models.Notice
        geo_field = "location"
        fields = ('id', 'location', 'title', 'details', 'data''starts_at', 'ends_at', 'timezone')

    def validate(self, attrs):
        #use the model's validation
        notice = models.Notice(**attrs)
        notice.clean()
        return attrs
        
    def get_properties(self, instance, fields):

        #get the default serialisation
        properties = super(NoticeGeojsonSerializer, self).get_properties(instance, fields)

        #extract the hstore field
        hstore_field_name = 'data'
        hstore_data = None
        for key, value  in properties.items():
            if key == hstore_field_name:
                hstore_data = value
                del properties[key]

        #add the items from the hstore field at the 'properties' level
        if hstore_data:
            for key, value in hstore_data.items():
                properties[key] = value

        return properties

class NoticeSerializer(ModelSerializer):
    data = HStoreField()

    class Meta:
        model = models.Notice
        fields = ('id', 'location', 'title', 'details', 'data', 'starts_at', 'ends_at', 'timezone')

    def validate(self, attrs):
        #use the model's validation
        notice = models.Notice(**attrs)
        notice.clean()
        return attrs

class NoticeList(ListView):
    model = models.Notice

class NoticeListAPI(generics.ListAPIView):
    queryset = models.Notice.objects.all()
    serializer_class = NoticeSerializer

    def get(self, request, format='json', *args, **kwargs):
        if format == 'geojson':
            serializer = NoticeGeojsonSerializer(self.get_queryset(), many=True)
            return Response(serializer.data)
        else:
            return super(NoticeListAPI, self).get(request, format, *args, **kwargs)

class NoticeDetail(DetailView):
    model = models.Notice

class NoticeDetailAPI(generics.RetrieveAPIView):
    queryset = models.Notice.objects.all()
    serializer_class = NoticeSerializer

    def get(self, request, format='json', *args, **kwargs):
        if format == 'geojson':
            serializer = NoticeGeojsonSerializer(self.get_object())
            return Response(serializer.data)
        else:
          return super(NoticeDetailAPI, self).get(request, format, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class NoticeCreate(FormView):
    template_name = 'notices/notice_create.html'
    form_class = forms.CreateNotice

    def get_initial(self):
        initial = super(NoticeCreate, self).get_initial()
        initial['timezone'] = default=settings.TIME_ZONE
        return initial

    def form_valid(self, form):
        notice = form.save()
        return redirect(notice)


class NoticeCreateAPI(generics.CreateAPIView):

    serializer_class = NoticeSerializer

    def post(self, request, format='json', *args, **kwargs):
        #Only JSON accepted for edit/create/delete
        if not format == 'json':
            raise MethodNotAllowed('')
        else:
            return super(NoticeCreateAPI, self).post(request, format, *args, **kwargs)

