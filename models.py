from django.db import models
from django.contrib.auth.models import User
import datetime
from django.conf import settings
import os
from xgallery.thumbnail.field import ImageWithThumbnailField

# Create your models here.

class Gallery(models.Model):
    """(Gallery description)"""
    title = models.CharField(blank=True, max_length=255)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=False, null=False)

    class Admin:
        #list_display = ('',)
        #search_fields = ('',)
        pass 
        
    def __str__(self):
        return "Gallery %s" % self.title

class Album(models.Model):
    """ Gallery Albums """
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    title = models.CharField(blank=True, max_length=255)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=False, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(blank=True, default=datetime.datetime.now)
    update_date = models.DateTimeField(blank=True, default=datetime.datetime.now)
    
    def get_random_thumbnail(self):
        # not really random, is it?
        if self.galleryitem_set.all()[0]:
          return [self.galleryitem_set.all()[0]]
        else:
          return []
    
    def get_absolute_url(self):
        return "%s%s/%s" % (settings.SITE_URL,'gallery',self.slug)


    class Admin:
        #list_display = ('',)
        #search_fields = ('',)
        pass

    def __str__(self):
        return "Album % s" % self.title

class GalleryItem(models.Model):
    """ Pictures and Movies..."""
    album        = models.ForeignKey(Album, on_delete=models.CASCADE)
    # image        = ImageWithThumbnailField(upload_to="gallery_uploads", auto_rename=False, height_field='image_height', width_field='image_width')
    image = models.ImageField(upload_to="gallery_uploads", height_field='image_height', width_field='image_width')
    image_height = models.IntegerField(blank=True, null=True)
    image_width  = models.IntegerField(blank=True, null=True)
    title        = models.CharField(blank=True, max_length=255)
    slug         = models.SlugField(blank=False, null=False)
    mimetype     = models.CharField(blank=True, max_length=255)

    class Admin:
        #list_display = ('',)
        #search_fields = ('',)
        pass

    def get_file_name(self):
        # returns the path to my file name
        src = self.get_image_url()
        return os.path.split(src)[-1]
        
    def __str__(self):
        return "GalleryItem %s" % self.title
