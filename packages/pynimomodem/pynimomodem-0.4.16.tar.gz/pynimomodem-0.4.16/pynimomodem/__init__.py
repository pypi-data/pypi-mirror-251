"""Library to interface with a Viasat-approved NIMO modem for satellite IoT.

This library abstracts various low-level AT command operations useful for
interacting with a NIMO modem to send and receive data, check network status
and get location-based information.

Most `get` methods will raise a `ModemAtError` if a valid response is not
received to a command/query.

`ModemTimeout` will be raised if no response is received to a command within
the default or specified timeout.

AT command errors will raise `ModemAtError` with a property `error_code` to
provide further details with the `AtErrorCode`.

"""

from .constants import (
    AtErrorCode,
    BeamState,
    ControlState,
    DataFormat,
    EventNotification,
    GeoBeam,
    GeoSatellite,
    GnssMode,
    GnssModeOrbcomm,
    GnssModeQuectel,
    MessagePriority,
    MessageState,
    NetworkStatus,
    PowerMode,
    SignalQuality,
    UrcCode,
    UrcControl,
    WakeupPeriod,
    WakeupWay,
    WorkMode,
)
from .modem import (
    Manufacturer,
    ModemLocation,
    MoMessage,
    MtMessage,
    NimoModem,
    ModemAtError,
    ModemCrcConfig,
    ModemCrc,
    ModemError,
    ModemTimeout,
    AcquisitionInfo,
    SatelliteLocation,
)

__all__ = [
    'AtErrorCode',
    'BeamState',
    'ControlState',
    'DataFormat',
    'GeoBeam',
    'GeoSatellite',
    'GnssMode',
    'GnssModeOrbcomm',
    'GnssModeQuectel',
    'Manufacturer',
    'MessagePriority',
    'MessageState',
    'ModemLocation',
    'MoMessage',
    'MtMessage',
    'NetworkStatus',
    'NimoModem',
    'ModemAtError',
    'ModemCrcConfig',
    'ModemCrc',
    'ModemError',
    'ModemTimeout',
    'PowerMode',
    'AcquisitionInfo',
    'SatelliteLocation',
    'SignalQuality',
    'WakeupPeriod',
    'WakeupWay',
    'WorkMode',
    'UrcCode',
    'UrcControl',
    'EventNotification',
]