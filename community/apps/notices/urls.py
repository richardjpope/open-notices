from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^/?$', views.NoticeList.as_view(), name='notice-list'),
    url(r'^/new$', views.NoticeCreate.as_view(), name='notice-create'),
    url(r'^/(?P<pk>[0-9]+)/?$', views.NoticeDetail.as_view(), name='notice-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html', 'api', 'geojson', 'csv'])