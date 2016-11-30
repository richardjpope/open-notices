from django.views.generic import TemplateView, FormView
from django.views.generic.edit import FormMixin
from django.shortcuts import render, redirect, reverse
from django.http import Http404
from rest_framework.authtoken.models import Token
from django.views.generic import FormView
from core import forms
from django.utils.http import is_safe_url
from django.contrib.auth import authenticate, login

class RegistrationView(FormView):
    template_name = "core/register.html"
    form_class = forms.RegistrationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)        
        if not self.request.GET.get('next', False):
            return redirect(reverse('index'))
        else:
            if is_safe_url(self.request.GET['next']):
                return redirect(self.request.GET['next'])
            else:
                return redirect(reverse('index'))   

class IndexView(TemplateView):
    template_name = "core/index.html"

class AboutView(TemplateView):
    template_name = "core/about.html"

class APIView(TemplateView):
    template_name = "core/api.html"

    def get_context_data(self, **kwargs):
        data = {}
        if self.request.user.is_authenticated():
            token = Token.objects.filter(user=self.request.user).first()
            data['token'] = token
        
        return data

    def post(self, request):
        if not request.user.is_authenticated():
            raise Http404
        if request.POST.get('generate', False):
            Token.objects.get_or_create(user=request.user)
        if request.POST.get('regenerate', False):
            token = Token.objects.get_or_create(user=request.user)
            if token:
                token[0].delete()
                Token.objects.create(user=request.user)
            else:
                Token.objects.get_or_create(user=request.user)

        return render(request, self.template_name, self.get_context_data())