"""
Script: get_current_datetime.py
Purpose: Get current date/time from reliable NTP server and store in workspace
Inputs: None (queries NTP servers)
Outputs: Current Eastern Time stored in .tmp/current_time.json
Author: AI-Assisted
Created: 2025-11-30

This script MUST be called before any agent executes any task.
It validates the current date/time against authoritative NTP servers
and stores the result for all agents to use.

NTP Servers used (in priority order):
1. time.nist.gov (NIST, Boulder, Colorado)
2. time.google.com (Google Public NTP)
3. pool.ntp.org (NTP Pool Project)
"""

import os
import sys
import json
import socket
import struct
from datetime import datetime, timezone
from pathlib import Path
import pytz

# Ensure .tmp directory exists
Path(".tmp").mkdir(parents=True, exist_ok=True)

# NTP servers (in priority order)
NTP_SERVERS = [
    "time.nist.gov",      # NIST - Most authoritative for US
    "time.google.com",    # Google - Fast and reliable
    "pool.ntp.org"        # NTP Pool - Fallback
]

# Eastern Time zone
EASTERN_TZ = pytz.timezone('America/New_York')

# Output file for all agents to read
CURRENT_TIME_FILE = ".tmp/current_time.json"


def get_ntp_time(ntp_server: str, timeout: int = 5) -> datetime:
    """
    Query NTP server for current time

    Args:
        ntp_server: NTP server hostname
        timeout: Socket timeout in seconds

    Returns:
        datetime object in UTC

    Raises:
        Exception if NTP query fails
    """
    # NTP packet format (48 bytes)
    ntp_packet = b'\x1b' + 47 * b'\0'

    # Connect to NTP server
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(timeout)

    try:
        client.sendto(ntp_packet, (ntp_server, 123))
        data, _ = client.recvfrom(1024)
    finally:
        client.close()

    if len(data) < 48:
        raise Exception(f"Invalid NTP response from {ntp_server}")

    # Extract transmit timestamp (bytes 40-47)
    # NTP timestamp is seconds since 1900-01-01 00:00:00
    ntp_timestamp = struct.unpack('!12I', data)[10]

    # Convert NTP timestamp to Unix timestamp
    # (NTP epoch is 1900-01-01, Unix epoch is 1970-01-01)
    # Difference is 2208988800 seconds
    unix_timestamp = ntp_timestamp - 2208988800

    # Create UTC datetime
    utc_time = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)

    return utc_time


def get_reliable_current_time() -> dict:
    """
    Get current time from NTP servers with fallback logic

    Returns:
        dict with:
        - utc_time: Current time in UTC
        - eastern_time: Current time in Eastern
        - timestamp: Unix timestamp
        - iso_format: ISO 8601 string
        - ntp_server: Which server was used
        - date_only: Date in YYYY-MM-DD format
        - time_only: Time in HH:MM:SS format
    """
    utc_time = None
    successful_server = None
    errors = []

    # Try each NTP server in order
    for ntp_server in NTP_SERVERS:
        try:
            print(f"Querying NTP server: {ntp_server}...")
            utc_time = get_ntp_time(ntp_server)
            successful_server = ntp_server
            print(f"[OK] Successfully got time from {ntp_server}")
            break
        except Exception as e:
            error_msg = f"Failed to get time from {ntp_server}: {str(e)}"
            print(f"[ERROR] {error_msg}")
            errors.append(error_msg)
            continue

    # If all NTP servers failed, fall back to system time with warning
    if utc_time is None:
        print("\n[WARN] WARNING: All NTP servers failed. Using system time as fallback.")
        print("[WARN] System time may not be accurate. Verify your system clock.")
        utc_time = datetime.now(timezone.utc)
        successful_server = "system_clock_fallback"
        for error in errors:
            print(f"  - {error}")

    # Convert to Eastern Time
    eastern_time = utc_time.astimezone(EASTERN_TZ)

    # Create comprehensive time data
    time_data = {
        "utc_time": utc_time.isoformat(),
        "eastern_time": eastern_time.isoformat(),
        "timestamp": utc_time.timestamp(),
        "iso_format": eastern_time.isoformat(),
        "date_only": eastern_time.strftime("%Y-%m-%d"),
        "time_only": eastern_time.strftime("%H:%M:%S"),
        "year": eastern_time.year,
        "month": eastern_time.month,
        "day": eastern_time.day,
        "hour": eastern_time.hour,
        "minute": eastern_time.minute,
        "second": eastern_time.second,
        "weekday": eastern_time.strftime("%A"),
        "ntp_server": successful_server,
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "timezone": "America/New_York",
        "timezone_offset": eastern_time.strftime("%z"),
        "is_dst": bool(eastern_time.dst())
    }

    return time_data


def save_current_time(time_data: dict):
    """
    Save current time to file for all agents to read

    Args:
        time_data: Dictionary with time information
    """
    with open(CURRENT_TIME_FILE, 'w', encoding='utf-8') as f:
        json.dump(time_data, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Current time saved to: {CURRENT_TIME_FILE}")


def load_current_time() -> dict:
    """
    Load current time from file

    Returns:
        dict with time information or None if file doesn't exist
    """
    if not os.path.exists(CURRENT_TIME_FILE):
        return None

    with open(CURRENT_TIME_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def display_current_time(time_data: dict):
    """
    Display current time in human-readable format

    Args:
        time_data: Dictionary with time information
    """
    print("\n" + "="*80)
    print("CURRENT DATE & TIME (Verified via NTP)")
    print("="*80)
    print(f"Date:           {time_data['date_only']} ({time_data['weekday']})")
    print(f"Time:           {time_data['time_only']} Eastern")
    print(f"Full:           {time_data['eastern_time']}")
    print(f"Timezone:       {time_data['timezone']} (UTC{time_data['timezone_offset']})")
    print(f"DST Active:     {'Yes' if time_data['is_dst'] else 'No'}")
    print(f"NTP Server:     {time_data['ntp_server']}")
    print(f"Unix Timestamp: {time_data['timestamp']}")
    print("="*80 + "\n")


def main():
    """
    Main function - get current time from NTP and save to file
    """
    try:
        print("\n" + "="*80)
        print("GET CURRENT DATE/TIME FROM NTP SERVER")
        print("="*80)
        print("Purpose: Validate current date/time for all agents")
        print("Output:  .tmp/current_time.json")
        print("="*80 + "\n")

        # Get current time from NTP servers
        time_data = get_reliable_current_time()

        # Save to file
        save_current_time(time_data)

        # Display for verification
        display_current_time(time_data)

        print("[OK] All agents can now read current time from:")
        print(f"  {os.path.abspath(CURRENT_TIME_FILE)}")
        print("\n[OK] Script completed successfully.\n")

        return 0

    except Exception as e:
        print(f"\n[ERROR] FATAL ERROR: {str(e)}", file=sys.stderr)
        print("\nStack trace:", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
