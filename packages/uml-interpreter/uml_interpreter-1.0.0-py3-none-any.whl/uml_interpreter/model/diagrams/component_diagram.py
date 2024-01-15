from typing import Optional
from uuid import UUID

import uml_interpreter.model.diagrams.abstract as dg
import uml_interpreter.model.diagrams.class_diagram as cd
from uml_interpreter.model.abstract import UMLObject


class ComponentDiagram(dg.StructuralDiagram):
    """
    Class representing component diagram.
    """

    def __init__(self, name: str, id: UUID | None = None) -> None:
        """
        ComponentDiagram initializer

        Args:
            name (str): Diagram name
            id (UUID | None, optional): Diagram ID
        """
        super().__init__(name, id)
        self.components: list[Component] = []


class ComponentRelationMember(UMLObject):
    """
    Class representing component diagram relation member.
    """

    def __init__(self, id: UUID | None = None) -> None:
        """
        ComponentRelationMember initializer

        Args:
            id (UUID | None, optional): Member ID
        """
        self.relations_to: list[ComponentRelationship] = []
        self.relations_from: list[ComponentRelationship] = []
        super().__init__(id)


class ComponentRelationship(UMLObject):
    """
    Class representing component diagram relationship.
    """

    def __init__(
        self,
        source: ComponentRelationMember,
        target: ComponentRelationMember,
        id: UUID | None = None,
    ) -> None:
        """
        ComponentRelationship initializer

        Args:
            source (ComponentRelationMember): Relationship source
            target (ComponentRelationMember): Relationship target
            id (UUID | None, optional): Relationship ID
        """
        self.source = source
        source.relations_from.append(self)
        self.target = target
        target.relations_to.append(self)
        self.related_relationship: Optional[cd.ClassRelationship] = None
        super().__init__(id)


class Component(ComponentRelationMember):
    """
    Class representing component in component diagram.
    """

    def __init__(self, id: UUID | None = None) -> None:
        """
        Component initializer

        Args:
            id (UUID | None, optional): Component ID
        """
        super().__init__(id)
        self.children: list[Component] = []
        self.ports: list[Port] = []
        self.interfaces: list[ComponentInterface] = []
        self.elements: list[cd.ClassDiagramElement] = []
        self.name: str = ""


class Port(ComponentRelationMember):
    """
    Class representing port in component diagram.
    """

    def __init__(self, id: UUID | None = None) -> None:
        """
        Port initializer

        Args:
            id (UUID | None, optional): Port ID
        """
        super().__init__(id)
        self.interfaces: list[ComponentInterface] = []


class ComponentInterface(ComponentRelationMember):
    """
    Class representing interface in component diagram.
    """

    def __init__(self, id: UUID | None = None) -> None:
        """
        ComponentInterface initializer

        Args:
            id (UUID | None, optional): Interface ID
        """
        super().__init__(id)
        self.methods: list[cd.ClassDiagramMethod] = []
        self.name: str = ""


class ProvidedComponentInterface(ComponentInterface):
    """
    Class representing provided component interface in component diagram.
    """

    def __init__(self, id: UUID | None = None) -> None:
        """
        ProvidedComponentInterface initializer

        Args:
            id (UUID | None, optional): Provided interface ID
        """
        super().__init__(id)
        self.fulfills: list[RequiredComponentInterface] = []


class RequiredComponentInterface(ComponentInterface):
    """
    Class representing required component interface in component diagram.
    """

    def __init__(self, id: UUID | None = None) -> None:
        """
        RequiredComponentInterface initializer

        Args:
            id (UUID | None, optional): Required interface ID
        """
        super().__init__(id)
        self.fulfilled_by: list[ProvidedComponentInterface] = []
