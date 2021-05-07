"""pro_test01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^student/',views.index_views),
    url(r'^project_test01/',include('project_test01.urls')),
    url(r'^pro_student/',include('project_test01.urls')),
    url(r'^url/',include('project_test01.urls')),
    url(r'^pro1/',include('project_test01.urls',namespace='pro',app_name='pro_test01')),
    url(r'^http/',include('project_test01.urls')),
    url(r'^file/',include('project_test01.urls')),
    url(r'^error_page/',include('project_test01.urls')),
    url(r'^redirect/',include('project_test01.urls')),
    url(r'^cookie_session/',include('project_test01.urls')),
    url(r'^avoid_login/',include('project_test01.urls')),
    url(r'^view/',include('project_test01.urls')),
    url(r'^filter/',include('project_test01.urls')),
    url(r'^context/',include('project_test01.urls')),
    url(r'^inherit_template/',include('project_test01.urls')),
    url(r'^forms/',include('project_test01.urls')),
    url(r'^AJAX/',include('project_test01.urls')),


    url(r'^blog/',include('blog.urls', namespace='blog', app_name='blog')),
    url(r'^search/$', include('haystack.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

from django.views.static import  serve
from .settings import DEBUG, MEDIA_ROOT
if DEBUG:
    urlpatterns+=url(r'^media/(?P<path>.*)/$',serve, {"document_root": MEDIA_ROOT}),

