#
# This file is part of the antplus project
#
# Copyright (c) 2024 Tiago Coutinho
# Distributed under the GPLv3 license. See LICENSE for more info.

"""
[Device profiles documentation](https://www.thisisant.com/developer/resources/downloads/#documents_tab)
"""


import asyncio
import enum
import functools
import logging
import pathlib
import time

import serialio


SYS_USB_SERIAL_PATH = pathlib.Path("/sys/bus/usb-serial")
SYS_USB_SERIAL_DEVICES_PATH = SYS_USB_SERIAL_PATH / "devices"


# Garmin Canada
VENDOR_ID = 0x0FCF


# Product
ANTUSB1_STICK_ID = 0x1004
DEV_BOARD_USB_ID = 0x1006
ANTUSB2_STICK_ID = 0x1008
ANTUSB_M_ID = 0x1009

VENDORS = {
    VENDOR_ID: {ANTUSB1_STICK_ID, DEV_BOARD_USB_ID, ANTUSB2_STICK_ID, ANTUSB_M_ID}
}

SYNC = 0xA4
ANTPLUS_NETWORK_KEY = bytes([0xB9, 0xA5, 0x21, 0xFB, 0xBD, 0x72, 0xC3, 0x45])


class DeviceType(enum.IntEnum):
    """
    ANT+ device profile identifiers
    """

    Unknown = 255
    PowerMeter = 11
    FitnessEquipment = 17
    ControlsDevice = 16
    BloodPressure = 18
    Geocache = 19
    Environment = 25
    TirePressureMonitor = 48
    WeightScale = 119
    HeartRate = 120
    BikeSpeedCadence = 121
    BikeCadence = 122
    BikeSpeed = 123
    StrideSpeed = 124
    Lev = 20
    Radar = 40
    Shifting = 34
    DropperSeatpost = 115


class BatteryStatus(enum.IntEnum):
    """
    ANT+ battery status
    """

    Unknown = 0
    New = 1
    Good = 2
    Ok = 3
    Low = 4
    Critical = 5
    Charging = 6
    Invalid = 7


class ChannelType(enum.IntEnum):
    BIDIRECTIONAL_RECEIVE = 0x00 # AKA slave
    BIDIRECTIONAL_TRANSMIT = 0x10 # AKA master

    SHARED_BIDIRECTIONAL_RECEIVE = 0x20
    SHARED_BIDIRECTIONAL_TRANSMIT = 0x30

    UNIDIRECTIONAL_RECEIVE_ONLY = 0x40
    UNIDIRECTIONAL_TRANSMIT_ONLY = 0x50
    

class ResetType(enum.IntFlag):
    POWER_ON_RESET = 0
    HARDWARE = 1 << 0
    WATCH_DOG = 1 << 1
    COMMAND = 1 << 5
    SYNCHRONOUS = 1 << 6
    SUSPEND = 1 << 7


class MessageType(enum.IntEnum):
    INVALID = 0x00

    # Configuration messages
    UNASSIGN_CHANNEL = 0x41
    ASSIGN_CHANNEL = 0x42
    SET_CHANNEL_ID = 0x51
    SET_CHANNEL_PERIOD = 0x43
    SET_CHANNEL_SEARCH_TIMEOUT = 0x44
    SET_CHANNEL_RF_FREQ = 0x45
    SET_NETWORK_KEY = 0x46
    SET_TRANSMIT_POWER = 0x47
    SET_SEARCH_WAVEFORM = 0x49
    ADD_CHANNEL_ID = 0x59  # Only used for slave channels
    ADD_ENCRYPTION_ID = 0x59  # Only used for encrypted ANT master channels
    CONFIG_LIST = 0x5A  # Only used for slave channels
    CONFIG_ENCRYPTION_LIST = 0x5A  # Only used for encrypted ANT master channels
    SET_CHANNEL_TX_POWER = 0x60
    LOW_PRIORITY_CHANNEL_SEARCH_TIMEOUT = 0x63
    SERIAL_NUMBER_SET_CHANNEL = 0x65
    ENABLE_EXT_RX_MESGS = 0x66
    ENABLE_LED = 0x68
    ENABLE_CRYSTAL = 0x6D
    LIB_CONFIG = 0x6E
    FREQUENCY_AGILITY = 0x70
    PROXIMITY_SEARCH = 0x71
    CONFIG_EVENT_BUFFER = 0x74
    CHANNEL_SEARCH_PRIORITY = 0x75
    SET_128_NETWORK_KEY = 0x76
    HIGH_DUTY_SEARCH = 0x77
    CONFIG_ADVANCED_BURST = 0x78
    CONFIG_EVENT_FILTER = 0x79
    CONFIG_SELECTIVE_DATA_UPDATE = 0x7A
    SET_SDU_MASK = 0x7B
    CONFIG_USER_NVM = 0x7C
    ENABLE_SINGLE_CHANNEL_ENCRYPTION = 0x7D
    SET_ENCRYPTION_KEY = 0x7E
    SET_ENCRYPTION_INFO = 0x7F
    CHANNEL_SEARCH_SHARING = 0x81
    LOAD_STORE_ENCRYPTION_KEY = 0x83
    SET_USB_DESCRIPTOR_STRING = 0xC7
    # SET_USB_INFO = 0xff

    # Notifications
    STARTUP_MESSAGE = 0x6F
    SERIAL_ERROR_MESSAGE = 0xAE

    # Control messags
    RESET_SYSTEM = 0x4A
    OPEN_CHANNEL = 0x4B
    CLOSE_CHANNEL = 0x4C
    REQUEST_MESSAGE = 0x4D
    OPEN_RX_SCAN_MODE = 0x5B
    SLEEP_MESSAGE = 0xC5

    # Data messages
    BROADCAST_DATA = 0x4E
    ACKNOWLEDGED_DATA = 0x4F
    BURST_TRANSFER_DATA = 0x50
    ADVANCED_BURST_TRANSFER_DATA = 0x72

    # Responses (from channel)
    # CHANNEL_EVENT = 0x40
    CHANNEL = 0x40

    # Responses (from REQUEST_MESSAGE, 0x4d)
    CHANNEL_STATUS = 0x52
    CHANNEL_ID = 0x51
    ANT_VERSION = 0x3E
    CAPABILITIES = 0x54
    SERIAL_NUMBER = 0x61
    EVENT_BUFFER_CONFIG = 0x74  # dupe
    ADVANCED_BURST_CAPABILITIES = 0x78  # dupe
    # ADVANCED_BURST_CURRENT_CONFIG = 0x78 # dupe
    EVENT_FILTER = 0x79  # dupe

    # Test mode
    TEST_MODE_CW_INIT = 0x53
    TEST_MODE_CW_TEST = 0x48

    # Extended data messages (legacy)
    LEGACY_EXTENDED_BROADCAST_DATA = 0x5D
    LEGACY_EXTENDED_ACKNOWLEDGED_DATA = 0x5E
    LEGACY_EXTENDED_BURST_DATA = 0x5F


class Code(enum.IntEnum):
    NO_ERROR = 0

    EVENT_RX_SEARCH_TIMEOUT = 1
    EVENT_RX_FAIL = 2
    EVENT_TX = 3
    EVENT_TRANSFER_RX_FAILED = 4
    EVENT_TRANSFER_TX_COMPLETED = 5
    EVENT_TRANSFER_TX_FAILED = 6
    EVENT_CHANNEL_CLOSED = 7
    EVENT_RX_FAIL_GO_TO_SEARCH = 8
    EVENT_CHANNEL_COLLISION = 9
    EVENT_TRANSFER_TX_START = 10

    EVENT_TRANSFER_NEXT_DATA_BLOCK = 17

    CHANNEL_IN_WRONG_STATE = 21
    CHANNEL_NOT_OPENED = 22
    CHANNEL_ID_NOT_SET = 24
    CLOSE_ALL_CHANNELS = 25

    TRANSFER_IN_PROGRESS = 31
    TRANSFER_SEQUENCE_NUMBER_ERROR = 32
    TRANSFER_IN_ERROR = 33

    MESSAGE_SIZE_EXCEEDS_LIMIT = 39
    INVALID_MESSAGE = 40
    INVALID_NETWORK_NUMBER = 41
    INVALID_LIST_ID = 48
    INVALID_SCAN_TX_CHANNEL = 49
    INVALID_PARAMETER_PROVIDED = 51
    EVENT_SERIAL_QUE_OVERFLOW = 52
    EVENT_QUE_OVERFLOW = 53
    ENCRYPT_NEGOTIATION_FAIL = 57
    NVM_FULL_ERROR = 64
    NVM_WRITE_ERROR = 65
    USB_STRING_WRITE_FAIL = 112
    MESG_SERIAL_ERROR_ID = 174

    EVENT_RX_BROADCAST = 1000
    EVENT_RX_FLAG_BROADCAST = 1001
    EVENT_RX_ACKNOWLEDGED = 2000
    EVENT_RX_FLAG_ACKNOWLEDGED = 2001
    EVENT_RX_BURST_PACKET = 3000
    EVENT_RX_FLAG_BURST_PACKET = 3001


class ExtendedAssignment(enum.IntFlag):
    BACKGROUND_SCANNING = 1 << 0
    FREQUENCY_AGILITY = 1 << 2
    FAST_CHANNEL_INITIATION = 1 << 4
    ASYNCHCRONOUS_TRANSMISSION = 1 << 5


class ANTError(Exception):

    def __init__(self, code):
        self.code = code
        super().__init__(f"{code.value}: {code.name}")

'''
class Message:

    SYNC = 0xA4

    def __init__(self, message_type: MessageType, payload: bytes):
        self.message_type = message_type
        self.payload = payload

    def __repr__(self):
        return f"<ant.Message {self.message_type.name}:{self.payload!r}>"

    @property
    def payload_size(self) -> int:
        return len(self.payload)

    @property
    def checksum(self) -> int:
        return self.SYNC ^ self.payload_size ^ self.message_type ^ functools.reduce(lambda x, y: x ^ y, self.payload)

    def __bytes__(self):
        return bytes((self.SYNC, self.payload_size, self.message_type)) + self.payload + bytes((self.checksum,))

    @classmethod
    def from_bytes(cls, buf: bytes) -> "Message":
        """
        Parse a message from an array
        """
        sync, length, message_type = buf[:3]
        payload, checksum = buf[3:-1], buf[-1]

        assert sync == cls.SYNC
        assert length == len(payload)
        assert checksum == functools.reduce(lambda x, y: x ^ y, buf[:-1])

        return Message(MessageType(message_type), payload)
'''


def message_decode(data: bytes, previous_message: dict | None = None) -> dict:
    assert data[0] == SYNC
    message_size = data[1]
    message_type = MessageType(data[2])
    payload = data[3:3+message_size]
    reply = {
        "type": message_type,
        "message_payload": payload,
        "data": data,
        "timestamp": time.time(),
        "previous_timestamp": 0 if previous_message is None else previous_message["timestamp"],
    }
    if message_type == MessageType.ANT_VERSION:
        reply["version"] = payload[:-1].decode()
    elif message_type == MessageType.CAPABILITIES:
        max_channels, max_networks = payload[0:2]
        options = Options.from_buffer(payload, offset=2)
        max_sensorcore_channels = payload[5]
        reply["capabilities"] = Capabilities(max_channels, max_networks, max_sensorcore_channels, options)
    elif message_type == MessageType.CHANNEL:
        reply["channel_id"] = payload[0]
        reply["message_id"] = MessageType(payload[1])
        reply["code"] = Code(payload[2])
    elif message_type == MessageType.BROADCAST_DATA:
        reply["channel_id"] = payload[0]
        reply["payload"] = payload[1:9]
        reply["extended"] = len(payload) > 9 and payload[9] == 0x80
        if reply["extended"]:
            reply["device_number"] = int.from_bytes(payload[10:12], "little")
            reply["device_type"] = DeviceType(payload[12])
            reply["transmission_type"] = payload[13]
            if reply["device_type"] == DeviceType.HeartRate:
                reply["heart_rate"] = heart_rate_decode(reply["payload"], previous_message)
            elif reply["device_type"] == DeviceType.BikeSpeed:
                reply["bike_speed"] = bike_speed_decode(reply["payload"], previous_message)
    return reply


class HeartRatePageType(enum.IntEnum):
    Unknown = 0
    OperatingTime = 1
    ManufacturerSerial = 2
    HardwareSoftware = 3
    PreviousTime = 4
    Swim = 5
    Features = 6
    Battery = 7


def heart_rate_decode(payload, previous_message = None):
    page = HeartRatePageType(payload[0] & 0x0F)
    page_toggle = (payload[0] >> 7) & 0x1
    reply = {
        "page": page,
        "page_nb": page.value,
        "page_toggle": page_toggle,
    }
    if page < 7:
        reply["heart_beat_time"] = int.from_bytes(payload[4:6], byteorder="little") / 1024
        reply["heart_beat_count"] = payload[6]
        reply["heart_rate"] = payload[7]
        if page == HeartRatePageType.OperatingTime:
            reply["operating_time"] = int.from_bytes(payload[1:4], byteorder="little") * 2
        elif page == HeartRatePageType.ManufacturerSerial:
            reply["manufacturer_id"] = payload[1]
            reply["serial_high"] = payload[2:4]
        # background page product info
        elif page == HeartRatePageType.HardwareSoftware:
            reply["hardware_version"] = payload[1]
            reply["software_version"] = payload[2]
            reply["model"] = payload[3]
        elif page == HeartRatePageType.PreviousTime:
            reply["heart_beat_previous_time"] = int.from_bytes(payload[2:4], byteorder="little") / 1024
        # swim interval stuff
        elif page == HeartRatePageType.Swim:
            pass
        elif page == HeartRatePageType.Features:
            reply["features_supported"] = payload[2]
            reply["features_enabled"] = payload[3]
        elif page == HeartRatePageType.Battery:
            reply["battery_percentage"] = payload[1]
            reply["voltage_fractional"] = payload[2] / 256
            reply["voltage_coarse"] = payload[3] & 0x0F
            reply["battery_status"] = BatteryStatus((payload[7] & 0x70) >> 4)
    return reply


def bike_speed_decode(payload):
    page = payload[0] & 0x0F
    page_toggle = (payload[0] >> 7) & 0x1
    reply = {
        "page_nb": page,
        "page_toggle": page_toggle,
    }
    if page < 6:
        reply["wheel_revolutions"] = int.from_bytes(payload[6:8], byteorder="little") / 1024
        reply["time"] = int.from_bytes(payload[4:6], byteorder="little") / 1024
        if page == 1:
            reply["operating_time"] = int.from_bytes(payload[1:4], byteorder="little") * 2
        elif page == 2:
            reply["manufacturer_id"] = payload[1]
            reply["serial_high"] = payload[2:4]
        elif page == 3:
            reply["hardware_version"] = payload[1]
            reply["software_version"] = payload[2]
            reply["model"] = payload[3]
        elif page == 4:
            reply["battery_percentage"] = payload[1]
            reply["voltage_fractional"] = payload[2] / 256
            reply["voltage_coarse"] = payload[3] & 0x0F
            reply["battery_status"] = BatteryStatus((payload[3] & 0x70) >> 4)
        elif page == 5:
            reply["stopped"] = bool(payload[1] & 0x1)


def message(message_type: MessageType, payload: bytes):
    size = len(payload)
    checksum = SYNC ^ size ^ message_type ^ functools.reduce(lambda x, y: x ^ y, payload)
    return bytes((SYNC, size, message_type)) + payload + bytes((checksum,))


def raise_for_status(message_type, payload):
    if message_type == MessageType.CHANNEL:
        code = Code(payload[2])
        if code != Code.NO_ERROR:
            raise ANTError(code)
    return message_type, payload


async def read_packet(serial) -> bytes:
    data = await serial.read(3)
    assert data[0] == SYNC
    data += await serial.read(data[1] + 1)
    logging.debug(f"READ: %s", data)
    return data


async def read_message(serial) -> tuple[MessageType, bytes]:
    data = await read_packet(serial)
    message_type = MessageType(data[2])
    payload = data[3:-1]
    checksum = data[-1]
    assert checksum == functools.reduce(lambda x, y: x ^ y, data[:-1])
    logging.info(f"READ: {message_type.name}(0x{message_type.value:x}) {payload=}")
    return raise_for_status(message_type, payload)


async def write_message(serial, message_type: MessageType, payload: bytes):
    logging.info(f"WRITE: {message_type.name}(0x{message_type.value:x}) {payload=}")
    data = message(message_type, payload)
    logging.debug(f"WRITE: %s", data)
    return await serial.write(data)


async def write_read_message(serial, message_type: MessageType, payload: bytes) -> tuple[MessageType, bytes]:
    await write_message(serial, message_type, payload)
    return await read_message(serial)


async def request(serial, message_id, channel=0):
    return await write_read_message(serial, MessageType.REQUEST_MESSAGE, bytes([channel, message_id]))


async def reset(serial):
    message_type, payload = await write_read_message(serial, MessageType.RESET_SYSTEM, b'\x00')
    start = time.monotonic()
    # Discard eventual broadcast messages that may be inbound while we send the reset command
    while message_type != MessageType.STARTUP_MESSAGE and time.monotonic() - start < 0.5:
        message_type, payload = await read_message(serial)
    dt = time.monotonic() - start
    if dt < 0.5:
        await asyncio.sleep(0.5 - dt)
    return ResetType(payload[0])


async def set_network_key(serial, network=0x00, key=ANTPLUS_NETWORK_KEY):
    await write_read_message(serial, MessageType.SET_NETWORK_KEY, bytes([network]) + key)


async def assign_channel(serial, channel_number: int, channel_type: ChannelType, network_number, ext_assign: ExtendedAssignment = ExtendedAssignment(0)):
    payload = [channel_number, channel_type, network_number]
    if ext_assign:
        payload.append(ext_assign)
    return await write_read_message(serial, MessageType.ASSIGN_CHANNEL, bytes(payload))


async def set_channel_id(serial, channel_number: int, device_number: int, device_type: DeviceType, transmission_type = 0):
    payload = (bytes((channel_number,)), device_number.to_bytes(2, "little"), bytes((device_type, transmission_type)))
    return await write_read_message(serial, MessageType.SET_CHANNEL_ID, b"".join(payload))
    

async def set_channel_extended_messages(serial, channel_number: int, enable: bool | int):
    return await write_read_message(serial, MessageType.ENABLE_EXT_RX_MESGS, bytes((channel_number, int(enable))))


async def set_channel_period(serial, channel_number: int, period: int):
    """period in ticks"""
    payload = (bytes((channel_number,)), period.to_bytes(2, "little"))
    return await write_read_message(serial, MessageType.SET_CHANNEL_PERIOD, b"".join(payload))


async def set_channel_period_seconds(serial, channel_number: int, period: float):
    """period in seconds"""
    return await set_channel_period(serial, channel_number, int(period * 32768))


async def set_channel_rf_frequency(serial, channel_number: int, frequency: int):
    """frequency in raw units"""
    if 0 <= frequency <= 124:
        payload = bytes((channel_number, frequency))
        return await write_read_message(serial, MessageType.SET_CHANNEL_RF_FREQ, payload)
    raise ValueError("Frequency must be in range [0, 124]")


async def set_channel_rf_frequency_mhz(serial, channel_number: int, frequency: int = 2466):
    """frequency in MHz"""
    if 2400 <= frequency <= 2524:
        frequency -= 2400
        return await set_channel_rf_frequency(serial, channel_number, frequency)
    raise ValueError("Frequency must be in range [2400, 2524] MHz")


async def set_channel_search_timeout(serial, channel_number: int, timeout: int | None):
    """timeout in in raw units"""
    if timeout is None:
        timeout = 0xFF
    if 0 <= timeout <= 255:
        payload = bytes((channel_number, timeout))
        return await write_read_message(serial, MessageType.SET_CHANNEL_SEARCH_TIMEOUT, payload)
    raise ValueError("Timeout out of range None or [0, 637.5] seconds")


async def set_channel_search_timeout_seconds(serial, channel_number: int, timeout: float | None = 25.0):
    """timeout in seconds"""
    if timeout is None:
        timeout = 0xFF
    else:
        timeout = int(timeout / 2.5)
    if 0 <= timeout <= 255:
        payload = bytes((channel_number, timeout))
        return await write_read_message(serial, MessageType.SET_CHANNEL_SEARCH_TIMEOUT, payload)
    raise ValueError("Timeout out of range None or [0, 637.5] seconds")



async def open_channel(serial, channel_number: int):
    return await write_read_message(serial, MessageType.OPEN_CHANNEL, bytes((channel_number,)))


async def close_channel(serial, channel_number: int):
    return await write_read_message(serial, MessageType.CLOSE_CHANNEL, bytes((channel_number,)))


#                   adv. 4   adv. 3  rcore     adv. 2     adv. standard
OPTIONS_MASK = 0b_00000001_11011111_00000000_11110111_11111010_00111111


class Options(enum.IntFlag):
    NoRxChannels = 1 << 0
    NoTxChannels = 1 << 1
    NoRxMessages = 1 << 2
    NoTxMessages = 1 << 3
    NoAckMessages = 1 << 4
    NoBurstMessages = 1 << 5

    Network = 1 << (8 + 1)
    SerialNumber = 1 << (8 + 3)
    PerChannelTxPower = 1 << (8 + 4)
    LowPrioritySearch = 1 << (8 + 5)
    Script = 1 << (8 + 6)
    SearchList = 1 << (8 + 7)

    Led = 1 << (16 + 0)
    ExtMessage = 1 << (16 + 1)
    ScanMode = 1 << (16 + 2)
    ProximitySearch = 1 << (16 + 4)
    ExtAssign = 1 << (16 + 5)
    FsAntFs = 1 << (16 + 6)
    Fit1 = 1 << (16 + 7)

    AdvancedBurst = 1 << (24 + 0)
    EventBuffering = 1 << (24 + 0)
    EventFiltering = 1 << (24 + 1)
    HighDutySearch = 1 << (24 + 2)
    SearchSharing = 1 << (24 + 4)
    SelectiveDataUpdate = 1 << (24 + 6)
    EncryptedChannel = 1 << (24 + 7)

    RFActiveNotification = 1 << (32 + 0)

    @classmethod
    def from_buffer(cls, data, offset=0):
        return cls(int.from_bytes(data[offset:], "little") & OPTIONS_MASK)


class Capabilities:

    def __init__(self, max_channels, max_networks, max_sensorcore_channels, options):
        self.max_channels = max_channels
        self.max_networks = max_networks
        self.max_sensorcore_channels = max_sensorcore_channels
        self.options = options


class Channel:
    """
    ANT+ device channel
    """
    
    def __init__(self, device: "Device", channel_number: int):
        self.device = device
        self.channel_number = channel_number
        self.assigned = False
    
    def __int__(self) -> int:
        return self.channel_number

    async def assign(self, channel_type: ChannelType, network_number: int = 0, ext_assign = ExtendedAssignment.BACKGROUND_SCANNING):
        """Assign the channel"""
        if self.assigned:
            raise RuntimeError(f"Channel {self.channel_number} is already assigned. Unassign first")
        return await assign_channel(self.device.serial, self.channel_number, channel_type, network_number, ext_assign)
    
    async def set_id(self, device_number: int, device_type: DeviceType, transmission_type = 0):
        """Set the channel to a device type"""
        return await set_channel_id(self.device.serial, self.channel_number, device_number, device_type, transmission_type)

    async def set_extended_messages(self, enable: bool | int):
        """Enable/disable extended messages"""
        return await set_channel_extended_messages(self.device.serial, self.channel_number, enable)

    async def set_period(self, period: int):
        """Set channel period"""
        return await set_channel_period(self.device.serial, self.channel_number, period)
    
    async def set_period_seconds(self, period: float):
        """Set channel period"""
        return await set_channel_period_seconds(self.device.serial, self.channel_number, period)

    async def set_rf_frequency(self, frequency: int):
        """Set channel Radio Frequency frequency"""
        return await set_channel_rf_frequency(self.device.serial, self.channel_number, frequency)
    
    async def set_rf_frequency_mhz(self, frequency: int):
        """Set channel Radio Frequency frequency in MHz"""
        return await set_channel_rf_frequency_mhz(self.device.serial, self.channel_number, frequency)

    async def set_search_timeout(self, timeout: int):
        return await set_channel_search_timeout(self.device.serial, self.channel_number, timeout)

    async def set_search_timeout_seconds(self, timeout: float):
        return await set_channel_search_timeout_seconds(self.device.serial, self.channel_number, timeout)
    
    async def open(self):
        """Open the channel"""
        return await open_channel(self.device.serial, self.channel_number)

    async def close(self):
        """Close the channel"""
        return await close_channel(self.device.serial, self.channel_number)


class Device:

    def __init__(self, url):
        self.serial = serialio.serial_for_url(url, baudrate=115200)
        #self.capabilities : Capabilities | None = None
        #self.channels: list[Channel] = []

    async def open(self):
        await self.serial.open()

    async def close(self):
        await self.serial.close()

    async def __aenter__(self):
        await self.open()
        return self
    
    async def __aexit__(self, *_):
        await self.close()

    @property
    def url(self):
        return self.serial.port
    
    async def request(self, message_id, channel=0):
        return await request(self.serial, message_id, channel)

    async def reset(self):
        return await reset(self.serial)

    async def set_network_key(self, network=0, key=ANTPLUS_NETWORK_KEY):
        return await set_network_key(self.serial, network, key)

    async def get_capabilities(self):
        _, caps = await self.request(MessageType.CAPABILITIES)
        max_channels, max_networks = caps[0:2]
        options = Options.from_buffer(caps, offset=2)
        max_sensorcore_channels = caps[5]
        return Capabilities(max_channels, max_networks, max_sensorcore_channels, options)

    async def get_serial_number(self) -> int:
        _, serial_number = await self.request(MessageType.SERIAL_NUMBER)
        return int.from_bytes(serial_number, 'little')

    async def get_ant_version(self) -> str:
        _, version = await self.request(MessageType.ANT_VERSION)
        return version[:-1].decode()

    async def __aiter__(self):
        msg = None
        while True:
            packet = await read_packet(self.serial)
            yield message_decode(packet, msg)


class HeartRate:

    #             ~4.06Hz ~2.03Hz ~1.02Hz
    VALID_PERIODS = [8070, 2*8070, 4*8070]
    RF_FREQUENCY = 57  # 2457 MHz
    DEFAULT_PERIOD = 8070

    def __init__(self, device, device_number: int = 0):
        self.device = device
        self.device_number = device_number
        self.channel = None

    async def __aenter__(self):
        await self.open()
        return self
    
    async def __aexit__(self, *_):
        await self.close()

    async def open(self):
        channel = Channel(self.device, 0)
        await channel.assign(ChannelType.BIDIRECTIONAL_RECEIVE, 0)
        await channel.set_search_timeout(None)
        await channel.set_id(self.device_number, DeviceType.HeartRate, 0)
        await channel.set_extended_messages(True)
        await channel.set_period(self.DEFAULT_PERIOD)
        await channel.set_rf_frequency(self.RF_FREQUENCY)
        await channel.open()
        self.channel = channel

    async def close(self):
        if self.channel:
            await self.channel.close()


class BikeSpeed:

    #             ~4.04Hz ~2.02Hz ~1.12Hz
    VALID_PERIODS = [8118, 2*8118, 4*8118]
    RF_FREQUENCY = 57  # 2457 MHz
    DEFAULT_PERIOD = 8118

    def __init__(self, device, device_number: int = 0):
        self.device = device
        self.device_number = device_number
        self.channel = None

    async def __aenter__(self):
        await self.open()
        return self
    
    async def __aexit__(self, *_):
        await self.close()

    async def open(self):
        channel = Channel(self.device, 0)
        await channel.assign(ChannelType.BIDIRECTIONAL_RECEIVE, 0)
        await channel.set_search_timeout(None)
        await channel.set_id(self.device_number, DeviceType.BikeSpeed, 0)
        await channel.set_extended_messages(True)
        await channel.set_period(self.DEFAULT_PERIOD)
        await channel.set_rf_frequency(self.RF_FREQUENCY)
        await channel.open()
        self.channel = channel

    async def close(self):
        if self.channel:
            await self.channel.close()

def iter_paths():
    for item in SYS_USB_SERIAL_DEVICES_PATH.iterdir():
        path = item.resolve().parent.parent
        with (path / "idVendor").open() as fobj:
            vendor_id = int(fobj.read(), 16)
        products = VENDORS[vendor_id]
        if not products:
            continue
        with (path / "idProduct").open() as fobj:
            product_id = int(fobj.read(), 16)
        if product_id not in products:
            continue
        yield pathlib.Path("/dev") / item.stem


def iter_devices():
    for path in iter_paths():
        yield Device(f"serial://{path}")


def find(find_all=False, custom_match=None, **kwargs):
    idevs = iter_devices()
    if kwargs or custom_match:
        def accept(dev):
            result = all(getattr(dev, key) == value for key, value in kwargs.items())
            if result and custom_match:
                return custom_match(dev)
            return result

        idevs = filter(accept, idevs)
    return idevs if find_all else next(idevs, None)


if __name__ == "__main__":
    fmt = "%(threadName)-10s %(asctime)-15s %(levelname)-5s %(name)s: %(message)s"
    logging.basicConfig(level='INFO', format=fmt)

    async def init():
        ant = find()
        hr = HeartRate(ant, 0)
        await ant.open()
        await ant.reset()
        await ant.get_capabilities()
        await ant.set_network_key()
        await ant.get_serial_number()
        await ant.get_ant_version()

        await hr.open()
        return ant, hr
