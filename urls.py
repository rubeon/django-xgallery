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

urlpatterns = [
    re_path(r'^re_path(?P<slug>[-\w]+)/simpleviewer/$', views.simpleviewer),
    re_path(r'^re_path(?P<slug>[-\w]+)/photocast/$', views.photocast),
    #re_path(r'^re_path(?P<slug>[-\w]+)/cooliris/$', 'xgallery.views.cooliris'),
    #re_path(r'^re_path(?P<slug>[-\w]+)/$', 'xgallery.views.showalbum'),
    # re_path(r'^item/re_path(?P<slug>[-\w]+)/$', 'xgallery.views.showitem'),
    re_path(r'^$', views.overview),
]