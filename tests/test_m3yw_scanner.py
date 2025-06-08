import pytest
import binascii
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from m3yw_scanner import M3YWScanner
from base_scanner import NotSupportedError


class TestM3YWScannerIntegration:
    """Integration tests with real M3Y-W hardware (requires actual M3Y-W scanner)."""

    @pytest.mark.integration
    def test_real_sw_version(self, real_m3yw_scanner):
        """Test software version query with real M3Y-W hardware."""
        reply, extra = real_m3yw_scanner.cmd_get_sw_version()
        
        # This should not be None if the method is implemented
        assert reply is not None, "cmd_get_sw_version returned None - method may not be implemented"
        assert len(reply) >= 1, "Software version response should contain at least 1 byte"
        print(f"M3Y-W Software version: {reply}")
        print(f"M3Y-W Software version (hex): {binascii.hexlify(reply)}")

    @pytest.mark.integration
    def test_real_hw_version(self, real_m3yw_scanner):
        """Test hardware version query with real M3Y-W hardware."""
        with pytest.raises(NotSupportedError):
            real_m3yw_scanner.cmd_get_hw_version()
        print("✓ M3Y-W correctly reports hardware version query as not supported")

    @pytest.mark.integration
    def test_real_sw_year(self, real_m3yw_scanner):
        """Test software year query with real M3Y-W hardware."""
        with pytest.raises(NotSupportedError):
            real_m3yw_scanner.cmd_get_sw_year()
        print("✓ M3Y-W correctly reports software year query as not supported")

    @pytest.mark.integration
    def test_real_get_settings(self, real_m3yw_scanner):
        """Test get settings with real M3Y-W hardware."""
        with pytest.raises(NotSupportedError):
            real_m3yw_scanner.cmd_get_settings()
        print("✓ M3Y-W correctly reports bulk settings query as not supported")

    @pytest.mark.integration
    def test_real_set_settings(self, real_m3yw_scanner):
        """Test set settings with real M3Y-W hardware."""
        with pytest.raises(NotSupportedError):
            real_m3yw_scanner.cmd_set_settings(b'\x00')
        print("✓ M3Y-W correctly reports bulk settings modification as not supported")

    @pytest.mark.integration
    def test_real_save_settings(self, real_m3yw_scanner):
        """Test save settings with real M3Y-W hardware."""
        with pytest.raises(NotSupportedError):
            real_m3yw_scanner.cmd_save_settings()
        print("✓ M3Y-W correctly reports explicit settings save as not supported")

    @pytest.mark.integration
    def test_real_continuous_mode(self, real_m3yw_scanner):
        """Test setting continuous mode with real M3Y-W hardware."""
        try:
            reply, extra = real_m3yw_scanner.cmd_set_continuous_mode()
            
            # For M3Y-W, this should return some response or at least not None
            print(f"M3Y-W Set continuous mode response: {reply}")
            if reply is not None:
                print(f"M3Y-W Set continuous mode (hex): {binascii.hexlify(reply)}")
            
            # The command should execute without raising NotImplementedError
            assert True, "cmd_set_continuous_mode executed successfully"
                
        except NotImplementedError:
            pytest.fail("cmd_set_continuous_mode is not implemented for M3Y-W scanner")

    @pytest.mark.integration
    def test_real_command_mode(self, real_m3yw_scanner):
        """Test setting command mode with real M3Y-W hardware."""
        try:
            reply, extra = real_m3yw_scanner.cmd_set_command_mode()
            
            print(f"M3Y-W Set command mode response: {reply}")
            if reply is not None:
                print(f"M3Y-W Set command mode (hex): {binascii.hexlify(reply)}")
            
            # The command should execute without raising NotImplementedError
            assert True, "cmd_set_command_mode executed successfully"
                
        except NotImplementedError:
            pytest.fail("cmd_set_command_mode is not implemented for M3Y-W scanner")

    @pytest.mark.integration
    def test_real_illumination_control(self, real_m3yw_scanner):
        """Test illumination control with real M3Y-W hardware."""
        try:
            # Test setting illumination to always on
            reply, extra = real_m3yw_scanner.cmd_set_illumination(1)
            
            print(f"M3Y-W Set illumination (always on) response: {reply}")
            if reply is not None:
                print(f"M3Y-W Set illumination (hex): {binascii.hexlify(reply)}")
            
            # Test setting illumination to normal mode
            reply2, extra2 = real_m3yw_scanner.cmd_set_illumination(0)
            
            print(f"M3Y-W Set illumination (normal) response: {reply2}")
            if reply2 is not None:
                print(f"M3Y-W Set illumination normal (hex): {binascii.hexlify(reply2)}")
            
            # The command should execute without raising NotImplementedError
            assert True, "cmd_set_illumination executed successfully"
                
        except NotImplementedError:
            pytest.fail("cmd_set_illumination is not implemented for M3Y-W scanner")

    @pytest.mark.integration
    def test_real_aimer_control(self, real_m3yw_scanner):
        """Test aimer control with real M3Y-W hardware."""
        try:
            # Test setting aimer to always on
            reply, extra = real_m3yw_scanner.cmd_set_aimer(1)
            
            print(f"M3Y-W Set aimer (always on) response: {reply}")
            if reply is not None:
                print(f"M3Y-W Set aimer (hex): {binascii.hexlify(reply)}")
            
            # The command should execute without raising NotImplementedError
            assert True, "cmd_set_aimer executed successfully"
                
        except NotImplementedError:
            pytest.fail("cmd_set_aimer is not implemented for M3Y-W scanner")

    @pytest.mark.integration
    def test_real_beeper_control(self, real_m3yw_scanner):
        """Test beeper control with real M3Y-W hardware."""
        try:
            # Test unmuting beeper
            reply, extra = real_m3yw_scanner.cmd_set_beeper(1)
            
            print(f"M3Y-W Set beeper (unmute) response: {reply}")
            if reply is not None:
                print(f"M3Y-W Set beeper (hex): {binascii.hexlify(reply)}")
            
            # The command should execute without raising NotImplementedError
            assert True, "cmd_set_beeper executed successfully"
                
        except NotImplementedError:
            pytest.fail("cmd_set_beeper is not implemented for M3Y-W scanner")

    @pytest.mark.integration
    def test_real_read_interval(self, real_m3yw_scanner):
        """Test read interval setting with real M3Y-W hardware."""
        try:
            # Test setting read interval to 1 second
            reply, extra = real_m3yw_scanner.cmd_set_read_interval(1.0)
            
            print(f"M3Y-W Set read interval response: {reply}")
            if reply is not None:
                print(f"M3Y-W Set read interval (hex): {binascii.hexlify(reply)}")
            
            # The command should execute without raising NotImplementedError
            assert True, "cmd_set_read_interval executed successfully"
                
        except NotImplementedError:
            pytest.fail("cmd_set_read_interval is not implemented for M3Y-W scanner")

    @pytest.mark.integration
    def test_real_same_barcode_delay(self, real_m3yw_scanner):
        """Test same barcode delay setting with real M3Y-W hardware."""
        try:
            # Test setting same barcode delay to 2 seconds
            reply, extra = real_m3yw_scanner.cmd_set_same_barcode_delay(2.0)
            
            print(f"M3Y-W Set same barcode delay response: {reply}")
            if reply is not None:
                print(f"M3Y-W Set same barcode delay (hex): {binascii.hexlify(reply)}")
            
            # The command should execute without raising NotImplementedError
            assert True, "cmd_set_same_barcode_delay executed successfully"
                
        except NotImplementedError:
            pytest.fail("cmd_set_same_barcode_delay is not implemented for M3Y-W scanner")

    @pytest.mark.integration
    def test_real_raw_command(self, real_m3yw_scanner):
        """Test raw command sending with real M3Y-W hardware."""
        try:
            # Test sending the software version command as raw
            reply, extra = real_m3yw_scanner.cmd_send_raw('T_OUT_CVER')
            
            assert reply is not None, "cmd_send_raw returned None - method may not be implemented"
            assert len(reply) >= 1, "Raw command response should contain at least 1 byte"
            print(f"M3Y-W Raw command response: {reply}")
            print(f"M3Y-W Raw command (hex): {binascii.hexlify(reply)}")
                
        except NotImplementedError:
            pytest.fail("cmd_send_raw is not implemented for M3Y-W scanner")

    @pytest.mark.integration
    def test_real_baudrate_control(self, real_m3yw_scanner):
        """Test baudrate control with real M3Y-W hardware."""
        try:
            # Test setting baudrate (this might change the connection)
            # We'll test with the current baudrate to avoid breaking the connection
            current_baudrate = real_m3yw_scanner.serial_port.baudrate
            
            reply, extra = real_m3yw_scanner.cmd_set_baudrate(current_baudrate)
            
            print(f"M3Y-W Set baudrate response: {reply}")
            if reply is not None:
                print(f"M3Y-W Set baudrate (hex): {binascii.hexlify(reply)}")
            
            # The command should execute without raising NotImplementedError
            assert True, "cmd_set_baudrate executed successfully"
                
        except NotImplementedError:
            pytest.fail("cmd_set_baudrate is not implemented for M3Y-W scanner")

    @pytest.mark.integration
    def test_real_baudrate_detection(self, real_m3yw_scanner):
        """Test baudrate detection with real M3Y-W hardware."""
        try:
            baudrate = real_m3yw_scanner.find_baudrate()
            
            if baudrate is not None:
                assert baudrate in ['9600', '14400', '19200', '38400', '57600', '115200']
                print(f"M3Y-W Detected baudrate: {baudrate}")
            else:
                print("M3Y-W Baudrate detection returned None")
                
        except NotImplementedError:
            pytest.fail("find_baudrate is not implemented for M3Y-W scanner")

    @pytest.mark.integration
    def test_real_safe_for_binary_qr(self, real_m3yw_scanner):
        """Test binary QR safety check with real M3Y-W hardware."""
        try:
            safe = real_m3yw_scanner.get_safe_for_binaryqr()
            
            print(f"M3Y-W Safe for binary QR: {safe}")
            
            # Should return True, False, or None
            assert safe in [True, False, None], "get_safe_for_binaryqr should return True, False, or None"
                
        except NotImplementedError:
            pytest.fail("get_safe_for_binaryqr is not implemented for M3Y-W scanner")


if __name__ == "__main__":
    pytest.main([__file__])
