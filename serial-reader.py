#!/usr/bin/env python3
"""
SerialBarcodeReaderTools - Refactored Version

This file has been refactored into the src/ directory for better organization.
You can still use this file as before, or use: python src/main.py [arguments]
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import main

if __name__ == "__main__":
    main()
