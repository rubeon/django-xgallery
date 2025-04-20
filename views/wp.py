import logging
import mimetypes
import base64
import easy_thumbnails.files

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponseForbidden
from django.core.files.base import ContentFile

try:
    from xmlrpc.client import Fault
    from xmlrpc.client import DateTime
except ImportError:  # Python 2
    from xmlrpclib import Fault
    from xmlrpclib import DateTime

from xgallery.models import Album, Gallery, GalleryItem

LOGGER=logging.getLogger(f"xgallery.views.{__name__}")

try:
    from xblog.models import Blog, Author, Post
except ModuleNotFoundError:
    LOGGER.warn('xblog not found')

LOGIN_ERROR = 801
PERMISSION_DENIED = 803



def get_user(username, apikey, blogid=None):
    """
    checks if a user is authorized to make this call
    """
    LOGGER.debug("get_user entered")
    LOGGER.debug("user: %s" % username)
    LOGGER.debug("apikey: %s" % apikey)
    try:
        user = User.objects.get(**{'username':username})
    except User.DoesNotExist:
        raise Fault(LOGIN_ERROR, 'Username is incorrect.')
    if not apikey == user.author.remote_access_key:
        raise Fault(LOGIN_ERROR, 'Password is invalid.')
    if not user.author.remote_access_enabled:
        raise Fault(PERMISSION_DENIED, 'Remote access not enabled for this user.')
    # if not author.is_staff or not author.is_active:
    #    raise Fault(PERMISSION_DENIED, _('User account unavailable.'))
    #        raise Fault(PERMISSION_DENIED, _('User cannot %s.') % permission)
    return user

def is_user_blog(user, blogid):
    """
    checks if the blog in question belongs to the use
    """

def get_user_blog(blog_id, username, password):
    """
    converts the triplet into a Blog object
    """

    LOGGER.debug(f"get_user_blog  entered with {blog_id},{username},<password>")
    user = get_user(username, password)
    try:
        blog = Blog.objects.get(owner=user, id=int(blog_id))
    except ValueError:
        # probably passed a bad ID
        LOGGER.debug(f"bad id? {blog_id}")
        blog = Blog.objects.filter(owner=user)[0]
    except Blog.DoesNotExist:
        LOGGER.debug(f"bad id? {blog_id}")
        blog = Blog.objects.filter(owner=user)[0]
        
    LOGGER.debug(f"Blog: {blog}")
    return blog

def media_item_size(item, alias):
    """
    MediaItemSize

    struct
        string file: The filename of this version of the media item, at this size, without the path (eg. "foo-768x1024.jpg" or "foo-940x198.jpg")
        string width
        string height
        string mime-type : image/jpeg or ...    
    """
    
    struct = {
        'file': item.get_file_name(),
        'width': item.image_width,
        'height': item.image_height,
        'mimetype': mimetypes.guess_type(str(item.image.name))[0] or 'application/octet-stream',
    }
    
    return struct

def media_metadata(item):
    """
    MediaItemMetadata

    struct
        int width
        int height
        string file: The filename, including path from the uploads directory (eg "2013/09/foo.jpg")
        struct sizes: A struct (array) of MediaItemSize objects describing each of the sizes of this media item which are available. Note that not every size exists for every media item.
            MediaItemSize thumbnail
            MediaItemSize medium
            MediaItemSize large
            MediaItemSize post-thumbnail
            PostThumbnailImageMeta image_meta
    """
    
    tm = easy_thumbnails.files.get_thumbnailer(item.image)
    size_array = []
    for key in settings.THUMBNAIL_ALIASES['xgallery.GalleryItem'].keys():
        options = settings.THUMBNAIL_ALIASES['xgallery.GalleryItem'][key]
        size_dict = {}
        thistm = tm.get_existing_thumbnail(options)
        if not thistm:
            continue
        size_dict[key] = {
            'file': thistm.name or "Untitled",
            'filesize': thistm.size or 0,
            'mime-type': mimetypes.guess_type(str(thistm.file))[0] or 'application/octet-stream',
            'width': thistm.width or 0,
            'height': thistm.height or 0,
        }
        size_array.append(size_dict)
    
    LOGGER.debug(size_array)
        
    struct = {
        'file': item.get_file_name(),
        'width': item.image_width,
        'height': item.image_height,
        'sizes': size_array,
    }
    
    return struct

def getMediaItem(blog_id, username, password, attachment_id):
    """
    Parameters

        int blog_id
        string username
        string password
        int attachment_id

    Return Values

        struct
            string attachment_id (Added in WordPress 3.4)
            datetime date_created_gmt
            int parent: ID of the parent post.
            string link: URL to the media item itself (the actual .jpg/.pdf/etc file, eg http://domain.tld/wp-content/uploads/2013/09/foo.jpg)
            string title
            string caption
            string description
            MediaItemMetadata metadata
            string thumbnail: URL to the media item thumbnail (eg http://domain.tld/wp-content/uploads/2013/09/foo-150x150.jpg)
    """
    LOGGER.debug(f"getMediaItem entered with {blog_id}, {username}, <password>, {attachment_id}")
    # must have xblog installed, might make this configurable at some point
    if not 'xblog' in settings.INSTALLED_APPS:
        raise Exception("Not Implemented")
    
    blog = get_user_blog(blog_id, username, password)
    LOGGER.debug(f"found user blog {blog}")
    gallery_item = GalleryItem.objects.get(id=attachment_id)
    LOGGER.debug(f"found gallery item blog {gallery_item}")
    if gallery_item.album.gallery.blog != blog:
        LOGGER.debug(f"{gallery_item} not in this {blog}")
        raise Fault(PERMISSION_DENIED, 'Not owner')
    """
    MediaItemMetadata

    struct
        int width
        int height
        string file: The filename, including path from the uploads directory (eg "2013/09/foo.jpg")
        struct sizes: A struct (array) of MediaItemSize objects describing each of the sizes of this media item which are available. Note that not every size exists for every media item.
        MediaItemSize thumbnail
        MediaItemSize medium
        MediaItemSize large
        MediaItemSize post-thumbnail
        PostThumbnailImageMeta image_meta    
    
    """
    metadata = media_metadata(gallery_item)
    
    LOGGER.debug(f"metadata: {metadata}")
    struct = {
        'attachment_id': str(gallery_item.id),
        'date_created_gmt': gallery_item.pub_date,
        'parent': 0,
        'link': gallery_item.image.url,
        'title': gallery_item.title or '',
        'caption': gallery_item.caption or '',
        'description': gallery_item.description or '',
        'metadata': metadata,
    }
    LOGGER.debug(f"struct: {struct}")    
    return struct

def getMediaLibrary(blog_id, username, password, filter=None):
    """
    int blog_id
    string username
    string password
    struct filter: Optional (and all members are optional).
        int number: Total number of media items to retrieve.
        int offset
        int parent_id: Limit to attachments on this post ID. 0 shows unattached media items. Empty string shows all media items.
        string mime_type
    array
        struct: see #wp.getMediaItem
    """
    LOGGER.debug(f"getMediaLibrary entered with {blog_id}, {username}, <password>, {filter}")
    # must have xblog installed, might make this configurable at some point
    if not 'xblog' in settings.INSTALLED_APPS:
        raise Exception("Not Implemented")
    
    blog = get_user_blog(blog_id, username, password)
    LOGGER.debug(f"found user blog {blog}")
    items =  GalleryItem.objects.filter(album__gallery__blog=blog).order_by('-pub_date')

    if filter:
        offset = filter.get('offset',0)
        limit = filter.get('number')
        post_id = filter.get('parent_id')
    else:
        offset = 0
        limit = None
        post_id = None

    if post_id:
        LOGGER.debug("Got parent_id %s", post_id)
        post = Post.objects.get(id=post_id)
        LOGGER.debug("Got post: %s", post)
        items =  post.images.all()

    if limit:
        LOGGER.debug("Got limit: %s", limit)
        limit = int(limit)
        items =  items[offset:offset+limit]
    else:
        items =  items[offset:]
    # find gallery from blog
    # galleries = Gallery.objects.filter(blog=blog)
    media_items = [getMediaItem(blog_id, username, password, att.id) for att in items]
    LOGGER.debug(f"found {len(media_items)}")
    return media_items

def uploadFile(blog_id, username, password, data, overwrite=True):
    """
    int blogid
    string username
    string password
    struct data
        string name: Filename.
        string type: File MIME type.
        base64 bits: binary data. Needs to be base64-encoded.
        bool overwrite: Optional. Has no effect (see 17604). Was intended to overwrite an existing attachment of the same name. (Added in WordPress 2.2)
        int post_id: Optional. Allows an attachment to be assigned to a post. (User must have permission to edit the assigned post)

    Return Values
    struct
        string id (Added in WordPress 3.4)
        string file: Filename.
        string url
        string type
    """
    LOGGER.debug("uploadFile entered with %s, %s, <password>", (blog_id, username))
    # must have xblog installed, might make this configurable at some point
    if not 'xblog' in settings.INSTALLED_APPS:
        raise Exception("Not Implemented")
    blog = get_user_blog(blog_id, username, password)
    LOGGER.debug(f"found user blog {blog}")
    
    gallery = Gallery.objects.filter(blog=blog)[0]
    album, created = Album.objects.get_or_create(title='Blog Uploads', gallery=gallery)
    if created:
        LOGGER.debug(f"Automatically created album {album.title}")
        album.description = "Automatically created by Django"
        album.save()
    item = GalleryItem(
        album=album,
        title=data.get('name', 'Untitled'),
        mimetype=data.get('type'),
    )
    item.save()
    if data.get('post_id'):
        item.posts.add(data.get('post_id'))
    else:
        LOGGER.debug("no posts :-(")
    LOGGER.debug("processing data...")
    # bitsfd = base64.standard_b64decode(data.get('bits'))
    bitsfd = ContentFile(data['bits'].data)
    LOGGER.debug("got bitsfd...")
    item.image.save(data.get('name'), bitsfd)
    LOGGER.debug("saving")
    item.save()
    
    res = {
        'id': item.id,
        'file': item.image.name,
        'url': item.image.url,
        'type': item.mimetype
    }            
    return res    
        
def ping():
    """
    """
    return True
    