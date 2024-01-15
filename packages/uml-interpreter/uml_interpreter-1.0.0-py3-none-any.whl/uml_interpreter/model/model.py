from typing import Optional
from uuid import UUID

from uml_interpreter.model.abstract import UMLObject
from uml_interpreter.model.diagrams.abstract import UMLDiagram
from uml_interpreter.visitor.model_visitor import ModelPrinter, ModelVisitor


class UMLModel(UMLObject):
    """
    Class representing UML model.
    """

    def __init__(
        self,
        diagrams: Optional[list[UMLDiagram]] = None,
        filename: Optional[str] = None,
        name="New Model",
        id: UUID | None = None,
    ) -> None:
        """
        UMLModel initializer

        Args:
            diagrams (Optional[list[UMLDiagram]], optional): Model diagrams.
            filename (Optional[str], optional): Model filename
            name (str, optional): Model name
            id (UUID | None, optional): Model ID
        """
        super().__init__(id)
        self.diagrams: list[UMLDiagram] = diagrams or []
        self.filename: Optional[str] = filename
        self.name: str = name

    def accept(self, visitor: ModelVisitor):
        """
        Method used to accept a model traversing Visitor

        Args:
            visitor (ModelVisitor): Visitor used to traverse through model
        """
        visitor.visit_model(self)

    def print(self, indent: int = 0, indent_inc: int = 2):
        """
        Function used to fully print the model object into the command line.

        Args:
            indent (int, optional): Print line indentation. Defaults to 0.
            indent_inc (int, optional): Indentation increment. Defaults to 2.
        """
        self.accept(ModelPrinter(indent, indent_inc))
