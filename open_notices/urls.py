from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    url(r'^', include('core.urls')),
    url(r'^', include('notices.urls')),
    url(r'^alerts', include('alerts.urls')),
    url(r'^signin/$', auth_views.login, name='login'),
    url(r'^signout/$', auth_views.logout,  {'next_page': '/'}, name='logout'),
    url(r'^api/documentation', include('rest_framework_docs.urls')),
]
