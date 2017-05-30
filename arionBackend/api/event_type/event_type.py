"""
This module contains all classes for the query API.
"""
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from rest_framework import status

from arionBackend.api import GetXByIdView
from arionBackend.models.event_type import EventType


class GetEventTypesByHierarchyId(GetXByIdView):
	"""
	This class holds the methods to get queries of a hierarchy by id.
	"""

	def get(self, request, hierarchy_id, format=None):
		"""
		This works as the API endpoint to return the event types for a defined hierarchy.
		:param request: The request object that the client sent.
		:param hierarchy_id: The requested hierarchy defined by the id.
		:param format: The data format that was requested.
		:return: JsonResponse with the event types.
		"""
		if not self.__class__.validate_input(hierarchy_id):
			return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
		event_types = EventType.objects.filter(hierarchy__id=hierarchy_id).order_by("name")
		if not len(event_types):
			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
		response = []
		for event_type in event_types:
			response.append(event_type.to_json())
		return JsonResponse(response, safe=False)


class GetEventTypeById(GetXByIdView):
	"""
	This class holds the methods to get an event type by id.
	"""

	def get(self, request, event_type_id, format=None):
		"""
		This works as the API endpoint to return an event type specified by an id.
		:param request: The request object that the client sent.
		:param event_type_id: The requested event type defined by the id.
		:param format: The data format that was requested.
		:return: JsonResponse with the event type.
		"""
		if not self.__class__.validate_input(event_type_id):
			return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
		try:
			event_type = EventType.objects.get(id=event_type_id)
		except ObjectDoesNotExist:
			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
		return JsonResponse(event_type.to_complete_json(), safe=False)
