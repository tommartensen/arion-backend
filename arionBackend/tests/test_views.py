"""
This module holds the test cases for the different views.
"""

from django.test import TestCase
from rest_framework.test import APIClient


class ViewsTestCase(TestCase):
    """
    This class tests the generic view.
    """
    c = APIClient()

    @classmethod
    def setUpTestData(cls):
        pass

    def test_get_all_hierarchies(self):
        """The user is not authenticated, thus will not be allowed access."""
        request = self.c.get('/api/hierarchy', follow=True)
        self.assertEqual(request.status_code, 200)
