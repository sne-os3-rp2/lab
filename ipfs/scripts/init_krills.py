#! /usr/local/bin/python3


import argparse

import subprocess

parser = argparse.ArgumentParser()

# script configuration

parser.add_argument("-c", "--count", help="Number of child CA to add")
parser.add_argument("-rd", "--roadepth", help="Depth to break prefix to create roas for")
parser.add_argument("-mo", "--mode", help="cli or http", default="cli")
parser.add_argument("-st", "--sleeptime", help="seconds to sleep between request to prevent overwhelminh", default=2)
parser.add_argument("-pr", "--caprefix", help="ca prefix", default="bob")

parser.add_argument("-sr", "--startrange", help="range to start allocating from", default="1.0.0.0/24")

args = parser.parse_args()

no_ca = args.count
roa_depth = int(args.roadepth) - 1
mode = args.mode
sleep_time = float(args.sleeptime)
ca_prefix = args.caprefix
start_range = args.startrange

subprocess.call(f"docker exec -it krill_1 /usr/bin/python3 data_generator.py --token itworks --host https://localhost:3000 --count {no_ca} --roadepth {roa_depth} --sleeptime {sleep_time} -pr {ca_prefix} -sr {start_range}", shell=True)
