import logging
from uuid import UUID
import xml.etree.ElementTree as ET
from collections import deque
from typing import Optional, Callable, Any

from uml_interpreter.deserializer.enterprise_architect.constants import (
    EA_ATTRIBUTES,
    EA_ATTR_EXT,
    EA_TAGS,
    FRAGMENT_TYPE_MAPPING,
    SEQUENCE_SYNCH_MAPPING_TYPE,
)
from uml_interpreter.deserializer.enterprise_architect.utils import (
    AddCoveredSubject,
    AssignLifelineToActor,
    AddEventAsReceive,
    AddEventAsSend,
    AppendEventToLifeline,
)
from uml_interpreter.deserializer.errors import (
    TAGS_ERRORS,
    InvalidXMLError,
)
from uml_interpreter.model.diagrams.sequence_diagram import (
    SequenceSubject,
    SequenceMessage,
    Lifeline,
    SequenceDiagram,
    LifespanEvent,
)


class EAXMLSequenceBuilder:
    def __init__(
        self,
        id_to_evaluation_queue: dict[str, deque[Callable]],
        id_to_instance_mapping: dict[str, Any],
        _parse_id: Callable[[str], UUID],
    ) -> None:
        """
        Requires reference to the shared dictionary of evaluation queues.
        """
        self._id_to_evaluation_queue: dict[
            str, deque[Callable]
        ] = id_to_evaluation_queue
        self._id_to_instance_mapping: dict[str, Any] = id_to_instance_mapping
        self._parse_id = _parse_id

    def _parse_diagram(self, model_node: ET.Element, diag_name: str | None) -> SequenceDiagram:
        """
        Parse using tags specific for this diagram type
        """
        lifelines = list()
        events_and_fragments = list()
        messages = list()
        actors: list[SequenceSubject] = []
        packaged_elems = model_node.iter(EA_TAGS["elem"])
        seq_diag = SequenceDiagram(diag_name)

        for packaged_elem in packaged_elems:
            if packaged_elem.attrib[EA_ATTRIBUTES["type"]] == "uml:Collaboration":
                for actor in self._parse_actors(packaged_elem):
                    actors.append(actor)

                behaviour_nodes = packaged_elem.iter(EA_TAGS["sequence_behaviour"])
                for _ in behaviour_nodes:
                    lifelines += self._parse_lifelines(packaged_elem)
                    events_and_fragments += self._parse_fragments(
                        packaged_elem, seq_diag
                    )
                    messages += self._parse_messages(packaged_elem)

        for uml_object in lifelines + actors + events_and_fragments + messages:

            try:
                self._id_to_instance_mapping[str(uml_object.id)] = uml_object
            except KeyError as e:
                logging.warning(e)

        for actor in actors:
            actor.id = self._id_to_instance_mapping[str(actor.id)].id

        seq_diag.actors = actors
        return seq_diag

    def _parse_lifelines(self, model_node: ET.Element) -> list[Lifeline]:
        lifeline_nodes = model_node.iter(EA_TAGS["lifeline"])
        lifelines = [self._parse_lifeline(lifeline) for lifeline in lifeline_nodes]
        return lifelines

    def _parse_lifeline(self, lifeline_node: ET.Element) -> Lifeline:
        uuid_id = self._parse_id(lifeline_node.attrib[EA_ATTRIBUTES["id"]])
        lifeline = Lifeline(uuid_id)
        lifeline_name = lifeline_node.attrib[EA_ATTRIBUTES["name"]]
        represented_type_id = self._parse_id(
            lifeline_node.attrib[EA_ATTRIBUTES["represents"]]
        )
        self._id_to_evaluation_queue[str(represented_type_id)].append(
            AssignLifelineToActor(lifeline, lifeline_name)
        )
        return lifeline

    def _parse_actors(self, colab_node: ET.Element) -> list[SequenceSubject]:
        subject_nodes = colab_node.iter(EA_TAGS["elem_attr"])
        actors = [self._parse_actor(actor) for actor in subject_nodes]
        return actors

    def _parse_actor(self, actor_node: ET.Element) -> SequenceSubject:
        uuid_id = self._parse_id(actor_node.attrib[EA_ATTRIBUTES["id"]])
        actor = SequenceSubject(uuid_id=uuid_id)
        return actor

    def _parse_fragments(
        self, model_node: ET.Element, seq_diag: SequenceDiagram
    ):
        fragment_nodes = model_node.iter(EA_TAGS["fragment"])
        fragments = [
            self._parse_fragment(fragment, seq_diag) for fragment in fragment_nodes
        ]
        return [frag for frag in fragments if frag is not None]

    def _parse_fragment(
        self, fragment_node: ET.Element, seq_diag: SequenceDiagram
    ):
        if fragment_type := fragment_node.attrib[EA_ATTRIBUTES["type"]]:

            match fragment_type:
                case "uml:CombinedFragment":
                    fragment_type = fragment_node.attrib[
                        EA_ATTRIBUTES["interaction_type"]
                    ]

                    fragment_name = ""
                    operand = fragment_node.find(EA_TAGS["operand"])
                    if (operand):
                        guard = operand.find(EA_TAGS["guard"])
                        if (guard):
                            spec = guard.find(EA_TAGS["specification"])
                            if (spec):
                                fragment_name = spec.attrib[EA_ATTRIBUTES["type"]]

                    FragmentType = FRAGMENT_TYPE_MAPPING[fragment_type]

                    uuid_id = self._parse_id(fragment_node.attrib[EA_ATTRIBUTES["id"]])
                    fragment = FragmentType(seq_diag, fragment_name, uuid_id)

                    for covered in fragment_node.findall(EA_TAGS["covered"]):
                        self._id_to_evaluation_queue[
                            str(self._parse_id(covered.attrib[EA_ATTR_EXT["elem_id"]]))
                        ].append(AddCoveredSubject(fragment))
                    return fragment

                case "uml:OccurrenceSpecification":
                    uuid_id = self._parse_id(fragment_node.attrib[EA_ATTRIBUTES["id"]])
                    event = LifespanEvent(uuid_id)
                    lifeline_id = self._parse_id(
                        fragment_node.attrib[EA_ATTRIBUTES["covered"]]
                    )
                    self._id_to_evaluation_queue[str(lifeline_id)].append(
                        AppendEventToLifeline(event)
                    )

                    return event
                case _:
                    logging.warning(f"Fragment type {fragment_type} not supported")

    def _parse_messages(self, model_node: ET.Element) -> list[SequenceMessage]:
        message_nodes = model_node.iter(EA_TAGS["message"])
        messages = [self._parse_message(message) for message in message_nodes]
        return messages

    def _parse_message(self, message_node: ET.Element) -> SequenceMessage:
        message_synch = message_node.attrib[EA_ATTRIBUTES["message_synch"]]
        MessageType: type[SequenceMessage] = SEQUENCE_SYNCH_MAPPING_TYPE[message_synch]
        send_event_id = self._parse_id(message_node.attrib[EA_ATTRIBUTES["send_event"]])
        receive_event_id = self._parse_id(
            message_node.attrib[EA_ATTRIBUTES["receive_event"]]
        )
        uuid_id = self._parse_id(message_node.attrib[EA_ATTRIBUTES["id"]])

        message = MessageType(uuid_id=uuid_id)
        # message.name = message_node.attrib.get(EA_ATTRIBUTES["name"])

        self._id_to_evaluation_queue[str(send_event_id)].append(AddEventAsSend(message))
        self._id_to_evaluation_queue[str(receive_event_id)].append(
            AddEventAsReceive(message)
        )

        return message

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
