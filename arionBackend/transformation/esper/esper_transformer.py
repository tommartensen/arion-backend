"""
This module holds the class for the EsperTransformer.
"""
from arionBackend.models.event_type import EventType
from arionBackend.models.hierarchy import Hierarchy
from arionBackend.models.query import Query
from arionBackend.transformation.esper.esper_query import QueryParser
from arionBackend.transformation.esper.event_type_retriever import EventTypeRetriever
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
		for query in queries:
			parsed_query = QueryParser.parse_query_to_eqmn(query)
			feeding_event_type_objects = []
			if parsed_query:
				output_event_type, created = EventType.objects.get_or_create(
					name=EventTypeRetriever.find_inserting_event_type(parsed_query["eqmn_representation"]["output"]),
					hierarchy=hierarchy)
				feeding_event_types = list(EventTypeRetriever.find_feeding_event_types(
					parsed_query["eqmn_representation"]["input"]))
				for feeding_event_type in feeding_event_types:
					event_type, created = EventType.objects.get_or_create(
						name=feeding_event_type, hierarchy=hierarchy)
					feeding_event_type_objects.append(event_type)
				query = Query(
					query_string=query, hierarchy=hierarchy, eqmn_representation=parsed_query["eqmn_representation"],
					output_event_type=output_event_type)
				query.save()
				query.inserting_event_types.set(feeding_event_type_objects)
				query.save()
			else:
				hierarchy.delete()
				return False
		return True
