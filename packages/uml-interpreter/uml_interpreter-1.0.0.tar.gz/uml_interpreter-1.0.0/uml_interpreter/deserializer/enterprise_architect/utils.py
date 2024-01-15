from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from uml_interpreter.model.diagrams.class_diagram import (
    ClassDiagramElement,
    ClassRelationship,
)
from uml_interpreter.model.diagrams.sequence_diagram import (
    SequenceSubject,
    SequenceFragment,
    SequenceMessage,
    Lifeline,
    LifespanEvent,
)


class RelationshipEditor(ABC):
    def __init__(self, relationship: ClassRelationship) -> None:
        self._relationship = relationship

    @abstractmethod
    def __call__(self, *args: Any, **kwds: Any) -> ClassRelationship:
        pass


class SetRelationshipTarget(RelationshipEditor):
    def __call__(self, target: ClassDiagramElement) -> ClassRelationship:
        self._relationship.target = target
        return self._relationship


class SetRelationshipSource(RelationshipEditor):
    def __call__(self, source: ClassDiagramElement) -> ClassRelationship:
        self._relationship.source = source
        return self._relationship


class LifelineManager(ABC):
    def __init__(self, lifeline: Lifeline) -> None:
        self._lifeline = lifeline

    @abstractmethod
    def __call__(self, *args: Any, **kwds: Any) -> Lifeline:
        pass


class AssignLifeline(LifelineManager):
    def __call__(self, referrer: Any) -> Lifeline:
        referrer.lifeline = self._lifeline
        return self._lifeline


class AssignLifelineToActor(AssignLifeline):
    def __init__(self, lifeline: Lifeline, name: str) -> None:
        super().__init__(lifeline)
        self._name = name

    def __call__(self, actor: SequenceSubject) -> Lifeline:
        super().__call__(actor)
        actor.name = self._name
        self._lifeline.subject = actor
        return self._lifeline


@dataclass
class SourceDestinationPair:
    source: Any = None
    target: Any = None


"""
TODO: all managers should be replaced with one - since no typing in python"""


class FragmentManager(ABC):
    def __init__(self, fragment: SequenceFragment) -> None:
        self._fragment = fragment

    @abstractmethod
    def __call__(self, *args: Any, **kwds: Any) -> SequenceFragment:
        pass


class AddCoveredSubject(FragmentManager):
    def __call__(self, subject: SequenceSubject) -> SequenceFragment:
        self._fragment.actors.append(subject)
        return self._fragment


class MessageManager(ABC):
    def __init__(self, message: SequenceMessage) -> None:
        self._message = message

    @abstractmethod
    def __call__(self, *args: Any, **kwds: Any) -> SequenceMessage:
        pass


class AddEventAsSend(MessageManager):
    def __call__(self, event: LifespanEvent) -> SequenceMessage:
        self._message.send_event = event
        event.lifeline.subject.messages_from.append(self._message)
        return self._message


class AddEventAsReceive(MessageManager):
    def __call__(self, event: LifespanEvent) -> SequenceMessage:
        self._message.receive_event = event
        event.lifeline.subject.messages_to.append(self._message)
        return self._message


class EventManager(ABC):
    def __init__(self, event: LifespanEvent) -> None:
        self._event = event

    @abstractmethod
    def __call__(self, *args: Any, **kwds: Any) -> LifespanEvent:
        pass


class AppendEventToLifeline(EventManager):
    def __call__(self, lifeline: Lifeline) -> LifespanEvent:
        lifeline.events.append(self._event)
        self._event.lifeline = lifeline
        return self._event
