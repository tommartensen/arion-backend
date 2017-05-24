"""
This module contains the class to represent the real-world event query.
"""

from django.db import models

from arionBackend.models.hierarchy import Hierarchy
from arionBackend.serializers.json import serialize_query


class Query(models.Model):
	"""
	This class represents a real world event query.
	"""
	hierarchy = models.ForeignKey(Hierarchy, on_delete=models.CASCADE)
	query_string = models.TextField()
	eqmn_representation = models.TextField()

	def to_json(self):
		return serialize_query(self)
