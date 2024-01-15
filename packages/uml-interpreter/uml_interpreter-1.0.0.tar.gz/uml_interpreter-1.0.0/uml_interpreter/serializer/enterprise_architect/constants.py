from enum import Enum

from uml_interpreter.model.diagrams.class_diagram import (
    ClassDiagramClass,
    ClassDiagramElement,
    ClassDiagramInterface,
    RelationshipType,
)


class EAFormat(Enum):
    XML2_1 = "XMI"


class AttributeType(Enum):
    INTEGER = "integer"
    VOID = "void"


class UMLDataType(Enum):
    UNLIMITED_NATURAL = "uml:LiteralUnlimitedNatural"
    INTEGER = "uml:LiteralInteger"


ROOT_INFO: dict[EAFormat, dict[str, str]] = {
    EAFormat.XML2_1: {
        "xmlns:xmi": "http://schema.omg.org/spec/XMI/2.1",
        "xmi:version": "2.1",
        "xmlns:uml": "http://schema.omg.org/spec/UML/2.1",
    }
}

NAMESPACE_PREFIX: dict[EAFormat, str] = {EAFormat.XML2_1: "xmi"}

CLASS_IFACE_MAPPING: dict[type[ClassDiagramElement], str] = {
    ClassDiagramClass: "uml:Class",
    ClassDiagramInterface: "uml:Interface",
}

CLASS_REL_MAPPING: dict[RelationshipType, str] = {
    RelationshipType.Association: "uml:Association"
}

ATTRIBUTE_TYPE_INFO: dict[AttributeType, dict[str, str]] = {
    AttributeType.INTEGER: {
        "xmi:type": "uml:PrimitiveType",
        "href": "http://schema.omg.org/spec/UML/2.1/uml.xml#Integer",
    },
    AttributeType.VOID: {
        # commented because custom primitive types are not working
        # "name": "return",
        # "direction": "return",
        # "type": "EAnone_void",
    },
}

ATTRIBUTE_TYPE_UML_DATA_TYPE_MAPPING: dict[AttributeType, UMLDataType] = {
    AttributeType.INTEGER: UMLDataType.INTEGER
}
