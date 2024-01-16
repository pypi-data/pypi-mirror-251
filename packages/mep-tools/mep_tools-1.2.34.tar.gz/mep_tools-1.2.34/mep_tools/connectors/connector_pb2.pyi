from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DispatcherRequest(_message.Message):
    __slots__ = ["payload"]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    payload: _any_pb2.Any
    def __init__(self, payload: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class DispatcherResponse(_message.Message):
    __slots__ = ["success", "cached", "payload"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    CACHED_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    success: bool
    cached: bool
    payload: _any_pb2.Any
    def __init__(self, success: bool = ..., cached: bool = ..., payload: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...
