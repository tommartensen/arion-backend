from django.http import JsonResponse
from rest_framework.views import APIView


class GetAllHierarchies(APIView):

    def get(self, request, format=None):
        return JsonResponse({})


class CreateHierarchy(APIView):
    """This class may greet the user."""

    def get(self, request, format=None):
        return JsonResponse({'greeting': 'Create'})


class GetHierarchyById(APIView):

    def get(self, request, hierarchy_id, format=None):
        return JsonResponse({'greeting': hierarchy_id})