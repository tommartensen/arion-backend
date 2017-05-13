"""
This module holds the url patterns for the project.
"""

from django.conf.urls import url

from arionBackend.api.hierarchy.hierarchy import CreateHierarchy, GetHierarchyById, GetAllHierarchies

urlpatterns = [
    url(r'^esper$', GetAllHierarchies.as_view(), name="get-all-esper-hierarchies"),
    url(r'^esper/(?P<hierarchy_id>(\d){1,32})$', GetHierarchyById.as_view(), name="get-esper-hierarchy-by-id"),
    url(r'^esper/create$', CreateHierarchy.as_view(), name="create-esper-hierarchy"),
]
