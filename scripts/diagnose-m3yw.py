#!/usr/bin/env python3
"""
Diagnostic script for M3Y-W barcode scanner troubleshooting.
Tests various configurations and baud rates to find working settings.
"""

import serial
import time
import sys
import glob
import binascii

def find_scanner_ports():
    """Find all available serial ports that might be the scanner."""
    port_patterns = [
        '/dev/ttyACM*',
        '/dev/tty.usbmodem*',
        '/dev/tty.usbserial*',
        '/dev/cu.usbmodem*',
        '/dev/cu.usbserial*',
    ]
    
    ports = []
    for pattern in port_patterns:
        ports.extend(glob.glob(pattern))
    
    return sorted(set(ports))

def test_port_with_baudrate(port_name, baudrate, timeout=1):
    """Test a specific port and baudrate with M3Y-W protocol."""
    try:
        ser = serial.Serial(port_name, baudrate, timeout=timeout)
        
        # Send M3Y-W software version command
        # M3Y-W uses: 5a00 (header) + command + checksum (BCC)
        cmd = b'S_CMD_GVER'
        bcc = 0
        for byte in cmd:
            bcc ^= byte
        full_cmd = b'\x5a\x00' + cmd + bytes([bcc]) + b'\xa5'
        
        ser.write(full_cmd)
        time.sleep(0.2)
        
        response = ser.read(1024)
        ser.close()
        
        return response if response else None
    except Exception as e:
        return None

def main():
    print("=" * 70)
    print("M3Y-W BARCODE SCANNER DIAGNOSTIC")
    print("=" * 70)
    
    # Find available ports
    ports = find_scanner_ports()
    
    if not ports:
        print("\n❌ No serial ports found!")
        print("   Expected ports: /dev/tty.usbmodem*, /dev/tty.usbserial*, etc.")
        return 1
    
    print(f"\n📍 Found {len(ports)} serial port(s):")
    for port in ports:
        print(f"   - {port}")
    
    # Test each port with different baud rates
    baud_rates = [9600, 14400, 19200, 38400, 57600, 115200]
    
    print("\n" + "=" * 70)
    print("TESTING PORTS AND BAUD RATES")
    print("=" * 70)
    
    found_working = False
    
    for port in ports:
        print(f"\n🔍 Testing {port}:")
        
        for baudrate in baud_rates:
            response = test_port_with_baudrate(port, baudrate)
            
            if response:
                print(f"   ✓ {baudrate:6d} baud: GOT RESPONSE!")
                print(f"     Response (hex): {binascii.hexlify(response).decode()}")
                print(f"     Response (raw): {response}")
                found_working = True
            else:
                print(f"   ✗ {baudrate:6d} baud: no response")
    
    print("\n" + "=" * 70)
    
    if found_working:
        print("✓ SUCCESS: Found working configuration!")
        print("\nUse the port and baud rate shown above with:")
        print("  python src/main.py <port> --baudrate <baudrate>")
        return 0
    else:
        print("❌ FAILED: No working configuration found")
        print("\nPossible issues:")
        print("  1. Scanner is not connected")
        print("  2. Scanner needs to be powered on or reset")
        print("  3. Scanner requires special initialization commands")
        print("  4. Scanner is in a different mode")
        print("\nTroubleshooting steps:")
        print("  1. Check if scanner is powered on")
        print("  2. Try resetting the scanner (power off/on)")
        print("  3. Check the M3Y-W manual for serial mode setup")
        print("  4. Try running: ./scripts/detect.sh")
        print("     Then plug/unplug the scanner to see if it's detected")
        return 1

if __name__ == "__main__":
    sys.exit(main())

