#!/usr/bin/env python
# encoding: utf-8
"""
sitemap.py

Created by Eric Williams on 2007-04-03.
Copyright (c) 2007 xoffender Administration & Development. All rights reserved.
"""

from django.contrib.sitemaps import Sitemap
from common.xgallery.models import Album

class GallerySitemap(Sitemap):
    """
    this creates the googleable part of the
    site-wide sitemap file...
    """
    changefreq = 'weekly'
    def items(self):
        return Album.objects.all()
    
    def lastmod(self, obj):
        return obj.pub_date
        
    def location(self, obj):
        return obj.get_site_url()
