from abc import ABCMeta, abstractmethod


class Transformer(metaclass=ABCMeta):
    """
    This class is an abstract base class for transformers of type "event language" -> "hierarchy".
    """

    @abstractmethod
    def transform(self, queries):
        """
        This abstract method transforms the queries into the hierarchy.
        :param queries: The queries to put into a hierarchy. 
        :return: boolean on success.
        """
        pass
