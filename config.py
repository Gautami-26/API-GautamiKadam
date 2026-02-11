"""
Configuration File for API Scheduling
"""

API_URL = "https://ifconfig.co/" #url for IP
LOG_FILE = "./Log.txt" #log file

import datetime

def get_timestamps():
    """
    Get Comma-separated timestamps from user input. FIXED: Strip quotes.
    """
    user_input = input("Enter the timestamps(comma separated):")
    #FIXED: Clean quotes and whitespaces
    cleaned = user_input.strip().strip('"').strip("'")
    timestamps = [t.strip().strip('"').strip("'") for t in cleaned.split(",")]
    return [t for t in timestamps if t] #remove empty strings

def Formatting_Time(time_str):
    """Parse HH:MM:SS string to datetime object. Fixed: Extra validation."""
    time_str = time_str.strip().strip('"').strip("'")
    return datetime.datetime.strptime(time_str, "%H:%M:%S").time()


