import pytest
import binascii
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils import (
    compute_crc16_xmodem, 
    check_crc16_xmodem,
    compute_bcc,
    check_bcc,
    set_bit,
    clear_bit,
    toggle_bit,
    check_bit,
    common_baud_rates
)


class TestCRC16Functions:
    """Test CRC16-XMODEM functions."""

    def test_compute_crc16_xmodem(self):
        """Test CRC16-XMODEM computation."""
        # Test with known data
        data = binascii.unhexlify('070100e201')
        crc = compute_crc16_xmodem(data)
        
        assert len(crc) == 2
        assert isinstance(crc, bytes)
        
        # Test with empty data
        empty_crc = compute_crc16_xmodem(b'')
        assert len(empty_crc) == 2

    def test_check_crc16_xmodem_valid(self):
        """Test CRC16 validation with valid data."""
        # Known good data with valid CRC
        data_with_crc = binascii.unhexlify('070100e2017791')
        assert check_crc16_xmodem(data_with_crc) is True

    def test_check_crc16_xmodem_invalid(self):
        """Test CRC16 validation with invalid data."""
        # Data with wrong CRC
        data_with_bad_crc = binascii.unhexlify('070100e201ffff')
        assert check_crc16_xmodem(data_with_bad_crc) is False

    def test_check_crc16_xmodem_too_short(self):
        """Test CRC16 validation with too short data."""
        short_data = b'ab'
        assert check_crc16_xmodem(short_data) is False

    def test_crc16_roundtrip(self):
        """Test CRC16 computation and validation roundtrip."""
        test_data = b'Hello, World!'
        crc = compute_crc16_xmodem(test_data)
        data_with_crc = test_data + crc
        
        assert check_crc16_xmodem(data_with_crc) is True


class TestBCCFunctions:
    """Test Block Check Character (BCC) functions."""

    def test_compute_bcc(self):
        """Test BCC computation."""
        data = b'test'
        bcc = compute_bcc(data)
        
        assert len(bcc) == 1
        assert isinstance(bcc, bytes)
        
        # Manual calculation: t(0x74) ^ e(0x65) ^ s(0x73) ^ t(0x74) = 0x06
        expected = bytes([0x74 ^ 0x65 ^ 0x73 ^ 0x74])
        assert bcc == expected

    def test_compute_bcc_empty(self):
        """Test BCC computation with empty data."""
        bcc = compute_bcc(b'')
        assert bcc == bytes([0])

    def test_check_bcc_valid(self):
        """Test BCC validation with valid data."""
        data = b'test'
        bcc = compute_bcc(data)
        data_with_bcc = data + bcc
        
        assert check_bcc(data_with_bcc) is True

    def test_check_bcc_invalid(self):
        """Test BCC validation with invalid data."""
        data_with_bad_bcc = b'test\xff'
        assert check_bcc(data_with_bad_bcc) is False

    def test_check_bcc_too_short(self):
        """Test BCC validation with too short data."""
        short_data = b'a'
        assert check_bcc(short_data) is False

    def test_bcc_roundtrip(self):
        """Test BCC computation and validation roundtrip."""
        test_data = b'Hello, BCC!'
        bcc = compute_bcc(test_data)
        data_with_bcc = test_data + bcc
        
        assert check_bcc(data_with_bcc) is True


class TestBitOperations:
    """Test bit manipulation functions."""

    def test_set_bit(self):
        """Test setting bits."""
        value = 0b00000000
        
        # Set bit 0
        result = set_bit(value, 0)
        assert result == 0b00000001
        
        # Set bit 7
        result = set_bit(value, 7)
        assert result == 0b10000000
        
        # Set bit that's already set
        value = 0b00000001
        result = set_bit(value, 0)
        assert result == 0b00000001

    def test_clear_bit(self):
        """Test clearing bits."""
        value = 0b11111111
        
        # Clear bit 0
        result = clear_bit(value, 0)
        assert result == 0b11111110
        
        # Clear bit 7
        result = clear_bit(value, 7)
        assert result == 0b01111111
        
        # Clear bit that's already clear
        value = 0b11111110
        result = clear_bit(value, 0)
        assert result == 0b11111110

    def test_toggle_bit(self):
        """Test toggling bits."""
        value = 0b10101010
        
        # Toggle bit 0 (currently 0)
        result = toggle_bit(value, 0)
        assert result == 0b10101011
        
        # Toggle bit 1 (currently 1)
        result = toggle_bit(value, 1)
        assert result == 0b10101000

    def test_check_bit(self):
        """Test checking bit values."""
        value = 0b10101010
        
        # Check set bits
        assert check_bit(value, 1) == 1
        assert check_bit(value, 3) == 1
        assert check_bit(value, 5) == 1
        assert check_bit(value, 7) == 1
        
        # Check clear bits
        assert check_bit(value, 0) == 0
        assert check_bit(value, 2) == 0
        assert check_bit(value, 4) == 0
        assert check_bit(value, 6) == 0

    def test_bit_operations_edge_cases(self):
        """Test bit operations with edge cases."""
        # Test with 0
        assert set_bit(0, 0) == 1
        assert clear_bit(0, 0) == 0
        assert toggle_bit(0, 0) == 1
        assert check_bit(0, 0) == 0
        
        # Test with 255 (all bits set)
        assert set_bit(255, 0) == 255
        assert clear_bit(255, 0) == 254
        assert toggle_bit(255, 0) == 254
        assert check_bit(255, 0) == 1


class TestConstants:
    """Test utility constants."""

    def test_common_baud_rates(self):
        """Test common baud rates constant."""
        expected_rates = ['9600', '14400', '19200', '38400', '57600', '115200']
        
        assert common_baud_rates == expected_rates
        assert len(common_baud_rates) == 6
        assert all(isinstance(rate, str) for rate in common_baud_rates)


if __name__ == "__main__":
    pytest.main([__file__])
