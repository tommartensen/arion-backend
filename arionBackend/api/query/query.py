"""
This module contains all classes for the query API.
"""
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from rest_framework import status

from arionBackend.api import GetXByIdView
from arionBackend.models.hierarchy import Hierarchy
from arionBackend.models.query import Query


class GetQueriesByHierarchyId(GetXByIdView):
	"""
	This class holds the methods to get queries of a hierarchy by id.
	"""

	def get(self, request, hierarchy_id, format=None):
		"""
		This works as the API endpoint to return the queries for a defined hierarchy.
		:param request: The request object that the client sent.
		:param hierarchy_id: The requested hierarchy defined by the id.
		:param format: The data format that was requested.
		:return: JsonResponse with the queries.
		"""
		if not self.__class__.validate_input(hierarchy_id):
			return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
		queries = Query.objects.filter(hierarchy__id=hierarchy_id)
		if not len(queries):
			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
		response = []
		for query in queries:
			response.append(query.to_json())
		return JsonResponse(response, safe=False)


class GetQueryById(GetXByIdView):
	"""
	This class holds the methods to get queries of a hierarchy by id.
	"""

	def get(self, request, query_id, format=None):
		"""
		This works as the API endpoint to return the queries for a defined hierarchy.
		:param request: The request object that the client sent.
		:param hierarchy_id: The requested hierarchy defined by the id.
		:param format: The data format that was requested.
		:return: JsonResponse with the queries.
		"""
		if not self.__class__.validate_input(query_id):
			return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
		try:
			query = Query.objects.get(id=query_id)
		except ObjectDoesNotExist:
			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
		return JsonResponse(query.to_json(), safe=False)


class GetQueriesByEventTypeId(GetXByIdView):
	def get(self, request, event_type_id, format=None):
		if not self.__class__.validate_input(event_type_id):
			return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
		queries = Query.objects.filter(output_event_type__id=event_type_id)
		if not len(queries):
			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
		response = []
		for query in queries:
			response.append(query.to_json())
		return JsonResponse(response, safe=False)