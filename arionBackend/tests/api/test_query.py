"""
This module holds the test cases for the query API module.
"""
import json

from rest_framework import status
from rest_framework.test import APITestCase

from arionBackend.models.event_type import EventType
from arionBackend.models.hierarchy import Hierarchy
from arionBackend.models.query import Query


class QueryTestCase(APITestCase):
	"""
	This class contains the tests for the query API.
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
		query = Query(
			hierarchy=hierarchy, query_string="INSERT INTO asd SELECT * FROM asd", output_event_type=event_type,
			eqmn_representation=json.dumps({'output': {'name': 'asd', 'select': '*'}, 'input': {'single': 'asd'}}))
		query.save()
		query.input_event_types.add(event_type)
		query.save()

	def test_get_queries_by_hierarchy_id_success(self):
		"""
		Tests if queries can be retrieved by hierarchy id.
		"""
		hierarchy = Hierarchy.objects.get(name="TestHierarchy")
		response = self.client.get('/api/query/esper/hierarchy/' + str(hierarchy.id), follow=True)
		json_response = json.loads(response.content.decode('utf-8'))
		query = json_response[0]
		self.assertEqual(query["id"], 1)
		self.assertEqual(query["query"], 'INSERT INTO asd SELECT * FROM asd')
		self.assertDictEqual(
			query["eqmnRepresentation"],
			{'output': {'name': 'asd', 'select': '*'}, 'input': {'single': 'asd'}})
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_get_queries_by_hierarchy_id_invalid_id(self):
		"""
		Tests if the queries cannot be retrieved, if the id is invalid.
		"""
		request = self.client.get('/api/query/esper/hierarchy/0', follow=True)
		self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

	def test_get_queries_by_hierarchy_id_not_found(self):
		"""
		Tests if the queries cannot be retrieved, if there is no hierarchy with the id.
		"""
		hierarchy = Hierarchy.objects.get(name="TestHierarchy")
		request = self.client.get('/api/query/esper/hierarchy/' + str(hierarchy.id + 1), follow=True)
		self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

	def test_get_event_query_by_id(self):
		"""
		Tests if an event query can be retrieved by its id.
		"""
		query = Query.objects.get(query_string="INSERT INTO asd SELECT * FROM asd")
		response = self.client.get('/api/query/esper/' + str(query.id), follow=True)
		json_response = json.loads(response.content.decode('utf-8'))
		self.assertEqual(json_response["query"], "INSERT INTO asd SELECT * FROM asd")
		self.assertEqual(json_response["outputEventType"], {'id': 1, 'name': 'asd', 'isBasicEventType': False})
		self.assertEqual(type(json_response["inputEventTypes"]), list)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_get_event_query_by_id_invalid_id(self):
		"""
		Tests if the event query cannot be retrieved, if the id is invalid.
		"""
		request = self.client.get('/api/query/esper/0', follow=True)
		self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

	def test_get_event_query_by_id_not_found(self):
		"""
		Tests if the event query cannot be retrieved, if the id does not exist.
		"""
		query = Query.objects.get(output_event_type__name="asd")
		request = self.client.get('/api/query/esper/' + str(query.id + 1), follow=True)
		self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

	def test_get_queries_by_event_type_id_success(self):
		"""
		Tests if queries can be retrieved by event type id.
		"""
		event_type = EventType.objects.get(name="asd")
		response = self.client.get('/api/query/esper/event_type/' + str(event_type.id), follow=True)
		json_response = json.loads(response.content.decode('utf-8'))
		query = json_response[0]
		self.assertEqual(query["id"], 1)
		self.assertEqual(query["query"], 'INSERT INTO asd SELECT * FROM asd')
		self.assertDictEqual(
			query["eqmnRepresentation"],
			{'output': {'name': 'asd', 'select': '*'}, 'input': {'single': 'asd'}})
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_get_queries_by_event_type_id_invalid_id(self):
		"""
		Tests if the queries cannot be retrieved, if the id is invalid.
		"""
		request = self.client.get('/api/query/esper/event_type/0', follow=True)
		self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

	def test_get_queries_by_event_type_id_id_not_found(self):
		"""
		Tests if the queries cannot be retrieved, if there is no event type with the id.
		"""
		event_type = EventType.objects.get(name="asd")
		request = self.client.get('/api/query/esper/event_type/' + str(event_type.id + 1), follow=True)
		self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)
