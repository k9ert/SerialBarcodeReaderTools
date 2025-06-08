import binascii
import sys
import os
from abc import ABC, abstractmethod

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from utils import common_baud_rates


# Custom exceptions
class NotSupportedError(Exception):
    """Raised when a feature is not supported by the specific scanner model."""
    pass


# ------------------------
# Abstract Scanner Class
# ------------------------
class BaseScanner(ABC):
    def __init__(self, serial_port):
        self.serial_port = serial_port
        self.commands = {}

    @abstractmethod
    def tx_header(self) -> bytes:
        pass

    @abstractmethod
    def compute_checksum(self, data: bytes) -> bytes:
        pass

    @abstractmethod
    def check_checksum(self, data: bytes) -> bool:
        pass

    @abstractmethod
    def header_ok(self) -> bytes:
        pass

    @abstractmethod
    def rx_struct_fmt(self) -> str:
        pass

    @abstractmethod
    def create_tx(self, command: bytes, value: bytes = b'') -> bytes:
        pass

    @abstractmethod
    def parse_rx(self, data: bytes):
        pass

    @abstractmethod
    def cmd_send_raw(self, value: str = ''):
        pass

    @abstractmethod
    def cmd_set_baudrate(self, value: int = 9600):
        pass

    @abstractmethod
    def get_safe_for_binaryqr(self):
        pass

    def etx_bytes(self) -> bytes:
        pass

    def send_and_parse(self, tx_data):
        print("Sent (Raw):", tx_data, "AsHex:", binascii.hexlify(tx_data))
        self.serial_port.write(tx_data)

        # Give device time to respond
        import time
        time.sleep(0.1)

        rx_data = self.serial_port.read(1024)
        print("Got (Raw):", rx_data, "AsHex:", binascii.hexlify(rx_data))
        print(f"Received {len(rx_data)} bytes")

        if len(rx_data) > 0:
            print("Raw bytes:", [hex(b) for b in rx_data])

        reply, extra = self.parse_rx(rx_data)
        if reply:
            print("Reply:", reply, "AsHex:", binascii.hexlify(reply))
            print("Extra:", extra, "AsHex:", binascii.hexlify(extra))
        else:
            print("Parse failed - no valid reply extracted")
        return reply, extra

    # Placeholder command methods
    def cmd_get_hw_version(self):
        raise NotImplementedError("cmd_get_hw_version not implemented for this reader")

    def cmd_get_sw_version(self):
        raise NotImplementedError("cmd_get_sw_version not implemented for this reader")

    def cmd_get_sw_year(self):
        raise NotImplementedError("cmd_get_sw_year not implemented for this reader")

    def cmd_get_settings(self):
        raise NotImplementedError("cmd_get_settings not implemented for this reader")

    def cmd_set_settings(self, value: bytes = b''):
        raise NotImplementedError("cmd_set_settings not implemented for this reader")

    def cmd_save_settings(self):
        raise NotImplementedError("cmd_save_settings not implemented for this reader")

    def cmd_set_continuous_mode(self):
        raise NotImplementedError("cmd_set_continuous_mode not implemented for this reader")

    def cmd_set_command_mode(self):
        raise NotImplementedError("cmd_set_command_mode not implemented for this reader")

    def cmd_set_illumination(self, value: int = 0):
        raise NotImplementedError("cmd_set_illumination not implemented for this reader")

    def cmd_set_aimer(self, value: int = 0):
        raise NotImplementedError("cmd_set_aimer not implemented for this reader")

    def cmd_set_beeper(self, value: int = 0):
        raise NotImplementedError("cmd_set_beeper not implemented for this reader")

    def cmd_set_read_interval(self, value: float = 0):
        raise NotImplementedError("cmd_set_read_interval not implemented for this reader")

    def cmd_set_same_barcode_delay(self, value: float = 0):
        raise NotImplementedError("cmd_set_same_barcode_delay not implemented for this reader")

    def test_baudrates(self):
        for baudrate in common_baud_rates + list(reversed(common_baud_rates)):
            works, _ = self.cmd_set_baudrate(int(baudrate))
            if works:
                print(baudrate, "Success")
            else:
                print(baudrate, "Failed")

    def find_baudrate(self):
        for baudrate in common_baud_rates:
            print("Checking at...", baudrate)
            self.serial_port.baudrate = int(baudrate)
            reply, _ = self.cmd_get_sw_version()
            if reply:
                return baudrate

        return None
