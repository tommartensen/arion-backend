"""
This module holds the class for the EsperTransformer.
"""
from arionBackend.models.hierarchy import Hierarchy
from arionBackend.models.query import Query
from arionBackend.transformation.esper.esper_query import QueryParser
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

		hierarchy = Hierarchy(name=name, json_representation={})
		hierarchy.save()
		query_objects = []
		for query in queries:
			parsed_query = QueryParser.parse_query_to_eqmn(query)
			if parsed_query:
				query_objects.append(Query(
					query_string=query, hierarchy=hierarchy, eqmn_representation=parsed_query["eqmn_representation"]))
			else:
				hierarchy.delete()
				return False

		for query in query_objects:
			query.save()
		return True
