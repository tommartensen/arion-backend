"""
This module holds the test cases for the hierarchy API module.
"""
import json

from rest_framework import status
from rest_framework.test import APITestCase

from arionBackend.models.hierarchy import Hierarchy


class HierarchyTestCase(APITestCase):
	"""
	This class contains the tests for the Hierarchy API.
	"""

	@classmethod
	def setUpTestData(cls):
		"""
		This method sets up the test class with the required data.
		"""
		Hierarchy(name="TestHierarchy", json_representation="{}").save()

	def test_get_all_hierarchies(self):
		"""
		Tests if all hierarchies can be retrieved.
		"""
		response = self.client.get('/api/hierarchy/esper', follow=True)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		json_response = json.loads(response.content.decode('utf-8'))
		self.assertEqual(json_response[0]["name"], "TestHierarchy")
		self.assertEqual(type(json_response[0]["id"]), int)

	def test_get_hierarchy_by_id_success(self):
		"""
		Tests if one hierarchy can be retrieved via id.
		"""
		hierarchy = Hierarchy.objects.get(name="TestHierarchy")
		response = self.client.get('/api/hierarchy/esper/' + str(hierarchy.id), follow=True)
		json_response = json.loads(response.content.decode('utf-8'))
		self.assertEqual(json_response["name"], "TestHierarchy")
		self.assertEqual(type(json_response["id"]), int)
		self.assertEqual(type(json_response["hierarchy"]), dict)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_get_hierarchy_by_id_invalid_id(self):
		"""
		Tests if the hierarchy cannot be retrieved, if the id is invalid.
		"""
		request = self.client.get('/api/hierarchy/esper/0', follow=True)
		self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

	def test_get_hierarchy_by_id_not_found(self):
		"""
		Tests if the hierarchy cannot be retrieved, if there is no hierarchy with the id.
		"""
		hierarchy = Hierarchy.objects.get(name="TestHierarchy")
		request = self.client.get('/api/hierarchy/esper/' + str(hierarchy.id + 1), follow=True)
		self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

	def test_create_hierarchy_success(self):
		"""
		Tests if a hierarchy can be created via API call.
		"""
		request = self.client.post(
			'/api/hierarchy/esper/create',
			follow=True,
			data={"name": "Test", "queries": ["INSERT INTO asd SELECT asd FROM asd", "INSERT INTO asd SELECT asd FROM asd WHERE 1=1"]},
			format="json")
		self.assertEqual(request.status_code, status.HTTP_201_CREATED)

	def test_create_hierarchy_bad_request(self):
		"""
		Tests if a hierarchy cannot be created, if one of the parameters is missing.
		"""
		response = self.client.post(
			'/api/hierarchy/esper/create',
			follow=True,
			data={"queries": ["SELECT * FROM asd"]},
			format="json")
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

		response = self.client.post(
			'/api/hierarchy/esper/create',
			follow=True,
			data={"name": "Test"},
			format="json")
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

		response = self.client.post(
			'/api/hierarchy/esper/create',
			follow=True,
			data={"name": "Test", "queries": []},
			format="json")
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

		response = self.client.post(
			'/api/hierarchy/esper/create',
			follow=True,
			data={"name": "Test", "queries": [""]},
			format="json")
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

		response = self.client.post(
			'/api/hierarchy/esper/create',
			follow=True,
			data={"name": "Test", "queries": ["SELECT * FROM asd"]},
			format="json")
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
