"""
This module contains all classes for the query API.
"""
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from arionBackend.models.hierarchy import Hierarchy
from arionBackend.models.query import Query


class GetQueriesByHierarchyId(APIView):
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
		try:
			hierarchy = Hierarchy.objects.get(id=hierarchy_id)
		except ObjectDoesNotExist:
			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
		queries = Query.objects.filter(hierarchy=hierarchy)
		response = []
		for query in queries:
			response.append(query.to_json())
		return JsonResponse(response, safe=False)

	@staticmethod
	def validate_input(hierarchy_id):
		"""
		Static method to validate the input.
		:param hierarchy_id: the input by the client.
		:return: true, if valid; else if invalid.
		"""
		return int(hierarchy_id)
