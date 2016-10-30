from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.NoticeListView.as_view(), name='notice-list'),
    url(r'^new$', views.NoticeCreateView.as_view(), name='notice-create'),
    url(r'^(?P<pk>[0-9]+)/$', views.NoticeDetailView.as_view(), name='notice-detail'),
]