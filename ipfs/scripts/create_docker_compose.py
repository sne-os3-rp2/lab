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
  krill_1:    
    container_name: krill_1
    build: ./krill_1
    volumes:
        - /tmp/ipfs/nexus:/usr/local/nexus/
    cap_add:
        - NET_ADMIN
    environment:
        - ENV_SWARM_KEY=/09b7fe038a241d5e38650b0f1811933644d6195814f863902d44698fa38b8cfa
        - BOOTNODE_IP=192.168.1.101
        - KRILL_TEST=true
        - KRILL_USE_TA=true
        - KRILL_AUTH_TOKEN=itworks
        - IS_BOOTNODE=true
    expose:
       - 3000
       - 4001 
       - 8080
       - 8081
       - 5001
    ports:
       - 3001:3000
    networks:
       ipfs_private_net:
           ipv4_address: \"192.168.1.101\"

networks:
  ipfs_private_net:
    driver: bridge
    ipam:
     config:
       - subnet: 192.168.1.0/24
"""


compose_dict = yaml.load(krills_yaml)


routinator_dicts = {}
base_port = 7000
base_id = IPv4Address("192.168.1.102")
for i in range(1, count+1):
    routinator_dicts = {}
    routinator_dicts["depends_on"] = ["krill_1"]
    routinator_dicts["container_name"] = f"routinator_{i}"
    routinator_dicts["build"] = "./routinator_img"
    routinator_dicts["volumes"] = ["/tmp/ipfs/nexus:/usr/local/nexus/"]
    routinator_dicts["environment"] = [
        "ENV_SWARM_KEY=/09b7fe038a241d5e38650b0f1811933644d6195814f863902d44698fa38b8cfa",
        "BOOTNODE_IP=192.168.1.101"
    ]
    routinator_dicts["expose"] = [9556]
    routinator_dicts["ports"] = [f"{7000+i}:9556"]
    routinator_dicts["networks"] = {
        "ipfs_private_net": {
            "ipv4_address": dq(f'{(base_id + i).exploded}')
        }
    }
    compose_dict["services"][f"routinator_{i}"] = routinator_dicts


with open(r"../docker-compose.yml", "w") as out_file:
    yaml.dump(compose_dict, out_file)
