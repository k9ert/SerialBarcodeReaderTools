#!/usr/bin/env python3
"""
Test runner script for SerialBarcodeReaderTools

Usage:
    python run_tests.py                    # Run unit tests only
    python run_tests.py --integration      # Run integration tests (requires hardware)
    python run_tests.py --all              # Run all tests
"""

import sys
import subprocess
import argparse


def run_command(cmd):
    """Run a command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="Run tests for SerialBarcodeReaderTools")
    parser.add_argument("--integration", action="store_true",
                       help="Run integration tests (requires real GM65 hardware on /dev/ttyACM0)")
    parser.add_argument("--all", action="store_true",
                       help="Run all tests including integration")

    args = parser.parse_args()

    # Base pytest command
    cmd = ["python", "-m", "pytest", "-v"]

    if args.integration:
        cmd.extend(["-m", "integration"])
        print("Running integration tests (requires GM65 scanner on /dev/ttyACM0)...")
    elif args.all:
        print("Running all tests...")
    else:
        # Run only unit tests (exclude integration)
        cmd.extend(["-m", "not integration"])
        print("Running unit tests only...")

    return run_command(cmd)


if __name__ == "__main__":
    sys.exit(main())
