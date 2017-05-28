"""
This module contains the class to represent the real-world event type.
"""

from django.db import models

from arionBackend.models.hierarchy import Hierarchy
from arionBackend.serializers.json import JSONSerializer


class EventType(models.Model):
	"""
	This class represents a real world event type.
	"""
	hierarchy = models.ForeignKey(Hierarchy)
	name = models.TextField()

	def is_basic_event_type(self):
		"""
		Checks, if event type has no source and is therefore considered a basic event type.
		:return: boolean
		"""
		return True

	def to_json(self):
		return JSONSerializer.serialize_basic_event_type(self)
