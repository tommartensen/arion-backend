"""
This module contains all the APIs of the project.
"""
from rest_framework.views import APIView


class GetXByIdView(APIView):

	@staticmethod
	def validate_input(id):
		return int(id)