from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EmbedRequest(_message.Message):
    __slots__ = ("Audio",)
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    Audio: bytes
    def __init__(self, Audio: _Optional[bytes] = ...) -> None: ...

class EmbedResponse(_message.Message):
    __slots__ = ("Embedding",)
    EMBEDDING_FIELD_NUMBER: _ClassVar[int]
    Embedding: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, Embedding: _Optional[_Iterable[float]] = ...) -> None: ...

class FilterRequest(_message.Message):
    __slots__ = ("Audio", "Embedding")
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    EMBEDDING_FIELD_NUMBER: _ClassVar[int]
    Audio: bytes
    Embedding: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, Audio: _Optional[bytes] = ..., Embedding: _Optional[_Iterable[float]] = ...) -> None: ...

class FilterResponse(_message.Message):
    __slots__ = ("Audio",)
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    Audio: bytes
    def __init__(self, Audio: _Optional[bytes] = ...) -> None: ...
