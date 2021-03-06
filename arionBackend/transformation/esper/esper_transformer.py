"""
This module holds the class for the EsperTransformer.
"""
from json import dumps as json_dumps
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

	@staticmethod
	def generate_hierarchy(hierarchy):
		"""
		This methods generates the hierarchy represented as a directed graph and saves it in a given hierarchy instance.
		:param hierarchy: the hierarchy to generate the representation for.
		"""

		hierarchy_graph = {}
		event_types = EventType.objects.filter(hierarchy=hierarchy)

		for event_type in event_types:
			input_queries = Query.objects.filter(output_event_type=event_type).values("input_event_types")
			for input_query in input_queries:
				input_event_type_id = input_query["input_event_types"]
				if input_event_type_id not in hierarchy_graph:
					hierarchy_graph[input_event_type_id] = []
				if event_type.id not in hierarchy_graph[input_event_type_id]:
					hierarchy_graph[input_event_type_id].append(event_type.id)
		hierarchy.graph_representation = json_dumps(hierarchy_graph)
		hierarchy.save()

	@staticmethod
	def transform(name, queries):
		"""
		This method transform an Esper EPL query into a hierarchy.
		:param name: name of hierarchy
		:param queries: Esper EPL queries
		"""

		hierarchy = Hierarchy(name=name, graph_representation={})
		hierarchy.save()
		for query in queries:
			parsed_query = QueryParser.parse_query_to_eqmn(query)
			input_event_type_objects = []
			if parsed_query:
				output_event_type, created = EventType.objects.get_or_create(
					name=EventTypeRetriever.find_inserting_event_type(parsed_query["eqmn_representation"]["output"]),
					hierarchy=hierarchy)
				if parsed_query["eqmn_representation"]["input"]["type"] == "PATTERN":
					input_event_types = list(EventTypeRetriever.find_input_event_types_for_pattern(
						parsed_query["eqmn_representation"]["input"]["data"]))
				else:
					input_event_types = list(EventTypeRetriever.find_input_event_types(
						parsed_query["eqmn_representation"]["input"]))
				for input_event_type in input_event_types:
					event_type, created = EventType.objects.get_or_create(
						name=input_event_type, hierarchy=hierarchy)
					input_event_type_objects.append(event_type)
				query = Query(
					query_string=query, hierarchy=hierarchy,
					eqmn_representation=json_dumps(parsed_query["eqmn_representation"]),
					output_event_type=output_event_type)
				query.save()
				query.input_event_types.set(input_event_type_objects)
				query.save()
			else:
				hierarchy.delete()
				return False
		EsperTransformer.generate_hierarchy(hierarchy)
		return True
