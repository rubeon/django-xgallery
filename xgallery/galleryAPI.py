#!/usr/bin/env python
# encoding: utf-8
"""
galleryAPI.py

Created by Eric Williams on 2007-03-21.
Copyright (c) 2007 xoffender Administration & Development. All rights reserved.

NOTE: this is obsolete, I don't think the gallery2 API really exists any more

https://github.com/dakanji/G2Project
"""

import sys
import os
import urllib
import hashlib
import traceback

from django.template import RequestContext, Context, loader
import django
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import authenticate, login
from xgallery.gallery_constants import grStatusCodes
from xgallery.models import Album, Gallery, GalleryItem
from xblog.external.postutils import SlugifyUniquely

def dispatcher(request):
    try:
        if request.POST:
            if request.session:
                try:
                    cmd = request.POST.get('g2_form[cmd]')
                except Exception as e:
                    res = ""
            if cmd=='login':
                username = request.POST['g2_form[uname]']
                password = request.POST['g2_form[password]']
                res = login_request(request, username, password)
                if res:

                    try:
                        request.session['auth_token'] = hashlib.md5.new(request.user.username).hexdigest()
                    except Exception as e:
                        pass

            elif cmd=='fetch-albums-prune' or cmd=='fetch-albums':
                res = fetch_albums(request)
            elif cmd=='new-album':
                res = new_album(request)
        
            elif cmd=='add-item':
                res = add_item(request)
            else:
                res="je ne comprends pas...."
            
        else:
            # print request
            res = fetch_albums(request)

        return res
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
def fetch_albums(request):
    # grabs all albums
    t = loader.get_template('fetch_albums.html')
    d = {}
    albumlist = Album.objects.all()
    d['numalbums']=len(albumlist)+1
    d['album_list']=albumlist
    d['status_text']="Success"
    d['status']=grStatusCodes['SUCCESS']
    context = RequestContext(request, d)
    return HttpResponse(t.render(context), mimetype="text/plain")
    
#def fetch_albums_prune(request):
#    # grabs all albums that user can write to...
#    print "fetch_albums_prune called"
#    t = loader.get_template('fetch_albums.html')
#    d = {}
#    albumlist = Album.objects.all()
#    d['numalbums']=len(albumlist)
#    d['album_list']=albumlist
#    context = RequestContext(request, d)
#    return HttpResponse(t.render(context))
#
def add_item(request):
    """
    REQUEST:
    cmd=add-item
    protocol_version=2.0
    set_albumName=album name
    userfile=user-file
    userfile_name=file-name
    caption=caption [optional]
    force_filename=force-filename [optional]
    auto_rotate=yes/no [optional, since 2.5]
    extrafield.fieldname=fieldvalue [optional, since 2.3]
    
    RESPONSE:
    #__GR2PROTO__
    status=result-code
    status_text=explanatory-text
    item_name=name-of-new-item [G2 since 2.7]
    
    - If the status is equal to GR_STAT_SUCCESS, the file upload succeeded.
    - name-of-new-item is the name (or rather the Id) of the newly created item (only available in G2).
    
    """
    user = request.user

    
    p = request.POST
    album = Album.objects.get(id=p['g2_form[set_albumName]'])
    upload_dir = os.path.join(settings.MEDIA_ROOT,'gallery_uploads',album.slug)
    upload_url = "%s/%s/%s" % (settings.MEDIA_URL, 'gallery_uploads',album.slug)
    
    savename = None
    if p.has_key('g2_form[force_filename]'):
        savename   = p['g2_form[force_filename]']            
    # new_data = request.POST.copy()
    # new_data.update(request.FILES)
    try:
        upfile = request.FILES['g2_userfile']
        if not savename:
            savename=upfile['filename']
        # upfile_mimetype = request.FILES['g2_userfile'][0]['mimetype']
        bits=upfile['content']
        if request.POST.has_key('g2_form[caption]'):
            title=request.POST['g2_form[caption]']
        else:
            title=request.POST['g2_form[force_filename]']
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        bits=None
    # print type(newdata['g2_userfile'].read())
    #print request.raw_post_data
    
    renametmpl = "%.2d-%s"
    i = 1
    
    if not os.path.exists(upload_dir):
        try:
            os.makedirs(upload_dir)
        except:
            traceback.print_exc(file=sys.stdout)
    newname = savename
    while os.path.exists(os.path.join(upload_dir,newname)):
        newname = renametmpl % (i,savename)
        i = i + 1

    savename = newname
    f = open(os.path.join(upload_dir,savename),'wb')
    f.write("%s" % bits)
    f.close()
    # ok file is uploaded, let's create the gallery object...
    try:
        item = GalleryItem(
            album=album,
            image=os.path.join('gallery_uploads',album.slug, newname),
            title=title
        )
        item.slug=SlugifyUniquely(item.title, item.__class__)
        item.save()
    except:
         traceback.print_exc(file=sys.stdout)
        
    t = loader.get_template('add_item.html')
    d = {
        'item':item,
        'status':grStatusCodes['SUCCESS'],
        'status_text':"Success",
    }
    c = RequestContext(request, d)
    return HttpResponse(t.render(c))
    
    
    

def album_properties(request):
    """
    REQUEST:
    cmd=album-properties
    protocol_version=2.0
    set_albumName=album-name
    
    RESPONSE:
    __GR2PROTO__
    status=result-code
    status_text=explanatory-text
    auto_resize=resize-dimension
    max_size=max-dimension [since 2.15]
    add_to_beginning=yes/no [since 2.10]
    """
    p = request.POST
    album = Album.objects.get(slug__iexact=p['set_albumName'])
    t = loader.get_template('album_properties.html')
    d = {
        'album':album,
        'status': grStatusCodes['SUCCESS'],
        'status_text':'Success',
    }
    

def new_album(request):
    """
    REQUEST:
    cmd=new-album
    protocol_version=2.1
    set_albumName=parent-album-name
    newAlbumName=album-name [optional]
    newAlbumTitle=album-title [optional]
    newAlbumDesc=album-description [optional]
    
    RESPONSE:
    #__GR2PROTO__
    status=result-code
    status_text=explanatory-text
    album_name=actual-name [since 2.5]
    """
    p = request.POST
    # get the default gallery...
    g = Gallery.objects.all()[0]
    try:
        a = Album(
            title=p['g2_form[newAlbumTitle]'],
            slug=SlugifyUniquely(p['g2_form[newAlbumTitle]'], Album),
            description=p['g2_form[newAlbumDesc]'],
            gallery=g,
            owner=request.user,
            )
        a.save()
    except Exception as e:
        a=None
    
    t = loader.get_template('new_album.html')
    d = {
        'album':a,
        'status':grStatusCodes['SUCCESS'],
        'status_text':'Album Successfully Created',
    }
    c = RequestContext(request, d)
    return HttpResponse(t.render(c),  mimetype="text/plain")
    
def fetch_album_images(request):
    """
    REQUEST:
    cmd=fetch-album-images
    protocol_version=2.4
    set_albumName=album-name
    albums_too=yes/no [optional, since 2.13]
    random=yes/no [optional, G2 since ***]
    limit=number-of-images [optional, G2 since ***]
    
    
    RESPONSE:
    #__GR2PROTO__
    status=result-code
    status_text=explanatory-text
    album.caption=caption associated with the album [G2 since 2.11]
    --- start foreach ---
    image.name.ref-num=filename of the image
    image.raw_width.ref-num=the width of the full-sized image
    image.raw_height.ref-num=the height of the full-sized image
    image.raw_filesize.ref-num=size of the full-sized image
    image.resizedName.ref-num=filename of the resized image, if there is one
    image.resized_width.ref-num=the width of the resized image, if there is one [since 2.9]
    image.resized_height.ref-num=the height of the resized image, if there is one [since 2.9]
    image.thumbName.ref-num=filename of the thumbnail [since 2.9]
    image.thumb_width.ref-num=the width of the thumbnail [since 2.9]
    image.thumb_height.ref-num=the height of the thumbnail [since 2.9]
    image.caption.ref-num=caption associated with the image
    image.title.ref-num=title associated with the image [G2]
    image.extrafield.fieldname.ref-num=value of the extra field of key fieldname
    image.clicks.ref-num=number of clicks on the image
    image.capturedate.year.ref-num=date of capture of the image (year) [G1]
    image.capturedate.mon.ref-num=date of capture of the image (month) [G1]
    image.capturedate.mday.ref-num=date of capture of the image (day of the month) [G1]
    image.capturedate.hours.ref-num=date of capture of the image (hour) [G1]
    image.capturedate.minutes.ref-num=date of capture of the image (minute) [G1]
    image.capturedate.seconds.ref-num=date of capture of the image (second) [G1]
    image.forceExtension.ref-num=the extension of the image [G2]
    image.hidden.ref-num=yes/no [since 2.14]
    --- end foreach ---
    album.name.ref-num=name of the album [since 2.13]
    image_count=total number of images in the album
    baseurl=URL of the album
    """
def move_album(request):
    """
    REQUEST:
    cmd=move-album
    protocol_version=2.7
    set_albumName=source-album
    set_destalbumName=destination-album
    
    RESPONSE:
    #__GR2PROTO__
    status=result-code
    status_text=explanatory-text
    """

def increment_view_count(request):
    """
    REQUEST:
    cmd=image-properties
    protocol_version=****
    itemId=item-id
    
    RESPONSE:
    #__GR2PROTO__
    status=result-code
    status_text=explanatory-text
    """

def image_properties(request):
    """
    REQUEST:
    cmd=image-properties
    protocol_version=***
    id=item-id
    
    RESPONSE:
    #__GR2PROTO__
    status=result-code
    status_text=explanatory-text
    image.name=filename of the image
    image.raw_width=the width of the full-sized image
    image.raw_height=the height of the full-sized image
    image.raw_filesize=size of the full-sized image
    image.resizedName=filename of the resized image, if there is one
    image.resized_width=the width of the resized image, if there is one
    image.resized_height=the height of the resized image, if there is one
    image.thumbName=filename of the thumbnail
    image.thumb_width=the width of the thumbnail
    image.thumb_height=the height of the thumbnail
    image.caption=caption associated with the image
    image.title=title associated with the image
    image.forceExtension=the extension of the image
    image.hidden=yes/no

    """

def no_op(request):
    """
    RESPONSE:
    #__GR2PROTO__
    status=result-code
    status_text=explanatory-text
    """



def login_request(request, username, password):
    template = """
    #__GR2PROTO__
    status=%s
    status_text=%s
    server_version=%s
    """
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponse(template % (grStatusCodes['SUCCESS'], 'Login Successful','2.2'))
        else:
            return HttpResponse(template % (grStatusCodes['LOGIN_MISSING'], 'User not active', '2.2'))
    else:
        return HttpResponse(template % (grStatusCodes['PASSWORD_WRONG'], 'Bad Password', '2.2'))
