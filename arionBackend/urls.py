"""
This module holds the url patterns for the project.
"""

from django.conf.urls import url, include

from arionBackend.api import urls as api_urls

urlpatterns = [
    url(r'^api/', include(api_urls)),
]
