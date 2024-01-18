from abc import abstractmethod, ABC

from .messages import BaseMessage


class BaseSerializer(ABC):

    @abstractmethod
    def serialize(self, message: BaseMessage) -> bytes:
        ...

    @abstractmethod
    def deserialize(self, response: bytes) -> BaseMessage:
        ...
