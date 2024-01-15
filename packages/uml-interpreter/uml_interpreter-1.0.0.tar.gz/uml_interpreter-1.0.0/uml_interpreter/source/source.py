import xml.etree.ElementTree as ET

from uml_interpreter.source.abstract import XMLSource


class FileSource(XMLSource):
    """
    Represents UML model XML file source
    """

    def __init__(self, path: str) -> None:
        """
        FileSource initializer.

        Args:
            path (str): Path under which XML file is located
        """
        self.path = path

    def read_tree(self) -> ET.ElementTree:
        """
        Method used to read the file source

        Returns:
            XML file elements tree
        """
        return ET.parse(self.path)


class StringSource(XMLSource):
    """
    Represents UML model XML string source
    """

    def __init__(self, xmlstring: str) -> None:
        """
        StringSource initializer.

        Args:
            xmlstring (str): String constant source
        """
        self.xmlstring = xmlstring

    def read_tree(self) -> ET.ElementTree:
        """
        Method used to read the source

        Returns:
            XML elements tree
        """
        return ET.ElementTree(ET.fromstring(self.xmlstring))
