# Create your views here.
from django.template import RequestContext, Context, loader
import logging
from django.http import HttpResponseRedirect, HttpResponse, Http404
from xgallery.models import *

LOGGER=logging.getLogger(__name__)

def overview(request):
    albums = Album.objects.all()[:10]
    d = {}
    d['albums']=albums
    c = RequestContext(request, d)
    t = loader.get_template('overview.html')
    return HttpResponse(t.render(c))
    
    
def photocast(request, slug=None):
    d = {}
    try:
      a = Album.objects.get(slug__iexact=slug)
    except Album.DoesNotExist:
      raise Http404
    d['album']=a
    t = loader.get_template('album_photocast.html')
    c = RequestContext(request, d)
    return HttpResponse(t.render(c))
 
def cooliris(request, slug=None):
    # theoretically, it would create the rss-feed necessary
    # to generate content for the cooliris safari plugin.
    # then again, I've been drinking
    d = {}
    # catch an exception...
    try:
      a = Album.objects.get(slug__iexact=slug)
    except Album.DoesNotExist:
      raise Http404
      
    d['album']=a
    t = loader.get_template('album_cooliris.html')
    c = RequestContext(request,d)
    return HttpResponse(t.render(c))

def showalbum(request, slug):
    # shows a particular gallery
    try:
        album = Album.objects.get(slug__iexact=slug)
    except:
        album=[]
    
    d = {}
    d['album']=album
    c = RequestContext(request, d)
    if request.GET.get('fullscreen', False):
        LOGGER.debug("REQUEST:FULLSCREEN")
        t = loader.get_template('fullscreen.html')
    else:
        t = loader.get_template('album.html')
    return HttpResponse(t.render(c))
    

def simpleviewer(request, slug):
    # spits out xml file for simpleviewer
    try:
        album = Album.objects.get(slug__iexact=slug)
    except:
        album=None

    d = {}
    d['album']=album
    c = RequestContext(request, d)
    t = loader.get_template('simple_viewer.html')
    return HttpResponse(t.render(c))


def xdomain(request):
    # provides the x-domain thingamabob for flash...
    # hard-coded for now..
    tmpl = """
    <?xml version="1.0"?>
    <!DOCTYPE cross-domain-policy SYSTEM "http://www.macromedia.com/xml/dtds/cross-domain-policy.dtd">
      <cross-domain-policy>
        <allow-access-from domain="*.youbitch.org" />
      </cross-domain-policy>
    """
    return HttpResponse(tmpl)
    
