"""
This module holds the test cases for the different views.
"""

from rest_framework import status
from rest_framework.test import APITestCase


class HierarchyTestCase(APITestCase):
    """
    This class contains the tests for the Hierarchy API.
    """

    @classmethod
    def setUpTestData(cls):
        """
        This method sets up the test class with the required data.
        """
        pass

    def test_get_all_hierarchies(self):
        """
        Tests if all hierarchies can be retrieved.
        """
        request = self.client.get('/api/hierarchy/esper', follow=True)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_hierarchy_by_id_success(self):
        """
        Tests if one hierarchy can be retrieved via id.
        """
        request = self.client.get('/api/hierarchy/esper/1', follow=True)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_hierarchy_by_id_invalid_id(self):
        """
        Tests if the hierarchy cannot be retrieved, if the id is invalid.
        :return: 
        """
        request = self.client.get('/api/hierarchy/esper/0', follow=True)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_hierarchy_success(self):
        """
        Tests if a hierarchy can be created via API call.
        """
        request = self.client.post(
            '/api/hierarchy/esper/create',
            follow=True,
            data={"name": "Test", "queries": ["S"]},
            format="json")
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
