from django.urls import path
from . import views

urlpatterns=[
    path(r'', views.post_list_view, name='post_list_view'),
    path(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$', views.post_detail_view, name='post_detail_view'),
]