class EventTypeRetriever(object):

	@staticmethod
	def find_inserting_event_type(output_query):
		return output_query["name"]

	@staticmethod
	def find_feeding_event_types(input_query):
		"""
		Finds all event types that are used as input streams to feed the event query.
		:param input_query: the input part of the event query representation.
		:return: yields event types that are found, must be caught in a list.
		"""
		for key, value in input_query.items():
			if key == "name":
				yield value
			elif isinstance(value, dict):
				for result in EventTypeRetriever.find_feeding_event_types(value):
					yield result
			elif isinstance(value, list):
				for dictionary in value:
					for result in EventTypeRetriever.find_feeding_event_types(dictionary):
						yield result
