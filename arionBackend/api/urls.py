"""
This module holds the url patterns for the project.
"""

from django.conf.urls import url, include
from arionBackend.api.hierarchy import urls as hierarchy_urls
from arionBackend.api.query import urls as query_urls
from arionBackend.api.event_type import urls as event_type_urls

urlpatterns = [
	url(r'^hierarchy/', include(hierarchy_urls)),
	url(r'^query/', include(query_urls)),
	url(r'^event_type/', include(event_type_urls))
]
