"""
This module contains all the APIs of the project.
"""
from rest_framework.views import APIView


class GetXByIdView(APIView):
	"""
	This is a parent class for the API view used in the project and contains a basic validator.
	"""
	@staticmethod
	def validate_input(id):
		"""
		Basic validator for ids.
		:param id: id to check
		:return: true, if id > 0
		"""
		return int(id)
