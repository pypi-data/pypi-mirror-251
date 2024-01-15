import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod

from uml_interpreter.deserializer.errors import InvalidXMLError
from uml_interpreter.model.model import UMLModel
from uml_interpreter.source.source import XMLSource


class Deserializer(ABC):
    """
    Deserializer abstract base class.
    """

    @abstractmethod
    def read_model(self) -> UMLModel:
        """
        Function responsible for reading the model's source

        Returns:
            UML model read from the source
        """
        pass

    @property
    @abstractmethod
    def source(self):
        """
        Model source representation
        """
        pass

    @source.setter
    @abstractmethod
    def source(self, source):
        pass


class XMLDeserializer(Deserializer):
    """
    Deserializer implementation, that reads XML sources.
    """

    def read_model(self) -> UMLModel:
        """
        Function responsible for reading the model's source in XML

        Raises:
            InvalidXMLError: Exception thrown in case of an error in XML source.

        Returns:
            UML model read from the XML
        """
        try:
            tree: ET.ElementTree = self.source.read_tree()
            return self._parse_model(tree)
        except ET.ParseError as exc:
            raise InvalidXMLError(exc.msg)

    @property
    def source(self) -> XMLSource:
        """
        Model XML source representation
        """
        return self._source

    @source.setter
    def source(self, source: XMLSource) -> None:
        self._source = source

    @abstractmethod
    def _parse_model(self, tree: ET.ElementTree) -> UMLModel:
        pass
