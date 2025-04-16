from django.conf import settings
from django.conf.urls import include
from django.urls import re_path

from threadedcomments.models import ThreadedComment
from voting.views import xmlhttprequest_vote_on_object

from exampleblog.views import (
    auth_login,
    check_exists,
    comment_partial,
    latest_post,
    register,
)

urlpatterns = [
    re_path(r'^register/$', register, name="exampleblog_register"),
    re_path(r'^login/$', auth_login, name="exampleblog_login"),
    re_path(r'^check_exists/$', check_exists, name="exampleblog_checkexists"),
    re_path(r'^blog/$', latest_post, name="exampleblog_latest"),
    re_path(r'^vote/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/$', xmlhttprequest_vote_on_object, { 'model' : ThreadedComment }, name="vote_on_object"),
    re_path(r'^partial/(?P<comment_id>\d+)/$', comment_partial, name="comment_partial"),
    re_path(r'^threadedcomments/', include('threadedcomments.urls')),
    re_path(r'^admin/', include('django.contrib.admin.urls')),
    re_path(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
]
