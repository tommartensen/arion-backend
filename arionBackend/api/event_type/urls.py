"""
This module holds the url patterns for the query API.
"""

from django.conf.urls import url

from arionBackend.api.event_type.event_type import GetEventTypesByHierarchyId, GetEventTypeById

urlpatterns = [
	url(r'^esper/hierarchy/(?P<hierarchy_id>(\d){1,32})$', GetEventTypesByHierarchyId.as_view(),
		name="get-event-types-by-hierarchy-id"),
	url(r'^esper/(?P<event_type_id>(\d){1,32})$', GetEventTypeById.as_view(), name="get-event-type-by-id"),
]
