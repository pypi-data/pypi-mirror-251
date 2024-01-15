from uuid import UUID
import xml.etree.ElementTree as ET
from collections import deque
from typing import Optional, Callable

from uml_interpreter.deserializer.enterprise_architect.constants import (
    CLASS_IFACE_MAPPING,
    CLASS_REL_MAPPING_TYPE,
    CLASS_RELATIONSHIPS_TYPES,
    EA_ATTRIBUTES,
    EA_ATTR_MAPPING,
    EA_TAGS,
    EA_INF,
)
from uml_interpreter.deserializer.enterprise_architect.utils import (
    SourceDestinationPair,
    SetRelationshipSource,
    SetRelationshipTarget,
)
from uml_interpreter.deserializer.errors import (
    ERROR_MESS,
    TAGS_ERRORS,
    ErrorType,
    InvalidXMLError,
)
from uml_interpreter.model.diagrams.class_diagram import (
    ClassDiagramAttribute,
    ClassDiagramElement,
    ClassDiagramMethod,
    ClassDiagramMethodParameter,
    ClassRelationship,
    RelationshipSide,
)


class EAXMLClassBuilder:
    def __init__(
        self, id_to_evaluation_queue: dict[str, deque[Callable]], _parse_id: Callable[[str], UUID]
    ) -> None:
        """
        Requires reference to the shared dictionary of evaluation queues.
        """
        self._id_to_evaluation_queue: dict[
            str, deque[Callable]
        ] = id_to_evaluation_queue
        self._parse_id = _parse_id

    def _try_build_class_or_iface(
        self, elem: ET.Element
    ) -> Optional[ClassDiagramElement]:
        if ElemClass := CLASS_IFACE_MAPPING.get(
            elem.attrib[EA_ATTRIBUTES["elem_type"]]
        ):
            curr_elem = ElemClass(elem.attrib[EA_ATTRIBUTES["elem_name"]])

            attrs: list[ClassDiagramAttribute] = self._build_attributes(elem)
            meths: list[ClassDiagramMethod] = self._build_methods(elem)

            curr_elem.attributes = attrs
            curr_elem.methods = meths
            return curr_elem

        return None

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

    def _build_attributes(self, elem: ET.Element) -> list[ClassDiagramAttribute]:
        attrs: list[ClassDiagramAttribute] = []
        for attr in elem.iter(EA_TAGS["elem_attr"]):
            name: str = attr.attrib[EA_ATTRIBUTES["elem_attr_name"]]
            if not (
                type_name := EA_ATTR_MAPPING.get(
                    self._get_mandatory_node(attr, "elem_attr_type").attrib[
                        EA_ATTRIBUTES["elem_attr_type"]
                    ]
                )
            ):
                type_name = ""

            if (visibility := attr.attrib.get(EA_ATTRIBUTES["visibility"])) is None:
                visibility = "private"
            is_private = visibility == "private"

            attrs.append(ClassDiagramAttribute(name, type_name, private=is_private))
        return attrs

    def _build_methods(self, elem: ET.Element) -> list[ClassDiagramMethod]:
        meths: list[ClassDiagramMethod] = []
        for meth in elem.iter(EA_TAGS["elem_meth"]):
            if (name := meth.attrib.get(EA_ATTRIBUTES["elem_meth_name"])) is None:
                name = ""

            if (visibility := meth.attrib.get(EA_ATTRIBUTES["visibility"])) is None:
                visibility = "private"
            is_private = visibility == "private"

            ret_type: Optional[str] = ""
            params: list[ClassDiagramMethodParameter] = []
            for param in meth.iter(EA_TAGS["elem_meth_param"]):
                if (
                    param_name := param.attrib.get(
                        EA_ATTRIBUTES["elem_meth_param_name"]
                    )
                ) == "return":
                    if not (
                        ret_type := EA_ATTR_MAPPING.get(
                            param.attrib[EA_ATTRIBUTES["elem_meth_ret_type"]]
                        )
                    ):
                        ret_type = ""

                else:
                    if not (
                        type_name := EA_ATTR_MAPPING.get(
                            self._get_mandatory_node(
                                param, "elem_meth_param_type"
                            ).attrib[EA_ATTRIBUTES["elem_meth_param_type"]]
                        )
                    ):
                        type_name = ""

                    params.append(ClassDiagramMethodParameter(param_name, type_name))

            meths.append(ClassDiagramMethod(name, ret_type, is_private, params))
        return meths

    def _create_relation_source_side(self, end: ET.Element) -> RelationshipSide:
        source_side = RelationshipSide()

        low = "inf"
        high = "inf"
        for src_vals in end.findall(EA_TAGS["end_low"]):
            src_low = src_vals.attrib[EA_ATTRIBUTES["end_low_type"]]
            if src_low == EA_INF:
                low = "inf"
            else:
                low = src_vals.attrib[EA_ATTRIBUTES["end_low_val"]]

        for src_vals in end.findall(EA_TAGS["end_high"]):
            src_high = src_vals.attrib[EA_ATTRIBUTES["end_high_type"]]
            if src_high == EA_INF:
                high = "inf"
            else:
                high = src_vals.attrib[EA_ATTRIBUTES["end_high_val"]]

        source_side.min_max_multiplicity = (low, high)

        if role := end.attrib.get(EA_ATTRIBUTES["end_name_src"]):
            source_side.role = role

        return source_side

    def _create_relation_target_side(self, end: ET.Element) -> RelationshipSide:
        target_side = RelationshipSide()

        low = "inf"
        high = "inf"
        for src_vals in end.findall(EA_TAGS["end_low"]):
            dst_low = src_vals.attrib[EA_ATTRIBUTES["end_low_type"]]
            if dst_low == EA_INF:
                low = "inf"
            else:
                low = src_vals.attrib[EA_ATTRIBUTES["end_low_val"]]

        for src_vals in end.findall(EA_TAGS["end_high"]):
            dst_high = src_vals.attrib[EA_ATTRIBUTES["end_high_type"]]
            if dst_high == EA_INF:
                high = "inf"
            else:
                high = src_vals.attrib[EA_ATTRIBUTES["end_high_val"]]

        target_side.min_max_multiplicity = (low, high)

        if role := end.attrib.get(EA_ATTRIBUTES["end_name_dst"]):
            target_side.role = role

        return target_side

    def _try_build_relationship(self, elem: ET.Element) -> Optional[ClassRelationship]:
        if elem.attrib[EA_ATTRIBUTES["elem_type"]] in CLASS_RELATIONSHIPS_TYPES:
            rel_name = elem.attrib.get(EA_ATTRIBUTES["end_name"])
            type_name = CLASS_REL_MAPPING_TYPE[elem.attrib[EA_ATTRIBUTES["elem_type"]]]

            # Final relationship uninitialized placeholder
            processed_relation = ClassRelationship(type_name, rel_name)
            ends_ids = SourceDestinationPair()

            for end in elem.iter(EA_TAGS["end"]):
                if end.attrib[EA_ATTRIBUTES["end_id"]].startswith("EAID_src"):
                    ends_ids.source = self._parse_id(
                        self._get_mandatory_node(end, "end_type").attrib[
                            EA_ATTRIBUTES["end_type_src"]
                        ]
                    )
                    processed_relation.source_side = self._create_relation_source_side(
                        end
                    )

                elif end.attrib[EA_ATTRIBUTES["end_id"]].startswith("EAID_dst"):
                    ends_ids.target = self._parse_id(
                        self._get_mandatory_node(end, "end_type").attrib[
                            EA_ATTRIBUTES["end_type_dst"]
                        ]
                    )
                    processed_relation.target_side = self._create_relation_target_side(
                        end
                    )

            if not (all(vars(ends_ids).values())):
                raise InvalidXMLError(ERROR_MESS[ErrorType.REL_ENDS])

            self._id_to_evaluation_queue[str(ends_ids.source)].append(
                SetRelationshipSource(processed_relation)
            )
            self._id_to_evaluation_queue[str(ends_ids.target)].append(
                SetRelationshipTarget(processed_relation)
            )

            return processed_relation
        return None
