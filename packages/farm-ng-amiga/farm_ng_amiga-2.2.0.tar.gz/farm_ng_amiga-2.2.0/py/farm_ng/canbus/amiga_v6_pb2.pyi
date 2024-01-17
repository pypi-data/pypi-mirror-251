from farm_ng.canbus import canbus_pb2 as _canbus_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AmigaControlState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STATE_BOOT: _ClassVar[AmigaControlState]
    STATE_MANUAL_READY: _ClassVar[AmigaControlState]
    STATE_MANUAL_ACTIVE: _ClassVar[AmigaControlState]
    STATE_CC_ACTIVE: _ClassVar[AmigaControlState]
    STATE_AUTO_READY: _ClassVar[AmigaControlState]
    STATE_AUTO_ACTIVE: _ClassVar[AmigaControlState]
    STATE_ESTOPPED: _ClassVar[AmigaControlState]
STATE_BOOT: AmigaControlState
STATE_MANUAL_READY: AmigaControlState
STATE_MANUAL_ACTIVE: AmigaControlState
STATE_CC_ACTIVE: AmigaControlState
STATE_AUTO_READY: AmigaControlState
STATE_AUTO_ACTIVE: AmigaControlState
STATE_ESTOPPED: AmigaControlState

class AmigaTpdo1(_message.Message):
    __slots__ = ("node_id", "stamp", "control_state", "measured_speed", "measured_angular_rate", "pto_bits", "hbridge_bits")
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    CONTROL_STATE_FIELD_NUMBER: _ClassVar[int]
    MEASURED_SPEED_FIELD_NUMBER: _ClassVar[int]
    MEASURED_ANGULAR_RATE_FIELD_NUMBER: _ClassVar[int]
    PTO_BITS_FIELD_NUMBER: _ClassVar[int]
    HBRIDGE_BITS_FIELD_NUMBER: _ClassVar[int]
    node_id: int
    stamp: float
    control_state: AmigaControlState
    measured_speed: float
    measured_angular_rate: float
    pto_bits: int
    hbridge_bits: int
    def __init__(self, node_id: _Optional[int] = ..., stamp: _Optional[float] = ..., control_state: _Optional[_Union[AmigaControlState, str]] = ..., measured_speed: _Optional[float] = ..., measured_angular_rate: _Optional[float] = ..., pto_bits: _Optional[int] = ..., hbridge_bits: _Optional[int] = ...) -> None: ...

class AmigaPdo2(_message.Message):
    __slots__ = ("node_id", "stamp", "motor_a_rpm", "motor_b_rpm", "motor_c_rpm", "motor_d_rpm")
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    MOTOR_A_RPM_FIELD_NUMBER: _ClassVar[int]
    MOTOR_B_RPM_FIELD_NUMBER: _ClassVar[int]
    MOTOR_C_RPM_FIELD_NUMBER: _ClassVar[int]
    MOTOR_D_RPM_FIELD_NUMBER: _ClassVar[int]
    node_id: int
    stamp: float
    motor_a_rpm: int
    motor_b_rpm: int
    motor_c_rpm: int
    motor_d_rpm: int
    def __init__(self, node_id: _Optional[int] = ..., stamp: _Optional[float] = ..., motor_a_rpm: _Optional[int] = ..., motor_b_rpm: _Optional[int] = ..., motor_c_rpm: _Optional[int] = ..., motor_d_rpm: _Optional[int] = ...) -> None: ...

class AmigaV6CanbusState(_message.Message):
    __slots__ = ("amiga_tpdo1", "motor_states", "battery_charge_level", "last_send_error")
    AMIGA_TPDO1_FIELD_NUMBER: _ClassVar[int]
    MOTOR_STATES_FIELD_NUMBER: _ClassVar[int]
    BATTERY_CHARGE_LEVEL_FIELD_NUMBER: _ClassVar[int]
    LAST_SEND_ERROR_FIELD_NUMBER: _ClassVar[int]
    amiga_tpdo1: AmigaTpdo1
    motor_states: _canbus_pb2.MotorStates
    battery_charge_level: float
    last_send_error: bool
    def __init__(self, amiga_tpdo1: _Optional[_Union[AmigaTpdo1, _Mapping]] = ..., motor_states: _Optional[_Union[_canbus_pb2.MotorStates, _Mapping]] = ..., battery_charge_level: _Optional[float] = ..., last_send_error: bool = ...) -> None: ...
