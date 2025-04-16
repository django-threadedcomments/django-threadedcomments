from django.conf.urls import include
from django.urls import re_path

from blog.views import latest_post

urlpatterns = [
     re_path(r'^blog/$', latest_post),
     re_path(r'^admin/', include('django.contrib.admin.urls')),
     re_path(r'^threadedcomments/', include('threadedcomments.urls')),
]
