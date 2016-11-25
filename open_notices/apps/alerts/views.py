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
from alerts import models, forms

success_message = 'Your alert has been created'

@method_decorator(login_required, name='dispatch')
class AlertListView(ListView):
    model = models.Alert

    def get_queryset(self):
        return models.Alert.objects.filter(user=self.request.user)

@method_decorator(login_required, name='dispatch')
class AlertDeleteView(DeleteView):
    model = models.Alert
    success_url = reverse_lazy('alert-list')

    def get_object(self, queryset=None):
        #users can only delete their own alerts
        alert = super(AlertDeleteView, self).get_object()
        if not alert.user == self.request.user:
            raise Http404
        return alert

    def post(self, request, *args, **kwargs):
        if not 'yes' in request.POST:
            return redirect(self.success_url)
        else:
            return super(AlertDeleteView, self).post(request, *args, **kwargs)

class AlertCreateView(FormView):
    template_name = 'alerts/alert_create.html'
    form_class = forms.CreateAlert

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('new-alert', False):
            self.request.session.pop('new-alert')
        return super(AlertCreateView, self).dispatch(self.request, *args, **kwargs)

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

class AlertCreateUserView(FormView):
    template_name = 'alerts/create_user.html'
    form_class = forms.CreateUser

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('new-alert', False):
            return redirect(reverse('alert-create'))
        else:
            return super(AlertCreateUserView, self).dispatch(request, *args, **kwargs)

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
        messages.add_message(self.request, messages.SUCCESS, 'success_message')

        return redirect(reverse('alert-list'))


