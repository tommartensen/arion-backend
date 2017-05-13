"""
This module holds the test cases for the different views.
"""

from rest_framework import status
from rest_framework.test import APITestCase


class ViewsTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def test_get_all_hierarchies(self):
        request = self.client.get('/api/hierarchy/esper', follow=True)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_hierarchy_by_id_success(self):
        request = self.client.get('/api/hierarchy/esper/1', follow=True)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_hierarchy_by_id_invalid_id(self):
        request = self.client.get('/api/hierarchy/esper/0', follow=True)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_hierarchy_success(self):
        request = self.client.post(
            '/api/hierarchy/esper/create',
            follow=True,
            data={"name": "Test", "queries": ["S"]},
            format="json")
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
