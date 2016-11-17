from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin
from django.shortcuts import render
from django.http import Http404
from rest_framework.authtoken.models import Token

class IndexView(TemplateView):
    template_name = "core/index.html"

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