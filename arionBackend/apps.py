"""
This module holds every app in the project.
"""

from django.apps import AppConfig


class arionBackendConfig(AppConfig):
    """
    This class sets the name of the Django project.
    """
    name = 'arionBackend'

    def ready(self):
        from arionBackend.signals import authentication
