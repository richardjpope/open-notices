from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^/?$', views.NoticeList.as_view(), name='notice-list'),
    url(r'^/new/?$', views.NoticeCreate.as_view(), name='notice-create'),
    url(r'^/new/location/?$', views.NoticeCreateLocation.as_view(), name='notice-create-location'),
    url(r'^/new/datetime/?$', views.NoticeCreateDatetime.as_view(), name='notice-create-datetime'),    
    url(r'^/(?P<pk>[0-9]+)/?$', views.NoticeDetail.as_view(), name='notice-detail'),
]

api_urlpatterns = [
    url(r'^$', views.NoticeListAPI.as_view(), name='notice-list-api'),
    url(r'^/new$', views.NoticeCreateAPI.as_view(), name='notice-create-api'),    
    url(r'^/(?P<pk>[0-9]+)/?$', views.NoticeDetailAPI.as_view(), name='notice-detail-api'),
]

api_urlpatterns = format_suffix_patterns(api_urlpatterns, allowed=['json', 'geojson', 'csv'])

urlpatterns += api_urlpatterns