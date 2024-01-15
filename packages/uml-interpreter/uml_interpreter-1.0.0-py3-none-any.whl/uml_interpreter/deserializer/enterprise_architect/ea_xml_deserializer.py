import logging
import uuid
import xml.etree.ElementTree as ET
from abc import ABC
from collections import defaultdict, deque
from functools import wraps
from typing import Any, Optional, Callable

from uml_interpreter.deserializer.abstract import XMLDeserializer
from uml_interpreter.deserializer.enterprise_architect.constants import (
    EA_ATTRIBUTES,
    DIAGRAMS_TYPES,
    EA_TAGS,
)
from uml_interpreter.deserializer.enterprise_architect.uml_object_builders.uml_class_builder import (
    EAXMLClassBuilder,
)
from uml_interpreter.deserializer.enterprise_architect.uml_object_builders.uml_sequence_builder import (
    EAXMLSequenceBuilder,
)
from uml_interpreter.deserializer.errors import (
    ERROR_MESS,
    TAGS_ERRORS,
    ErrorType,
    InvalidXMLError,
    IdMismatchException,
)
from uml_interpreter.model.abstract import UMLObject
from uml_interpreter.model.diagrams.abstract import UMLDiagram
from uml_interpreter.model.diagrams.class_diagram import (
    ClassDiagram,
    ClassDiagramElement,
)
from uml_interpreter.model.diagrams.sequence_diagram import SequenceDiagram
from uml_interpreter.model.model import UMLModel
from uml_interpreter.source.source import FileSource, StringSource, XMLSource


def evaluate_elements_afterwards(blocking: bool = False) -> Callable:
    """
    Decorator that evaluates all elements from the evaluation queue.

    Args:
        blocking (bool, optional): if set to True, it raises IdMismatchException when ID present as a key in evaluation queue is not present in the ID to instance mapping.
    """

    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        def inner(self, *args, **kwargs) -> Any:
            returned_value = func(self, *args, **kwargs)
            self._evaluate_elements(blocking)
            return returned_value

        return inner

    return wrapper


class DelayedCaller(ABC):
    def __init__(self) -> None:
        self._id_to_instance_mapping: dict[str, Any] = dict()
        self._id_to_evaluation_queue: dict[str, deque[Callable]] = defaultdict(deque)
        """
        Queue of functions to be called when Instance of the Object with given ID is available.
        The Instance has to be given as an argument to function call.
        """

    def _evaluate_elements(self, blocking: bool = False) -> None:
        """
        Function that evaluates all elements from the evaluation queue.
        :arg blocking - if set to True, it raises IdMismatchException when ID present as key in the evaluation
            queue is not present in the ID to instance mapping. Used for partial evaluation.
        """
        for element_id, evaluation_queue in self._id_to_evaluation_queue.items():
            try:
                element_instance = self._id_to_instance_mapping[element_id]
            except KeyError as ex:
                message = f"Couldn't associate given referred object id: {element_id} with any known instance."
                if blocking:
                    raise IdMismatchException(message) from ex
                else:
                    logging.log(logging.INFO, message)
                    continue

            while evaluation_queue:
                function_to_call = evaluation_queue.popleft()
                function_to_call(element_instance)


class EAXMLDeserializer(XMLDeserializer, DelayedCaller):
    """
    Deserializer implementation for Enterprise Architect modelling tool.
    """
    IGNORED_XML_ELEMENTS = ["uml:Package"]

    def __init__(self, source: XMLSource) -> None:
        """
        EAXMLDeserializer initializer

        Args:
            source (XMLSource): XML model source.
        """
        self._source: XMLSource = source
        super().__init__()

        # TODO: Extract lazy evaluation to separate base class
        self.class_builder = EAXMLClassBuilder(
            self._id_to_evaluation_queue, self._parse_id
        )
        self.sequence_builder = EAXMLSequenceBuilder(
            self._id_to_evaluation_queue, self._id_to_instance_mapping, self._parse_id
        )

    @classmethod
    def from_string(cls, string):
        return cls(StringSource(string))

    @classmethod
    def from_path(cls, path):
        return cls(FileSource(path))

    def _parse_id(self, raw_id: str) -> uuid.UUID:
        slicing_index = None
        UUID_N_CHARS = 32
        pad_char = "a"

        if raw_id.startswith("EAID_") or raw_id.startswith("EAPK_"):
            slicing_index = 5

        if raw_id.startswith("EAID_AT"):
            pad_char = "1"
            slicing_index = 7

        if raw_id.startswith("EAID_LL"):
            pad_char = "2"
            slicing_index = 7

        if raw_id.startswith("EAID_FR"):
            pad_char = "3"
            slicing_index = 7

        if raw_id.startswith("EAID_CB"):
            pad_char = "4"
            slicing_index = 7

        if raw_id.startswith("EAID_src") or raw_id.startswith("EAID_dst"):
            slicing_index = 8

        if slicing_index is not None:
            str_uuid = raw_id[slicing_index:].lower().replace("_", "")
            str_uuid = (UUID_N_CHARS - len(str_uuid)) * pad_char + str_uuid
            return uuid.UUID(str_uuid)

        raise InvalidXMLError(ERROR_MESS[ErrorType.UNKNOWN_ID_FORMAT])

    def _parse_model(self, tree: ET.ElementTree) -> UMLModel:
        root = self._get_root(tree)

        model_node = self._get_mandatory_node(root, "model")

        # TODO: iteration for each builder instead
        elems: list[UMLObject] = self._parse_elems(model_node)

        diagrams: list[UMLDiagram] = self._parse_diagrams(
            root,
            [elem for elem in elems if isinstance(elem, ClassDiagramElement)],
            model_node,
        )

        return UMLModel(
            name=model_node.get("name", "New Model"),
            diagrams=diagrams,
            filename=self.source.path if isinstance(self.source, FileSource) else None,
        )

    def _get_root(self, tree: ET.ElementTree) -> ET.Element:
        root = tree.getroot()
        if not isinstance(root, ET.Element):
            raise InvalidXMLError(ERROR_MESS[ErrorType.ROOT_ERROR])
        return root

    def _get_mandatory_node(self, root: ET.Element, tag: str) -> ET.Element:
        """
        Retrieves the node of XML document containing specified tag.
        Its absence raises InvalidXMLError.
        """
        if (node := self._get_node_by_tag(root, tag)) is None:
            raise InvalidXMLError(TAGS_ERRORS[tag])
        return node

    def _get_node_by_tag(self, root: ET.Element, tag: str) -> Optional[ET.Element]:
        return root.find(EA_TAGS[tag])

    @evaluate_elements_afterwards()
    def _parse_sequence(
        self, model_node: ET.Element, diag_name: str | None
    ) -> SequenceDiagram:
        """
        Functions dependent on the initialization of the element with id given as the key of the dictionary.
        """
        return self.sequence_builder._parse_diagram(model_node, diag_name)

    @evaluate_elements_afterwards()
    def _parse_elems(self, model_node: ET.Element) -> list[UMLObject]:
        """
        Functions dependent on the initialization of the element with id given as the key of the dictionary.
        """
        elements_info = [
            element_info
            for element in model_node.iter(EA_TAGS["elem"])
            if (element_info := self._parse_elem(element)) is not None
        ]
        return elements_info

    def _parse_elem(self, elem: ET.Element) -> Optional[UMLObject]:
        if not self._is_supported_element(elem):
            return None

        if elem_id := elem.attrib.get(EA_ATTRIBUTES["elem_id"]):
            uuid_id = self._parse_id(elem_id)

            if parsed_elem := self.class_builder._try_build_class_or_iface(elem):
                parsed_elem.id = uuid_id
                self._id_to_instance_mapping[str(uuid_id)] = parsed_elem

            elif parsed_elem := self.class_builder._try_build_relationship(elem):
                parsed_elem.id = uuid_id
                self._id_to_instance_mapping[str(uuid_id)] = parsed_elem

            # TODO
            # elif parsed_elem := self.sequence_builder._try_build_sequence_element(elem):
            #     parsed_elem.id = elem_id
            #     self._id_to_instance_mapping[elem_id] = parsed_elem

            else:
                logging.log(
                    logging.INFO,
                    """Retrieved object is unknown - couldn't build class or
                    interface or their relationship based on the object data.""",
                )
                return None

            return parsed_elem

        else:
            raise InvalidXMLError(ERROR_MESS[ErrorType.MODEL_ID_MISSING])

    def _parse_diagrams(
        self, root: ET.Element, elems: list[UMLObject], model_node: ET.Element
    ) -> list[UMLDiagram]:
        diagrams: list[UMLDiagram] = []

        ext = self._get_mandatory_node(root, "ext")
        diags = self._get_mandatory_node(ext, "diags")

        self._populate_diagrams(elems, diagrams, diags, root, model_node)

        return diagrams

    def _populate_diagrams(
        self,
        elems: list[UMLObject],
        diagrams: list[UMLDiagram],
        diags: ET.Element,
        root: ET.Element,
        model_node: ET.Element,
    ) -> None:
        for diag in diags.iter(EA_TAGS["diag"]):
            diag_properties = self._get_mandatory_node(diag, "diag_propty")
            diag_type = diag_properties.attrib.get(EA_ATTRIBUTES["property_type"])
            diag_name = diag_properties.attrib.get(EA_ATTRIBUTES["elem_name"])

            if not diag_type:
                return

            if DIAGRAMS_TYPES.get(diag_type) == ClassDiagram:
                if (
                    filled_diag := self._get_filled_class_diag(diag, elems, diag_name)
                ) is not None:
                    diagrams.append(filled_diag)
            elif DIAGRAMS_TYPES.get(diag_type) == SequenceDiagram:
                if (
                    seq_diag := self._parse_sequence(model_node, diag_name)
                ) is not None:
                    diagrams.append(seq_diag)

    def _get_filled_class_diag(
        self, diag: ET.Element, elems: list[UMLObject], diag_name: str | None
    ) -> UMLDiagram:

        diag_elems = diag.find(EA_TAGS["diag_elems"])
        if diag_elems is None or len(diag_elems) == 0:
            return UMLDiagram(diag_name)

        elem_ids: list[str] = [
            diag_elem.attrib[EA_ATTRIBUTES["diag_elem_id"]]
            for diag_elem in diag_elems.iter(EA_TAGS["diag_elem"])
        ]

        elem_uuids: list[uuid.UUID] = [self._parse_id(id) for id in elem_ids]

        uml_elems: list[UMLObject] = [elem for elem in elems if elem.id in elem_uuids]

        if all(isinstance(elem, ClassDiagramElement) for elem in uml_elems):
            return ClassDiagram(diag_name, uml_elems)
        else:
            raise InvalidXMLError(ERROR_MESS[ErrorType.MIXED_ELEMS])

    def _is_supported_element(self, elem: ET.Element) -> bool:
        is_supported_element = (
            elem.attrib[EA_ATTRIBUTES["elem_type"]] not in self.IGNORED_XML_ELEMENTS
        )
        return is_supported_element
