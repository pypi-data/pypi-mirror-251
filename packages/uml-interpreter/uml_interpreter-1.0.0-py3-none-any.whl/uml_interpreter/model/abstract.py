import uuid
from abc import ABC


class UMLObject(ABC):
    """
    Represents an abstraction of a component of UML model.
    """

    def __init__(self, object_id: uuid.UUID | None = None) -> None:
        """
        UMLObject initializer

        Args:
            object_id (uuid.UUID | None, optional): Object ID
        """
        super().__init__()
        self._id = object_id or uuid.uuid4()

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @id.setter
    def id(self, new_id: uuid.UUID) -> None:
        self._id = new_id
