"""
This module contains all json serializers in the project.
"""
import json


def serialize_hierarchy_overview(hierarchy):
    """
    Serializes a hierarchy to JSON format with basic information.
    :param hierarchy: given hierarchy to serialize.
    :return: Dictionary with hierarchy information
    """
    return {
        "id": hierarchy.id,
        "name": hierarchy.name,
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
        "hierarchy": json.loads(hierarchy.json_representation)
    }
