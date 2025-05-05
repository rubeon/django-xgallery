# meh
from django.urls import include, re_path, path

from django.contrib import admin
import xgallery.urls
from django_xmlrpc_dx.views import handle_xmlrpc


urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'gallery/', include(xgallery.urls, namespace='xgallery')),
    path(r'xmlrpc/', handle_xmlrpc, name='xmlrpc'),
]