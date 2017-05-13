"""
This module contains all the greetings APIs.
"""

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def hello(request, format=None):
    """This method greets the user."""
    return JsonResponse({'greeting': 'Hello'})


class Moin(APIView):
    """This class may greet the user."""
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        return JsonResponse({'greeting': 'Moin'})
