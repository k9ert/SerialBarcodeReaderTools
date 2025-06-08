import struct
import binascii
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from base_scanner import BaseScanner
from utils import compute_bcc, check_bcc


# ------------------------
# M3Y-W Scanner
# ------------------------
class M3YWScanner(BaseScanner):
    def __init__(self, serial_port):
        super().__init__(serial_port)

    def tx_header(self):
        return binascii.unhexlify('5a00')

    def compute_checksum(self, data: bytes) -> bytes:
        return compute_bcc(data)

    def check_checksum(self, data: bytes) -> bool:
        return check_bcc(data)

    def header_ok(self):
        return b'5a01'

    def rx_struct_fmt(self):
        return ">2sH"

    def etx_bytes(self):
        return binascii.unhexlify('a5')

    def create_tx(self, command: bytes, value: bytes = b'') -> bytes:
        # Value not used here in this reader
        command_len = len(command).to_bytes(2, byteorder='big')
        raw_data = self.tx_header() + command_len + command
        checksum = self.compute_checksum(command_len + command)
        return raw_data + checksum + self.etx_bytes()

    def parse_rx(self, data: bytes):
        header_len = struct.calcsize(self.rx_struct_fmt())
        try:
            header, data_len = struct.unpack(self.rx_struct_fmt(), data[:header_len])
        except struct.error:
            return None, b''

        if header.hex() in self.header_ok().decode():
            if self.check_checksum(data[header_len - 3:header_len + data_len + 1]):
                return data[header_len:header_len + data_len], data[header_len + data_len + 2:]
        return None, b''

    # Command functions for M3YW that directly create the command and send
    def cmd_get_sw_version(self):
        command = b'T_OUT_CVER'
        return self.send_and_parse(self.create_tx(command))

    def cmd_set_continuous_mode(self):
        command = b'S_CMD_020E'
        return self.send_and_parse(self.create_tx(command))

    def cmd_set_command_mode(self):
        command = b'S_CMD_020D'
        return self.send_and_parse(self.create_tx(command))

    # Command functions for M3YW that directly create the command and send
    # Always Off  S_CMD_03L0 (Value = -1)
    # Normal Mode S_CMD_03L2 (Value = 0)
    # Always On   S_CMD_03L1 (Value = 1)
    def cmd_set_illumination(self, value: int = 0):
        if value < 0:
            command = b'S_CMD_03L0'
        elif value == 0:
            command = b'S_CMD_03L2'
        elif value > 0:
            command = b'S_CMD_03L1'
        return self.send_and_parse(self.create_tx(command))

    # Always Off  S_CMD_03A0 (Value = -1)
    # Normal Mode S_CMD_03A2 (Value = 0)
    # Always On S_CMD_03A1 (Value = 1)
    def cmd_set_aimer(self, value: int = 0):
        if value < 0:
            command = b'S_CMD_03A0'
        elif value == 0:
            command = b'S_CMD_03A2'
        elif value > 0:
            command = b'S_CMD_03A1'

        return self.send_and_parse(self.create_tx(command))

    # Mute all        S_CMD_04F0 (Value = -1)
    # Unmute all      S_CMD_04F1 (Value = 1)
    def cmd_set_beeper(self, value: int = 0):
        if value < 0:
            command = b'S_CMD_04F0'
        elif value == 0:
            raise NotImplementedError
        elif value > 0:
            command = b'S_CMD_04F1'
        return self.send_and_parse(self.create_tx(command))

    def cmd_set_read_interval(self, value: float = 0):
        command = b'S_CMD_MARR' + str(round(value*1000)).encode()
        return self.send_and_parse(self.create_tx(command))

    def cmd_set_same_barcode_delay(self, value: float = 0):
        command = b'S_CMD_MA31'
        self.send_and_parse(self.create_tx(command))
        command = b'S_CMD_MA41'
        self.send_and_parse(self.create_tx(command))
        command = b'S_CMD_MARI' + str(round(value*1000)).encode()
        return self.send_and_parse(self.create_tx(command))

    def cmd_send_raw(self, value: str = ''):
        command = value.encode()
        return self.send_and_parse(self.create_tx(command))

    def cmd_set_baudrate(self, value: int = 9600):
        command = b'S_CMD_H3BR' + str(value).encode()
        reply, extra = self.send_and_parse(self.create_tx(command, value))
        self.serial_port.baudrate = value
        # Test to see if everything worked...
        reply, extra = self.cmd_get_sw_version()
        if reply:
            return True, None
        else:
            return False, None

    def get_safe_for_binaryqr(self):
        return True
