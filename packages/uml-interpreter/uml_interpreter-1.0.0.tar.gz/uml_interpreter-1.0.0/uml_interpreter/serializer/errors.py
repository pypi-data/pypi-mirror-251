from enum import Enum, auto


class ErrorType(Enum):
    TYPE_ERROR = (auto(),)
    ATTR_TYPE_ERROR = (auto(),)


ERROR_MESS: dict[ErrorType, str] = {
    ErrorType.TYPE_ERROR: "Unknown type of serialized element.",
    ErrorType.ATTR_TYPE_ERROR: "Unknown type of attribute.",
}


class SerializationError(Exception):
    """
    Exception thrown by Serializer, caused by critical failure while serializing.

    Error message structure:
        Serializer Error: {error_message}
    """

    def __init__(self, msg: str) -> None:
        self.msg = msg

    def __str__(self):
        return f"Serializer Error: {self.msg}"
