from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.views import APIView

from arionBackend.transformation.esper.esper_transformator import EsperTransformer


class GetAllHierarchies(APIView):

    def get(self, request, format=None):
        return JsonResponse(
            [{"id": 1, "name": "Hierarchy", "queries": ["Select * From Test", "Select * from Test2"]},
            {"id": 2, "name": "Horst", "queries": ["Select * From Test3", "Select * from Test4"]}],
            safe=False
        )


class CreateHierarchy(APIView):
    """This class may greet the user."""

    def post(self, request, format=None):
        data = request.data
        if not self.__class__.validate_input(data):
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        if EsperTransformer().transform(data["queries"]):
            return HttpResponse(status=status.HTTP_201_CREATED)
        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def validate_input(data):
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


class GetHierarchyById(APIView):

    def get(self, request, hierarchy_id, format=None):
        if not self.__class__.validate_input(hierarchy_id):
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({"name": "Hierarchy", "queries": ["Select * From Test", "Select * from Test2"]})

    @staticmethod
    def validate_input(hierarchy_id):
        return int(hierarchy_id)
