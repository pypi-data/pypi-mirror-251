from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MetricType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    VALUE_TYPE_UNKNOWN: _ClassVar[MetricType]
    VALUE_TYPE_INTEGER: _ClassVar[MetricType]
    VALUE_TYPE_FLOAT: _ClassVar[MetricType]
    VALUE_TYPE_STRING: _ClassVar[MetricType]
    VALUE_TYPE_DATE: _ClassVar[MetricType]
    VALUE_TYPE_BOOLEAN: _ClassVar[MetricType]

class OperationEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    GET: _ClassVar[OperationEnum]
    CREATE: _ClassVar[OperationEnum]
    READ: _ClassVar[OperationEnum]
    UPDATE: _ClassVar[OperationEnum]
    DELETE: _ClassVar[OperationEnum]
    SYNC: _ClassVar[OperationEnum]
VALUE_TYPE_UNKNOWN: MetricType
VALUE_TYPE_INTEGER: MetricType
VALUE_TYPE_FLOAT: MetricType
VALUE_TYPE_STRING: MetricType
VALUE_TYPE_DATE: MetricType
VALUE_TYPE_BOOLEAN: MetricType
GET: OperationEnum
CREATE: OperationEnum
READ: OperationEnum
UPDATE: OperationEnum
DELETE: OperationEnum
SYNC: OperationEnum

class MetricReadRequest(_message.Message):
    __slots__ = ["connect_portal_uuid"]
    CONNECT_PORTAL_UUID_FIELD_NUMBER: _ClassVar[int]
    connect_portal_uuid: str
    def __init__(self, connect_portal_uuid: _Optional[str] = ...) -> None: ...

class MetricGetRequest(_message.Message):
    __slots__ = ["metric_uuid"]
    METRIC_UUID_FIELD_NUMBER: _ClassVar[int]
    metric_uuid: str
    def __init__(self, metric_uuid: _Optional[str] = ...) -> None: ...

class MetricCreateRequest(_message.Message):
    __slots__ = ["connect_portal_uuid", "key", "name", "custom", "type", "configuration"]
    CONNECT_PORTAL_UUID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    connect_portal_uuid: str
    key: str
    name: str
    custom: str
    type: MetricType
    configuration: _any_pb2.Any
    def __init__(self, connect_portal_uuid: _Optional[str] = ..., key: _Optional[str] = ..., name: _Optional[str] = ..., custom: _Optional[str] = ..., type: _Optional[_Union[MetricType, str]] = ..., configuration: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class MetricUpdateRequest(_message.Message):
    __slots__ = ["metric_uuid", "name", "type", "configuration"]
    METRIC_UUID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    metric_uuid: str
    name: str
    type: MetricType
    configuration: _any_pb2.Any
    def __init__(self, metric_uuid: _Optional[str] = ..., name: _Optional[str] = ..., type: _Optional[_Union[MetricType, str]] = ..., configuration: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class MetricDeleteRequest(_message.Message):
    __slots__ = ["metric_uuid"]
    METRIC_UUID_FIELD_NUMBER: _ClassVar[int]
    metric_uuid: str
    def __init__(self, metric_uuid: _Optional[str] = ...) -> None: ...

class MetricResponse(_message.Message):
    __slots__ = ["operation", "success", "uuid", "key", "name", "custom", "type", "connect_portal_uuid", "connected_metrics", "configuration", "created_at", "updated_at"]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CONNECT_PORTAL_UUID_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_METRICS_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    operation: OperationEnum
    success: bool
    uuid: str
    key: str
    name: str
    custom: bool
    type: MetricType
    connect_portal_uuid: str
    connected_metrics: _containers.RepeatedScalarFieldContainer[str]
    configuration: _any_pb2.Any
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, operation: _Optional[_Union[OperationEnum, str]] = ..., success: bool = ..., uuid: _Optional[str] = ..., key: _Optional[str] = ..., name: _Optional[str] = ..., custom: bool = ..., type: _Optional[_Union[MetricType, str]] = ..., connect_portal_uuid: _Optional[str] = ..., connected_metrics: _Optional[_Iterable[str]] = ..., configuration: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class MetricsResponse(_message.Message):
    __slots__ = ["operation", "success", "metrics"]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    operation: OperationEnum
    success: bool
    metrics: _containers.RepeatedCompositeFieldContainer[MetricResponse]
    def __init__(self, operation: _Optional[_Union[OperationEnum, str]] = ..., success: bool = ..., metrics: _Optional[_Iterable[_Union[MetricResponse, _Mapping]]] = ...) -> None: ...
