from django.conf.urls import url
from django.urls import include

from blog import views

urlpatterns = [
    url(r'^home-page/$', views.home_page),
    url(r'^home-page/(\d+)$', views.home_page),
    url(r'^content-detail/(\d+)$', views.content_detail),
    url(r'^category/(\d+)/$', views.query_blog_by_categroyid),
    url(r'^archive/(\d+)/(\d+)/(\d+)/$', views.query_blog_by_archive_time),
    url(r'^cache/$', views.test_cache),



]