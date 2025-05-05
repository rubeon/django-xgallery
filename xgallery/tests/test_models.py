import pytest
from django.test import TestCase
from xgallery.models import Gallery
from django.apps import apps

@pytest.mark.django_db
def test_app_config():
    assert apps.get_app_config('xgallery').name == 'xgallery'

@pytest.mark.django_db
def test_gallery_creation():
    obj = Gallery.objects.create(title="Test Object")
    assert obj.title == "Test Object"
    assert str(obj) == "Gallery Test Object"  # Test __str__ method


