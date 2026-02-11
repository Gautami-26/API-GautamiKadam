import argparse
import datetime
import threading
import logging
from collections import defaultdict
from urllib import request, error

import config	
logs = logging.getLogger(__name__)  
logs.setLevel(logging.INFO)

format = logging.Formatter("%(message)s")  
f_handler = logging.FileHandler(config.LOG_FILE)
f_handler.setFormatter(format)
logs.addHandler(f_handler)

def Calling_Ifconfig(time_stamp, call_id=1):
    # Execute API call with exact log format.
    
    try:
        curr_day = datetime.date.today()
        target_time = datetime.datetime.combine(curr_day, config.Formatting_Time(time_stamp))
    except ValueError as e:
        print(f"Invalid timestamp '{time_stamp}' (Call #{call_id})")
        return
    
    try:
        with request.urlopen("https://ifconfig.co/ip", timeout=10) as res:
            response = res.read().decode().strip()
            
            log_msg = f"{target_time.strftime('%Y-%m-%d %H:%M:%S')}: Successfully called API at ifconfig.co"
            logs.info(log_msg)
            print(f" {log_msg} (Call #{call_id})")
            
    except error.URLError as e:
        log_msg = f"{target_time.strftime('%Y-%m-%d %H:%M:%S')}: Failed to call API at ifconfig.co"
        logs.error(log_msg)
        print(f" {log_msg} (Call #{call_id})")
    except Exception as e:
        log_msg = f"{target_time.strftime('%Y-%m-%d %H:%M:%S')}: Error calling API"
        logs.error(log_msg)
        print(f" {log_msg} (Call #{call_id})")

def grp_timestamps(timestamps):
    # Group by second for concurrent execution.
    groups = defaultdict(list)
    curr_day = datetime.date.today()
    
    for ts in timestamps:
        try:
            target_time = datetime.datetime.combine(curr_day, config.Formatting_Time(ts))
            groups[target_time].append(ts)
        except ValueError:
            print(f"Skipping invalid timestamp: '{ts}'")
    
    return dict(sorted(groups.items()))

def main():
    parser = argparse.ArgumentParser(description="API Scheduler - Exact format")
    parser.add_argument("--timestamps", "-t", required=True,
                       help="Comma-separated timestamps e.g. '09:15:25,13:45:09'")
    args = parser.parse_args()
    
    time_stamps = [t.strip().strip('"').strip("'") for t in args.timestamps.split(",") if t.strip()]
    print(f"Timestamps: {time_stamps}")
    
    if not time_stamps:
        print("No valid timestamps.")
        return
    
    groups = grp_timestamps(time_stamps)
    print(f"Grouped: {[(k.strftime('%H:%M:%S'), len(v)) for k,v in groups.items()]}")
    
    # Execute everything immediately
    for target_time, same_sec_stamps in groups.items():
        print(f"Executing {len(same_sec_stamps)} calls for {target_time.strftime('%H:%M:%S')}")
        
        threads = []
        for i, ts in enumerate(same_sec_stamps, 1):
            t = threading.Thread(target=Calling_Ifconfig, args=(ts, i))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        print(f"Batch complete: {target_time.strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()