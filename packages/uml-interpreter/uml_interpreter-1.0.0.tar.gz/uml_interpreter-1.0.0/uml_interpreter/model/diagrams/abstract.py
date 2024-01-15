from typing import Optional
from uuid import UUID

from uml_interpreter.model.abstract import UMLObject
from uml_interpreter.visitor.model_visitor import ModelVisitor


class UMLDiagram(UMLObject):
    """
    Class representing an UML diagram
    """

    def __init__(self, name: Optional[str] = None, id: UUID | None = None) -> None:
        """
        UMLDiagram initializer

        Args:
            name (Optional[str], optional): Diagram's name
            id (UUID | None, optional): Diagram's ID
        """
        self.name: str = name or ""
        super().__init__(id)

    def accept(self, visitor: ModelVisitor):
        """
        Method used to accept a model traversing Visitor

        Args:
            visitor (ModelVisitor): Visitor used to traverse through model
        """
        visitor.visit_diagram(self)


class StructuralDiagram(UMLDiagram):
    """
    Class representing a Structural UML diagram
    """

    def __init__(self, name: Optional[str] = None, id: UUID | None = None) -> None:
        """
        StructuralDiagram initializer

        Args:
            name (Optional[str], optional): Diagram's name
            id (UUID | None, optional): Diagram's ID
        """
        super().__init__(name, id)


class BehavioralDiagram(UMLDiagram):
    """
    Class representing a Behavioral UML diagram
    """

    def __init__(self, name: Optional[str] = None, id: UUID | None = None) -> None:
        """
        BehavioralDiagram initializer

        Args:
            name (Optional[str], optional): Diagram's name
            id (UUID | None, optional): Diagram's ID
        """
        super().__init__(name, id)
