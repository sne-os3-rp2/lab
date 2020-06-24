#! /usr/local/bin/python3

import argparse
parser = argparse.ArgumentParser()
from ipaddress import IPv4Address

import ruamel.yaml
from ruamel.yaml.scalarstring import DoubleQuotedScalarString as dq


yaml = ruamel.yaml.YAML()
yaml.indent(sequence=4, offset=2)
yaml.preserve_quotes = True


parser.add_argument("-c", "--count", help="number of routinator instances to add", default=10) 
args = parser.parse_args()
count = int(args.count)

krills_yaml = """
version: "3.7"
services:
  krill_unmodified_1:    
    container_name: krill_unmodified_1
    build: ./krill_img
    volumes:
        - ./krill_1_data:/var/krill/data/
    cap_add:
        - NET_ADMIN
    environment:
        - KRILL_TEST=true
        - KRILL_USE_TA=true
        - KRILL_AUTH_TOKEN=itworks
    expose:
       - 3000
    ports:
       - 3000:3000
    networks:
       normal_private_net:
           ipv4_address: \"192.168.2.101\"

networks:
  normal_private_net:
    driver: bridge
    ipam:
     config:
       - subnet: 192.168.2.0/24
"""


compose_dict = yaml.load(krills_yaml)


routinator_dicts = {}
base_port = 7000
base_id = IPv4Address("192.168.2.102")
for i in range(1, count+1):
    routinator_dicts = {}
    routinator_dicts["depends_on"] = ["krill_unmodified_1"]
    routinator_dicts["container_name"] = f"routinator_unmodified_{i}"
    routinator_dicts["build"] = "./routinator_img"
    routinator_dicts["expose"] = [9556]
    routinator_dicts["ports"] = [f"{7000+i}:9556"]
    routinator_dicts["networks"] = {
        "normal_private_net": {
            "ipv4_address": dq(f'{(base_id + i).exploded}')
        }
    }
    compose_dict["services"][f"routinator_unmodified_{i}"] = routinator_dicts


with open(r"../docker-compose.yml", "w") as out_file:
    yaml.dump(compose_dict, out_file)
