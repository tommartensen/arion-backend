"""
This module holds the test cases for the event type API module.
"""
import json

from rest_framework import status
from rest_framework.test import APITestCase

from arionBackend.models.event_type import EventType
from arionBackend.models.hierarchy import Hierarchy
from arionBackend.models.query import Query


class EventTypeTestCase(APITestCase):
	"""
	This class contains the tests for the event type API.
	"""

	@classmethod
	def setUpTestData(cls):
		"""
		This method sets up the test class with the required data.
		"""
		hierarchy = Hierarchy(name="TestHierarchy", json_representation="{}")
		hierarchy.save()
		event_type = EventType(name="asd", hierarchy=hierarchy)
		event_type.save()
		query = Query(
			hierarchy=hierarchy, query_string="INSERT INTO asd SELECT * FROM asd",
			output_event_type=event_type,
			eqmn_representation="{'output': {'name': 'asd', 'select': '*'}, 'input': {'single': 'asd'}}")
		query.save()
		query.inserting_event_types.add(event_type)
		query.save()

	def test_get_event_types_by_hierarchy_id_success(self):
		"""
		Tests if event types can be retrieved by hierarchy id.
		"""
		hierarchy = Hierarchy.objects.get(name="TestHierarchy")
		response = self.client.get('/api/event_type/esper/hierarchy/' + str(hierarchy.id), follow=True)
		json_response = json.loads(response.content.decode('utf-8'))
		self.assertEqual(type(json_response), list)
		event_type = json_response[0]
		self.assertEqual(event_type["name"], "asd")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_get_event_types_by_hierarchy_id_invalid_id(self):
		"""
		Tests if the event types cannot be retrieved, if the id is invalid.
		"""
		request = self.client.get('/api/event_type/esper/hierarchy/0', follow=True)
		self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

	def test_get_event_types_by_hierarchy_id_not_found(self):
		"""
		Tests if the event types cannot be retrieved, if there is no hierarchy with the id.
		"""
		hierarchy = Hierarchy.objects.get(name="TestHierarchy")
		request = self.client.get('/api/event_type/esper/hierarchy/' + str(hierarchy.id + 1), follow=True)
		self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

	def test_get_event_type_by_id(self):
		"""
		Tests if an event type can be retrieved by its id.
		"""
		event_type = EventType.objects.get(name="asd")
		response = self.client.get('/api/event_type/esper/' + str(event_type.id), follow=True)
		json_response = json.loads(response.content.decode('utf-8'))
		self.assertEqual(json_response["name"], "asd")
		self.assertEqual(type(json_response["feeding_queries"]), list)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_get_event_type_by_id_invalid_id(self):
		"""
		Tests if the event type cannot be retrieved, if the id is invalid.
		"""
		request = self.client.get('/api/event_type/esper/0', follow=True)
		self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

	def test_get_event_type_by_id_not_found(self):
		"""
		Tests if the event type cannot be retrieved, if the id does not exist.
		"""
		event_type = EventType.objects.get(name="asd")
		request = self.client.get('/api/event_type/esper/' + str(event_type.id + 1), follow=True)
		self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)
