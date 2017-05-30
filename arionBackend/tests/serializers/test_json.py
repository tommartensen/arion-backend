"""
This module holds the test cases for the json serializer.
"""
import json

from django.utils import timezone
from django.test import TestCase

from arionBackend.models.event_type import EventType
from arionBackend.models.hierarchy import Hierarchy
from arionBackend.models.query import Query
from arionBackend.serializers.json import JSONSerializer


class JsonTestCase(TestCase):
	"""
	This class contains the tests for the Hierarchy API.
	"""

	@classmethod
	def setUpTestData(cls):
		"""
		This method sets up the test class with the required data.
		"""
		hierarchy = Hierarchy(name="TestHierarchy", graph_representation="{}")
		hierarchy.save()
		event_type = EventType(name="asd", hierarchy=hierarchy)
		event_type.save()
		query = Query(hierarchy=hierarchy, query_string="INSERT INTO asd SELECT * FROM asd",
					output_event_type=event_type,
					eqmn_representation=json.dumps({'output': {'name': 'asd', 'select': '*'}, 'input': {'single': 'asd'}}))
		query.save()
		query.feeding_event_types.set([event_type])
		query.save()

	def test_get_hierarchy_json_basic(self):
		"""
		Tests if the hierarchy can be serialized into a json object with few information.
		"""
		hierarchy = JSONSerializer.serialize_hierarchy_overview(Hierarchy.objects.get(name="TestHierarchy"))
		self.assertEqual(hierarchy["id"], 1)
		self.assertEqual(hierarchy["name"], "TestHierarchy")
		self.assertLessEqual(hierarchy["timestamp"], timezone.now())

	def test_get_hierarchy_json(self):
		"""
		Tests if the hierarchy can be serialized into a json object with all information.
		"""
		hierarchy = JSONSerializer.serialize_hierarchy_complete(Hierarchy.objects.get(name="TestHierarchy"))
		self.assertEqual(hierarchy["id"], 1)
		self.assertEqual(hierarchy["name"], "TestHierarchy")
		self.assertLessEqual(hierarchy["timestamp"], timezone.now())
		self.assertEqual(hierarchy["hierarchy"], {})

	def test_get_query_json(self):
		"""
		Tests if the query can be serialized into a json object.
		"""

		query = JSONSerializer.serialize_query(Query.objects.get(query_string="INSERT INTO asd SELECT * FROM asd"))
		self.assertEqual(query["id"], 1)
		self.assertEqual(query["query"], "INSERT INTO asd SELECT * FROM asd")
		self.assertDictEqual(
			query["eqmnRepresentation"],
			{'output': {'name': 'asd', 'select': '*'}, 'input': {'single': 'asd'}})
