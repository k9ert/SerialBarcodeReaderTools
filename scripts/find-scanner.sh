#!/bin/bash
# Find barcode scanner device information

echo "🔍 Barcode Scanner Device Finder"
echo "=================================="
echo ""

echo "📋 Available Serial Ports (for GM65/M3YW scanners):"
ls -la /dev/tty.usbserial* /dev/cu.usbserial* /dev/ttyACM* 2>/dev/null || echo "   No serial ports found"

echo ""
echo "📋 All Serial Devices:"
ls -la /dev/tty.* /dev/cu.* 2>/dev/null || echo "   No serial devices found"

echo ""
echo "📋 HID Devices (for keyboard-emulating scanners like Yokoscan):"
ls -la /dev/hidraw* 2>/dev/null || echo "   No /dev/hidraw devices found"

echo ""
echo "📋 Connected USB Devices (Barcode Scanners Only):"

# Blacklist of common non-scanner devices
BLACKLIST_VENDORS="05e3|045e|1050|1a7c|214b"  # Genesys Logic, Microsoft, Yubico, Kingsis, etc.
BLACKLIST_PRODUCTS="0610|082c|0407|0191|7250"  # Common keyboard/hub/security key products

system_profiler SPUSBDataType 2>/dev/null | awk -v blacklist_vendors="$BLACKLIST_VENDORS" -v blacklist_products="$BLACKLIST_PRODUCTS" '
    /Product ID:/ { product = $NF; getline; if ($0 ~ /Vendor ID:/) vendor = $NF }
    /Vendor ID:/ { vendor = $NF }
    /Manufacturer:/ {
        manufacturer = $0
        # Check if this device should be blacklisted
        if (vendor !~ blacklist_vendors && product !~ blacklist_products) {
            print manufacturer
        }
    }
' | head -20

echo ""
echo "ℹ️  Note:"
echo "   - Serial ports (tty.usbserial-*, ttyACM*) are for GM65/M3YW scanners"
echo "   - HID devices (/dev/hidraw*) are for keyboard-emulating scanners like Yokoscan"
echo "   - Your Yokoscan appears as a USB HID Keyboard device"
echo "   - Blacklisted: Genesys Logic hubs, Microsoft keyboards, Yubico keys, etc."

