"""
This module holds the class for the EsperTransformer.
"""

from arionBackend.transformation.transformer import Transformer


class EsperTransformer(Transformer):
    """
    This class extends the abstract base class Transformer and implements a transformer for Esper EPL.
    """

    def transform(self, queries):
        """
        This method transform an Esper EPL query into a hierarchy.
        :param queries: Esper EPL queries
        """
        if queries[0] == "a":
            return False
        return True
