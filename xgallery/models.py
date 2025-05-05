from django.db import models
from django.contrib.auth.models import User
import datetime
from django.conf import settings
import os
from xblog.models import Blog, Post
import easy_thumbnails.files
from django.utils.text import slugify

# Create your models here.

class Gallery(models.Model):
    """(Gallery description)"""
    title = models.CharField(blank=True, max_length=255)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=False, null=False)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, blank=True, null=True)
        
    def __str__(self):
        return "Gallery %s" % self.title

class Album(models.Model):
    """ Gallery Albums """
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    title = models.CharField(blank=True, max_length=255)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=False, null=False)
    pub_date = models.DateTimeField(blank=True, default=datetime.datetime.now)
    update_date = models.DateTimeField(blank=True, default=datetime.datetime.now)
    
    @property
    def owner(self):
        return self.gallery.blog.owner

    def get_random_thumbnail(self):
        # not really random, is it?
        return [self.galleryitem_set.all().first()] or []
    
    def get_absolute_url(self):
        return "%s%s/%s" % (settings.SITE_URL,'gallery',self.slug)


    class Admin:
        #list_display = ('',)
        #search_fields = ('',)
        pass

    def __str__(self):
        return "Album % s" % self.title

    __unicode__ = __str__ 

    def save(self, *args, **kwargs):
        if not self.slug:
          self.slug = slugify(str(self.title))
        self.update_date = datetime.datetime.now()
        super(Album, self).save(*args, **kwargs)

def image_upload_path(instance, filename):
    return os.path.join(
      'gallery_uploads',
      instance.album.slug,
      filename
    )

class GalleryItem(models.Model):
    """ Pictures and Movies..."""
    # TODO: put in some metadata capture when something gets uploaded...
    album        = models.ForeignKey(Album, on_delete=models.CASCADE)
    # image        = ImageWithThumbnailField(upload_to="gallery_uploads", auto_rename=False, height_field='image_height', width_field='image_width')
    # image = models.ImageField(upload_to=f"gallery_uploads/{self.album.slug}/", height_field='image_height', width_field='image_width')
    image = models.ImageField(upload_to=image_upload_path, height_field='image_height', width_field='image_width')
    image_height = models.IntegerField(blank=True, null=True)
    image_width  = models.IntegerField(blank=True, null=True)
    title        = models.CharField(blank=True, max_length=255)
    caption = models.CharField(blank=True, null=True, max_length=255)
    description = models.TextField(blank=True)
    slug         = models.SlugField(blank=False, null=False)
    mimetype     = models.CharField(blank=True, max_length=255)
    pub_date = models.DateTimeField(blank=True, default=datetime.datetime.now)
    update_date = models.DateTimeField(blank=True, default=datetime.datetime.now)
    posts = models.ManyToManyField(Post, blank=True, null=True, related_name='images')

    class Admin:
        #list_display = ('',)
        #search_fields = ('',)
        pass

    def post_id(self):
        LOGGER.debug("post_id entered")
        if self.posts:
          return self.posts.first()
        else:
          return 0

    def get_file_name(self):
        # returns the path to my file name
        return os.path.basename(self.image.name)

    def save(self, *args, **kwargs):
        self.update_date = datetime.datetime.now()
        self.slug = slugify(str(self.title))
        # easy_thumbnails.files.generate_all_aliases(self.image, False) 
        super(GalleryItem, self).save(*args, **kwargs)
        
    def __str__(self):
        return "GalleryItem %s" % self.title
    __unicode__=__str__

from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global

saved_file.connect(generate_aliases_global)