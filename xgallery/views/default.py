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
    # c = RequestContext(request, d)
    t = loader.get_template('overview.html')
    return HttpResponse(t.render(d))
    
    
def showalbum(request, slug):
    # shows a particular gallery
    try:
        album = Album.objects.get(slug__iexact=slug)
    except:
        album=[]
    
    d = {}
    d['album']=album
    # c = RequestContext(request, d)
    t = loader.get_template('album.html')
    return HttpResponse(t.render(d))
    

def simpleviewer(request, slug):
    # spits out xml file for simpleviewer
    try:
        album = Album.objects.get(slug__iexact=slug)
    except:
        album=None

    d = {}
    d['album']=album
    # c = RequestContext(request, d)
    t = loader.get_template('simple_viewer.html')
    return HttpResponse(t.render(d))


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
    
