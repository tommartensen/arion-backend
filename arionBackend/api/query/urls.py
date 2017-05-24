"""
This module holds the url patterns for the query API.
"""

from django.conf.urls import url

from arionBackend.api.query.query import GetQueriesByHierarchyId

urlpatterns = [
	url(r'^esper/hierarchy/(?P<hierarchy_id>(\d){1,32})$',
		GetQueriesByHierarchyId.as_view(), name="get-queries-by-hierarchy-id"),
]
