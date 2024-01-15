from enum import Enum
from typing import Optional
from uuid import UUID

import uml_interpreter.model.diagrams.abstract as dg
import uml_interpreter.visitor.model_visitor as v
from uml_interpreter.model.abstract import UMLObject


class SequenceDiagram(dg.BehavioralDiagram):
    """
    Class representing sequence diagram.
    """

    # TODO - error?
    def __init__(self, name: str | None, id: UUID | None = None) -> None:
        """
        SequenceDiagram initializer

        Args:
            name (str | None, optional): Diagram name
            id (UUID | None, optional): Diagram ID
        """
        super().__init__(name, id)
        self.actors: list[SequenceSubject] = []

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_sequence_diagram(self)


class LifespanEvent(UMLObject):
    """
    Class representing a lifespan event in sequence diagram.
    """

    def __init__(self, uuid_id: Optional[UUID] = None) -> None:
        """
        LifespanEvent initializer

        Args:
            uuid_id (UUID | None, optional): LifespanEvent ID
        """
        super().__init__(uuid_id)
        self.lifeline: Optional[Lifeline] = None
        self.predecessor: Optional[LifespanEvent] = None
        self.successor: Optional[LifespanEvent] = None
        self.time: int = 0

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_lifespan_event(self)


class Lifeline(UMLObject):
    """
    Class representing a lifeline in sequence diagram.
    """

    def __init__(self, object_id: UUID | None = None) -> None:
        """
        Lifeline initializer

        Args:
            object_id (UUID | None, optional): Lifeline ID
        """

        self.events: list[LifespanEvent] = list()
        self.subject: Optional[SequenceSubject] = None
        super().__init__(object_id)

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_lifeline(self)


class SequenceSubject(UMLObject):
    """
    Class representing an actor in sequence diagram.
    """

    def __init__(self, name: str | None = None, uuid_id: Optional[UUID] = None) -> None:
        """
        SequenceSubject initializer

        Args:
            name (str): Subject name
            uuid_id (UUID | None, optional): Subject ID
        """
        super().__init__(uuid_id)
        self.messages_from: list[SequenceMessage] = []
        self.messages_to: list[SequenceMessage] = []
        self.name = name

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_sequence_subject(self)


class SequenceMessageStatus(Enum):
    """
    Message status values.
    """

    FAILED = 0
    SUCCEEDED = 1


class SequenceMessage(UMLObject):
    """
    Class representing a message in sequence diagram.
    """

    def __init__(
        self,
        send_event: Optional[LifespanEvent] = None,
        receive_event: Optional[LifespanEvent] = None,
        uuid_id: Optional[UUID] = None,
    ) -> None:
        """
        SequenceMessage initializer.

        Args:
            send_event (LifespanEvent | None, optional): Event of sending the message
            receive_event (LifespanEvent | None, optional): Event of receiving the message
            uuid_id (UUID | None, optional): Message ID
        """
        super().__init__(uuid_id)
        self.send_event = send_event
        self.receive_event = receive_event
        self.status: Optional[SequenceMessageStatus] = SequenceMessageStatus.SUCCEEDED
        self.display_text: Optional[str] = None

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_sequence_message(self)


class SyncSequenceMessage(SequenceMessage):
    """
    Class representing a synchronous message in sequence diagram.
    """

    def __init__(
        self,
        send_event: Optional[LifespanEvent] = None,
        receive_event: Optional[LifespanEvent] = None,
        uuid_id: Optional[UUID] = None,
    ) -> None:
        """
        SyncSequenceMessage initializer.

        Args:
            send_event (LifespanEvent | None, optional): Event of sending the message
            receive_event (LifespanEvent | None, optional): Event of receiving the message
            uuid_id (UUID | None, optional): Message ID
        """
        super().__init__(send_event, receive_event, uuid_id)
        self.response: Optional[AsyncSequenceMessage] = None

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_sync_sequence_message(self)


class AsyncSequenceMessage(SequenceMessage):
    """
    Class representing an asynchronous message in sequence diagram.
    """

    def __init__(
        self,
        send_event: Optional[LifespanEvent] = None,
        receive_event: Optional[LifespanEvent] = None,
        uuid_id: Optional[UUID] = None,
    ) -> None:
        """
        AsyncSequenceMessage initializer.

        Args:
            send_event (LifespanEvent | None, optional): Event of sending the message
            receive_event (LifespanEvent | None, optional): Event of receiving the message
           uuid_id (UUID | None, optional): Message ID
        """

        super().__init__(send_event, receive_event, uuid_id)
        self.response: Optional[SyncSequenceMessage] = None

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_async_sequence_message(self)


class SequenceFragment(SequenceDiagram, LifespanEvent):
    """
    Class representing a sequence fragment sequence diagram.
    """

    def __init__(
        self,
        parent: SequenceDiagram,
        name: str,
        uuid_id: Optional[UUID] = None,
        actors_subgroup: Optional[list[SequenceSubject]] = None,
    ) -> None:
        """
        SequenceFragment initializer

        Args:
            parent (SequenceDiagram): Fragment parent
            name (str): Fragment name
            uuid_id (UUID | None, optional): Fragment ID
        """
        super().__init__(name)
        super(LifespanEvent, self).__init__(uuid_id)
        self.actors = actors_subgroup or parent.actors

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_sequence_fragment(self)


class LoopSequenceFragment(SequenceFragment):
    """
    Class representing a loop in sequence diagram.
    """

    def __init__(
        self,
        parent: SequenceDiagram,
        name: str,
        uuid_id: UUID | None = None,
        actors_subgroup: Optional[list[SequenceSubject]] = None,
    ) -> None:
        """
        LoopSequenceFragment initializer

        Args:
            parent (SequenceDiagram): Fragment parent
            name (str): Fragment name
            uuid_id (UUID | None, optional): Fragment ID
        """
        super().__init__(parent, name, uuid_id, actors_subgroup)


class ConditionSequenceFragment(SequenceFragment):
    """
    Class representing a condition in sequence diagram.
    """

    def __init__(
        self,
        parent: SequenceDiagram,
        name: str,
        uuid_id: UUID | None = None,
        actors_subgroup: Optional[list[SequenceSubject]] = None,
    ) -> None:
        """
        ConditionSequenceFragment initializer

        Args:
            parent (SequenceDiagram): Fragment parent
            name (str): Fragment name
            uuid_id (UUID | None, optional): Fragment ID
        """

        super().__init__(parent, name, uuid_id, actors_subgroup)
