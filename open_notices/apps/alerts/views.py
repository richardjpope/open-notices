import json
from django.http import Http404
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.serializers import serialize
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, DeleteView
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import MethodNotAllowed
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import permissions
from alerts import models, forms

success_message = 'Your alert has been created'

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class AlertSerializer(ModelSerializer):

    class Meta:
        model = models.Alert
        fields = ('id', 'location', 'last_checked_at')

    def validate(self, attrs):
        #use the model's validation
        alert = models.Alert(**attrs)
        alert.clean()
        return attrs

class AlertGeojsonSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = models.Alert
        geo_field = "location"
        fields = ('id', 'location', 'last_checked_at')

    def validate(self, attrs):
        #use the model's validation
        alert = models.Alert(**attrs)
        alert.clean()
        return attrs

@method_decorator(login_required, name='dispatch')
class AlertList(ListView):
    model = models.Alert

    def get_queryset(self):
        return models.Alert.objects.filter(user=self.request.user)

class AlertListAPI(generics.ListAPIView):
    serializer_class = AlertSerializer
    pagination_class = None
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return models.Alert.objects.filter(user=self.request.user)

    def get(self, request, format='json', *args, **kwargs):
        if format == 'geojson':
            serializer = AlertGeojsonSerializer(self.get_queryset(), many=True)
            return Response(serializer.data)
        else:
            return super(AlertListAPI, self).get(request, format, *args, **kwargs)

class AlertDetailAPI(generics.RetrieveAPIView):
    queryset = models.Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get(self, request, format='json', *args, **kwargs):
        if format == 'geojson':
            serializer = AlertGeojsonSerializer(self.get_object())
            return Response(serializer.data)
        else:
          return super(AlertDetailAPI, self).get(request, format, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class AlertDelete(DeleteView):
    model = models.Alert
    success_url = reverse_lazy('alert-list')

    def get_object(self, queryset=None):
        #users can only delete their own alerts
        alert = super(AlertDelete, self).get_object()
        if not alert.user == self.request.user:
            raise Http404
        return alert

    def post(self, request, *args, **kwargs):
        if request.POST.get('delete', None) == 'yes':
            return super(AlertDelete, self).post(request, *args, **kwargs)
        else:
            return redirect(self.success_url)

class AlertCreate(FormView):
    template_name = 'alerts/alert_create.html'
    form_class = forms.CreateAlert

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('new-alert', False):
            self.request.session.pop('new-alert')
        return super(AlertCreate, self).dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
      alert = models.Alert()
      alert.location = form.cleaned_data['location']
      if self.request.user.is_authenticated:
          
          #save alert
          alert.user = self.request.user
          alert.save()

          #create a success message
          messages.add_message(self.request, messages.SUCCESS, success_message)

          return redirect(reverse('alert-list'))
      else:
        self.request.session['new-alert'] = serialize('geojson', [alert],
          fields=('location',))

        return redirect(reverse('create-alert-user'))

class AlertCreateAPI(generics.CreateAPIView):

    serializer_class = AlertSerializer

    def perform_create(self, serializer):
        alert = serializer.save(user=self.request.user)

    def post(self, request, format='json', *args, **kwargs):
        #Only JSON accepted for edit/create/delete
        if not format == 'json':
            raise MethodNotAllowed('')
        else:
            return super(AlertCreateAPI, self).post(request, format, *args, **kwargs)

class AlertCreateUser(FormView):
    template_name = 'alerts/create_user.html'
    form_class = forms.CreateUser

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('new-alert', False):
            return redirect(reverse('alert-create'))
        else:
            return super(AlertCreateUser, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        #create user
        UserModel = get_user_model()
        user = UserModel(email=form.cleaned_data['email'])
        user.set_password(form.cleaned_data['password'])
        user.save()

        #sign new user in
        login(self.request, user)

        #get the location out of the session
        location = json.loads(self.request.session['new-alert'])

        #save alert
        alert = models.Alert()
        alert.location = json.dumps(location['features'][0]['geometry'])
        alert.user = user
        alert.save()

        #create a success message
        messages.add_message(self.request, messages.SUCCESS, success_message)

        return redirect(reverse('alert-list'))

