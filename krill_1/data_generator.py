#! /usr/local/bin/python3

import argparse
import json
import urllib.request
import ssl
import time
import subprocess

import ipaddress
from ipaddress import ip_network

parser = argparse.ArgumentParser()
gcontext = ssl.SSLContext()

# script configuration

parser.add_argument("-to", "--token", help="Bearer token")
parser.add_argument("-ho", "--host", help="Target host")
parser.add_argument("-co", "--count", help="Number of child CA to add")
parser.add_argument("-rd", "--roadepth", help="Depth to break prefix to create roas for")
parser.add_argument("-mo", "--mode", help="cli or http", default="cli")
parser.add_argument("-st", "--sleeptime", help="seconds to sleep between request to prevent overwhelminh", default=2)
parser.add_argument("-pr", "--caprefix", help="prefix to append to ca added", default="ca")



args = parser.parse_args()
no_ca = args.count
host = args.host
token = args.token
mode = args.mode
roa_depth = int(args.roadepth) - 1
sleep_time = float(args.sleeptime)
ca_prefix = args.caprefix

if mode != "cli" and mode != "http":
    print("specify mode using -mo flag. cli and http are supported mode")
    exit(-1)




# cargo run --bin krillc add --ca ca_in --token itworks
def add_ca(ca_handle, server):
    if mode == "http":
       url = f"{server}/api/v1/cas"
       req = urllib.request.Request(url, None, {"Authorization": f"Bearer {str(token)}"})
       req.add_header('Content-Type', 'application/json; charset=utf-8')
       jsondata = json.dumps({"handle": ca_handle})
       jsondataasbytes = jsondata.encode('utf-8')
       req.add_header('Content-Length', len(jsondataasbytes))
       return urllib.request.urlopen(req, jsondataasbytes, context=gcontext)
    else:
        subprocess.call(f"krillc add --ca {ca_handle} --token {str(token)}", shell=True)

# cargo run --bin krillc parents add embedded --ca ca_in --parent ta --token itworks
def add_as_ta_child(ca_handle, server):
    if mode == "http":
        # https://{domain}:{port}/api/v1/cas/{ca_handle}/parents
        url = f"{server}/api/v1/cas/{ca_handle}/parents"
        req = urllib.request.Request(url, None, {"Authorization": f"Bearer {str(token)}"})
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = json.dumps({"handle": "ta", "contact" : "embedded"})
        jsondataasbytes = jsondata.encode('utf-8')
        req.add_header('Content-Length', len(jsondataasbytes))
        return urllib.request.urlopen(req, jsondataasbytes, context=gcontext)
    else:
        subprocess.call(f"krillc parents add embedded --ca {ca_handle} --parent ta --token {str(token)}", shell=True)

# cargo run --bin krillc repo update embedded --ca ca_in --token itworks
def grant_repo_rights(ca_handle, server):
    if mode == "http":
        # https://{domain}:{port}/api/v1/cas/{ca_handle}/repo
        url = f"{server}/api/v1/cas/{ca_handle}/repo"
        req = urllib.request.Request(url, None, {"Authorization": f"Bearer {str(token)}"})
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = json.dumps("embedded")
        jsondataasbytes = jsondata.encode('utf-8')
        req.add_header('Content-Length', len(jsondataasbytes))
        return urllib.request.urlopen(req, jsondataasbytes, context=gcontext)
    else:
        subprocess.call(f"krillc repo update embedded --ca {ca_handle} --token {str(token)}", shell=True)

# cargo run --bin krillc children add embedded --ca ta --token itworks --child ca_in --ipv4 "100.0.0.0/8,200.0.0.0/8"
def delegete_resource(ca_handle, server, index):
    if mode == "http":
       # https://{domain}:{port}/api/v1/cas/{ca_handle}/children
       url = f"{server}/api/v1/cas/ta/children"
       req = urllib.request.Request(url, None, {"Authorization": f"Bearer {str(token)}"})
       req.add_header('Content-Type', 'application/json; charset=utf-8')
       jsondata = json.dumps({"handle": ca_handle,"resources": {"asn": "", "v4": f"{index}.0.0.0/8", "v6":""},"auth": "embedded"})
       jsondataasbytes = jsondata.encode('utf-8')
       req.add_header('Content-Length', len(jsondataasbytes))
       return urllib.request.urlopen(req, jsondataasbytes, context=gcontext)
    else:
        subprocess.call(f"krillc children add embedded --ca ta --token itworks --child {ca_handle} --ipv4 {index}.0.0.0/8", shell=True)

def add_roa(ca_handle, server, index, r_depth):
    # https://{domain}:{port}/api/v1/cas/{ca_handle}/routes

    delegation = f"{index}.0.0.0/8"
    roas_ranges = get_roas_from_delegation(delegation, r_depth)

    url = f"{server}/api/v1/cas/{ca_handle}/routes"
    req = urllib.request.Request(url, None, {"Authorization": f"Bearer {str(token)}"})
    req.add_header('Content-Type', 'application/json; charset=utf-8')

    add_payload = []

    for roa_auth in roas_ranges:
        add_payload.append({"asn": int(f"{index}"), "prefix": str(roa_auth),"max_length": int(roa_auth.prefixlen)})

    jsondata = json.dumps({"added":add_payload, "removed":[]})
    jsondataasbytes = jsondata.encode('utf-8')
    print(jsondataasbytes)
    req.add_header('Content-Length', len(jsondataasbytes))
    return urllib.request.urlopen(req, jsondataasbytes, context=gcontext)


def get_roas_from_delegation(delegation, depth):
    depth_count = 0
    output = list(ip_network(delegation).subnets())
    roa_depth = depth
    
    while depth_count < roa_depth:
        _output = []
        for prefix in output:
            sub = list(ip_network(prefix).subnets())
            _output.extend(sub)
        output = _output
        depth_count = depth_count + 1
    
    return output




for n in range(int(no_ca)):
    index = n+1
    ca = f"{ca_prefix}_{index}"
    try:
        add_ca(ca, host)
        print(f"successfully added {ca} as a CA")
        time.sleep(sleep_time)
    except Exception as e: 
         print("adding ca failed with", e)
    try:
        delegete_resource(ca, host, index)
        print(f"successfully delegated resources to {ca}")
        time.sleep(sleep_time)
    except Exception as e: 
         print("delegating resource failed with", e)
    try:
        add_as_ta_child(ca, host)
        print(f"successfully added {ca} as a child of TA")
        time.sleep(sleep_time)
    except Exception as e: 
         print("adding ta as parent failed with", e)
    try:
        grant_repo_rights(ca, host)
        print(f"successfully granted {ca} the right to publish to embedded CA")
        time.sleep(sleep_time)
    except Exception as e: 
         print("granting repo rights failed with", e)
    try:
        time.sleep(sleep_time*2)
        add_roa(ca, host, index, roa_depth)
        print(f"successfully added roas for {ca}")
    except Exception as e: 
         print("creating roas failed with", e)

                 
