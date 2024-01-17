from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Component(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    Runner: _ClassVar[Component]
    Runtime: _ClassVar[Component]
Runner: Component
Runtime: Component

class JobCompleteEvent(_message.Message):
    __slots__ = ["success", "failure", "cancellation", "timeout"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    FAILURE_FIELD_NUMBER: _ClassVar[int]
    CANCELLATION_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    success: Success
    failure: Failure
    cancellation: Cancellation
    timeout: Timeout
    def __init__(self, success: _Optional[_Union[Success, _Mapping]] = ..., failure: _Optional[_Union[Failure, _Mapping]] = ..., cancellation: _Optional[_Union[Cancellation, _Mapping]] = ..., timeout: _Optional[_Union[Timeout, _Mapping]] = ...) -> None: ...

class Success(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class Failure(_message.Message):
    __slots__ = ["component", "error_message", "error_code", "stack_trace"]
    COMPONENT_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    STACK_TRACE_FIELD_NUMBER: _ClassVar[int]
    component: Component
    error_message: str
    error_code: int
    stack_trace: str
    def __init__(self, component: _Optional[_Union[Component, str]] = ..., error_message: _Optional[str] = ..., error_code: _Optional[int] = ..., stack_trace: _Optional[str] = ...) -> None: ...

class Cancellation(_message.Message):
    __slots__ = ["reason"]
    REASON_FIELD_NUMBER: _ClassVar[int]
    reason: str
    def __init__(self, reason: _Optional[str] = ...) -> None: ...

class Timeout(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
