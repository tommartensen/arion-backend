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
	def parse_query_to_eqmn(query):
		"""
		This method parses a query into a eqmn model.
		:param query: the query to parse
		:return: eqmn model in json representation or false if error
		"""
		try:
			tokenized_query = parse("insert into {output[name]} select {output[select]} from {input}", query).named
			tokenized_query = EsperTransformer.parse_optional_condition(tokenized_query)
			tokenized_query["input"] = EsperTransformer.parse_input_clause(tokenized_query["input"])
			return tokenized_query
		except AttributeError:
			return False

	@staticmethod
	def parse_optional_condition(tokenized_query):
		"""
		Looks for a "where" clause in the input clause.
		:param tokenized_query: the pre-parsed query
		:return: updated parsed query
		"""
		updated_tokenized_query = tokenized_query
		condition = regex_compile("(WHERE|Where|where)").split(tokenized_query["input"])
		updated_tokenized_query["input"] = condition[0].strip()
		if len(condition) > 1:
			updated_tokenized_query["condition"] = condition[2].strip()
		return updated_tokenized_query

	@staticmethod
	def find_selection(event_type):
		try:
			tokenized_event_type = parse("{name}.std:{selection}", event_type).named
			return tokenized_event_type
		except AttributeError:
			return {"name": event_type}

	@staticmethod
	def find_alias(event_type):
		if " as " in event_type:
			tokenized_with_alias = event_type.split(" as ")
			return {"event": tokenized_with_alias[0], "alias": tokenized_with_alias[1]}
		else:
			return {"event": event_type}

	@staticmethod
	def find_window(event_type):
		try:
			tokenized_event_type = parse("{name}.win:{type}", event_type["event"]["name"]).named
			event_type["event"]["name"] = tokenized_event_type["name"]
			tokenized_with_window = {"window": {"event": event_type["event"]}, "type": tokenized_event_type["type"]}
			if "alias" in event_type:
				tokenized_with_window["alias"] = event_type["alias"]
			return tokenized_with_window
		except AttributeError:
			return event_type

	@staticmethod
	def tokenize_input_stream(input_stream):
		tokenized_input = EsperTransformer.find_alias(input_stream)
		tokenized_input["event"] = EsperTransformer.find_selection(tokenized_input["event"])
		return EsperTransformer.find_window(tokenized_input)

	@staticmethod
	def parse_input_clause(input_clause):
		"""
		Parses the input clause: Single Event Types, Joins and Patterns are possible.
		:param input_clause: the input clause to parse
		:return: the updated input clause
		"""
		updated_input_clause = {"input": {}}
		if "," in input_clause:
			# if a comma is in the input clause, multiple event streams are joined as input
			stripped_event_streams = [event_stream.strip() for event_stream in input_clause.split(',')]
			updated_input_clause["input"]["data"] = \
				[EsperTransformer.tokenize_input_stream(event_stream) for event_stream in stripped_event_streams]
			input_type = "JOIN"
		else:
			try:
				tokenized_pattern = parse("pattern {pattern}", input_clause).named
				updated_input_clause["input"]["data"] = \
					EsperTransformer.parse_pattern(tokenized_pattern["pattern"].strip())
				input_type = "PATTERN"
			# if no error is thrown, the pattern clause was detected
			except AttributeError:
				# input must be single event type
				updated_input_clause["input"]["data"] = input_clause.strip()
				updated_input_clause["input"]["data"] = \
					EsperTransformer.tokenize_input_stream(updated_input_clause["input"]["data"])
				input_type = "SINGLE"
		updated_input_clause["input"]["type"] = input_type
		return updated_input_clause

	@staticmethod
	def parse_pattern(pattern):
		"""
		Parses the pattern from the input clause.
		:param pattern: the pattern to parse
		:return: eqmn representation of the pattern
		"""
		return pattern
