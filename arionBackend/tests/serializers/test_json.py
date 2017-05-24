"""
This module holds the test cases for the json serializer.
"""
from django.utils import timezone
from django.test import TestCase

from arionBackend.models.hierarchy import Hierarchy
from arionBackend.serializers.json import serialize_hierarchy_overview, serialize_hierarchy_complete


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

	def test_get_json_basic(self):
		"""
		Tests if the hierarchy can be serialized into a json object with few information.
		"""
		hierarchy = serialize_hierarchy_overview(Hierarchy.objects.get(name="TestHierarchy"))
		self.assertEqual(hierarchy["id"], 1)
		self.assertEqual(hierarchy["name"], "TestHierarchy")
		self.assertLessEqual(hierarchy["timestamp"], timezone.now())

	def test_get_json(self):
		"""
		Tests if the hierarchy can be serialized into a json object with all information.
		"""
		hierarchy = serialize_hierarchy_complete(Hierarchy.objects.get(name="TestHierarchy"))
		self.assertEqual(hierarchy["id"], 1)
		self.assertEqual(hierarchy["name"], "TestHierarchy")
		self.assertLessEqual(hierarchy["timestamp"], timezone.now())
		self.assertEqual(hierarchy["hierarchy"], {})
