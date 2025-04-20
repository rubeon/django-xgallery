from django.contrib import admin
from .models import Gallery, GalleryItem, Album

class GalleryAdmin(admin.ModelAdmin):
     prepopulated_fields = {"slug": ("title",)}
admin.site.register(Gallery, GalleryAdmin)

class GalleryItemAdmin(admin.ModelAdmin):
     prepopulated_fields = {"slug": ("title",)}
     list_display = ('title', 'image', 'pub_date',)
admin.site.register(GalleryItem, GalleryItemAdmin)

class AlbumAdmin(admin.ModelAdmin):
     prepopulated_fields = {"slug": ("title",)}
admin.site.register(Album, AlbumAdmin)
