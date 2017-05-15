"""
This module contains all json serializers in the project.
"""
import json


def serialize_hierarchy(hierarchy):
    """
    Serializes a hierarchy to JSON format.
    :param hierarchy: given hierarchy to serialize.
    :return: Dictionary with hierarchy information
    """
    return {
        "id": hierarchy.id,
        "name": hierarchy.name,
        "hierarchy": json.loads(hierarchy.json_representation)
    }
