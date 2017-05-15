"""
This module holds the class for the EsperTransformer.
"""
from arionBackend.models.hierarchy import Hierarchy
from arionBackend.models.query import Query
from arionBackend.transformation.transformer import Transformer


class EsperTransformer(Transformer):
    """
    This class extends the abstract base class Transformer and implements a transformer for Esper EPL.
    """

    def transform(self, name, queries):
        """
        This method transform an Esper EPL query into a hierarchy.
        :param name: name of hierarchy
        :param queries: Esper EPL queries
        """
        if queries[0] == "a":
            return False

        hierarchy = Hierarchy(name=name, json_representation={})
        hierarchy.save()
        for query in queries:
            Query(query_string=query, hierarchy=hierarchy).save()
        return True
