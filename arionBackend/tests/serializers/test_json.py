"""
This module holds the test cases for the json serializer.
"""
from django.utils import timezone
from django.test import TestCase

from arionBackend.models.hierarchy import Hierarchy
from arionBackend.models.query import Query
from arionBackend.serializers.json import serialize_hierarchy_overview, serialize_hierarchy_complete, serialize_query


class JsonTestCase(TestCase):
	"""
	This class contains the tests for the Hierarchy API.
	"""

	@classmethod
	def setUpTestData(cls):
		"""
		This method sets up the test class with the required data.
		"""
		hierarchy = Hierarchy(name="TestHierarchy", json_representation="{}")
		hierarchy.save()
		Query(hierarchy=hierarchy, query_string="INSERT INTO asd SELECT * FROM asd",
				eqmn_representation="{'output': {'name': 'asd', 'select': '*'}, 'input': {'single': 'asd'}}").save()

	def test_get_hierarchy_json_basic(self):
		"""
		Tests if the hierarchy can be serialized into a json object with few information.
		"""
		hierarchy = serialize_hierarchy_overview(Hierarchy.objects.get(name="TestHierarchy"))
		self.assertEqual(hierarchy["id"], 1)
		self.assertEqual(hierarchy["name"], "TestHierarchy")
		self.assertLessEqual(hierarchy["timestamp"], timezone.now())

	def test_get_hierarchy_json(self):
		"""
		Tests if the hierarchy can be serialized into a json object with all information.
		"""
		hierarchy = serialize_hierarchy_complete(Hierarchy.objects.get(name="TestHierarchy"))
		self.assertEqual(hierarchy["id"], 1)
		self.assertEqual(hierarchy["name"], "TestHierarchy")
		self.assertLessEqual(hierarchy["timestamp"], timezone.now())
		self.assertEqual(hierarchy["hierarchy"], {})

	def test_get_query_json(self):
		"""
		Tests if the query can be serialized into a json object.
		"""
		query = serialize_query(Query.objects.get(query_string="INSERT INTO asd SELECT * FROM asd"))
		self.assertEqual(query["id"], 1)
		self.assertEqual(query["query"], "INSERT INTO asd SELECT * FROM asd")
		self.assertEqual(
			query["eqmn_representation"],
			"{'output': {'name': 'asd', 'select': '*'}, 'input': {'single': 'asd'}}")
