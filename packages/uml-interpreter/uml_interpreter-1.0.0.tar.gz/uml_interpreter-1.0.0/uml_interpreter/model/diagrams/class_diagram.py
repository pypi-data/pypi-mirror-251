from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union
from uuid import UUID

import uml_interpreter.model.diagrams.abstract as dg
import uml_interpreter.model.diagrams.sequence_diagram as sd
import uml_interpreter.visitor.model_visitor as v
from uml_interpreter.model.abstract import UMLObject
from uml_interpreter.model.errors import InvalidModelInitialization


class ClassDiagram(dg.StructuralDiagram):
    """
    Class representing a Class UML diagram
    """

    def __init__(
        self, name: Optional[str] = None, elements=None, id: UUID | None = None
    ) -> None:
        """
        ClassDiagram initializer

        Args:
            name (Optional[str], optional): Diagram name
            elements (_type_, optional): Diagram elements
            id (UUID | None, optional): Diagram ID
        """
        super().__init__(name, id)
        self.elements: list[ClassDiagramElement] = elements or []

    def accept(self, visitor: v.ModelVisitor):
        """
        Method used to accept a model traversing Visitor

        Arguments:
            visitor ModelVisitor: Visitor used to traverse through model
        """
        visitor.visit_class_diagram(self)


class RelationshipType(Enum):
    """
    Enum representing Class Diagram relationships types.
    Values have to be strings to allow creation by calling
    RelationshipType(<name>)
    """

    Association = "Association"
    Generalization = "Generalization"


class ClassDiagramElement(sd.SequenceSubject):
    """
    Class representing element in a class diagram
    """

    def __init__(self, name: str, id: UUID | None = None) -> None:
        """
        ClassDiagramElement initializer

        Args:
            name (str): Element name
            id (UUID | None, optional): Element ID
        """
        super().__init__(name, id)
        self.relations_to: list[ClassRelationship] = []
        self.relations_from: list[ClassRelationship] = []
        self.methods: list[ClassDiagramMethod] = []
        self.attributes: list[ClassDiagramAttribute] = []

    def accept(self, visitor: v.ModelVisitor) -> None:
        """
        Method used to accept a model traversing Visitor

        Arguments:
            visitor ModelVisitor: Visitor used to traverse through model
        """
        visitor.visit_class_diagram_element(self)

    def add_relationship_to(
        self,
        target_element: ClassDiagramElement,
        relation_type: Union[RelationshipType, str] = (RelationshipType.Association),
        **rel_init_kwargs,
    ) -> ClassRelationship:
        """
        Adds relationship to a specified target. Accepts all key-word
        arguments supported by ClassRelationship
        initialization.

        Args:
            target_element (ClassDiagramElement): ClassDiagramElement instance, to which relationship should be created.
            relation_type (Union[RelationshipType, str], optional): RelationshipType enum instance or its string value, defining type of relationship.

        Returns:
            ClassRelationship: Added relationship
        """

        if isinstance(relation_type, str):
            relation_type = RelationshipType(relation_type)

        relationship = ClassRelationship(
            source=self, target=target_element, type=relation_type, **rel_init_kwargs
        )
        return relationship

    def _add_to_relations_to(
        self, relationship: ClassRelationship
    ) -> ClassRelationship:
        """
        Adds relation to self.relations_to list.
        Logic unifying assignment of the element on relationship
        side is applied.

        Args:
            relationship (ClassRelationship): predefined ClassRelationship instance.
        During assignment its source side is set to
        the current element, but target side is left as given.

        Returns:
            ClassRelationship: Added relationship
        """
        self.relations_to.append(relationship)
        relationship.source = self
        return relationship

    def set_as_source_of(self, relationship: ClassRelationship) -> (ClassRelationship):
        """
        Set current ClassDiagramElement as a source side of the given relationship.
        Logic unifying assignment of the element on relationship side is applied.
        """
        relationship = self._add_to_relations_to(relationship)
        return relationship

    def add_relationship_from(
        self,
        source_element: ClassDiagramElement,
        relation_type: Union[RelationshipType, str] = (RelationshipType.Association),
        **rel_init_kwargs,
    ) -> ClassRelationship:
        """
        Adds relationship from a specified target. Accepts all key-word arguments supported by ClassRelationship initialization.

        Args:
            source_element (ClassDiagramElement): ClassDiagramElement instance, from which relationship should be created.
            relation_type (Union[RelationshipType, str], optional): RelationshipType enum instance or its string value, defining type of relationship to be created.

        Returns:
            ClassRelationship: _description_
        """

        if isinstance(relation_type, str):
            relation_type = RelationshipType(relation_type)

        relationship = ClassRelationship(
            source=source_element, target=self, type=relation_type, **rel_init_kwargs
        )
        return relationship

    def _add_to_relations_from(
        self, relationship: ClassRelationship
    ) -> ClassRelationship:
        """
        Adds relation to self.relations_from list.
        Logic unifying assignment of the element on relationship side is
        applied.

        Args:
            relationship (ClassRelationship): predefined ClassRelationship instance. During assignment its source side is set to the current element, but target side is left as given.

        Returns:
            ClassRelationship: _description_
        """

        self.relations_from.append(relationship)
        relationship.target = self
        return relationship

    def set_as_target_of(self, relationship: ClassRelationship) -> (ClassRelationship):
        """
        Set current ClassDiagramElement as a target side of the given relationship.
        Logic unifying assignment of the element on relationship side is applied.
        """
        relationship = self._add_to_relations_from(relationship)
        return relationship


class ClassDiagramClass(ClassDiagramElement):
    """
    Represents a class in Class Diagram.
    """

    def __init__(self, name: str, id: UUID | None = None) -> None:
        """
        ClassDiagramClass initializer

        Args:
            name (str): Class name
            id (UUID | None, optional): Class ID.
        """
        super().__init__(name, id)

    def accept(self, visitor: v.ModelVisitor):
        """
        Method used to accept a model traversing Visitor

        Arguments:
            visitor ModelVisitor: Visitor used to traverse through model
        """
        visitor.visit_class_diagram_class(self)


class ClassDiagramInterface(ClassDiagramElement):
    """
    Represents an interface in Class Diagram.
    """

    def __init__(self, name: str, id: UUID | None = None) -> None:
        """
        ClassDiagramInterface initializer

        Args:
            name (str): Interface name
            id (UUID | None, optional): Interface ID.
        """
        super().__init__(name, id)

    def accept(self, visitor: v.ModelVisitor):
        """
        Method used to accept a model traversing Visitor

        Arguments:
            visitor ModelVisitor: Visitor used to traverse through model
        """
        visitor.visit_class_diagram_interface(self)


@dataclass()
class RelationshipSide:
    """
    Side of a relationship
    """

    element: Optional[ClassDiagramElement] = None
    role: Optional[str] = None
    min_max_multiplicity: tuple[str, str] = ("0", "1")
    # TODO: change type to dataclass with values from enum with possible
    #  values (would be created from config with mapping of name
    #  to python type (change name to multiplicity_range)


class ClassRelationship(UMLObject):
    """
    Represents a relationship between elements in class diagram.
    """

    def __init__(
        self,
        type: RelationshipType = RelationshipType.Association,
        name: Optional[str] = None,
        source: Optional[ClassDiagramElement] = None,
        target: Optional[ClassDiagramElement] = None,
        source_minmax: tuple[str, str] = ("0", "1"),
        target_minmax: tuple[str, str] = ("0", "1"),
        source_role: Optional[str] = None,
        target_role: Optional[str] = None,
        id: UUID | None = None,
        *,
        source_side: Optional[RelationshipSide] = None,
        target_side: Optional[RelationshipSide] = None,
    ) -> None:
        """
        ClassRelationship initializer

        Args:
            type (RelationshipType, optional): Relationship type.
            name (Optional[str], optional): Relationship name.
            source (Optional[ClassDiagramElement], optional): Relationship source.
            target (Optional[ClassDiagramElement], optional): Relationship target.
            source_minmax (tuple[str, str], optional): Relationship source multiplicity.
            target_minmax (tuple[str, str], optional): Relationship target mulitplicity.
            source_role (Optional[str], optional): Relationship source role.
            target_role (Optional[str], optional): Relationship target role.
            id (UUID | None, optional): Relationship ID.
            source_side (Optional[RelationshipSide], optional): Relationship source side object.
            target_side (Optional[RelationshipSide], optional): Relationship target side object.
        """
        self.source_side = source_side or RelationshipSide(
            source, source_role, source_minmax
        )
        self.target_side = target_side or RelationshipSide(
            target, target_role, target_minmax
        )

        self.type = type
        self.name = name
        super().__init__(id)

    @property
    def source_side(self) -> RelationshipSide:
        return self._source_side

    @property
    def source(self) -> Optional[ClassDiagramElement]:
        return self._source_side.element

    @source_side.setter
    def source_side(self, side: RelationshipSide) -> None:
        self._source_side = side
        if side.element is not None:
            """
            In case given side is a placeholder - not yet initialized.
            """
            side.element.set_as_source_of(self)

    @source.setter
    def source(self, new_source_element: ClassDiagramElement) -> None:
        if self.source is new_source_element:
            """
            Condition to avoid cyclic setters calls.
            """
            return

        if isinstance(new_source_element, ClassDiagramElement):
            self._source_side.element = new_source_element
            new_source_element.set_as_source_of(self)

        else:
            raise InvalidModelInitialization(
                f"Given class diagram element was not an instance "
                f"of defined class. New element: {str(new_source_element)}"
            )

    def create_source_side(
        self,
        source_element: ClassDiagramElement,
        role: Optional[str],
        min_max_multiplicity: Optional[tuple[str, str]],
    ) -> None:
        """
        Creates source side of the relationship

        Args:
            source_element (ClassDiagramElement): Relationship source
            role (Optional[str]): Source side role in relationship
            min_max_multiplicity (Optional[tuple[str, str]]): Source side multiplicity
        """
        new_source_side = RelationshipSide(
            source_element, role, min_max_multiplicity or ("0", "1")
        )
        self.source_side = new_source_side

    @property
    def target_side(self) -> RelationshipSide:
        return self._target_side

    @property
    def target(self) -> Optional[ClassDiagramElement]:
        return self._target_side.element

    @target_side.setter
    def target_side(self, side: RelationshipSide) -> None:
        self._target_side = side
        if side.element is not None:
            """
            In case given side is a placeholder - not yet initialized.
            """
            side.element.set_as_target_of(self)

    @target.setter
    def target(self, new_target_element: ClassDiagramElement) -> None:
        if self.target is new_target_element:
            """
            Condition to avoid cyclic setters calls.
            """
            return

        if isinstance(new_target_element, ClassDiagramElement):
            self._target_side.element = new_target_element
            new_target_element.set_as_target_of(self)

        else:
            raise InvalidModelInitialization(
                f"Given class diagram element was not an instance of defined"
                f" class. New element: {str(new_target_element)}"
            )

    def create_target_side(
        self,
        target_element: ClassDiagramElement,
        role: Optional[str],
        min_max_multiplicity: Optional[tuple[str, str]],
    ) -> None:
        """
        Creates target side of the relationship

        Args:
            target_element (ClassDiagramElement): Relationship target
            role (Optional[str]): Target side role in relationship
            min_max_multiplicity (Optional[tuple[str, str]]): Target side multiplicity
        """
        new_target_side = RelationshipSide(
            target_element, role, min_max_multiplicity or ("0", "1")
        )
        self.target_side = new_target_side

    def accept(self, visitor: v.ModelVisitor):
        """
        Method used to accept a model traversing Visitor

        Arguments:
            visitor ModelVisitor: Visitor used to traverse through model
        """
        visitor.visit_class_relationship(self)


class ClassDiagramMethod(UMLObject):
    """
    Represents an method in element in class diagram.
    """

    def __init__(
        self,
        name: str,
        ret_type: str,
        private: bool = True,
        parameters: None | list[ClassDiagramMethodParameter] = None,
        id: UUID | None = None,
    ) -> None:
        """
        ClassDiagramMethod initializer

        Args:
            name (str): Method name
            ret_type (str): Method return type
            private (bool, optional): Method visibility.
            parameters (None | list[ClassDiagramMethodParameter], optional): Method parameters list.
            id (UUID | None, optional): Method ID.
        """
        self.name = name
        self.parameters: list[ClassDiagramMethodParameter] = parameters or []
        self.ret_type = ret_type
        self.private: bool = private
        super().__init__(id)

    def accept(self, visitor: v.ModelVisitor):
        """
        Method used to accept a model traversing Visitor

        Arguments:
            visitor ModelVisitor: Visitor used to traverse through model
        """
        visitor.visit_diagram_method(self)


class ClassDiagramAttribute(UMLObject):
    """
    Represents an attribute in element in class diagram.
    """

    def __init__(
        self, name: str, type: str, private: bool = True, id: UUID | None = None
    ) -> None:
        """
        ClassDiagramAttribute initializer

        Args:
            name (str): Attribute name
            type (str): Attribute type
            private (bool, optional): Attribute visibility.
            id (UUID | None, optional): Attribute ID.
        """
        self.name = name
        self.type = type
        self.private: bool = private
        super().__init__(id)

    def accept(self, visitor: v.ModelVisitor):
        """
        Method used to accept a model traversing Visitor

        Arguments:
            visitor ModelVisitor: Visitor used to traverse through model
        """
        visitor.visit_class_diagram_attribute(self)


class ClassDiagramMethodParameter(UMLObject):
    """
    Represents a parameter of a mathod in element in class diagram.
    """

    def __init__(self, name: Optional[str], type: str, id: UUID | None = None) -> None:
        """
        ClassDiagramMethodParameter initializer

        Args:
            name (Optional[str]): Parameter name
            type (str): Parameter type
            id (UUID | None, optional): Parameter ID.
        """
        self.name = name or ""
        self.type = type
        super().__init__(id)

    def accept(self, visitor: v.ModelVisitor):
        """
        Method used to accept a model traversing Visitor

        Arguments:
            visitor ModelVisitor: Visitor used to traverse through model
        """
        visitor.visit_class_diagram_method_parameter(self)
