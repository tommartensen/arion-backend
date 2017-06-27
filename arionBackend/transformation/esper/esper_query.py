"""
This module holds the class for the parser for ESPER EPL queries.
"""
from parse import *
from re import compile as regex_compile


class QueryParser(object):
	"""
	This class parses an event query.
	"""

	@staticmethod
	def parse_query_to_eqmn(query):
		"""
		This method parses a query into a eqmn model.
		:param query: the query to parse
		:return: eqmn model in json representation or false if error
		"""
		if query[len(query) - 1] == ";":
			query = query[:len(query) - 1]
		try:
			tokenized_query = parse("insert into {output[name]} select {output[select]} from {input}", query).named
			tokenized_query = QueryParser.parse_optional_condition(tokenized_query)
			tokenized_query["input"] = QueryParser.parse_input_clause(tokenized_query["input"])
			return {"eqmn_representation": tokenized_query}
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
		if "pattern" not in updated_tokenized_query["input"].lower():
			condition = regex_compile("(WHERE|Where|where)").split(tokenized_query["input"])
			updated_tokenized_query["input"] = condition[0].strip()
			if len(condition) > 1:
				updated_tokenized_query["condition"] = QueryParser.parse_timer_window(condition[2].strip())
		return updated_tokenized_query

	@staticmethod
	def parse_timer_window(pattern):
		"""
		Finds a timer window (timer:interval, timer:within, ...) in the pattern
		:param pattern: the pattern to search in
		:return: updated pattern
		"""
		index = pattern.find("timer")
		if index > -1:
			tokenized_timer = parse("timer:{timer[type]}({timer[value]}) ", pattern[index:]).named
			return tokenized_timer
		return pattern

	@staticmethod
	def find_selection(event_type):
		"""
		Finds a selection clause (from the std namespace) and updates the event type.
		:param event_type: the event type to inspect
		:return: updated event type
		"""
		try:
			tokenized_event_type = parse("{name}.std:{selection}", event_type).named
			return tokenized_event_type
		except AttributeError:
			return {"name": event_type}

	@staticmethod
	def find_alias(event_type):
		"""
		Finds an alias clause ("as" keyword) and updates the event type.
		:param event_type: the event type to inspect
		:return: updated event type
		"""
		if " as " in event_type:
			tokenized_with_alias = event_type.split(" as ")
			return {"event": tokenized_with_alias[0], "alias": tokenized_with_alias[1]}
		else:
			return {"event": event_type}

	@staticmethod
	def find_window(event_type):
		"""
		Finds a window (from the window namespace) and updates the event type.
		:param event_type: the event type to inspect
		:return: updated event type
		"""
		try:
			tokenized_event_type = parse("{name}.win:{type}", event_type["event"]["name"]).named
			event_type["event"]["name"] = tokenized_event_type["name"]
			if tokenized_event_type["type"] != "keepall()":
				tokenized_type = parse("{type}({size})", tokenized_event_type["type"]).named
				tokenized_with_window = {
					"window": {"event": event_type["event"]},
					"type": tokenized_type["type"],
					"size": tokenized_type["size"]
				}
			else:
				tokenized_with_window = {"window": {"event": event_type["event"]}, "type": tokenized_event_type["type"]}
			if "alias" in event_type:
				tokenized_with_window["alias"] = event_type["alias"]
			return tokenized_with_window
		except AttributeError:
			return event_type

	@staticmethod
	def tokenize_input_stream(input_stream):
		"""
		Tokenizes a given input stream, looks for aliases, selections and windows.
		:param input_stream: the input stream to inspect
		:return: the tokenized input stream
		"""
		tokenized_input = QueryParser.find_alias(input_stream)
		tokenized_input["event"] = QueryParser.find_selection(tokenized_input["event"])
		return QueryParser.find_window(tokenized_input)

	@staticmethod
	def parse_input_clause(input_clause):
		"""
		Parses the input clause: Single Event Types, Joins and Patterns are possible.
		:param input_clause: the input clause to parse
		:return: the updated input clause
		"""
		updated_input_clause = {"data": {}}
		if "," in input_clause:
			# if a comma is in the input clause, multiple event streams are joined as input
			stripped_event_streams = [event_stream.strip() for event_stream in input_clause.split(',')]
			updated_input_clause["data"] = \
				[QueryParser.tokenize_input_stream(event_stream) for event_stream in stripped_event_streams]
			input_type = "JOIN"
		else:
			try:
				tokenized_pattern = parse("pattern {pattern}", input_clause).named
				updated_input_clause["data"] = \
					QueryParser.parse_pattern(tokenized_pattern["pattern"].strip())
				input_type = "PATTERN"
			# if no error is thrown, the pattern clause was detected
			except AttributeError:
				# input must be single event type
				updated_input_clause["data"] = input_clause.strip()
				updated_input_clause["data"] = \
					QueryParser.tokenize_input_stream(updated_input_clause["data"])
				input_type = "SINGLE"
		updated_input_clause["type"] = input_type
		return updated_input_clause

	@staticmethod
	def parse_pattern(pattern):
		"""
		Parses the pattern from the input clause.
		:param pattern: the pattern to parse
		:return: eqmn representation of the pattern
		"""
		pattern = pattern.strip("[").strip("]")
		# TODO(tommartensen): Implement pattern parsing (this is not necessary for the prototypical implementation)
		return pattern
