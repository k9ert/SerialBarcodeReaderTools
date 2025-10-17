import pytest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gm65_scanner import GM65Scanner
from m3yw_scanner import M3YWScanner


@pytest.fixture
def real_serial_port():
    """Fixture for real serial port testing (requires actual hardware)."""
    import serial
    import glob
    import binascii

    # Try common serial port patterns
    port_patterns = [
        '/dev/ttyACM0',           # Linux
        '/dev/tty.usbmodem*',     # macOS (GM65)
        '/dev/tty.usbserial*',    # macOS (other USB serial)
        '/dev/cu.usbmodem*',      # macOS (alternative)
        '/dev/cu.usbserial*',     # macOS (alternative)
    ]

    for pattern in port_patterns:
        ports = glob.glob(pattern)
        for port_name in ports:
            try:
                port = serial.Serial(port_name, 9600, timeout=1)

                # Test if this port has a responding scanner
                # Send GM65 software version command
                cmd = b'~\x00\x07\x01\x00\xe2\x01w\x91'
                port.write(cmd)
                import time
                time.sleep(0.2)
                response = port.read(1024)

                if response:
                    print(f"\n✓ Connected to scanner on {port_name}")
                    print(f"  Response: {binascii.hexlify(response).decode()}")
                    yield port
                    port.close()
                    return
                else:
                    port.close()
            except (serial.SerialException, FileNotFoundError):
                continue

    pytest.skip("No responding barcode scanner found. Tried: " + ", ".join(port_patterns))


@pytest.fixture
def real_gm65_scanner(real_serial_port):
    """Create a GM65Scanner instance with real serial port."""
    return GM65Scanner(real_serial_port)


@pytest.fixture
def real_m3yw_scanner():
    """Create a M3YWScanner instance with real serial port (M3Y-W specific)."""
    import serial
    import glob
    import binascii
    import time

    # Try common serial port patterns
    port_patterns = [
        '/dev/ttyACM0',           # Linux
        '/dev/tty.usbmodem*',     # macOS (M3Y-W)
        '/dev/tty.usbserial*',    # macOS (other USB serial)
        '/dev/cu.usbmodem*',      # macOS (alternative)
        '/dev/cu.usbserial*',     # macOS (alternative)
    ]

    for pattern in port_patterns:
        ports = glob.glob(pattern)
        for port_name in ports:
            try:
                port = serial.Serial(port_name, 9600, timeout=1)

                # Test if this port has a responding M3Y-W scanner
                # Send M3Y-W software version command
                cmd = b'S_CMD_GVER'
                bcc = 0
                for byte in cmd:
                    bcc ^= byte
                full_cmd = b'\x5a\x00' + cmd + bytes([bcc]) + b'\xa5'

                port.write(full_cmd)
                time.sleep(0.2)
                response = port.read(1024)

                if response:
                    print(f"\n✓ Connected to M3Y-W scanner on {port_name}")
                    print(f"  Response: {binascii.hexlify(response).decode()}")
                    yield port
                    port.close()
                    return
                else:
                    port.close()
            except (serial.SerialException, FileNotFoundError):
                continue

    pytest.skip("No responding M3Y-W barcode scanner found. Tried: " + ", ".join(port_patterns))
