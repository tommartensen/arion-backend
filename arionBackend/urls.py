"""
This module holds the url patterns for the project.
"""

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import obtain_auth_token

from arionBackend.api import greetings

urlpatterns = [
    url(r'^api/hello/$', greetings.hello, name="hello"),
    url(r'^api/moin/$', greetings.Moin.as_view(), name="moin"),
    url(r'^api/obtain-auth-token/$', csrf_exempt(obtain_auth_token))
]
