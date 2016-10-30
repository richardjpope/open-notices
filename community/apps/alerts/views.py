from django.http import Http404
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, DeleteView
from django.utils.decorators import method_decorator
from alerts import models, forms

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

@method_decorator(login_required, name='dispatch')
class AlertCreateView(FormView):
    template_name = 'alerts/alert_create.html'
    form_class = forms.CreateAlert

    def form_valid(self, form):
      
      alert = models.Alert()
      alert.location = form.cleaned_data['location']
      alert.user = self.request.user
      alert.save()

      return redirect(reverse('alert-list'))
