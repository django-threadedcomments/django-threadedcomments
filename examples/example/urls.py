from django.conf.urls import include
from django.urls import re_path
from django.contrib import admin

# Enable the admin
admin.autodiscover()

urlpatterns = [
    re_path(r'^admin/', include(admin.site.urls)),
    re_path(r'^comments/', include('django.contrib.comments.urls')),
    re_path(r'^$', 'core.views.home', name='homepage'),
    re_path(r'^message/(?P<id>.+)$', 'core.views.message', name='message_detail'),
]
