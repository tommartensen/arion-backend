"""
This module holds the test cases for the different views.
"""

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient


class ViewsTestCase(TestCase):
    """
    This class tests the generic view.
    """
    c = APIClient()

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(email="asd@asd.asd", password='123456789', username="asd")

    def test_hello_not_authenticated(self):
        """The user is not authenticated, thus will not be allowed access."""
        request = self.c.get('/api/hello', follow=True)
        self.assertEqual(request.status_code, 401)

    def test_wrong_authentication(self):
        """The credentials are wrong, thus will not be allowed access."""
        self.c.login(username='asd', password='12345678')
        response = self.c.get('/api/hello', follow=True)
        self.assertEqual(response.status_code, 401)

    def test_hello_authenticated(self):
        """Positive test"""
        self.c.login(username='asd', password='123456789')
        response = self.c.get('/api/hello', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['greeting'], 'Hello')


class MoinTestCase(TestCase):
    """This class tests the moin API."""
    c = APIClient()

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(email="asd@asd.asd", password='123456789', username="asd")

    def test_hello_not_authenticated(self):
        """The user is not authenticated, thus will not be allowed access."""
        request = self.c.get('/api/moin', follow=True)
        self.assertEqual(request.status_code, 401)

    def test_wrong_authentication(self):
        """The credentials are wrong, thus will not be allowed access."""
        self.c.login(username='asd', password='12345678')
        response = self.c.get('/api/moin', follow=True)
        self.assertEqual(response.status_code, 401)

    def test_hello_authenticated(self):
        """Positive test"""
        self.c.login(username='asd', password='123456789')
        response = self.c.get('/api/moin', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['greeting'], 'Moin')
