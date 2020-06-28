#! /usr/bin/python3


import argparse
import subprocess
import time

parser = argparse.ArgumentParser()

parser.add_argument("-rc", "--routinatorcount", help="No of routinator to use in test", default=1)
parser.add_argument("-cc", "--cacount", help="No of child ca to use in test", default=1)
parser.add_argument("-rd", "--rangedepth", help="How many times to split the /24", default=9)

parser.add_argument("-pd", "--pollduration", help="Duration to poll for results", default=10)

parser.add_argument("-rt", "--runtype", help="RRD or IPFS")

args = parser.parse_args()

r_count = args.routinatorcount
c_count = args.cacount
rd = int(args.rangedepth)
r_poll = int(args.pollduration)
r_type = args.runtype

subprocess.call(f"python3 scripts/create_docker_compose.py -c {r_count}", shell=True)
subprocess.call(f"docker-compose up -d --build krill_unmodified_1", shell=True)
time.sleep(10)
subprocess.call(f"python3 scripts/init_krills.py -c {c_count} -rd {rd}", shell=True)


subprocess.call(f"docker-compose up --build -d", shell=True)

subprocess.call(f"python3 ../shared/result_fetcher.py -c {r_count} -d {r_poll} -cc {c_count} -rt https", shell=True)


subprocess.call(f"docker-compose down --remove-orphans", shell=True)


