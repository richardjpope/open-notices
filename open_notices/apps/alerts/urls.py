from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/?$', views.AlertList.as_view(), name='alert-list'),
    url(r'^/new/?$', views.AlertCreate.as_view(), name='alert-create'),
    url(r'^/new/account/?$', views.AlertCreateUser.as_view(), name='create-alert-user'),
    url(r'^/(?P<pk>[0-9]+)/delete/?$', views.AlertDelete.as_view(), name='alert-delete'),
]

api_urlpatterns = [
    url(r'^/?$', views.AlertListAPI.as_view(), name='alert-list-api'),
    url(r'^/new/?$', views.AlertCreateAPI.as_view(), name='alert-create-api'),
    url(r'^/(?P<pk>[0-9]+)/?$', views.AlertDetailAPI.as_view(), name='alert-detail-api'),
]

api_urlpatterns = format_suffix_patterns(api_urlpatterns, allowed=['json', 'geojson', 'csv'])

urlpatterns += api_urlpatterns