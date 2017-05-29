"""
This module contains the abstract base class for the Transformer.
"""

from abc import ABCMeta, abstractmethod


class Transformer(metaclass=ABCMeta):
	"""
	This class is an abstract base class for transformers of type "event language" -> "hierarchy".
	"""

	@staticmethod
	@abstractmethod
	def transform(name, queries):
		"""
		This abstract method transforms the queries into the hierarchy.
		:param name: The name of the hierarchy.
		:param queries: The queries to put into a hierarchy.
		:return: boolean on success.
		"""
		pass
