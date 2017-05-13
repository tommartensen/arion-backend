from django.db import models


class Hierarchy(models.Model):
    name = models.TextField()
    json_representation = models.TextField()


class Query(models.Model):
    hierarchy = models.ManyToManyField(Hierarchy)
    query_string = models.TextField()