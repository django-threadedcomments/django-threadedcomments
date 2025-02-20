from django.urls import re_path
from threadedcomments.models import FreeThreadedComment
from threadedcomments import views

free = {'model': FreeThreadedComment}

urlpatterns = [
    ### Comments ###
    re_path(r'^comment/(?P<content_type>\d+)/(?P<object_id>\d+)/$', views.comment, name="tc_comment"),
    re_path(r'^comment/(?P<content_type>\d+)/(?P<object_id>\d+)/(?P<parent_id>\d+)/$', views.comment, name="tc_comment_parent"),
    re_path(r'^comment/(?P<object_id>\d+)/delete/$', views.comment_delete, name="tc_comment_delete"),
    re_path(r'^comment/(?P<edit_id>\d+)/edit/$', views.comment, name="tc_comment_edit"),

    ### Comments (AJAX) ###
    re_path(r'^comment/(?P<content_type>\d+)/(?P<object_id>\d+)/(?P<ajax>json|xml)/$', views.comment, name="tc_comment_ajax"),
    re_path(r'^comment/(?P<content_type>\d+)/(?P<object_id>\d+)/(?P<parent_id>\d+)/(?P<ajax>json|xml)/$', views.comment, name="tc_comment_parent_ajax"),
    re_path(r'^comment/(?P<edit_id>\d+)/edit/(?P<ajax>json|xml)/$', views.comment, name="tc_comment_edit_ajax"),

    ### Free Comments ###
    re_path(r'^freecomment/(?P<content_type>\d+)/(?P<object_id>\d+)/$', views.free_comment, name="tc_free_comment"),
    re_path(r'^freecomment/(?P<content_type>\d+)/(?P<object_id>\d+)/(?P<parent_id>\d+)/$', views.free_comment, name="tc_free_comment_parent"),
    re_path(r'^freecomment/(?P<object_id>\d+)/delete/$', views.comment_delete, free, name="tc_free_comment_delete"),
    re_path(r'^freecomment/(?P<edit_id>\d+)/edit/$', views.free_comment, name="tc_free_comment_edit"),

    ### Free Comments (AJAX) ###
    re_path(r'^freecomment/(?P<content_type>\d+)/(?P<object_id>\d+)/(?P<ajax>json|xml)/$', views.free_comment, name="tc_free_comment_ajax"),
    re_path(r'^freecomment/(?P<content_type>\d+)/(?P<object_id>\d+)/(?P<parent_id>\d+)/(?P<ajax>json|xml)/$', views.free_comment, name="tc_free_comment_parent_ajax"),
    re_path(r'^freecomment/(?P<edit_id>\d+)/edit/(?P<ajax>json|xml)/$', views.free_comment, name="tc_free_comment_edit_ajax"),
]
