from abc import ABC, abstractmethod
from io import TextIOWrapper

from uml_interpreter.model.model import UMLModel


class Serializer(ABC):
    """
    Serializer abstract base class.
    """

    @abstractmethod
    def save_to_file(self, model: UMLModel, path: str) -> None:
        """
        Function responsible for saving the model.

        Args:
            model (UMLModel): Model to be saved
            path (str): Path where model will be saved to
        """
        pass


class FileSerializer(Serializer):
    """
    Serializer implementation, that saves to files.
    """

    def save_to_file(self, model: UMLModel, path: str) -> None:
        """
        Function responsible for saving the model to file

        Args:
            model (UMLModel): Model to be saved
            path (str): Path where model will be saved to
        """
        with open(path, "w") as file:
            self._write_model(model, file)

    @abstractmethod
    def _write_model(self, model: UMLModel, target: TextIOWrapper) -> None:
        """
        Function writing model to opened stream. Abstract.

        Args:
            model (UMLModel): Model to be saved
            target (TextIOWrapper): Stream to save to
        """
        pass
