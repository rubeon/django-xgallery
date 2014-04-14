#!/usr/bin/env python
# encoding: utf-8
"""
urls.py

Created by Eric Williams on 2007-03-22.
Copyright (c) 2007 xoffender Administration & Development. All rights reserved.
"""


from django.conf.urls.defaults import *

urlpatterns = patterns(  '',
    (r'^(?P<slug>[-\w]+)/simpleviewer/$', 'xgallery.views.simpleviewer'),
    (r'^(?P<slug>[-\w]+)/photocast/$', 'xgallery.views.photocast'),
    (r'^(?P<slug>[-\w]+)/cooliris/$', 'xgallery.views.cooliris'),
    (r'^(?P<slug>[-\w]+)/$', 'xgallery.views.showalbum'),
    # (r'^item/(?P<slug>[-\w]+)/$', 'xgallery.views.showitem'),
    (r'^$', 'xgallery.views.overview')
)