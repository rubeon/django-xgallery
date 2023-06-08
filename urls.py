#!/usr/bin/env python
# encoding: utf-8
"""
urls.py

Created by Eric Williams on 2007-03-22.
Copyright (c) 2007 xoffender Administration & Development. All rights reserved.
"""


# from django.conf.urls.defaults import *
from django.urls import re_path
from . import views

app_name = 'xgallery'

urlpatterns = [
    re_path(r'(?P<slug>[-\w]+)/simpleviewer/$', views.default.simpleviewer),
    re_path(r'(?P<slug>[-\w]+)/photocast/$', views.default.photocast),
    re_path(r'(?P<slug>[-\w]+)/cooliris/$', views.default.cooliris),
    re_path(r'(?P<slug>[-\w]+)/$', views.default.showalbum),
    # re_path(r'^item/re_path(?P<slug>[-\w]+)/$', 'xgallery.views.default.showitem'),
    re_path(r'^$', views.default.overview),
]