import pytest
import binascii
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gm65_scanner import GM65Scanner


class TestGM65ScannerIntegration:
    """Integration tests with real hardware (requires actual GM65 scanner)."""

    @pytest.mark.integration
    def test_real_sw_version(self, real_gm65_scanner):
        """Test software version query with real hardware."""
        reply, extra = real_gm65_scanner.cmd_get_sw_version()
        
        assert reply is not None
        assert len(reply) >= 1
        print(f"Software version: {binascii.hexlify(reply)}")

    @pytest.mark.integration
    def test_real_sw_year(self, real_gm65_scanner):
        """Test software year query with real hardware."""
        reply, extra = real_gm65_scanner.cmd_get_sw_year()
        
        assert reply is not None
        assert len(reply) >= 1
        print(f"Software year: {binascii.hexlify(reply)}")

    @pytest.mark.integration
    def test_real_get_settings(self, real_gm65_scanner):
        """Test get settings with real hardware."""
        reply, extra = real_gm65_scanner.cmd_get_settings()
        
        assert reply is not None
        assert len(reply) >= 1
        print(f"Current settings: {binascii.hexlify(reply)}")

    @pytest.mark.integration
    def test_real_raw_command(self, real_gm65_scanner):
        """Test raw command with real hardware."""
        reply, extra = real_gm65_scanner.cmd_send_raw('070100e201')
        
        assert reply is not None
        assert len(reply) >= 1
        print(f"Raw command response: {binascii.hexlify(reply)}")

    @pytest.mark.integration
    def test_real_illumination_control(self, real_gm65_scanner):
        """Test illumination control with real hardware."""
        # Get current settings first
        original_settings, _ = real_gm65_scanner.cmd_get_settings()

        # Test setting illumination to always on
        success, _ = real_gm65_scanner.cmd_set_illumination(1)
        assert success is True

        # Get settings after change
        new_settings, _ = real_gm65_scanner.cmd_get_settings()

        print(f"Original settings: {binascii.hexlify(original_settings)}")
        print(f"New settings: {binascii.hexlify(new_settings)}")

        # The command should execute successfully even if settings don't change
        # (illumination might already be set to the requested value)
        assert new_settings is not None
        assert len(new_settings) >= 1

    @pytest.mark.integration
    def test_real_baudrate_detection(self, real_gm65_scanner):
        """Test baudrate detection with real hardware."""
        baudrate = real_gm65_scanner.find_baudrate()
        
        assert baudrate is not None
        assert baudrate in ['9600', '14400', '19200', '38400', '57600', '115200']
        print(f"Detected baudrate: {baudrate}")


if __name__ == "__main__":
    pytest.main([__file__])
