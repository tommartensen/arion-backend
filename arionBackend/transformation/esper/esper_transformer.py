"""
This module holds the class for the EsperTransformer.
"""
from arionBackend.models.hierarchy import Hierarchy
from arionBackend.models.query import Query
from arionBackend.transformation.transformer import Transformer
from parse import *
from re import compile as regex_compile

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
			eqmn_representation = EsperTransformer.parse_query_to_eqmn(query)
			if eqmn_representation:
				query_objects.append(
					Query(query_string=query, hierarchy=hierarchy, eqmn_representation=eqmn_representation))
			else:
				hierarchy.delete()
				return False

		for query in query_objects:
			query.save()
		return True

	@staticmethod
	def parse_optional_condition(tokenized_query):
		updated_tokenized_query = tokenized_query
		condition = regex_compile("(WHERE|Where|where)").split(tokenized_query["input"])
		updated_tokenized_query["input"] = condition[0]
		if len(condition) > 1:
			updated_tokenized_query["condition"] = condition[2]
		print(updated_tokenized_query)
		return updated_tokenized_query


	@staticmethod
	def parse_query_to_eqmn(query):
		try:
			tokenized_query = parse("insert into {output[name]} select {output[select]} from {input}", query).named
			EsperTransformer.parse_optional_condition(tokenized_query)
			return tokenized_query
		except AttributeError:
			return False
