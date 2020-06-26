#! /usr/local/bin/python3

import argparse
from urllib.request import urlopen
from datetime import datetime
import time

parser = argparse.ArgumentParser()

base_port = 7000
parser.add_argument("-c", "--count", help="number of routinator instances to get result from") 
parser.add_argument("-d", "--duration", help="Duration to run for", default=120) 

args = parser.parse_args()
count = int(args.count)
duration = int(args.duration)

# port -> last_update_time
prev_update_times = {}


def fetch_status_page(ip):
       return urlopen(ip).read().decode("utf-8")

def extract_last_done_at(content):
    if "last-update-done-at" not in content:
        exit("could not fetch the last update done at")
    else:
        return datetime.strptime(content.split(" ")[4].split(".")[0], '%H:%M:%S')


def extract_last_update_duration(content):
    if "last-update-duration" not in content:
        exit("last_update_duration not found") 
    else:
        duration_str = content.split("  ")[1]
        return duration_str[2:len(duration_str) - 1]

def extract_ipfs_durations(content):
    if "ipns" not in content:
        exit("ipfs-durations not found") 
    else:
        return content.split(" ")[5].split("=")[1][:-1]

def extract_rrdp_durations(content):
    if "rrdp" not in content:
        exit("rrdp duration not found")
    else:
        return content.split(" ")[5].split("=")[1][:-1]


def is_rrdp_result(page):
    return "ipns" not in page

def create_output_file():
    f = open("output.csv", "w")
    f.write("'port','type','validation_time','update_duration','repo_fetch'\n")
    return f

def write_result_to_file(page, port, last_update_done_at, out_file):
        page = fetch_status_page(f"http://localhost:{str(port)}/status")
        r_type = "rrdp" if is_rrdp_result(page) else "ipfs"

        update_duration = ""
        fetch_duration = ""
        for line in page.split("\n"):
            if "last-update-duration" in line:
                update_duration = extract_last_update_duration(line)
            if "https" in line:
                fetch_duration = extract_rrdp_durations(line)
            if "ipns" in line:
                fetch_duration = extract_ipfs_durations(line)

        out_file.write(f"{port},'{r_type}','{last_update_done_at}','{update_duration}','{fetch_duration}'\n")
        
        prev_update_times[port] = last_update_done_at



def run(output_file):
    target_port = base_port
    for i in range(count):
      try:  
        target_port = target_port + 1
        page = fetch_status_page(f"http://localhost:{str(target_port)}/status")

        for line in page.split("\n"):
            # - extract last_update_done_at

            if "last-update-done-at" in line:
                last_update_done_at = extract_last_done_at(line)
                if target_port in prev_update_times:
                    prev_update = prev_update_times.get(target_port)
                    if prev_update == last_update_done_at:
                        print("Not writing to file since validation has not occured since last time")
                    else:
                        print("A validation run has occurred. Updating output file")
                        write_result_to_file(page, target_port, last_update_done_at, output_file)
                else:
                    print("first run")
                    write_result_to_file(page, target_port, last_update_done_at, output_file)

      except Exception as e:
          print(f"Could not retrieve from http://localhost:{str(target_port)}/status. Error was {e}...skipping")
          continue       
    
if __name__ == '__main__':
    start_time = time.time()
    output_file = create_output_file()
    print("polling for validation result and writing to output.csv...")
    print(f"will last for {duration} seconds")
    while time.time() - start_time < duration:
        run(output_file)
        time.sleep(1)
    print("done")
