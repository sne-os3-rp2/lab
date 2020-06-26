#! /usr/local/bin/python3


import argparse

import subprocess

parser = argparse.ArgumentParser()

# script configuration

parser.add_argument("-c", "--count", help="Number of child CA to add")
parser.add_argument("-rd", "--roadepth", help="Depth to break prefix to create roas for")
parser.add_argument("-mo", "--mode", help="cli or http", default="cli")
parser.add_argument("-st", "--sleeptime", help="seconds to sleep between request to prevent overwhelminh", default=2)

args = parser.parse_args()

no_ca = args.count
roa_depth = int(args.roadepth) - 1
mode = args.mode
sleep_time = float(args.sleeptime)


subprocess.call(f"docker exec -it krill_unmodified_1 /usr/bin/python3 data_generator.py --token itworks --host https://localhost:3000 --count {no_ca} --roadepth {roa_depth} --sleeptime {sleep_time} -pr k1", shell=True)
