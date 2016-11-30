from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.IndexView.as_view(), name='index'),
  url(r'^about/?$', views.AboutView.as_view(), name='about'),
  url(r'^api/?$', views.APIView.as_view(), name='api'),
  url(r'^create-account/?$', views.RegistrationView.as_view(), name='register'),
]