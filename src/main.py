import serial
import time
import argparse
import binascii
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from base_scanner import BaseScanner
from gm65_scanner import GM65Scanner
from m3yw_scanner import M3YWScanner
from utils import common_baud_rates


# ------------------------
# Scanner Factory
# ------------------------
def detect_scanner(serial_port) -> BaseScanner:
    """
    Identify the scanner by sending a request for its software version.
    """
    for scanner in [GM65Scanner, M3YWScanner]:
        scanner = scanner(serial_port)
        print("Trying", scanner.__class__.__name__)
        foundbaud = scanner.find_baudrate()
        if foundbaud:
            print("Identified Scanner:", scanner.__class__.__name__, "at baudrate:", foundbaud)
            return scanner
        else:
            print(scanner.__class__.__name__, "not detected")

    raise RuntimeError("No supported scanner found")


# ------------------------
# Main Function
# ------------------------
def main():
    parser = argparse.ArgumentParser(description="Scanner Interface")
    parser.add_argument("port", help="Serial port to use")
    parser.add_argument("--scanner", type=str, help="Scanner type (gm65 or m3y)")
    parser.add_argument("--hw-version", action='store_true', help="Query the device for the hardware version")
    parser.add_argument("--sw-version", action='store_true', help="Query the device for the software version")
    parser.add_argument("--sw-year", action='store_true', help="Query the device for the software year")
    parser.add_argument("--get-settings", action='store_true', help="Get the common (aim light, illumination, beeper) settings zone (GM65) and represent as hex")
    parser.add_argument("--get-safe-for-binary-qr", help="Check if the connected reader is know to be safe for binary QR scanning")
    parser.add_argument("--set-settings", help="Save the supplied byte to the common settings (aim light, illumination, beeper) zone (GM65)")
    parser.add_argument("--get-address", help="Query a given memory address and return the result as a byte")
    parser.add_argument("--set-address", nargs=2, help="Update a given memory address with a byte (Format ")
    parser.add_argument("--save-address", help="Save a memory address so that the current setting is preserved across reboots.")
    parser.add_argument("--set-illumination", type=int, help="Adjust the illumination light. -1 = always off, 0 = On while scanning, 1 = always on")
    parser.add_argument("--set-aimer", type=int, help="Adjust the aiming light. -1 = always off, 0 = On while scanning, 1 = always on")
    parser.add_argument("--set-beeper", type=int, help="Adjust the beeper. -1 = muted, 1 = on")
    parser.add_argument("--set-read-interval", type=float, help="Adjust the minimum time between QR code reads")
    parser.add_argument("--set-same-barcode-delay", type=float, help="Adjust the minimumt ime between re-reading the same QR code")
    parser.add_argument("--send-raw-cmd", type=str, help="Send a raw command to the reader")
    parser.add_argument("--save-settings", action='store_true', help="Save settings to EEPROM (Required for GM65 to persist settings across reboots)")
    parser.add_argument("--set-continuous-mode", action='store_true', help="Put scanner in continious mode")
    parser.add_argument("--set-command-mode", action='store_true', help="Put scanner in command mode (will stop continious mode)")
    parser.add_argument("--set-baudrate", choices=common_baud_rates, help="Changes the scanners baudrate and checks if this was successful")
    parser.add_argument("--baudrate", choices=common_baud_rates, help="Sets the baudrate that this tool will use (Default 9600)")
    parser.add_argument("--test-baudrates", action='store_true', help="Runs through a list of common baud rates to see what your device supports (Or finds out what BAUD it is currently using)")

    args = parser.parse_args()

    baudrate = 9600
    if args.baudrate:
        baudrate = args.baudrate

    ser = serial.Serial(args.port, baudrate, timeout=1)

    if args.scanner:
        if "gm65" in args.scanner.lower():
            scanner = GM65Scanner(ser)
        elif "m3y" in args.scanner.lower():
            scanner = M3YWScanner(ser)
    else:
        scanner = detect_scanner(ser)

    scan_duration = 1
    if args.hw_version:
        reply, extra = scanner.cmd_get_hw_version()
    elif args.sw_version:
        reply, extra = scanner.cmd_get_sw_version()
    elif args.sw_year:
        reply, extra = scanner.cmd_get_sw_year()
    elif args.get_settings:
        reply, extra = scanner.cmd_get_settings()
    elif args.set_settings:
        reply, extra = scanner.cmd_set_settings(args.set_settings.encode())
    elif args.get_address:
        reply, extra = scanner.cmd_get_address(args.get_address.encode())
    elif args.set_address:
        reply, extra = scanner.cmd_set_address(args.set_address[0].encode(), args.set_address[1].encode())
    elif args.save_address:
        reply, extra = scanner.cmd_save_address(args.save_address.encode())
    elif args.save_settings:
        reply, extra = scanner.cmd_save_settings()
    elif args.set_illumination is not None:
        print("Setting Illumination")
        reply, extra = scanner.cmd_set_illumination(args.set_illumination)
    elif args.set_aimer is not None:
        print("Setting Aimer")
        reply, extra = scanner.cmd_set_aimer(args.set_aimer)
    elif args.set_beeper is not None:
        print("Setting Beeper")
        reply, extra = scanner.cmd_set_beeper(args.set_beeper)
    elif args.set_read_interval is not None:
        print("Setting Read Interval")
        reply, extra = scanner.cmd_set_read_interval(args.set_read_interval)
    elif args.set_same_barcode_delay is not None:
        print("Setting Same Barcode Delay")
        reply, extra = scanner.cmd_set_same_barcode_delay(args.set_same_barcode_delay)
    elif args.send_raw_cmd:
        print("Sending raw command")
        reply, extra = scanner.cmd_send_raw(args.send_raw_cmd)
    elif args.set_continuous_mode:
        print("Setting Continuous Mode")
        reply, extra = scanner.cmd_set_continuous_mode()
    elif args.set_command_mode:
        print("Setting Command Mode")
        reply, extra = scanner.cmd_set_command_mode()
    elif args.set_baudrate is not None:
        print("Setting Baud Rate")
        reply, extra = scanner.cmd_set_baudrate(int(args.set_baudrate))
        if reply:
            print("Baudrate Changed Successfully!")
        else:
            print("Baudrate Change Failed...")
    elif args.test_baudrates:
        scanner.test_baudrates()
    elif args.get_safe_for_binary_qr:
        safe = scanner.get_safe_for_binaryqr()
        if safe is not None:
            if safe:
                print("Good News: Safe to use")
            else:
                print("WARNING: Known to be unsafe for binary QR scanning")
        else:
            print("Unsure... Unable to match software version as known-good or known-bad...")

    else:
        print("Setting Continuous Mode")
        reply, extra = scanner.cmd_set_continuous_mode()

        print("Scanning for 10 Seconds")
        scan_duration = 10
        # Keep scanning
        start = time.time()
        rx_data = b''
        while (time.time() - start) <= scan_duration:
            rx_data += ser.read(1024)

        print("Setting Command Mode")
        reply, extra = scanner.cmd_set_command_mode()
        print("Got:", rx_data, "AsHex:", binascii.hexlify(rx_data))

    ser.close()


if __name__ == "__main__":
    main()
