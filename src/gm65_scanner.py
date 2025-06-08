import struct
import binascii
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from base_scanner import BaseScanner
from utils import compute_crc16_xmodem, check_crc16_xmodem, set_bit, clear_bit


# ------------------------
# GM65 Scanner
# ------------------------
class GM65Scanner(BaseScanner):
    def __init__(self, serial_port):
        super().__init__(serial_port)

    def tx_header(self):
        return binascii.unhexlify('7e00')

    def compute_checksum(self, data: bytes) -> bytes:
        return compute_crc16_xmodem(data)

    def check_checksum(self, data: bytes) -> bool:
        return check_crc16_xmodem(data)

    def header_ok(self):
        return b'020000'

    def rx_struct_fmt(self):
        return "3sB"

    def create_tx(self, command: bytes, value: bytes = b'') -> bytes:
        raw_data = self.tx_header() + command + value
        checksum = self.compute_checksum(command + value)
        return raw_data + checksum

    def parse_rx(self, data: bytes):
        header_len = struct.calcsize(self.rx_struct_fmt())
        try:
            header, data_len = struct.unpack(self.rx_struct_fmt(), data[:header_len])
        except struct.error:
            return None, b''

        if header.hex() in self.header_ok().decode():
            if self.check_checksum(data[1:header_len + data_len + 2]):
                return data[header_len:header_len + data_len], data[header_len + data_len + 2:]
        return None, b''

    # Command functions for GM65 that directly create the command and send
    def cmd_get_hw_version(self):
        command = binascii.unhexlify('070100e101')
        return self.send_and_parse(self.create_tx(command))

    def cmd_get_sw_version(self):
        command = binascii.unhexlify('070100e201')
        return self.send_and_parse(self.create_tx(command))

    def cmd_get_sw_year(self):
        command = binascii.unhexlify('070100e301')
        return self.send_and_parse(self.create_tx(command))

    def cmd_get_settings(self):
        command = binascii.unhexlify('0701000001')
        return self.send_and_parse(self.create_tx(command))

    def cmd_set_settings(self, value: bytes = b''):
        command = binascii.unhexlify('08010000')
        return self.send_and_parse(self.create_tx(command, value))

    def cmd_get_address(self, address: bytes):
        command = binascii.unhexlify(b'0701' + address + b'01')
        return self.send_and_parse(self.create_tx(command))

    def cmd_set_address(self, address: bytes, value: bytes):
        command = binascii.unhexlify(b'0801' + address)
        return self.send_and_parse(self.create_tx(command, binascii.unhexlify(value)))

    def cmd_save_address(self, address: bytes):
        command = binascii.unhexlify(b'0901' + address + b'00')
        return self.send_and_parse(self.create_tx(command))

    def cmd_save_settings(self):
        command = binascii.unhexlify('0901000000')
        return self.send_and_parse(self.create_tx(command))

    def cmd_set_continuous_mode(self):
        settings, extra = self.cmd_get_settings()
        settings_int = settings[0]
        settings_int = set_bit(settings_int, 1)
        settings_int = clear_bit(settings_int, 0)
        self.cmd_set_settings(bytes([settings_int]))
        self.cmd_save_settings()
        return True, None

    def cmd_set_command_mode(self):
        settings, extra = self.cmd_get_settings()
        settings_int = settings[0]
        settings_int = set_bit(settings_int, 0)
        settings_int = clear_bit(settings_int, 1)
        self.cmd_set_settings(bytes([settings_int]))
        self.cmd_save_settings()
        return True, None

    # Always Off   (Value = -1)
    # Normal Mode  (Value = 0)
    # Always On    (Value = 1)
    def cmd_set_illumination(self, value: int = 0):
        settings, extra = self.cmd_get_settings()
        settings_int = settings[0]
        if value < 0:
            settings_int = clear_bit(settings_int, 3)
            settings_int = clear_bit(settings_int, 2)
        elif value == 0:
            settings_int = set_bit(settings_int, 2)
            settings_int = clear_bit(settings_int, 3)
        elif value > 0:
            settings_int = set_bit(settings_int, 3)
            settings_int = set_bit(settings_int, 2)
        self.cmd_set_settings(bytes([settings_int]))
        self.cmd_save_settings()
        return True, None

    # Always Off   (Value = -1)
    # Normal Mode  (Value = 0)
    # Always On    (Value = 1)
    def cmd_set_aimer(self, value: int = 0):
        settings, extra = self.cmd_get_settings()
        settings_int = settings[0]
        if value < 0:
            settings_int = clear_bit(settings_int, 5)
            settings_int = clear_bit(settings_int, 4)
        elif value == 0:
            settings_int = set_bit(settings_int, 4)
            settings_int = clear_bit(settings_int, 5)
        elif value > 0:
            settings_int = set_bit(settings_int, 5)
            settings_int = set_bit(settings_int, 4)
        self.cmd_set_settings(bytes([settings_int]))
        self.cmd_save_settings()
        return True, None

    # Muted  (Value = -1)
    # On     (Value = 1)
    def cmd_set_beeper(self, value: int = 0):
        settings, extra = self.cmd_get_settings()
        settings_int = settings[0]
        if value < 0:
            settings_int = clear_bit(settings_int, 6)
        elif value == 0:
            raise NotImplementedError
        elif value > 0:
            settings_int = set_bit(settings_int, 6)
        self.cmd_set_settings(bytes([settings_int]))
        self.cmd_save_settings()
        return True, None

    def cmd_set_read_interval(self, value: float = 0):
        command = binascii.unhexlify('08010005')
        value = (round(value * 10)).to_bytes(1)
        return self.send_and_parse(self.create_tx(command, value))

    def cmd_set_same_barcode_delay(self, value: float = 0):
        if value > 12.7: # Value needs to be below 12.7s as bit7 is used for enable/disable the feature
            raise ValueError
        command = binascii.unhexlify('08010013')
        value = (round(value * 10)).to_bytes(1)
        value = set_bit(value[0], 7)
        return self.send_and_parse(self.create_tx(command, bytes([value])))

    def cmd_send_raw(self, value: str = ''):
        command = binascii.unhexlify(value)
        return self.send_and_parse(self.create_tx(command))

    def cmd_set_baudrate(self, value: int = 9600):
        baudvalues = { # Note that byte order here is reversed compared to what is in the datasheet...
            9600: b'3901',
            14400: b'd000',
            19200: b'9c00',
            38400: b'4e00',
            57600: b'3400',
            115200: b'1a00'
        }
        command = binascii.unhexlify('0802002A')
        reply, extra = self.send_and_parse(self.create_tx(command, binascii.unhexlify(baudvalues[value])))
        self.serial_port.baudrate = value
        # Test to see if everything worked...
        reply, extra = self.cmd_get_sw_version()
        if reply:
            return True, None
        else:
            return False, None

    def get_safe_for_binaryqr(self):
        gm65_known_bad_sw_versions = [b'69'] # Versions known to scan binaryQR codes unreliably
        gm65_known_good_sw_version = [b'87', b'af'] # Versions known to be work correctly
        version, extra = self.cmd_get_sw_version()
        version = binascii.hexlify(version)
        print("Got Software Version:", version, "Checking...")
        if version in gm65_known_bad_sw_versions:
            return False
        elif version in gm65_known_good_sw_version:
            return True
        else:
            return None
