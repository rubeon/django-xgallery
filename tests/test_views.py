import pytest
from django.urls import reverse
from django.test import Client

@pytest.mark.django_db
def test_home_view():
    client = Client()
    response = client.get(reverse("overview"))  # Assumes 'home' is a named URL
    assert response.status_code == 200
    assert "gallery overview" in str(response.content)  # Check template content

