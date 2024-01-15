import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


class Source(ABC):
    """
    Represents UML model source
    """

    @abstractmethod
    def read_tree(self):
        """
        Abstract method used to read the source
        """
        pass


class XMLSource(Source):
    """
    Represents UML model XML source
    """

    @abstractmethod
    def read_tree(self) -> ET.ElementTree:
        """
        Abstract method used to read the source

        Returns:
            XML file elements tree
        """
        pass
