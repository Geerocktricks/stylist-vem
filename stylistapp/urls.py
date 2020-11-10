from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .models import *

def add_post_ids_to_kategories():
    for post in Post.objects.all():
        post.save()
add_post_ids_to_kategories()

urlpatterns=[
    path(r'', views.post_list_view, name='post_list_view'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$', views.post_detail_view, name='post_detail_view'),
    path(r'shop/', views.product_list, name='product_list'),
    path(r'^(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
    path(r'^kategory/(?P<kategory_slug>[-\w]+)/$', views.post_list_by_kategory, name='post_list_by_kategory'),
    path(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
    path(r'streetdripwithstylistvem/', views.insta_recap, name = 'insta_recap'),
    
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)