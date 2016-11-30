import json
from django.shortcuts import redirect, reverse
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.core.serializers import serialize
from rest_framework import generics 
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_hstore.fields import HStoreField
from rest_framework.exceptions import MethodNotAllowed
from notices import models, forms
from django.conf import settings

class NoticeGeojsonSerializer(GeoFeatureModelSerializer):
    tags = HStoreField()

    class Meta:
        model = models.Notice
        geo_field = "location"
        fields = ('id', 'location', 'title', 'details', 'tags', 'starts_at', 'ends_at', 'timezone')

    def validate(self, attrs):
        #use the model's validation
        notice = models.Notice(**attrs)
        notice.clean()
        return attrs
        
    def get_properties(self, instance, fields):
        import collections
        #get the default serialisation
        properties = super(NoticeGeojsonSerializer, self).get_properties(instance, fields)
        # properties = dict(properties)

        #extract the hstore field
        hstore_field_name = 'tags'
        hstore_data = None
        for key, value  in properties.copy().items():
            if key == hstore_field_name:
                hstore_data = value
                del properties[key]

        #add the items from the hstore field at the 'properties' level
        if hstore_data:
            for key, value in hstore_data.items():
                properties[key] = value

        return properties

class NoticeSerializer(ModelSerializer):
    tags = HStoreField()

    class Meta:
        model = models.Notice
        fields = ('id', 'location', 'title', 'details', 'tags', 'starts_at', 'ends_at', 'timezone')

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

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('new-notice', False):
            self.request.session.pop('new-notice')
        return super(NoticeCreate, self).dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):

        notice = form.save(commit=False)

        serializer = NoticeSerializer(notice)
        self.request.session['new-notice'] = serializer.data

        return redirect(reverse('notice-create-location'))

@method_decorator(login_required, name='dispatch')
class NoticeCreateLocation(FormView):
    template_name = 'notices/notice_create_location.html'
    form_class = forms.CreateNoticeLocation

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('new-notice', False):
            return redirect(reverse('notice-create'))
        return super(NoticeCreateLocation, self).dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):

        notice = form.save(commit=False)
        serializer = NoticeSerializer(notice)
        session_data = self.request.session['new-notice']
        session_data['location'] = serializer.data['location']
        self.request.session['new-notice'] = session_data

        return redirect(reverse('notice-create-datetime'))

@method_decorator(login_required, name='dispatch')
class NoticeCreateDatetime(FormView):
    template_name = 'notices/notice_create_datetime.html'
    form_class = forms.CreateNoticeDatetime

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('new-notice', False):
            return redirect(reverse('notice-create'))
        return super(NoticeCreateDatetime, self).dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        #add the dates to the existing data in the sessions
        notice = form.save(commit=False)
        serializer = NoticeSerializer(notice)
        session_data = self.request.session['new-notice']
        session_data['starts_at'] = serializer.data['starts_at']
        session_data['ends_at'] = serializer.data['ends_at']
        session_data['timezone'] = serializer.data['timezone']

        #save
        serializer = NoticeSerializer(data=session_data)
        if serializer.is_valid():
            notice = serializer.save(user=self.request.user)
            messages.add_message(self.request, messages.SUCCESS, 'Your notice has been posted')
            return redirect(notice)
        else:
            messages.add_message(self.request, messages.ERROR, 'Sorry, something went wrong')

class NoticeCreateAPI(generics.CreateAPIView):

    serializer_class = NoticeSerializer

    def perform_create(self, serializer):
        notice = serializer.save(user=self.request.user)

    def post(self, request, format='json', *args, **kwargs):
        #Only JSON accepted for edit/create/delete
        if not format == 'json':
            raise MethodNotAllowed('')
        else:
            return super(NoticeCreateAPI, self).post(request, format, *args, **kwargs)

