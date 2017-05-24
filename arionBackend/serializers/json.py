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
		"hierarchy": json_loads(hierarchy.json_representation)
	}
