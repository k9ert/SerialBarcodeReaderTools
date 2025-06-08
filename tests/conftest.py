import pytest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gm65_scanner import GM65Scanner


@pytest.fixture
def real_serial_port():
    """Fixture for real serial port testing (requires actual hardware)."""
    import serial
    try:
        port = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        yield port
        port.close()
    except (serial.SerialException, FileNotFoundError):
        pytest.skip("Real serial port /dev/ttyACM0 not available")


@pytest.fixture
def real_gm65_scanner(real_serial_port):
    """Create a GM65Scanner instance with real serial port."""
    return GM65Scanner(real_serial_port)
