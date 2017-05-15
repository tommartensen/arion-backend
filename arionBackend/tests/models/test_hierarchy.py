"""
This module holds the test cases for the hierarchy model.
"""
from django.test import TestCase

from arionBackend.models.hierarchy import Hierarchy


class HierarchyTestCase(TestCase):
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
        hierarchy_as_json = Hierarchy.objects.get(name="TestHierarchy").to_json()
        self.assertEqual(hierarchy_as_json, {'id': 1, 'name': 'TestHierarchy', 'hierarchy': {}})
