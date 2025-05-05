import os
import pytest
import base64

from django.test import TestCase
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
try:
    from xmlrpc.client import Fault
    from xmlrpc.client import ServerProxy
except ImportError:  # Python 2
    from xmlrpclib import Fault
    from xmlrpclib import ServerProxy

from xgallery.views import wp
from xgallery.models import Gallery, GalleryItem

from xblog.models import Author, Blog
from hashlib import md5

from .utils import TestTransport

class WpTests(TestCase):
    def setUp(self):
        # Create a test user before each test
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )
        
        self.remote_user = User.objects.create_user(
            username='remotetestuser',
            password='remotetestpassword',
            email='test@example.com'
        )
        
        self.remote_user.author.remote_access_enabled = True
        self.remote_user.author.save()

        self.test_blog = Blog.objects.create(
            title="Remote User's Space",
            description="A blog for Remote User.  Slippery when wet!",
            owner=User.objects.get(username="remotetestuser"),
            site=Site.objects.get_current()
        )
        
        self.remoteuser_test_gallery = Gallery.objects.create(
            title = "Remote User's Gallery",
            description = "Hi, I am remote user, this is my gallery.",
            blog = self.test_blog,
        )

        self.server_proxy = ServerProxy('http://localhost:8000/xmlrpc/',
                                        transport=TestTransport(),
                                        verbose=0)

    def test_image_upload_with_logged_in_user(self):
        username = self.remote_user.username
        api_key = self.remote_user.author.remote_access_key
        image_filename = os.path.join(os.path.dirname(__file__), 'assets', '200x200.jpg')
        image = open(image_filename, 'rb').read()
        image_md5 = md5(image)
        blog = self.test_blog.id
        
        struct = {
            "name": "200x200.jpg",
            "type": "image/jpeg",
            "bits": image,
        }

        res = self.server_proxy.wp.uploadFile(
            blog,
            username,
            api_key,
            struct,
        )
        
        """
        Return Values
        struct
            string id (Added in WordPress 3.4)
            string file: Filename.
            string url
            string type
        """
        binary_content = b""
        with GalleryItem.objects.get(id=int(res['id'])).image.open('rb') as remote_image:
            for chunk in remote_image.chunks():
                binary_content += chunk

        remote_image_md5 = md5(binary_content)
        self.assertEqual(remote_image_md5.hexdigest(), image_md5.hexdigest())
    
    def test_image_upload_with_caption(self):
        """
        adding optional caption element to struct
        """
        username = self.remote_user.username
        api_key = self.remote_user.author.remote_access_key
        image_filename = os.path.join(os.path.dirname(__file__), 'assets', '200x200.jpg')
        image = open(image_filename, 'rb').read()
        image_md5 = md5(image)
        blog = self.test_blog.id
        caption = "A lovely image of something"

        struct = {
            "name": "200x200.jpg",
            "type": "image/jpeg",
            "bits": image,
            "caption": caption
        }

        res = self.server_proxy.wp.uploadFile(
            blog,
            username,
            api_key,
            struct,
        )
        
        item = GalleryItem.objects.get(id=int(res['id']))
        self.assertEqual(item.caption, caption)
        