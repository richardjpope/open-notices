from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from notices import views as notice_views

urlpatterns = [
    url(r'^$', notice_views.NoticeListView.as_view(), name='notice-list'),
    url(r'^', include('core.urls')),
    url(r'^notices/', include('notices.urls')),
    url(r'^alerts/', include('alerts.urls')),
    url(r'^signin/$', auth_views.login, name='login'),
    url(r'^signout/$', auth_views.logout,  {'next_page': '/'}, name='logout'),
    url(r'^admin/', admin.site.urls),
]