from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from notices import models, forms

class NoticeListView(ListView):
    model = models.Notice

class NoticeDetailView(DetailView):
    model = models.Notice

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