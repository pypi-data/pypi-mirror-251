import pickle

try:
    import ujson as json
except ImportError:
    import json

from .base import BaseMessage, BaseSerializer


class JSONSerializer(BaseSerializer):

    def serialize(self, message: BaseMessage) -> bytes:
        return json.dumps(message.model_dump()).encode("utf-8")

    def deserialize(self, response: bytes) -> BaseMessage:
        return BaseMessage(**json.loads(response))


class PickleSerializer(BaseSerializer):

    def serialize(self, message: BaseMessage) -> bytes:
        return pickle.dumps(message.model_dump())

    def deserialize(self, response: bytes) -> BaseMessage:
        return BaseMessage(**pickle.loads(response))


class MSGPackSerializer(BaseSerializer):

    def serialize(self, message: BaseMessage) -> bytes:
        import msgpack
        return msgpack.packb(message.model_dump())

    def deserialize(self, response: bytes) -> BaseMessage:
        import msgpack
        return BaseMessage(**msgpack.unpackb(response))
