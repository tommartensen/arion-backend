"""
This module contains the class to represent a real-world hierarchy.
"""

from django.db import models

from arionBackend.serializers.json import serialize_hierarchy


class Hierarchy(models.Model):
    """
    This class represents a real-world hierarchy of event types.
    """

    name = models.TextField()
    json_representation = models.TextField()

    def to_json(self):
        """
        This method calls the json serializer for the hierarchy.
        :return: The hierarchy object as a json object.
        """
        return serialize_hierarchy(self)
