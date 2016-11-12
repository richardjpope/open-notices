import json
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from notices import models, forms

class NoticeGeojsonSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = models.Notice
        geo_field = "location"
        fields = ('id', 'location', 'title', 'details')

class NoticeSerializer(ModelSerializer):

    class Meta:
        model = models.Notice
        fields = ('id', 'location', 'title', 'details')

class NoticeListView(generics.ListCreateAPIView):
    template_name = 'notices/notice_list.html'
    queryset = models.Notice.objects.all()
    serializer_class = NoticeSerializer

    def get(self, request, format='html', *args, **kwargs):

        if format == 'html':
            return Response({'notices': self.get_queryset()})
        elif format == 'geojson':
            serializer = NoticeGeojsonSerializer(self.get_queryset(), many=True)
            return Response(serializer.data)
        else:
            return super(NoticeListView, self).get(request, format, *args, **kwargs)

class NoticeDetailView(generics.RetrieveAPIView):
    queryset = models.Notice.objects.all()
    serializer_class = NoticeSerializer
    template_name = 'notices/notice_detail.html'

    def get(self, request, format='html', *args, **kwargs):
        
        if format == 'html':
          return Response({'notice': self.get_object()}, template_name='notices/notice_detail.html')          
        elif format == 'geojson':
            serializer = NoticeGeojsonSerializer(self.get_object())
            return Response(serializer.data)
        else:
          return super(NoticeDetailView, self).get(request, format, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class NoticeCreateView(FormView):
    template_name = 'notices/notice_create.html'
    form_class = forms.CreateNotice

    def form_valid(self, form):

      notice = models.Notice()
      notice.title = form.cleaned_data['title']
      notice.details = form.cleaned_data['details']
      notice.location = form.cleaned_data['location']
      notice.save()

      return redirect(notice)