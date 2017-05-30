"""
This module contains all json serializers in the project.
"""
from json import loads as json_loads


class JSONSerializer(object):
	"""
	This class contains methods for serializing model objects into JSON objects.
	"""

	@staticmethod
	def serialize_hierarchy_overview(hierarchy):
		"""
		Serializes a hierarchy to JSON format with basic information.
		:param hierarchy: given hierarchy to serialize.
		:return: Dictionary with hierarchy information
		"""
		return {
			"id": hierarchy.id,
			"name": hierarchy.name,
			"timestamp": hierarchy.timestamp
		}

	@staticmethod
	def serialize_hierarchy_complete(hierarchy):
		"""
		Serializes a hierarchy to JSON format with all information.
		:param hierarchy: given hierarchy to serialize.
		:return: Dictionary with hierarchy information
		"""
		return {
			"id": hierarchy.id,
			"name": hierarchy.name,
			"timestamp": hierarchy.timestamp,
			"hierarchy": json_loads(hierarchy.graph_representation),
		}

	@staticmethod
	def serialize_query(query):
		"""
		Serializes a query into JSON format.
		:param query: the query to serialize
		:return: Dictionary with query information
		"""
		return {
			"id": query.id,
			"query": query.query_string,
			"eqmnRepresentation": json_loads(query.eqmn_representation),
			"outputType": query.output_event_type.to_json(),
			"feedingTypes": [event_type.to_json() for event_type in query.feeding_event_types.all()]
		}

	@staticmethod
	def serialize_basic_event_type(event_type):
		"""
		Serializes an event type into JSON format.
		:param event_type: the event type to serialize
		:return: Dictionary with event type information
		"""
		return {
			"id": event_type.id,
			"name": event_type.name,
			"isBasicEventType": event_type.is_basic_event_type()
		}

	@staticmethod
	def serialize_complete_event_type(event_type):
		"""
		Serializes an event type into JSON format with enhanced information.
		:param event_type: the event type to serialize
		:return: Dictionary with enhanced event type information
		"""
		return {
			"id": event_type.id,
			"name": event_type.name,
			"isBasicEventType": event_type.is_basic_event_type(),
			"feedingQueries": [query.id for query in event_type.output_type.all()]
		}
