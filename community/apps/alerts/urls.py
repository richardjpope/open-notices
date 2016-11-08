from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.AlertListView.as_view(), name='alert-list'),
    url(r'^new$', views.AlertCreateView.as_view(), name='alert-create'),
    url(r'^new/account$', views.AlertCreateUserView.as_view(), name='create-alert-user'),
    url(r'^(?P<pk>[0-9]+)/delete$', views.AlertDeleteView.as_view(), name='alert-delete'),
]