"""
This module holds the url patterns for the project.
"""

from django.conf.urls import url, include
from arionBackend.api.hierarchy import urls as hierarchy_urls

urlpatterns = [
	url(r'^hierarchy/', include(hierarchy_urls))
]
