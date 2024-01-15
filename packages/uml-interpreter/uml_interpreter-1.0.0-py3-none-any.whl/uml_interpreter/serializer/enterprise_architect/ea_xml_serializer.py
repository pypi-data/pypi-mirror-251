import uuid
import xml.etree.ElementTree as ET
from io import TextIOWrapper

from uml_interpreter.model.diagrams.abstract import UMLDiagram
from uml_interpreter.model.diagrams.class_diagram import (
    ClassDiagram,
    ClassDiagramAttribute,
    ClassDiagramElement,
    ClassDiagramMethod,
    ClassDiagramMethodParameter,
    ClassRelationship,
    RelationshipSide,
)
from uml_interpreter.model.model import UMLModel
from uml_interpreter.serializer.abstract import FileSerializer
from uml_interpreter.serializer.enterprise_architect.constants import (
    ATTRIBUTE_TYPE_INFO,
    ATTRIBUTE_TYPE_UML_DATA_TYPE_MAPPING,
    CLASS_IFACE_MAPPING,
    CLASS_REL_MAPPING,
    NAMESPACE_PREFIX,
    ROOT_INFO,
    AttributeType,
    EAFormat,
    UMLDataType,
)
from uml_interpreter.serializer.errors import ERROR_MESS, ErrorType, SerializationError


class EAXMLSerializer(FileSerializer):
    """
    Serializer implementation, that saves to Enterprise Architect XML files.
    """

    def __init__(self, format: EAFormat) -> None:
        """
        EAXMLSerializer initializer

        Args:
            format (EAFormat): Format to save model within.
        """
        self._format = format
        self._root = ET.Element(
            NAMESPACE_PREFIX[self._format] + ":" + self._format.value,
            ROOT_INFO[self._format],
        )
        self._tree = ET.ElementTree(self._root)

    def _write_model(self, model: UMLModel, target: TextIOWrapper) -> None:
        """
        Function writing model to opened stream in Enterprise Architect XML format.

        Args:
            model (UMLModel): Model to be saved
            target (TextIOWrapper): Stream to save to
        """
        self._target = target
        self._input_model = model

        self._createNode(
            "Documentation", self._root, exporter="uml-interpreter", exporterVersion="1.0"
        )
        model_dict = {
            "visibility": "public",
            "name": self._input_model.name,
            "xmi:type": "uml:Model",
        }
        self._model_node = self._createNode("uml:Model", self._root, True, **model_dict)
        self._extensions_node = self._createNode(
            "Extension", self._root, extender="EnterpriseArchitect"
        )

        self._process_diagrams()

        self._process_primitive_types()
        if len(model.diagrams) > 0:
            self._process_extensions_diagrams()

        self._save()

    def _process_extensions_diagrams(self):
        """
        Method used to serialize diagrams to extensions.
        """
        diagrams_node = self._createNode("elements", self._extensions_node, True)

        diagrams_node = self._createNode("connectors", self._extensions_node, True)

        diagrams_node = self._createNode("diagrams", self._extensions_node, True)

        for diagram in self._input_model.diagrams:
            diagram_node_id = {"xmi:id": self._createId(uuid.uuid4())}
            new_diagram_node = self._createIdNode(
                "diagram",
                diagrams_node,
                None,
                diagram_node_id,
            )

            diagram_pk = self._createPkAttribute(diagram.id)["xmi:id"]
            self._createNode(
                "model",
                new_diagram_node,
                True,
                package=diagram_pk,
                owner=diagram_pk,
            )

            self._createNode(
                "properties", new_diagram_node, True, name=diagram.name, type="logical"
            )

            elements_node = self._createNode(
                "elements",
                new_diagram_node,
                True,
            )

            self._process_extension_diagram_elements(diagram, elements_node)

    def _process_extension_diagram_elements(
        self, diagram: UMLDiagram, parent: ET.Element
    ):
        """
        Method used to serialize diagram elements to extensions.

        Args:
            diagram (UMLDiagram): diagram to serialize elements of
            parent (Element): parent of created element nodes
        """
        if isinstance(diagram, ClassDiagram):
            relations: set[ClassRelationship] = set()

            for (idx, element) in enumerate(diagram.elements):
                element_id = "EAID_" + self._createId(element.id)
                self._createNode(
                    "element", parent, True, subject=element_id, seqno=str(idx)
                )

                [relations.add(e) for e in element.relations_from]
                [relations.add(e) for e in element.relations_to]

            for relation in relations:
                element_id = "EAID_" + self._createId(relation.id)
                self._createNode("element", parent, True, subject=element_id)

    def _process_primitive_types(self):
        """
        Method used to serialize custom primitive types to extensions.

        Custom primitive type import not working.
        Left for potential future use.
        """
        primitive_types_node = self._createNode(
            "primitivetypes", self._extensions_node, True
        )

        package_node_id = {"xmi:id": "EAPrimitiveTypesPackage"}
        package_node = self._createIdNode(
            "packagedElement",
            primitive_types_node,
            "uml:Package",
            package_node_id,
            name="EA_PrimitiveTypes_Package",
            visibility="public",
        )

        voids_node_id = {"xmi:id": "EAnoneTypesPackage"}
        voids_node = self._createIdNode(
            "packagedElement",
            package_node,
            "uml:Package",
            voids_node_id,
            name="EA_none_Types_Package",
            visibility="public",
        )

        eanone_void_node_id = {"xmi:id": "EAnone_void"}
        self._createIdNode(
            "packagedElement",
            voids_node,
            "uml:PrimitiveType",
            eanone_void_node_id,
            name="void",
            visibility="public",
        )

    def _process_diagrams(self):
        """
        Method used to serialize diagrams to model.
        """
        for diagram in self._input_model.diagrams:
            new_diagram_node = self._createIdNode(
                "packagedElement",
                self._model_node,
                "uml:Package",
                self._createPkAttribute(diagram.id),
                name=diagram.name,
                visibility="public",
            )
            self._process_diagram(diagram, new_diagram_node)

    def _process_diagram(self, diagram: UMLDiagram, diagram_node: ET.Element):
        """
        Method used to serialize singular diagram to model.

        Args:
            diagram (UMLDiagram): diagram to serialize
            diagram_node (Element): xml node of serialized diagram
        """
        if isinstance(diagram, ClassDiagram):
            relations: set[ClassRelationship] = set()

            for element in diagram.elements:
                [relations.add(e) for e in element.relations_from]
                [relations.add(e) for e in element.relations_to]

                self._process_class_element(element, diagram_node)

            for relation in relations:
                self._process_class_relationship(relation, diagram_node)

    def _process_class_relationship(
        self, relation: ClassRelationship, parent_node: ET.Element
    ):
        """
        Method used to serialize singular class relationship to model.

        Args:
            relation (ClassRelationship): relationship to serialize
            parent_node (Element): xml node of parent
        """
        relation_type = CLASS_REL_MAPPING.get(relation.type)
        if relation_type is None:
            raise SerializationError(ERROR_MESS[ErrorType.TYPE_ERROR])

        relation_node = self._createIdNode(
            "packagedElement",
            parent_node,
            relation_type,
            self._createIdAttribute(relation.id),
            visibility="public",
        )

        short_ref_id = str(relation.id)[2:].upper().replace("-", "_")
        dst_idref = {"xmi:idref": f"EAID_dst{short_ref_id}"}
        dst_id = {"xmi:id": f"EAID_dst{short_ref_id}"}
        src_idref = {"xmi:idref": f"EAID_src{short_ref_id}"}
        src_id = {"xmi:id": f"EAID_src{short_ref_id}"}
        owned_end_dict = {
            "visibility": "public",
            "association": "EAID_" + self._createId(relation.id),
            "isStatic": "false",
            "isReadonly": "false",
            "isDerived": "false",
            "isOrdered": "false",
            "isUnique": "true",
            "isDerivedUnion": "false",
            "aggregation": "none",
        }

        self._createNode(
            "memberEnd",
            relation_node,
            True,
            **dst_idref,
        )
        target_node = self._createIdNode(
            "ownedEnd",
            relation_node,
            "uml:Property",
            dst_id,
            **owned_end_dict,
            role=relation.target_side.role or "",
        )
        self._process_relationship_side(relation.target_side, target_node)

        self._createNode(
            "memberEnd",
            relation_node,
            True,
            **src_idref,
        )
        source_node = self._createIdNode(
            "ownedEnd",
            relation_node,
            "uml:Property",
            src_id,
            **owned_end_dict,
            role=relation.source_side.role or "",
        )
        self._process_relationship_side(relation.source_side, source_node)

    def _process_relationship_side(self, side: RelationshipSide, parent: ET.Element):
        """
        Method used to serialize one side of relationship to model.

        Args:
            side (RelationshipSide): relationship side to serialize
            parent (Element): xml node of parent
        """
        if not side.element:
            return

        idref_dict = {"xmi:idref": "EAID_" + self._createId(side.element.id)}
        self._createNode("type", parent, True, **idref_dict)

        min_str, max_str = side.min_max_multiplicity
        if max_str == "inf":
            max_str = "-1"

        max_multi_type = (
            UMLDataType.INTEGER.value
            if int(max_str) >= 0
            else UMLDataType.UNLIMITED_NATURAL.value
        )

        self._createIdNode(
            "lowerValue",
            parent,
            UMLDataType.INTEGER.value,
            self._createIdAttribute(uuid.uuid4()),
            value=min_str,
        )

        self._createIdNode(
            "upperValue",
            parent,
            max_multi_type,
            self._createIdAttribute(uuid.uuid4()),
            value=max_str,
        )

    def _process_class_element(
        self, element: ClassDiagramElement, diagram_node: ET.Element
    ):
        """
        Method used to serialize element of class diagram to model.

        Args:
            element (ClassDiagramElement): element to serialize
            diagram_node (Element): xml node of parent diagram
        """
        element_type = CLASS_IFACE_MAPPING.get(type(element))
        if element_type is None:
            raise SerializationError(ERROR_MESS[ErrorType.TYPE_ERROR])

        element_node = self._createIdNode(
            "packagedElement",
            diagram_node,
            element_type,
            self._createIdAttribute(element.id),
            name=element.name,
            visibility="public",
        )

        for attr in element.attributes:
            self._process_attribute(attr, element_node)

        for operation in element.methods:
            self._process_method(operation, element_node)

    def _process_attribute(
        self, attribute: ClassDiagramAttribute, element_node: ET.Element
    ):
        """
        Method used to serialize attribute of class of class diagram to model.

        Args:
            attribute (ClassDiagramAttribute): attribute to serialize
            element_node (Element): xml node of parent element
        """
        attr_node = self._createIdNode(
            "ownedAttribute",
            element_node,
            "uml:Property",
            self._createIdAttribute(attribute.id),
            visibility="private" if attribute.private else "public",
            isStatic="false",
            isDerived="false",
            isOrdered="false",
            isReadOnly="false",
            isUnique="true",
            name=attribute.name,
            isDerivedUnion="false",
        )

        self._create_type_node(attribute, attr_node)

        type = None

        try:
            type = ATTRIBUTE_TYPE_UML_DATA_TYPE_MAPPING[
                AttributeType(attribute.type)
            ].value
        except ValueError | KeyError:
            raise SerializationError(ERROR_MESS[ErrorType.ATTR_TYPE_ERROR])

        self._createIdNode(
            "upperValue",
            attr_node,
            type,
            self._createIdAttribute(uuid.uuid4()),
            value="1",
        )

        self._createIdNode(
            "lowerValue",
            attr_node,
            type,
            self._createIdAttribute(uuid.uuid4()),
            value="1",
        )

    def _process_method(self, method: ClassDiagramMethod, element_node: ET.Element):
        """
        Method used to serialize method of element of class diagram to model.

        Args:
            method (ClassDiagramMethod): method to serialize
            element_node (Element): xml node of parent element
        """
        method_node = self._createIdNode(
            "ownedOperation",
            element_node,
            None,
            self._createIdAttribute(method.id),
            name=method.name,
            visibility="private" if method.private else "public",
            concurrency="sequential",
        )

        for param in method.parameters:
            self._process_method_param(param, method_node)

        try:
            self._createIdNode(
                "ownedParameter",
                method_node,
                None,
                self._createIdAttribute(uuid.uuid4()),
                **ATTRIBUTE_TYPE_INFO[AttributeType(method.ret_type)],
            )
        except ValueError:
            raise SerializationError(ERROR_MESS[ErrorType.ATTR_TYPE_ERROR])

        method.ret_type

    def _process_method_param(
        self, param: ClassDiagramMethodParameter, method_node: ET.Element
    ):
        """
        Method used to serialize method parameter of class diagram to model.

        Args:
            param (ClassDiagramMethodParameter): parameter to serialize
            method_node (Element): xml node of parent method
        """
        param_node = self._createIdNode(
            "ownedParameter",
            method_node,
            None,
            self._createIdAttribute(param.id),
            name=param.name,
            direction="in",
            isStream="false",
            isException="false",
            isOrdered="false",
            isUnique="true",
        )

        self._create_type_node(param, param_node)

    def _create_type_node(
        self,
        param: ClassDiagramMethodParameter | ClassDiagramAttribute,
        parent: ET.Element,
    ):
        """
        Method used to create node with tag 'type'.

        Args:
            param (ClassDiagramMethodParameter | ClassDiagramAttribute): parameter with type
            parent (Element): xml node of parent
        """
        type_dict: dict[str, str] = {}

        try:
            type_dict = ATTRIBUTE_TYPE_INFO[AttributeType(param.type)]
        except ValueError | KeyError:
            raise SerializationError(ERROR_MESS[ErrorType.ATTR_TYPE_ERROR])

        self._createNode("type", parent, True, **type_dict)

    def _save(self) -> None:
        """
        Method used to write to target
        """
        ET.indent(self._tree, space="\t", level=0)
        self._target.write(ET.tostring(self._root).decode())

    def _createPkAttribute(self, id: uuid.UUID) -> dict[str, str]:
        """
        Method used to create dict with xmi:id primary key value.

        Args:
            id (UUID): id to insert to dict
        """
        uuid_str = self._createId(id)
        return {"xmi:id": f"EAPK_{uuid_str}"}

    def _createIdAttribute(self, id: uuid.UUID) -> dict[str, str]:
        """
        Method used to create dict with xmi:id identifier value.

        Args:
            id (UUID): id to insert to dict
        """
        uuid_str = self._createId(id)
        return {"xmi:id": f"EAID_{uuid_str}"}

    def _createId(self, id: uuid.UUID) -> str:
        """
        Method used to transform UUID to EA XML format

        Args:
            id (UUID): id to transform
        """
        uuid_str = str(id).upper().replace("-", "_")
        return uuid_str

    def _createIdNode(
        self,
        node_name: str,
        parent: ET.Element,
        _type: str | None,
        id_dict: dict[str, str],
        **props,
    ) -> ET.Element:
        """
        Method used to create XML node with id and type

        Args:
            node_name (str): tag of new node
            parent (Element): parent of new node
            _type (str | None): value of xmi:type attribute for new node
            id_dict (dict[str, str]): dict containing id or pk attributes
            **props: rest of props for new node
        """
        arg_dict = {"xmi:type": _type} if _type else {}
        arg_dict.update(props)
        arg_dict.update(id_dict)
        return ET.SubElement(parent, node_name, arg_dict)

    def _createNode(
        self, node_name: str, parent: ET.Element, use_literal_name=False, **attributes
    ) -> ET.Element:
        """
        Method used to create XML node with optional namespace prefix

        Args:
            node_name (str): tag of new node
            parent (Element): parent of new node
            use_literal_name (Bool, optional): whether to omit insertion of namespace prefix to tag
            **attributes: rest of props for new node
        """
        name = (
            NAMESPACE_PREFIX[self._format] + ":" + node_name
            if not use_literal_name
            else node_name
        )
        return ET.SubElement(parent, name, attributes)
