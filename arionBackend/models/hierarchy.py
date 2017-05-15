from django.db import models


class Hierarchy(models.Model):
    """
    This class represents a real-world hierarchy of event types.
    """

    name = models.TextField()
    json_representation = models.TextField()
