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

	def to_json(self):
		"""
		Serializes an event type to a basic JSON.
		:return: basic event type information in JSON format
		"""
		return JSONSerializer.serialize_basic_event_type(self)

	def to_complete_json(self):
		"""
		Serializes an event type to an enhanced JSON.
		:return: enhanced event type information in JSON format
		"""
		return JSONSerializer.serialize_complete_event_type(self)

	def is_basic_event_type(self):
		"""
		Tests is the event type is not fed by any query.
		:return: Boolean
		"""
		if not len(self.output_type.all()):
			return True
		else:
			return False
