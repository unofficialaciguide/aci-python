#!/usr/bin/env python
# coding: utf-8

# Unofficial ACI Guide
# Python 3 - Get epgs Example

# This is a simple Python example demonstrating how to list all epgs in a fabric.  
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


### Construct the Request
requests.packages.urllib3.disable_warnings() 
s = requests.session()
s.post(auth_url, json=auth_data, verify=False)

### Define the Class you want to search
epg_class="node/class/fvAEPg.json"
epg_url = base_url + epg_class

epgs = s.get(epg_url, verify=False)
s_out = epgs.json()
#print(s_out)

# Uncomment to print full output.
#print(json.dumps(s_out, indent=4, sort_keys=True))


# Let's get all our epgs now.
# Start with an empty list.
# We'll have a list for the full EPG DN
epg_dn_list = []
count = 0

epg_out_list = s_out['imdata']


## Grab the EPG DN and put it in a list
for epg in epg_out_list:
    dn = epg['fvAEPg']['attributes']['dn']
    count = count + 1
    split_dn = dn.split("/")
    epg_dn_list.append(dn)

print("\nEPGs in the Fabric: ")
print('====================')
[print(e) for e in epg_dn_list]
print('=========================================')
print('\nThere are', count, 'EPGs in the fabric')

