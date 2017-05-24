"""
This module contains all classes for the hierarchy API.
"""
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.views import APIView

from arionBackend.models.hierarchy import Hierarchy
from arionBackend.transformation.esper.esper_transformer import EsperTransformer


class GetAllHierarchies(APIView):
	"""
	This class holds the methods to get all hierarchies.
	"""

	def get(self, request, format=None):
		"""
		This works as the API endpoint to return all hierarchies.
		:param request: The request object that the client sent.
		:param format: The data format that was requested.
		:return: JSonResponse with the hierarchies.
		"""
		hierarchies = Hierarchy.objects.all()
		response = []
		for hierarchy in hierarchies:
			response.append(hierarchy.to_basic_json())
		return JsonResponse(data=response, safe=False)


class GetHierarchyById(APIView):
	"""
	This class holds the methods to get one hierarchy by id.
	"""

	def get(self, request, hierarchy_id, format=None):
		"""
		This works as the API endpoint to return a defined hierarchy.
		:param request: The request object that the client sent.
		:param hierarchy_id: The requested hierarchy defined by the id.
		:param format: The data format that was requested.
		:return: JsonResponse with the hierarchies.
		"""
		if not self.__class__.validate_input(hierarchy_id):
			return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
		try:
			hierarchy = Hierarchy.objects.get(id=hierarchy_id)
		except ObjectDoesNotExist:
			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
		return JsonResponse(hierarchy.to_json())

	@staticmethod
	def validate_input(hierarchy_id):
		"""
		Static method to validate the input.
		:param hierarchy_id: the input by the client.
		:return: true, if valid; else if invalid.
		"""
		return int(hierarchy_id)


class CreateHierarchy(APIView):
	"""
	This class holds the methods to create a new hierarchy.
	"""

	def post(self, request, format=None):
		"""
		This works as the API endpoint to create a new hierarchy.
		:param request: The request object that the client sent.
		:param format: The data format that was requested.
		:return: HttpResponse with a status code, depending on the success.
		"""
		data = request.data
		if not self.__class__.validate_input(data):
			return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

		if EsperTransformer().transform(name=data["name"], queries=data["queries"]):
			return HttpResponse(status=status.HTTP_201_CREATED)
		return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

	@staticmethod
	def validate_input(data):
		"""
		Static method to validate the input.
		:param data: the input by the client.
		:return: true, if valid; else if invalid.
		"""
		try:
			if not (data["name"] and len(data["queries"]) and type(data["queries"]) is list):
				return False
		except KeyError:
				return False

		are_valid_queries = True
		for query in data["queries"]:
			if not query:
				are_valid_queries = False
		return are_valid_queries
