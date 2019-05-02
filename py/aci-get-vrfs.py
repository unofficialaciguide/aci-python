#!/usr/bin/env python
# coding: utf-8

# Unofficial ACI Guide
# Python 3 - Get vrfs Example

# This is a simple Python example demonstrating how to list all vrfs in a fabric.  
# This is boilerplate. Feel free to use in your own stuff.


import requests
import json
import pandas as pd
import os

# Clear screen
os.system('cls' if os.name == 'nt' else 'clear')


# Enter your controller hostname/IP and user credentials below.  

# Put your credentials in the config.py file.

from config import controller, username, password
base_url = "https://" + str(controller) + "/api/"
auth_bit = "aaaLogin.json"
auth_url = base_url + auth_bit
auth_data = {
  "aaaUser":{
    "attributes":{
      "name":username,
      "pwd":password
    }
  }
}


# ## Construct the Request
requests.packages.urllib3.disable_warnings() 
s = requests.session()
s.post(auth_url, json=auth_data, verify=False)

vrf_class="node/class/fvCtx.json"
vrf_url = base_url + vrf_class

vrfs = s.get(vrf_url, verify=False)
s_out = vrfs.json()
#print(s_out)

# Uncomment to print full output.
#print(json.dumps(s_out, indent=4, sort_keys=True))


# Let's get all our vrfs now.
# Start with an empty list.
vrf_list = []
count = 0

vrf_out_list = s_out['imdata']

for vrf in vrf_out_list:
   # print(vrf)
    dn = vrf['fvCtx']['attributes']['dn']
    #print(dn)
    split_dn = dn.split("/")
    vrf_list.append(dn)
    count = count + 1

print("\nVRFs in the Fabric: ")
print('====================')
[print(v) for v in vrf_list]
print('====================')
print('\nThere are', count, 'VRFs')
