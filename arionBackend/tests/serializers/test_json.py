"""
This module holds the test cases for the json serializer.
"""
from django.test import TestCase

from arionBackend.models.hierarchy import Hierarchy
from arionBackend.serializers.json import serialize_hierarchy


class JsonTestCase(TestCase):
    """
    This class contains the tests for the Hierarchy API.
    """

    @classmethod
    def setUpTestData(cls):
        """
        This method sets up the test class with the required data.
        """
        Hierarchy(name="TestHierarchy", json_representation="{}").save()

    def test_get_json(self):
        """
        Tests if the hierarchy can be serialized into a json object.
        """
        hierarchy = Hierarchy.objects.get(name="TestHierarchy")
        self.assertEqual(serialize_hierarchy(hierarchy), {'id': 1, 'name': 'TestHierarchy', 'hierarchy': {}})
