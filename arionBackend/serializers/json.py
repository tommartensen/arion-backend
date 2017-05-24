"""
This module contains all json serializers in the project.
"""
from json import loads as json_loads


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
		"hierarchy": json_loads(hierarchy.json_representation),
	}


def serialize_query(query):
	"""
	Serializes a query into JSON format.
	:param query: the query to serialize
	:return: Dictionary with query information
	"""
	return {
		"id": query.id,
		"query": query.query_string,
		"eqmn_representation": query.eqmn_representation
	}
