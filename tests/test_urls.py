import pytest
from django.urls import reverse, resolve

def test_home_url():
    url = reverse("xgallery:overview")
    assert resolve(url).view_name == "xgallery:overview"
    