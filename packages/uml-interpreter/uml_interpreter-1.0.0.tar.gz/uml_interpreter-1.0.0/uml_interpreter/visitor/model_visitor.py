from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uml_interpreter.model.model import UMLDiagram, UMLModel
    from uml_interpreter.model.diagrams.class_diagram import (
        ClassDiagram,
        ClassDiagramAttribute,
        ClassDiagramClass,
        ClassDiagramElement,
        ClassDiagramInterface,
        ClassDiagramMethod,
        ClassDiagramMethodParameter,
        ClassRelationship,
    )
    from uml_interpreter.model.diagrams.sequence_diagram import (
        SequenceDiagram,
        SequenceFragment,
        SequenceMessage,
        SequenceSubject,
        Lifeline,
        LifespanEvent,
        AsyncSequenceMessage,
        SyncSequenceMessage
    )


class ModelVisitor(ABC):
    """
    Visitor that traverse through UML model.
    """

    @abstractmethod
    def visit_model(self, model: UMLModel):
        pass

    @abstractmethod
    def visit_diagram(self, diag: UMLDiagram):
        pass

    @abstractmethod
    def visit_class_diagram(self, diag: ClassDiagram):
        pass

    @abstractmethod
    def visit_class_diagram_element(self, elem: ClassDiagramElement):
        pass

    @abstractmethod
    def visit_class_diagram_class(self, elem: ClassDiagramClass):
        pass

    @abstractmethod
    def visit_class_diagram_interface(self, elem: ClassDiagramInterface):
        pass

    @abstractmethod
    def visit_class_relationship(self, diag: ClassRelationship):
        pass

    @abstractmethod
    def visit_class_diagram_attribute(self, diag: ClassDiagramAttribute):
        pass

    @abstractmethod
    def visit_diagram_method(self, diag: ClassDiagramMethod):
        pass

    @abstractmethod
    def visit_class_diagram_method_parameter(self, diag: ClassDiagramMethodParameter):
        pass

    @abstractmethod
    def visit_sequence_diagram(self, diag: SequenceDiagram) -> None:
        pass

    @abstractmethod
    def visit_sequence_message(self, message: SequenceMessage) -> None:
        pass

    @abstractmethod
    def visit_async_sequence_message(self, message: AsyncSequenceMessage) -> None:
        pass

    @abstractmethod
    def visit_sync_sequence_message(self, message: SyncSequenceMessage) -> None:
        pass

    @abstractmethod
    def visit_lifeline(self, lifeline: Lifeline) -> None:
        pass

    @abstractmethod
    def visit_lifespan_event(self, event: LifespanEvent) -> None:
        pass

    @abstractmethod
    def visit_sequence_fragment(self, fragment: SequenceFragment) -> None:
        pass

    @abstractmethod
    def visit_sequence_subject(self, actor: SequenceSubject) -> None:
        pass


class ModelPrinter(ModelVisitor):
    """
    Used to print out UML Model's hierarchical structure to the user's console.
    """

    def __init__(self, indent: int = 0, indent_inc: int = 2) -> None:
        """
        ModelPrinter initializer

        Args:
            indent (int, optional): Initial line indentation. Defaults to 0.
            indent_inc (int, optional): Line indentation increment value. Defaults to 2.
        """
        self._indent = indent
        self._indent_inc = indent_inc

    def visit_model(self, model: UMLModel) -> None:
        """
        Method used to start traversing thorugh an UML model

        Args:
            model (UMLModel):
        """
        self.print(f'Model: "{model.name}"')

        self.incr_ident()
        for diagram in model.diagrams:
            diagram.accept(self)
        self.decr_ident()

    def visit_diagram(self, diagram: UMLDiagram) -> None:
        self.print(f'UML Diagram: "{diagram.name}"')

    def visit_class_diagram(self, diagram: ClassDiagram) -> None:
        self.print(f'Class Diagram: "{diagram.name}"')

        self.incr_ident()
        for elem in diagram.elements:
            elem.accept(self)
        self.decr_ident()

    def visit_class_diagram_element(self, elem: ClassDiagramElement):
        self.print(f'Element: "{elem.name}" id: {elem.id}')

        self.incr_ident()
        self._visit_class_diagram_element_data(elem)
        self.decr_ident()

    def visit_class_diagram_class(self, elem: ClassDiagramClass):
        self.print(f'Class: "{elem.name}" id: {elem.id}')

        self.incr_ident()
        self._visit_class_diagram_element_data(elem)
        self.decr_ident()

    def visit_class_diagram_interface(self, elem: ClassDiagramInterface):
        self.print(f'Interface: "{elem.name}" id: {elem.id}')

        self.incr_ident()
        self._visit_class_diagram_element_data(elem)
        self.decr_ident()

    def _visit_class_diagram_element_data(self, elem: ClassDiagramElement):
        if elem.relations_from:
            self.print("Relationships (target):")
            self.incr_ident()
            for rel in elem.relations_from:
                rel.accept(self)
            self.decr_ident()

        if elem.relations_to:
            self.print("Relationships (source):")
            self.incr_ident()
            for rel in elem.relations_to:
                rel.accept(self)
            self.decr_ident()

        if elem.attributes:
            self.print("Attributes:")
            self.incr_ident()
            for attr in elem.attributes:
                attr.accept(self)
            self.decr_ident()

        if elem.methods:
            self.print("Methods:")
            self.incr_ident()
            for meth in elem.methods:
                meth.accept(self)
            self.decr_ident()

    def visit_class_relationship(self, rel: ClassRelationship):
        from uml_interpreter.model.diagrams.class_diagram import ClassDiagramElement

        if isinstance(rel.source, ClassDiagramElement) and isinstance(
            rel.target, ClassDiagramElement
        ):
            self.print(
                f"{rel.type} ({rel.name}) - {rel.source.name} ({rel.source_side.role})[{rel.source_side.min_max_multiplicity[0]}..."
                + f"{rel.source_side.min_max_multiplicity[1]}] -> [{rel.target_side.min_max_multiplicity[0]}..."
                + f"{rel.target_side.min_max_multiplicity[1]}] ({rel.target_side.role}) {rel.target.name}"
            )

    def visit_class_diagram_attribute(self, attr: ClassDiagramAttribute):
        self.print(f"{attr.name}: {attr.type}")

    def visit_diagram_method(self, meth: ClassDiagramMethod):
        self.print(
            f"{meth.name}: {[f'{param.name}: {param.type}' for param in meth.parameters]} -> {meth.ret_type}"
        )

    def visit_class_diagram_method_parameter(self, param: ClassDiagramMethodParameter):
        self.print(f"{param.name}: {param.type}")

    def visit_sequence_diagram(self, diag: SequenceDiagram) -> None:
        self.print(f'Sequence Diagram: "{diag.name}"')

        self.incr_ident()
        for actor in diag.actors:
            actor.accept(self)

        self.decr_ident()

    def visit_sequence_subject(self, actor: SequenceSubject) -> None:
        self.print(f'Actor: "{actor.name}"')

        self.incr_ident()

        for message in actor.messages_from:
            message.accept(self)

        for message in actor.messages_to:
            message.accept(self)
        self.decr_ident()

    def visit_sequence_message(self, message: SequenceMessage) -> None:
        se = message.send_event
        re = message.receive_event
        if se and re and se.lifeline and re.lifeline and se.lifeline.subject and re.lifeline.subject:
            self.print(
                f"({se.lifeline.subject.name}) -> ({re.lifeline.subject.name})"
            )

    def visit_async_sequence_message(self, message: AsyncSequenceMessage) -> None:
        self.visit_sequence_message(message)

    def visit_sync_sequence_message(self, message: SyncSequenceMessage) -> None:
        self.visit_sequence_message(message)

    def visit_lifeline(self, lifeline: Lifeline) -> None:
        self.print("Lifeline")

    def visit_lifespan_event(self, event: LifespanEvent) -> None:
        self.print(f"Event: {event.__class__.__name__}")

    def visit_sequence_fragment(self, fragment: SequenceFragment) -> None:
        self.print(f"Fragment: {fragment.name}")

        self.incr_ident()
        # for subject in fragment.covered_subjects:
        #     subject.accept(self)
        self.decr_ident()

    def incr_ident(self) -> None:
        self._indent = self._indent + self._indent_inc

    def decr_ident(self) -> None:
        self._indent = self._indent - self._indent_inc

    def print(self, mess: str) -> None:
        print("|" + "-" * self._indent + mess)
