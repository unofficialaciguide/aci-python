#!/usr/bin/env python
# coding: utf-8

# Unofficial ACI Guide
# Python 3 - Get bds Example

# This is a simple Python example demonstrating how to list all bds in a fabric.  
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

bd_class="node/class/fvBD.json"
bd_url = base_url + bd_class

bds = s.get(bd_url, verify=False)
s_out = bds.json()
#print(s_out)

# Uncomment to print full output.
#print(json.dumps(s_out, indent=4, sort_keys=True))


# Let's get all our bds now.
# Start with an empty list.
bd_list = []
count = 0

bd_out_list = s_out['imdata']

for bd in bd_out_list:
    dn = bd['fvBD']['attributes']['dn']
    split_dn = dn.split("/")
    bd_list.append(dn)
    count = count + 1

print("\nBDs in the Fabric: ")
print('====================')
[print(b) for b in bd_list]
print('====================')
print('\nThere are', count, 'BDs')
