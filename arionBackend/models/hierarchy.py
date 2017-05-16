"""
This module contains the class to represent a real-world hierarchy.
"""

from django.db import models

from arionBackend.serializers.json import serialize_hierarchy_complete, serialize_hierarchy_overview


class Hierarchy(models.Model):
    """
    This class represents a real-world hierarchy of event types.
    """

    name = models.TextField()
    json_representation = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def to_json(self):
        """
        This method calls the json serializer for the hierarchy and includes the hierarchy representation.
        :return: The hierarchy object as a json object.
        """
        return serialize_hierarchy_complete(self)

    def to_basic_json(self):
        """
        This method calls the json serializer for the hierarchy and does not include the hierarchy representation.
        :return: The hierarchy object as a json object.
        """
        return serialize_hierarchy_overview(self)
