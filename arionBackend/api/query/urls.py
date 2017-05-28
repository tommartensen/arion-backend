"""
This module holds the url patterns for the query API.
"""

from django.conf.urls import url

from arionBackend.api.query.query import GetQueriesByHierarchyId, GetQueryById

urlpatterns = [
	url(r'^esper/hierarchy/(?P<hierarchy_id>(\d){1,32})$',
		GetQueriesByHierarchyId.as_view(), name="get-queries-by-hierarchy-id"),
	url(r'^esper/(?P<query_id>(\d){1,32})$',
	    GetQueryById.as_view(), name="get-query-by-id"),
]
